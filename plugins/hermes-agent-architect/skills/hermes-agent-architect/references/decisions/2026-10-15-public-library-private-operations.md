---
id: 2026-10-15-public-library-private-operations
kind: decision
status: accepted
pinned_tag: v2026.9.14
verified_utc: 2026-10-15
---

# Public library with private operations context

The owner chose `alex_claude_marketplace` as the public source of truth for reusable Hermes mechanics, component cards, research and architecture decisions. The architect skill remains the primary library and its own Codex project folder. Generic VPS and Tailscale procedures may be public, but live host maps and bot runtime state remain in private sources read only when needed.

This preserves shareable knowledge and keeps the marketplace portable. A local symlink to the Git checkout makes edits visible to future skill reads; plugin caches and other hosts still require an update. Revisit if the repository visibility or installation model changes.
