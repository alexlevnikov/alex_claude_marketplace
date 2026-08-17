---
name: hetzner-server
description: >
  Use for any task that touches the Hetzner VPS running Alex's Agentic OS — reading what is
  currently on it, deploying or restarting a stack, adding a cron entry or a backup job,
  opening a port or a Tailscale Funnel path, changing SSH access or users, checking health,
  or investigating an alert from the auditor bot. Triggers on: "what's running on the
  server", "deploy this to Hetzner", "restart n8n", "is the box healthy", "the auditor
  flagged X", "add a cron job", "expose this endpoint", "why is the bot down", "check the
  backups", "ssh into the box". It says where the box's current state actually lives (not in
  the docs), which commands are safe to run, and — the part that keeps getting skipped —
  what must be updated after a change so the next session is not acting on a stale document.
---

# The Hetzner box

One VPS (`ubuntu-4gb-nbg1-2`, 4 cores / 8 GB / 75 GB, Ubuntu) is the always-on runtime for
every agent in the Agentic OS. Reach it as `ssh hetzner`. Everything is Docker Compose in
**user mode** under the account `alex`.

Throughout, the knowledge base is:

```bash
BOT=~/Library/Mobile\ Documents/com~apple~CloudDocs/alex.levnikov.root/Agents\ OS/hetzner-bot
```

## 1. Read before you act

**Docs go stale faster than the box changes.** Anything load-bearing gets verified live.

| Question | Answer it with |
|---|---|
| What is on the box right now? | `$BOT/facts/snapshot.md` — machine-generated. Regenerate first: `cd $BOT && ./refresh.py` |
| Is it healthy? What is open? | `ssh hetzner "cd ~/agents-os-audit/bin && python3 audit.py status"` |
| *Why* is it built this way? | `$BOT/knowledge/topology.md` — design intent, written by humans |
| How do I do X for project Y? | `$BOT/runbooks/<project>.md`; `_server.md` for the box itself |
| This surprised me / cost me an hour | `$BOT/knowledge/gotchas.md` — read it, then add to it |

`facts/` is machine output. **Never hand-edit it.** A wrong fact there means a wrong
collector: fix `$BOT/audit/collect.py` and regenerate.

## 2. Stop rules

They are **not** repeated here. All six live in `$BOT/../CLAUDE.md` §0, and that file
cascades into every session under `Agents OS/` — including the subproject sessions this
skill exists for, so nothing is lost by not restating them. A second, shorter copy is
exactly how a rule goes missing: the copy that used to sit here was four rules long and had
quietly dropped *never force-push, never partial-publish*.

Three box-specific notes those rules do not carry:

- **The one standing `sudo` exception.** The rule is no sudo. The single exception is the
  auditor's read-only whitelist — `ufw status`, `fail2ban-client status sshd`, `tail -n 200
  /var/log/auth.log` — via `/etc/sudoers.d/agents-os-audit`. Its header states what review a
  new line needs; nothing is added to it casually.
- **Generating a secret.** On the box, `openssl rand -hex 24`, straight into `secrets.env`.
  Never on the Mac — then it never exists there to leak.
- **What may be exposed.** `$BOT/knowledge/topology.md` carries the whole public surface and
  why each path is on it. Postgres ports are never published to the host or the internet:
  design intent, not a default.

## 3. After a change: close the loop

The box changes several times a day and most of it is noise. This loop runs on changes that
alter an answer someone would act on.

**Run it when the change is one of these:**

- **Public surface** — a port opens or closes, a Funnel path appears or disappears, a
  container publishes to something other than loopback.
- **Inventory** — a stack or long-lived container appears or disappears; a compose file
  moves; a service is pinned or unpinned.
- **Automation** — a crontab entry, systemd timer or backup job added, removed, rescheduled.
- **Identity** — a shell user, SSH key, group membership, sudoers entry, new secrets file.
- **Trust** — anything moving a boundary between the `alex` and `agentos` zones, or a new
  inbound integration.

**Do not run it for:** image rebuilds and digest changes from an ordinary deploy, container
restarts, uptime, disk / RAM / load, package counts, backup rotation, containers that live
for minutes. The auditor already tracks those and the generated files already carry them.

The test is not taste: *would a session reading the docs tomorrow act differently?* If no,
it is a measurement, and measurements are the machine's job.

**The steps, in order:**

1. **Re-capture the auditor's baseline** if the change added a container, port, cron entry
   or key — otherwise it reports your own deploy as an intruder until someone learns to
   ignore it. Procedure in `$BOT/audit/install/README.md`. Every line the diff adds is
   declared normal forever, so a human reads it. Copy `baseline.json` back into the repo and
   commit it.
2. **`cd $BOT && ./refresh.py`** — regenerates `facts/snapshot.md` and the `AUTO-STATE`
   block in `Agents OS/CLAUDE.md`. `--dry-run` first if unsure.
3. **`knowledge/topology.md`** if the *design intent* changed — a new stack, a deliberate
   new exposure, a moved boundary. No machine writes here; this file records *why*, and a
   collector can only ever see *what*.
4. **`runbooks/<project>.md`** if a *procedure* changed.
5. **`knowledge/gotchas.md`** if it cost more than a few minutes.
6. **This skill** if what you just learned changes how the box is *operated* — a new stop
   rule, a command that is no longer safe, a new place the truth lives. A skill that is
   never updated becomes the most confidently wrong document in the system.

Steps 2–6 are the agent's. Step 1 needs a human reading the baseline diff.

## 4. The auditor

A security auditor runs on cron every 30 minutes: it collects the box's state, judges it
against a git-reviewed baseline and against the previous snapshot, fixes a short whitelist
of reversible things itself, and messages Telegram **only** on a finding. Silence is the
design, so silence is watched: every completed run writes a heartbeat, and an n8n workflow
alerts through the *finance* bot if that beat goes stale.

Design and threat model: `$BOT/audit/README.md`.

A finding is not automatically a problem. `image_digest_changed` after you rebuilt an image
is the tool working. `new_cron_entry` after you added a cron entry is the tool working. Both
mean the baseline is now behind reality — step 1 above.

Day to day:

```bash
ssh hetzner "cd ~/agents-os-audit/bin && python3 audit.py status"
ssh hetzner "tail -20 ~/agents-os-audit/audit.log"     # every action it took or refused
```

## 5. Traps that have already cost hours

- **`PUT /workflows` in n8n deactivates the workflow.** Re-activate and verify. Most
  repeated mistake in this project.
- **The n8n container cannot see host files.** Its only mount is its own data volume. Route
  host state through Postgres, which both sides already reach.
- **cron's `PATH` is `/usr/bin:/bin` and its environment is otherwise empty.** A job that
  works by hand and does nothing on schedule is almost always this.
- **`docker system df` RECLAIMABLE is not what a prune reclaims** — it counted 7.5 GB while
  `docker image prune -f` took 0 B. Never `docker image prune -a`: it deletes locally built
  images and forces a rebuild.
- **Backup filenames differ per stack.** `finance-os` writes `pg-*.sql.gz.gpg`,
  `meditation-os` writes `meditation_os-*.sql.gz.gpg`. Guessing one pattern produced a false
  "no backups" alarm.
- **`timeout` does not exist on macOS** — a pipeline using it returns empty output, which
  reads exactly like the remote command returning nothing.

The full list is `$BOT/knowledge/gotchas.md`, and it is the first thing to add to when
something surprises you.
