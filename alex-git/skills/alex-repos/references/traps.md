# Traps, each with the incident that found it

Every entry here was paid for once. The rule at the end of each is the cheap part.

---

## 1. `Repository not found` is a transport error

**2026-08-19.** Three repositories were recorded as missing from GitHub. All three existed.
SSH port 22 was unreachable from that network, and GitHub answers a blocked or unauthenticated
SSH connection with the same words it uses for a repository that does not exist. An hour went
into "restoring" repositories that were never gone.

**Rule.** Before concluding a repo is missing, prove the transport:
`ssh -T git@github.com`, then `ssh -T -p 443 git@ssh.github.com`. If SSH is blocked, HTTPS
works — `git remote set-url origin https://github.com/<owner>/<repo>.git`.

---

## 2. A branch is not unpushed just because your clone says so

**2026-08-19.** Commit `a1de43c` was recorded as "local only, at risk". It had been on GitHub
for days. `git fetch` had never succeeded in that clone, so `git branch -r` was serving a
cache from before the branch existed.

**Rule.** `git fetch --all` first, then judge. The only trustworthy answer to *"what exists
nowhere but here?"* is:

```bash
git log --oneline --branches --not --remotes
```

Empty output means everything is on a remote. Anything printed exists in exactly one place
on earth.

---

## 3. Work hides in the other clone

**2026-08-19 → 20.** `yoursaunas-theme` had two working copies. `quality.yml` (71 lines of CI)
existed only in `~/Projects`; the Shopify CLI pin existed only in the iCloud copy; GitHub had
neither. A session checked the iCloud copy, found nothing, and wrote into `STATUS.md` that the
work was lost and had to be rewritten. It was sitting on disk the whole time.

**Rule.** Never declare work lost from one working copy. Enumerate the clones first:

```bash
find ~ -maxdepth 4 -name ".git" -type d 2>/dev/null | sed 's|/.git$||'
```

Then, in each: `git log --oneline --branches --not --remotes`, `git stash list`,
`git status --porcelain`. Merge — don't rewrite. And check the stale remote-tracking refs a
second clone may hold (`git for-each-ref`); one of them pointed at a commit nobody had
mentioned.

---

## 4. The Shopify theme integration writes to your branch

**2026-08-21 04:43 UTC.** A push was rejected with `fetch first`. Nobody had pushed —
`shopify[bot]` had, with a commit titled `Update from Shopify for theme
yoursaunas-theme/staging`. A `shopify theme push` performed minutes earlier had come back
into git through the GitHub integration, and Shopify had reformatted `templates/index.json`
on the way.

**Rules.**
- The integration is **two-way**: git → theme on push, theme → git on any change made
  outside git.
- Pushing `staging` is a deploy, not just a push.
- After any `shopify theme push` or theme-editor edit, `git fetch` before you commit — your
  local JSON template is probably the older formatting.
- The bot's version of a JSON template is authoritative once it exists; check your edit
  survived the normalization instead of forcing your copy over it.

---

## 5. Two sessions, one working tree

**2026-08-20.** Two Claude sessions worked in `Sauna` at the same time. One ran `git add -A`
and swept the other's uncommitted `STATUS.md` edits into its own commit (`a5d8a46`). Nothing
was lost — this time. Later the same day, one session rebased a shared branch while the other
was mid-edit; that one worked out only because the tree happened to be clean.

**Rules.**
- In a shared tree, commit with explicit pathspecs: `git commit -- path/a path/b`. Reserve
  `git add -A` for a tree you are certain is yours alone.
- Say which files you own before you start, and stay inside them.
- Never rebase or move `HEAD` on a branch someone else is editing without asking first — a
  peer's uncommitted work survives, but their next commit lands on a base they did not choose.
- `ListAgents` shows which sessions are live; `SendMessage` reaches them.

---

## 6. iCloud is a filesystem with opinions

- **Conflict copies.** iCloud resolves a two-machine collision by writing `«file 2.ts»` next
  to `file.ts`. Fourteen of them were removed from `yoursaunas-site` on 2026-08-19; each was
  older than its original and the originals matched `HEAD`, so nothing unique was lost —
  **but that has to be checked, not assumed.** Find them with
  `find . -name "* 2.*" -not -path "./.git/*"`.
- **`.nosync`.** A directory named `…​.nosync` is excluded from iCloud sync; `Agents OS` is a
  symlink onto `Agents OS.nosync`. It is one repository, reachable by either path.
- **Paths.** The root contains spaces and `com~apple~CloudDocs`, where `~` is literal. Quote
  every path; prefer `git -C "$PATH"` over `cd`.
- **Never store a secret in an iCloud repo** — `claude_plugins` is both synced and public.

---

## 7. `--dry-run` proves less than it looks

`git push --dry-run` skips sending the pack, so every server-side rule — workflow-file
permission, branch protection, hooks — goes unevaluated. It succeeded immediately before a
real push was rejected outright (2026-08-20). Use it to check *what* would move, never to
predict *whether* the push is allowed. Details in `auth.md`.

---

## 8. Write the correction, keep the wrong entry

Three separate status entries in `Sauna/STATUS.md` were wrong about git — a branch believed
unpushed, work believed lost, a clone believed missing. Each was corrected in place with the
old claim left visible and a note on what the faulty method was. That is the convention here:
the wrong conclusion is deleted only along with the reasoning that produced it, otherwise the
next session repeats the method and reaches the same wrong answer.
