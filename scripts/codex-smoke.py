#!/usr/bin/env python3
"""Install this marketplace in a disposable Codex home and inspect its skills."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())


def call(env: dict[str, str], *args: str) -> str:
    result = subprocess.run(args, cwd=ROOT, env=env, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(f"{' '.join(args)} failed:\n{result.stderr[-2000:]}\n{result.stdout[-2000:]}")
    return result.stdout


def main() -> int:
    if not shutil.which("codex"):
        print("Codex CLI is unavailable", file=sys.stderr)
        return 2
    with tempfile.TemporaryDirectory(prefix="harness-codex-smoke-") as home:
        env = dict(os.environ, CODEX_HOME=home)
        marketplace = json.loads(call(env, "codex", "plugin", "marketplace", "add", str(ROOT), "--json"))
        name = marketplace["marketplaceName"]
        installs = {}
        for entry in CATALOG["plugins"]:
            plugin = entry["name"]
            installs[plugin] = json.loads(call(env, "codex", "plugin", "add", f"{plugin}@{name}", "--json"))
        prompt = call(env, "codex", "debug", "prompt-input", "Harness smoke test")
        json.loads(prompt)  # The prompt must be valid JSON, not only printable text.
        skill_count = 0
        for entry in CATALOG["plugins"]:
            plugin = entry["name"]
            for skill in (ROOT / "plugins" / plugin / "skills").glob("*/SKILL.md"):
                qualified = f"{plugin}:{skill.parent.name}"
                if qualified not in prompt:
                    raise RuntimeError(f"{qualified} is absent from Codex prompt input")
                skill_count += 1
        installed = Path(installs["design-tools"]["installedPath"])
        selector = call(env, sys.executable, str(installed / "scripts" / "invoke.py"), "ui-craft:typeset")
        if "status: OK" not in selector or str(installed / "vendors" / "typeset" / "SKILL.md") not in selector:
            raise RuntimeError("installed design-tools selector cannot load the bundled skill")
        print(f"Codex smoke OK: {len(installs)} packs, {skill_count} entry skills, bundled vendor selector")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (RuntimeError, KeyError, json.JSONDecodeError) as exc:
        print(f"Codex smoke failed: {exc}", file=sys.stderr)
        sys.exit(1)
