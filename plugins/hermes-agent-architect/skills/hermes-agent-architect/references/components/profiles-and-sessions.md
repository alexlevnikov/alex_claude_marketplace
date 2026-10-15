---
id: profiles-and-sessions
kind: component
status: verified
pinned_tag: v2026.9.14
verified_utc: 2026-10-15
---

# Profiles and sessions

Use a separate profile and gateway when a bot needs its own identity, configuration, token and writable state. Use sessions for distinct conversations within one profile. A profile is an application boundary, not an operating-system security boundary; verify filesystem and process isolation separately.

Before deployment, identify the source repository, runtime profile owner, state mounts, channel token ownership and whether another poller already uses the same token. Verify the target image and profile; no feature is enabled merely because it appears in the docs.

Evidence: [official profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles), [multi-profile gateways](https://hermes-agent.nousresearch.com/docs/user-guide/multi-profile-gateways), [sessions](https://hermes-agent.nousresearch.com/docs/user-guide/sessions). Pinned files: `../../upstream/hermes-agent/website/docs/user-guide/profiles.md` and `../../upstream/hermes-agent/website/docs/user-guide/sessions.md` relative to the architect skill root. Review if profile or gateway semantics change upstream.
