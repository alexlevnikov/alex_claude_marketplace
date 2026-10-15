---
id: automation
kind: component
status: verified
pinned_tag: v2026.9.14
verified_utc: 2026-10-15
---

# Scheduled and event-driven work

Use Hermes cron for scheduled agent or script work and a documented hook for events. Decide who owns the schedule and idempotency before enabling a job. Distinguish a job definition in source from its live registration; inspect the target profile and scheduler state. Validate timezone, retries, permission scope and duplicate-execution behavior.

Evidence: [cron jobs](https://hermes-agent.nousresearch.com/docs/user-guide/features/cron), [hooks](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks), [cron troubleshooting](https://hermes-agent.nousresearch.com/docs/guides/cron-troubleshooting). Pinned docs are indexed by `scripts/find_docs.py`. Review if scheduler contracts change upstream.
