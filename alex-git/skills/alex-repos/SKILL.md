---
name: alex-repos
description: >
  Use for any git or GitHub work in Alex's repositories — pushing, checking whether
  something was ever pushed, adding a remote, diagnosing a rejected push, deciding which
  GitHub identity to act as, or working in a repo another session is also touching.
  Triggers on: "push this", "did that get pushed", "is anything unpushed", "why was my
  push rejected", "Repository not found", "which GitHub account am I", "set up the
  remote", "the branch diverged", "Shopify keeps committing to the branch", "delete the
  old clone", "commit the docs", "audit my repos". It carries the map of every working
  copy (path, remote, branch model, and what a push *does* besides pushing), the two
  GitHub identities and the exact limits of each token, and the traps that have already
  cost hours here. For the Hetzner VPS and its stacks, use `agents-os:hetzner-server`.
metadata:
  version: "0.1.0"
---

# Alex's git estate

Nine working copies across two roots, two GitHub identities, and one repo that deploys a
storefront when you push it. Nothing here is exotic; the cost has always come from
assuming instead of checking.

**Roots.** `~/Library/Mobile Documents/com~apple~CloudDocs/alex.levnikov.root/` (iCloud —
almost everything) and `~/Projects/` (one leftover clone). iCloud paths contain spaces and
a `~` in `com~apple~CloudDocs`: always quote them, never `cd` bare.

## The four rules that prevent every incident in `references/traps.md`

1. **`git fetch` before you conclude anything.** Every "the work is lost / never pushed /
   already pushed" mistake in this repo's history traces to a stale remote-tracking ref.
2. **Verify, don't recall.** Tables here are dated snapshots. Branch tips, and which repo
   is ahead of which, change hourly. `references/audit.sh` re-derives the truth in seconds.
3. **Know what a push does besides pushing.** In `yoursaunas-theme` a push to `staging`
   deploys a live Shopify theme *and* invites a bot commit back onto the branch.
4. **Never declare work lost from one working copy.** Two clones of the same repo held
   different unpushed commits for two days (2026-08-19/20) because only one was checked.

## The estate

| Repo | Path (under the iCloud root unless noted) | Remote | Branch you work on | A push also… |
|---|---|---|---|---|
| **Sauna** (planning, catalog) | `Sauna/` | `git@github.com:alexlevnikov/banya-builder-bay-area.git` | `v3/b0-data-foundation` | nothing. **Kept local on purpose (V24)** — do not push without asking |
| **yoursaunas-theme** | `yoursaunas-theme/` | HTTPS `alexlevnikov/yoursaunas-theme` | `staging` | **deploys theme `152536514721`** and triggers 2 CI workflows |
| ↳ second clone | `~/Projects/yoursaunas-theme` | same | `staging` | **obsolete** — merged and pushed 2026-08-20, safe to delete (`T6`) |
| **yoursaunas-site** (v1 site) | `yoursaunas-site/` | HTTPS `alexlevnikov/yoursaunas-site` | `main` | Cloudflare (`wrangler.jsonc`); `feat/lead-form-actions` is 6 commits local by choice |
| **design-studio** | `design-studio/` | **none** | `main` | — **not on GitHub at all**, one local commit (`GIT-1`) |
| **Agents OS** (umbrella) | `Agents OS/` → symlink to `Agents OS.nosync/` | HTTPS `alexlevnikov/agentic-os` | `main` | 3 submodules: `financial-agent`, `meditation-agent`, `coding-agent` |
| **claude_plugins** | `claude_plugins/` | HTTPS `alexlevnikov/alex_claude_marketplace` | `main` | nothing automatic — but the marketplace installs **from GitHub**, so an unpushed edit is invisible |
| **Finances** | `Finances/` | `git@github.com:alexlevnikov/finances.git` | `main` | — |

Detail per repo — conventions, deploy wiring, what is safe to touch:
`references/repos.md`.

## Identity: two accounts, one of which is not yours

`gh` holds **`alexlevnikov`** (active, fine-grained PAT named *Agentic OS*) and
**`alex-joyous`** (work OAuth token). Git gets its credentials from `gh` via a global
credential helper, so **whichever account `gh` calls active is the one that pushes.**

Before anything that writes to GitHub: `gh auth status`. The token's permission ceiling —
and what it silently cannot do (repository secrets: `403`) — is in `references/auth.md`,
together with the SSH setup, the work-account alias on port 443, and an error→cause table.

## Traps

Each one is documented with the measurement that exposed it, in `references/traps.md`:

| Symptom | Real cause |
|---|---|
| `Repository not found` on a repo that exists | transport, not permissions |
| `remote rejected … without workflow scope` | the token may not write `.github/workflows`; `--dry-run` never catches it |
| A branch "was never pushed" | `git fetch` had never run in that clone |
| Work "is lost" | it is in the *other* clone |
| `Update from Shopify for theme …` commits you did not make | the theme integration is **two-way** |
| Another session's files land in your commit | `git add -A` in a shared working tree |
| `«file 2.ts»` next to `file.ts` | iCloud conflict copies, not code |

## Audit before you plan

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/alex-repos/references/audit.sh"
```

Prints, for every working copy: branch, dirty files, commits that exist **nowhere on any
remote**, and whether the remote is reachable. Run it at the start of any session that
will touch more than one repo, and before telling Alex that something is or is not pushed.

## Scope: what this skill hands off

| The task is really about… | Owner |
|---|---|
| The Hetzner VPS, its stacks, cron, backups | `agents-os:hetzner-server` |
| Where the Sauna project stands, what to do next | `Sauna/STATUS.md` (printed by that repo's SessionStart hook) |
| Adding a plugin or skill to the marketplace | `claude_plugins/docs/AUTHORING.md` |
| Shopify theme content, templates, budgets | the theme repo's own docs; this skill only owns its git |
