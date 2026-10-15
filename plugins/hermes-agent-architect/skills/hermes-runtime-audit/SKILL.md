---
name: hermes-runtime-audit
description: Audit what a specific deployed Hermes bot actually runs against its source repository, pinned upstream version, official documentation, and intended profile. Use for capability drift, upgrade readiness, diagnostics, or pre-change verification.
---

# Hermes runtime audit

Start from the target bot's private service inventory or host-specific architecture skill. Identify source repository, Compose/systemd unit, deployed image digest, profile owner, mounted state and enabled channels/tools. Read current configuration and service status with the least access needed; redact secrets and user data from notes and outputs. A Git edit or documented feature is not proof of deployment.

Compare three columns: current official documentation, pinned Hermes source (locate it with `python3 ../hermes-agent-architect/scripts/resolve_upstream.py --json` relative to this installed SKILL.md; report unavailable source on exit code 2), and observed target runtime. Mark each claim `confirmed`, `not confirmed`, or `not applicable` with evidence and date. Check local patches separately. Report drift, impact, safe validation and rollback; do not mutate a production service merely to complete an audit. Save only transferable platform findings in the public architect library. Keep exact host topology and profiles private.
