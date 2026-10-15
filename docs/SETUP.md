# Install and update

This repository is the marketplace. Its 18 packs live in `plugins/`; install
each pack once, then use its skill names in any project. A clone outside a sync
folder such as iCloud is the recommended working copy. GitHub is the sync
channel. The GitHub repository can be public or private; private installs
require working Git credentials on each machine.

## Claude Code

```bash
claude plugin marketplace add alexlevnikov/alex_claude_marketplace
claude plugin install design-tools@alex-claude-marketplace
claude plugin install web-harvest@alex-claude-marketplace
claude plugin install browser-lab@alex-claude-marketplace
claude plugin install design-ui-craft@alex-claude-marketplace  # example standalone vendor
```

Install only the packs you use. For a quick local check before publishing, run
`claude plugin validate . --strict` from the repository root. Claude Code is not
installed on this VPS, so the nested `design-tools` commands were checked
against its documented command layout, not run here interactively.

After a published update:

```bash
claude plugin marketplace update alex-claude-marketplace
claude plugin update design-tools@alex-claude-marketplace
claude plugin update design-ui-craft@alex-claude-marketplace
```

Restart the Claude Code session so it loads the updated pack. An older separate
`design-pipeline` installation should be removed; that skill now ships inside
`design-tools`.

## Codex

```bash
codex plugin marketplace add alexlevnikov/alex_claude_marketplace
codex plugin add design-tools@alex-claude-marketplace
codex plugin add web-harvest@alex-claude-marketplace
codex plugin add browser-lab@alex-claude-marketplace
codex plugin add design-ui-craft@alex-claude-marketplace  # example standalone vendor
```

Use `$design-ui-craft:typeset <task>` to invoke a standalone vendor skill, or
`$design-ui-craft:overview` for its short catalog. The umbrella fallback is
`$design-tools:design-tools ui-craft:typeset <task>`;
`$design-tools:design-pipeline <task>` starts a whole-surface workflow. See the
[vendor pack list](../README.md#use-design-tools) and run
`python3 scripts/codex-smoke.py` after an update.

For a changed plugin version, refresh the marketplace with `codex plugin
marketplace upgrade alex-claude-marketplace`, then remove and add that plugin
again if the installed cache still points at the earlier version. Reopen the
session after installing.

## Local dependencies and credentials

- Each vendor pack includes its pinned skill resources and license evidence;
  `design-tools` retains a compatibility copy. Some procedures still need
  browser, image, or network capabilities. Impeccable's launcher can
  download its upstream binary on first use.
- `browser-lab` starts local MCP processes and requires its browser and runtime
  dependencies. Run `bash doctor.sh` on the machine using it.
- `web-harvest` needs provider credentials for the backends you choose. In
  Claude Code, its `.mcp.json` reads variables supplied through the local
  `~/.claude/settings.json` `env` field. Keep values out of this repository.
  Codex does not read Claude settings; configure its MCP credentials in the
  Codex environment or connector settings and verify a real request before
  relying on a backend.

## Before publishing

```bash
python3 scripts/check.py
python3 scripts/codex-smoke.py
claude plugin validate . --strict  # on a machine with Claude Code
pre-commit install                # once, with pre-commit installed
pre-commit run gitleaks --all-files
```

The [pre-commit configuration](../.pre-commit-config.yaml) pins Gitleaks. The
role catalog and plugin manifests contain no secrets or live account map. For
new third-party skills, record the upstream commit, path, license evidence,
copied content hash, and any local adaptations before adding them to a pack.
