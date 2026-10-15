"""Exercise source resolution from a plugin-cache layout using real Git repos."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


PLUGIN = Path(__file__).resolve().parents[1]
SCRIPTS = PLUGIN / "skills/hermes-agent-architect/scripts"
RELATIVE = Path("website/docs/user-guide/features/memory.md")


class UpstreamTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name).resolve()
        self.skill = self.home / "cache/0.3.0/skills/hermes-agent-architect"
        (self.skill / "scripts").mkdir(parents=True)
        (self.skill / "data").mkdir()
        for script in SCRIPTS.glob("*.py"):
            shutil.copy2(script, self.skill / "scripts" / script.name)
        self.canonical = self.home / ".local/share/alex-claude-marketplace/plugins/hermes-agent-architect/upstream/hermes-agent"
        self.adjacent = self.skill.parents[1] / "upstream/hermes-agent"
        self.env = dict(os.environ, HOME=str(self.home), PYTHONDONTWRITEBYTECODE="1")
        self.env.pop("HERMES_ARCHITECT_UPSTREAM", None)
        for key in list(self.env):
            if key.startswith("GIT_"):
                self.env.pop(key)

    def git(self, root, *args):
        return subprocess.run(["git", "-C", str(root), *args], env=self.env,
                              text=True, capture_output=True, check=True).stdout.strip()

    def repository(self, root):
        root.mkdir(parents=True)
        self.git(root, "init", "--quiet")
        file = root / RELATIVE
        file.parent.mkdir(parents=True)
        file.write_text("# Pinned memory\nActions: add, replace, remove.\n")
        self.git(root, "add", ".")
        self.git(root, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                 "-c", "commit.gpgsign=false", "commit", "--quiet", "-m", "fixture")
        commit = self.git(root, "rev-parse", "HEAD")
        self.catalog(commit)
        return commit

    def catalog(self, commit):
        data = {"pinned_tag": "fixture-tag", "pinned_commit": commit,
                "entries": [{"title": "Memory", "url": "https://example.invalid/current/memory",
                             "sections": ["Features"], "tag_doc_path": "user-guide/features/memory.md"}],
                "tag_documents": ["user-guide/features/memory.md"]}
        (self.skill / "data/docs-catalog.json").write_text(json.dumps(data))

    def run_script(self, script="resolve_upstream.py", *args):
        return subprocess.run([sys.executable, str(self.skill / "scripts" / script), *args],
                              cwd=self.home, env=self.env, capture_output=True, text=True)

    def test_cache_catalog_returns_existing_canonical_file(self):
        self.repository(self.canonical)
        self.adjacent.mkdir(parents=True)  # Codex leaves an empty submodule directory.
        result = self.run_script("find_docs.py", "memory")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(str(self.canonical / RELATIVE), result.stdout)
        self.assertIn("https://example.invalid/current/memory", result.stdout)

    def test_missing_source_is_explicit_without_a_fake_local_path(self):
        self.catalog("a" * 40)
        result = self.run_script("find_docs.py", "memory")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("unavailable", result.stderr.lower())
        self.assertNotIn(str(self.adjacent / RELATIVE), result.stdout)

    def test_missing_source_strict_mode_fails(self):
        self.catalog("a" * 40)
        result = self.run_script("resolve_upstream.py", "--json")
        self.assertEqual(result.returncode, 2)
        self.assertTrue(result.stdout.startswith("{"), result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "unavailable")

    def test_adjacent_source_can_resolve_and_select_a_tracked_file(self):
        commit = self.repository(self.adjacent)
        result = self.run_script("resolve_upstream.py", "--json", "--file", str(RELATIVE))
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["commit"], commit)
        self.assertEqual(data["file"], str(self.adjacent / RELATIVE))

    def test_environment_override_supports_nondefault_locations(self):
        source = self.home / "custom upstream"
        self.repository(source)
        self.env["HERMES_ARCHITECT_UPSTREAM"] = str(source)
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), str(source))

    def test_invalid_explicit_override_does_not_silently_fall_back(self):
        self.repository(self.canonical)
        self.env["HERMES_ARCHITECT_UPSTREAM"] = str(self.home / "missing")
        result = self.run_script()
        self.assertEqual(result.returncode, 2)
        self.assertIn("unavailable", result.stderr.lower())
        self.assertEqual(result.stdout, "")

    def test_wrong_commit_is_rejected(self):
        self.repository(self.canonical)
        self.catalog("a" * 40)
        result = self.run_script()
        self.assertEqual(result.returncode, 2)
        self.assertIn("commit", result.stderr.lower())

    def test_changed_tracked_document_is_rejected(self):
        self.repository(self.canonical)
        (self.canonical / RELATIVE).write_text("changed after commit")
        result = self.run_script()
        self.assertEqual(result.returncode, 2)
        self.assertIn("local changes", result.stderr.lower())

    def test_untracked_files_are_rejected(self):
        self.repository(self.canonical)
        (self.canonical / "extra.py").write_text("# local addition")
        result = self.run_script()
        self.assertEqual(result.returncode, 2)
        self.assertIn("local changes", result.stderr.lower())

    def test_assume_unchanged_cannot_conceal_modified_source(self):
        self.repository(self.canonical)
        self.git(self.canonical, "update-index", "--assume-unchanged", str(RELATIVE))
        (self.canonical / RELATIVE).write_text("hidden tracked change")
        result = self.run_script()
        self.assertEqual(result.returncode, 2)
        self.assertIn("index flags", result.stderr.lower())

    def test_skip_worktree_cannot_conceal_modified_source(self):
        self.repository(self.canonical)
        self.git(self.canonical, "update-index", "--skip-worktree", str(RELATIVE))
        (self.canonical / RELATIVE).write_text("hidden tracked change")
        result = self.run_script()
        self.assertEqual(result.returncode, 2)
        self.assertIn("index flags", result.stderr.lower())

    def test_parent_repository_cannot_masquerade_as_upstream(self):
        commit = self.repository(self.home / "parent")
        source = self.home / "parent/empty-submodule"
        source.mkdir()
        self.env["HERMES_ARCHITECT_UPSTREAM"] = str(source)
        self.catalog(commit)
        result = self.run_script()
        self.assertEqual(result.returncode, 2)
        self.assertIn("repository root", result.stderr.lower())

    def test_missing_docs_directory_is_rejected(self):
        source = self.home / "no docs"
        self.repository(source)
        self.git(source, "rm", "-r", "website")
        self.git(source, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                 "-c", "commit.gpgsign=false", "commit", "--quiet", "-m", "remove docs")
        self.catalog(self.git(source, "rev-parse", "HEAD"))
        self.env["HERMES_ARCHITECT_UPSTREAM"] = str(source)
        result = self.run_script()
        self.assertEqual(result.returncode, 2)
        self.assertIn("website/docs", result.stderr)

    def test_file_cannot_escape_upstream(self):
        self.repository(self.canonical)
        result = self.run_script("resolve_upstream.py", "--file", "../outside.md")
        self.assertEqual(result.returncode, 2)
        self.assertIn("relative", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
