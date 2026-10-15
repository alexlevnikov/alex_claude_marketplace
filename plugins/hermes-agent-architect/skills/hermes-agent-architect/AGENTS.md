# Hermes Agent Architect project

This directory is both the primary Hermes architecture skill and a suitable Codex project folder. Its owning Git repository is `alex_claude_marketplace`; edit that checkout, not a plugin cache. The pinned upstream stays outside `skills/` so its skills are not discovered as marketplace skills. Use `scripts/resolve_upstream.py` relative to this file to locate and verify the adjacent submodule or standard external marketplace checkout. Managed plugin caches need not contain the submodule; never edit them to add it. See README.md for setup and overrides. Report unavailable source explicitly before making pinned implementation claims.

Before advising on Hermes, use `SKILL.md`, the component index, relevant decision or pattern, `data/docs-catalog.json`, and the exact tagged source when available. Distinguish current official documentation, pinned `v2026.9.14`, and actual enablement in the target bot. Follow `references/knowledge-policy.md` when recording reusable findings.

A target bot's private inventory and deployment configuration belong to that bot or a private operations source. This public skill does not own secrets, runtime profiles, sessions or user memory. Keep upstream clean; bot-specific patches belong in bot repositories.
