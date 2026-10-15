---
name: vps-service-audit
description: Compare a VPS service's source repository with its deployed Compose or systemd definition, image, mounts, and live status. Use for pre-change checks, deployment drift, or service inventory maintenance.
---

# VPS service audit

Find the service's private inventory and owning source repository; use a local host-architecture skill if installed. Confirm the Compose project or systemd unit, deployed image or executable, mounts, environment sources, process status and recent errors. Use read-only commands first. Do not print secrets, full environment dumps or personal data into the public repository.

Report source revision, deployed revision/image, configuration owner, meaningful drift, and the evidence used. State when access is insufficient. A repository edit does not update a running container or unit. If the user authorizes a deployment, follow the target project's own procedure, verify the new instance, and preserve a rollback path. Put exact service maps in private operations records, not this plugin.
