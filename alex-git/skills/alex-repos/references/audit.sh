#!/usr/bin/env bash
# State of every working copy Alex keeps: branch, dirt, commits that exist nowhere else,
# and whether the remote answers. Read-only — no fetch, no write, nothing that changes a ref.
#
#   bash audit.sh            # fast: local facts only
#   bash audit.sh --remote   # also probes each remote (network, a few seconds per repo)

set -uo pipefail
PROBE_REMOTE=0
[ "${1:-}" = "--remote" ] && PROBE_REMOTE=1

ROOT="$HOME/Library/Mobile Documents/com~apple~CloudDocs/alex.levnikov.root"

repos=()
for d in "$ROOT"/*/ "$HOME/Projects"/*/; do
  [ -e "$d/.git" ] && repos+=("${d%/}")
done

for r in "${repos[@]}"; do
  name="$(basename "$r")"
  case "$r" in "$HOME/Projects"/*) name="~/Projects/$name";; esac

  branch="$(git -C "$r" symbolic-ref --short HEAD 2>/dev/null || echo DETACHED)"
  dirty="$(git -C "$r" status --porcelain 2>/dev/null | wc -l | tr -d ' ')"
  unpushed="$(git -C "$r" log --oneline --branches --not --remotes 2>/dev/null | wc -l | tr -d ' ')"
  remote="$(git -C "$r" config --get remote.origin.url || echo '(no remote)')"

  printf '\n%s\n' "$name"
  printf '  branch %-28s dirty %-4s local-only commits %s\n' "$branch" "$dirty" "$unpushed"
  printf '  remote %s\n' "$remote"

  if [ "$unpushed" != "0" ]; then
    git -C "$r" log --oneline --branches --not --remotes 2>/dev/null | sed 's/^/    ! /'
    printf '    (hashes, not content: a commit rebased or cherry-picked upstream still lists here)\n'
  fi
  [ -n "$(git -C "$r" stash list 2>/dev/null)" ] && git -C "$r" stash list | sed 's/^/    stash: /'

  if [ "$PROBE_REMOTE" = "1" ] && [ "$remote" != "(no remote)" ]; then
    if GIT_TERMINAL_PROMPT=0 git -C "$r" ls-remote --exit-code -h origin >/dev/null 2>&1; then
      printf '  remote reachable: yes\n'
    else
      printf '  remote reachable: NO — check transport before concluding anything (references/traps.md §1)\n'
    fi
  fi
done

printf '\n--- identity ---\n'
gh auth status 2>&1 | grep -E "Logged in|Active account|Token scopes" | sed 's/^/  /'
printf '  git will push as: '
printf 'protocol=https\nhost=github.com\n\n' | git credential fill 2>/dev/null \
  | awk -F= '/^username=/{u=$2} /^password=/{k=substr($2,1,11)} END{print u " (" k "…)"}'
