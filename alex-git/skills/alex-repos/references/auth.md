# Identities, tokens, transports

Verified **2026-08-20** with `gh` 2.89.0. Tokens rotate and permissions change — the probes
below are the point of this file; the values are just what they returned that day.

## Two GitHub accounts live on this machine

| Account | Token type | Role |
|---|---|---|
| **`alexlevnikov`** | fine-grained PAT, named *Agentic OS*, no expiry | **active** — every personal repo |
| `alex-joyous` | OAuth (`gho_…`), scopes `admin:public_key, gist, read:org, repo` | work; reachable through the `github.com-joyous` SSH alias |

Whoever `gh` calls active is who pushes: a single global helper feeds git from `gh`'s
keyring —

```
credential.https://github.com.helper = !/opt/homebrew/bin/gh auth git-credential
```

so `git push` inherits the `gh` account, not the repo. Some repos additionally carry a local
`credential.helper=osxkeychain`; the `gh` helper is consulted first and wins in practice.

**Check before writing to GitHub:**

```bash
gh auth status
```

**Check who git itself will authenticate as** — this prints the account and the token *kind*,
never the token:

```bash
printf 'protocol=https\nhost=github.com\n\n' | git credential fill \
  | awk -F= '/^username=/{print} /^password=/{print "token_prefix=" substr($2,1,11) "…"}'
```

`github_pat_` = fine-grained · `ghp_` = classic · `gho_` = OAuth. Switch accounts with
`gh auth switch`. Never print a token in full, never paste one into a file, a commit, or
chat — `gh` hands it to git directly and nothing else needs to see it.

## What the fine-grained token may do

Fine-grained tokens grant permissions **per repository**, and the failure is always a clean
refusal rather than a partial success:

| Capability | Permission needed | State on 2026-08-20 |
|---|---|---|
| push code | Contents: Read and write | ✅ |
| push `.github/workflows/**` | **Workflows: Read and write** | ✅ granted 2026-08-20, after a rejected push |
| `gh secret list` / `set` | Secrets: Read and write | ❌ `403 Resource not accessible by personal access token` — Alex adds secrets in the UI |
| create / delete repos | Administration | untested |

**Editing a fine-grained token's permissions does not change the token string.** Add a
permission in the GitHub UI (Settings → Developer settings → Personal access tokens →
Fine-grained → the token → Repository permissions) and everything keeps working with no
re-login, no keychain edit, no `gh` command. This is nearly always the cheapest fix.

Two dead ends worth remembering, both measured:

- `gh auth refresh -s workflow` **cannot** help a token-based login — it is OAuth-only.
- `gh auth login --web` against an already-authenticated account asks *"do you want to
  re-authenticate?"*, and declining leaves the old token in place while looking like
  success. If you go this route, `gh auth logout --user <name>` first, and confirm the
  browser is signed in as the intended account.

## SSH

`~/.ssh/config` carries two GitHub entries:

```
Host github.com            → HostName github.com,     User alexlevnikov
Host github.com-joyous     → HostName ssh.github.com, Port 443, User git
```

plus a global rewrite so the work org never uses port 22:

```
url.git@github.com-joyous:eyaljoyous/.insteadOf = git@github.com:eyaljoyous/
```

`Sauna` and `Finances` still have `git@github.com:` remotes; everything else is HTTPS.

**Port 22 is not reliably reachable from every network Alex works on.** It failed on
2026-08-19 (which produced decision V26 — "HTTPS only") and answered normally on 2026-08-20.
Test rather than believe either claim:

```bash
ssh -T git@github.com            # port 22
ssh -T -p 443 git@ssh.github.com # the fallback GitHub offers for blocked networks
```

Either printing `Hi alexlevnikov! You've successfully authenticated` means SSH is fine right
now. If only 443 answers, switch the remote to HTTPS or point it at the `ssh.github.com`
alias — don't spend an hour on a "missing" repository.

## Error → cause

| What git or gh prints | What it actually means |
|---|---|
| `ERROR: Repository not found` over SSH | **transport or identity**, almost never a deleted repo. GitHub returns the same words for "blocked", "wrong key" and "does not exist" |
| `! [remote rejected] … refusing to allow a Personal Access Token to create or update workflow … without workflow scope` | token lacks Workflows: Read and write. **`git push --dry-run` does not catch this** — it never sends the pack, so the server-side check never runs |
| `HTTP 403: Resource not accessible by personal access token` | a fine-grained permission is missing for that specific API |
| `! [rejected] … (fetch first)` | the remote moved. In `yoursaunas-theme` the mover is usually `shopify[bot]` |
| `could not read Username … terminal prompts disabled` | the credential helper returned nothing; check `gh auth status` before touching remotes |
| `Permission denied (publickey)` | wrong host alias — the work org must go through `github.com-joyous` |
