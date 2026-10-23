# Hermes Agent Architect

The [architect skill](skills/hermes-agent-architect/SKILL.md) remains the primary component and research library: [component cards](skills/hermes-agent-architect/references/components/index.md), [architecture decisions](skills/hermes-agent-architect/references/decisions/), [bot patterns](skills/hermes-agent-architect/references/patterns/), [full platform overview](skills/hermes-agent-architect/docs/hermes-platform-overview.md), memory research and an official documentation catalog. Focused sibling skills turn that library into bot blueprints, extension designs and runtime audits. The [OpenViking memory skill](skills/openviking-memory/SKILL.md) provides a pinned, searchable copy of the official OpenViking documentation plus architecture, configuration, integration and operations guides.

The clean Hermes `v2026.9.14` submodule is pinned at `upstream/hermes-agent`, outside `skills/`, to avoid discovering upstream skills as this plugin's skills. Initialize it after cloning with `git submodule update --init -- plugins/hermes-agent-architect/upstream/hermes-agent` from the marketplace root.

This plugin starts no MCP server and deploys no bot. A local Codex symlink to the marketplace checkout sees knowledge edits on the next read; published plugin caches need their own update. Host maps, credentials, profiles, sessions and personal memory stay in private sources.

## Pinned source for Codex installations

Codex plugin caches can omit Git submodules. Keep the plugin installed normally,
and provide the source from a separate checkout of this same public repository:

```sh
git clone https://github.com/alexlevnikov/alex_claude_marketplace.git ~/.local/share/alex-claude-marketplace
git -C ~/.local/share/alex-claude-marketplace submodule update --init --depth 1 -- plugins/hermes-agent-architect/upstream/hermes-agent
python3 ~/.local/share/alex-claude-marketplace/plugins/hermes-agent-architect/skills/hermes-agent-architect/scripts/resolve_upstream.py --json
```

Before using an existing destination, review its origin, branch and Git status.
Preserve local changes; do not clone over it or reset it. This checkout remains
outside iCloud and outside managed caches. It is source storage, not another
skill installation: do not link its skills into `~/.agents/skills` or add it as a
second marketplace. Codex should discover exactly the five plugin skills.

From the installed architect skill, `scripts/resolve_upstream.py` automatically
tries the adjacent submodule, then the standard checkout above. Both must match
the installed catalog's exact commit and be clean. Index flags that hide tracked changes (`assume-unchanged` or `skip-worktree`) are rejected; use a full, ordinary checkout. An explicit `--upstream` or
`HERMES_ARCHITECT_UPSTREAM` can select another upstream root; an invalid override
fails. The resolver never changes Git or downloads anything. On exit code 2,
report pinned source as unavailable. `scripts/find_docs.py` keeps current URLs
separate and labels unavailable pinned files; `--require-upstream` makes that a
failing check. `resolve_upstream.py --file <relative-path>` also verifies file
bytes against the pinned Git blob before returning its path.

Plugin upgrades/removal only replace managed caches; this external checkout
survives. Update the plugin by the [Codex setup procedure](../../docs/SETUP.md).
When an intentionally reviewed plugin update changes the pin, first review the
external checkout for local changes, fast-forward its main branch, then run the
submodule update command again. An old or edited source is rejected until it
matches; the resolver does not automatically advance or erase it.

### OpenViking documentation

The OpenViking skill includes all 304 Markdown pages under upstream `docs/` at commit `824e9c7ff5e7cebbc36f55257c39f8bbe75d5a24`. Its [manifest](skills/openviking-memory/references/upstream/manifest.json) records source blob hashes, and the copied documentation retains its [AGPL-3.0 license](skills/openviking-memory/references/upstream/LICENSE). It is a documentation snapshot, not a deployed OpenViking server. Verify it with `python3 plugins/hermes-agent-architect/skills/openviking-memory/scripts/verify_docs.py`.

### Project context

The [project context instructions](skills/hermes-agent-architect/docs/project-context-routing.md) tell each skill where to look for Reflection, Life Manager, Hermes Corpus and shared VPS memory: Linear Resources, current plans, checkout documents and relevant code. Research is supporting evidence for unresolved questions. Physical host paths and runtime inventories remain in private operations sources.

### Verification

```sh
python3 -m unittest discover -s plugins/hermes-agent-architect/tests -v
python3 plugins/hermes-agent-architect/skills/hermes-agent-architect/scripts/validate_knowledge.py --require-upstream
python3 scripts/check.py
python3 scripts/codex-smoke.py
```

The deferred `0.2.0` cache issue is addressed by the external-source resolver in
`0.2.1`. The external source does not establish any deployed bot's actual image,
profile or enabled tools; inspect those separately in private sources.
