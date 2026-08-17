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

The box changes several times a day and most of it is noise. A change that alters an answer
someone would act on — public surface, inventory, automation, identity, trust — has to reach
the docs before the session ends. A measurement does not: uptime, disk, load, package
counts, container restarts, an image digest from your own deploy. The auditor already
carries those.

The test is not taste: *would a session reading the docs tomorrow act differently?* If no,
it is a measurement, and measurements are the machine's job.

**The loop itself is `$BOT/README.md`, under "After a change on the box (RULE)" — which
class of change fires it, what to leave alone, and the six steps in order. Follow it there,
not from memory.** It is one file-open away; it sits beside every file the steps tell you to
edit; and it is the copy that gets maintained, because that is where the work happens. Step
2 puts you in that directory anyway (`./refresh.py`).

Two things about that loop are worth carrying here, because they decide whether you may
finish alone:

- **Step 1 is a human's.** Re-capturing the auditor's baseline declares every added line
  normal forever, so Alex reads the diff. Skipping it means the auditor reports your own
  deploy as an intruder until someone learns to ignore it — which is how an alarm dies.
- **Step 6 is this skill.** Update it when what you learned changes how the box is
  *operated*: a new stop rule, a command no longer safe, a new place the truth lives. A
  skill that is never updated becomes the most confidently wrong document in the system.

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

They live in `$BOT/knowledge/gotchas.md` — read it before you touch the box, and add to it
the moment something surprises you. That file is the reason the same afternoon is not lost
twice, and it is only worth what the last person put into it.

It is organised by where the trap lives, so go straight to the part you are in: **Docker ·
n8n · cron · Alerting · Git and GitHub accounts · Backups · sudo · Python · Docs.** Each
entry carries the symptom, the cause and what to do instead.

No selection of "the worst ones" is repeated here, deliberately. A second list stops being
the worst ones the week after it is written, and it repeats the old number long after the
original entry has been corrected — which is precisely the failure the file exists to
prevent.
