---
name: tailscale-access-review
description: Review Tailscale SSH, grants, Serve, Funnel, and port exposure for a VPS or bot without publishing tailnet topology. Use for access troubleshooting or network changes involving Tailscale.
---

# Tailscale access review

Read the target's private network inventory when available. Compare intended access with observed `tailscale status`, `tailscale serve status`, `tailscale funnel status`, relevant listening sockets and the applicable tailnet policy. Inspect only the data needed and redact node names, addresses, users and policy details from public artifacts. Distinguish private Serve routes from public Funnel routes and ordinary SSH from Tailscale SSH. Check both tailnet authorization and host/application controls where they apply.

Use current [Tailscale access-control documentation](https://tailscale.com/docs/features/access-control) and [grants reference](https://tailscale.com/docs/reference/syntax/grants); prefer current grants syntax for new policy examples. Tailscale SSH has its own [authorization requirements](https://tailscale.com/docs/features/tailscale-ssh). Produce a proposed change, expected reachability and rollback before modifying routes or policy. Keep actual tailnet policy, device names, IPs, keys and private URLs in the private operations source.
