# Server configuration and deployment

## Deployment shape

For a small VPS, start with one self-hosted HTTP server and local AGFS/vector persistence in a dedicated workspace. Pin an image digest or source revision; do not use the upstream Compose `latest` tag as a reproducible production release. Keep the listener on a private network or loopback, configure an API key, and do not publish port 1933 directly without an explicit access design. Check [deployment](upstream/docs/en/guides/03-deployment.md), [deployment checklist](upstream/docs/en/guides/19-deployment-checklist.md), [server fields](upstream/docs/en/configuration/01-server.md).

The open-source Docker/Systemd deployment differs from the commercial private VikingDB package. Do not apply the package's Kubernetes, license, or three-node capacity requirements to a standalone open-source installation. [Checklist](upstream/docs/en/guides/19-deployment-checklist.md).

## Identity and keys

Use `server.auth_mode="api_key"` with a nonempty `root_api_key`. Store the root key outside Git and use it only for account/user administration. Create a user/admin key for normal data traffic; the key determines account and user identity. In API key mode, a root key cannot access tenant data APIs. With no root key, the server uses localhost-only dev mode; this is not a production identity scheme. [Authentication](upstream/docs/en/guides/04-authentication.md), [multi-tenancy](upstream/docs/en/concepts/11-multi-tenant.md), [Admin API](upstream/docs/en/api/08-admin.md).

ACL enforcement is account-level and off by default. The shared Resource root grants `user:* = manage`, including when ACL is enabled, until a descendant is made `restricted` and receives explicit grants. Validate effective permissions with both allowed and denied identities. ACLs apply only to `viking://resources/...`. [ACL](upstream/docs/en/concepts/15-acl.md), [ACL API](upstream/docs/en/api/12-acl.md).

## Models and storage

The default dense embedding is local `bge-small-zh-v1.5-f16`, 512 dimensions; no VLM is configured by default. A working VLM is required for summaries and memory extraction. `query_planner` falls back to VLM. A configured reranker is optional. Changing embedding model or dimension requires a planned reindex/migration. For Russian sessions and books, benchmark a multilingual local embedding before promotion. A local database with an external VLM sends source text to that endpoint; choose the data policy deliberately. [Server fields](upstream/docs/en/configuration/01-server.md), [model guide](upstream/docs/en/guides/01-configuration.md).

On a constrained CPU host, begin with one commit worker and low VLM concurrency, then measure peak RSS, swap, queue delay and bot latency. Upstream defaults are not sizing proof. Use `openviking-server doctor` for configuration/model checks; `/health` and `/health/ready` check service readiness, not memory quality. [Deployment](upstream/docs/en/guides/03-deployment.md), [observability](upstream/docs/en/guides/05-observability.md).

Keep server `ov.conf`, client `ovcli.conf`, and each agent's connection settings separate. Do not put API keys into a skill or checked-in plan. Verify exact config fields against the [configuration reference](upstream/docs/en/configuration/01-server.md) before writing a profile.
