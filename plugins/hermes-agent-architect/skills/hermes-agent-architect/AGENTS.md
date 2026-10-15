# Hermes Agent Architect project

This directory is both the Codex skill and the main folder of the separate
`VPS · Hermes Architect` Codex project. The owning Git repository is
`/srv/repos/alex_claude_marketplace`; edit this checkout, not an installed
plugin cache. The installed Codex skill on this VPS is a symlink to this folder.

Before advising on Hermes, read `SKILL.md`, the relevant part of
`references/decision-guide.md`, `data/docs-catalog.json`, and the exact pinned
source document when available. Distinguish current official documentation,
the pinned `v2026.9.14` tag, and actual enablement in a target bot. Follow
`references/knowledge-policy.md` when recording reusable findings.

For a VPS bot, read `/home/ubuntu/Projects/CODEX_PROJECTS.md` and
`/srv/repos/agent-lab-mvp/docs/HERMES-SERVICES.md` before touching deployment.
This skill does not own bot runtime, secrets, profiles, sessions or user memory.
Keep upstream clean; bot-specific patches belong in bot repositories.
