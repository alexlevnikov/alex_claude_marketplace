# The repositories, one by one

Snapshot taken **2026-08-20**. Paths and wiring are stable; branch tips are not — re-derive
them with `audit.sh` rather than quoting the numbers below back at Alex.

`$ROOT` throughout is `~/Library/Mobile Documents/com~apple~CloudDocs/alex.levnikov.root`.
Quote it. The path contains spaces and `com~apple~CloudDocs`, where `~` is a literal
character, not your home directory — an unquoted `cd` lands somewhere surprising or fails.

---

## Sauna — planning, catalog, decisions

- `$ROOT/Sauna` · remote `git@github.com:alexlevnikov/banya-builder-bay-area.git` (SSH)
- Working branch `v3/b0-data-foundation`; `main` exists on origin and is not where work lands.
- **Deliberately not kept in sync with GitHub (decision V24).** Local commits accumulating
  here is the intended state, not a problem to fix. Ask before pushing.
- No code — plans, research, the product catalog and its Python pipeline. Site code lives in
  `yoursaunas-site`, theme code in `yoursaunas-theme`.

Two automations run in this repo and both matter to git work:

| Hook | What it does |
|---|---|
| `SessionStart` → `scripts/session-start.sh` | prints `STATUS.md`, and warns if it is older than 7 days |
| `Stop` → `scripts/session-end-check.sh` | **refuses to end the session** if planning files changed but `STATUS.md` did not |

So a session that edits anything under `roadmap/` or `docs/` must also update `STATUS.md`
before it can finish. Permissions in `.claude/settings.json` are `bypassPermissions` with a
deny list: `_archive/**` is unreadable by design, and `shopify theme publish` /
`shopify theme push --live` are denied outright — nothing here may publish a theme.

**Commit convention across all of Alex's repos:** English, Conventional Commits prefix, a
body that says *why* rather than restating the diff, and a `Co-Authored-By: Claude …`
trailer on agent-written commits. Match the last three commits of the repo you are in.

---

## yoursaunas-theme — the storefront theme (a Horizon fork)

- `$ROOT/yoursaunas-theme` · remote HTTPS `alexlevnikov/yoursaunas-theme`
- Branches: `main`, **`staging`** (where work goes), `skill/yoursaunas-horizon` (a skill,
  parked).
- **`staging` is wired to Shopify theme `152536514721`** (unpublished). The live theme is
  `152528158881` and is *stock Horizon* — the ordinary storefront URL does not render this
  work. Preview with `?preview_theme_id=152536514721` on top of a storefront-password login.
- **Every measurement needs that parameter, or it measures the stock theme.** A bare URL
  returns Horizon's own defaults — including its Russian UI strings, which on 2026-08-20 was
  read as "the store language change did not work" and kept a blocker open an extra day while
  the response header already said `content-language: en-US`. Budgets, screenshots and
  acceptance checks are all worthless without the preview id.

Two things happen when you push `staging`, and both have bitten:

1. **Shopify deploys the branch into that theme.** The store sits behind a password, so this
   is not a public release — but it is a real deploy.
2. **The integration is two-way.** Anything pushed *to the theme* by other means
   (`shopify theme push`, the theme editor) comes back as a commit authored by
   `shopify[bot]`, titled `Update from Shopify for theme yoursaunas-theme/staging`, and
   Shopify reformats JSON templates while it is there. Fetch before assuming your local
   `templates/*.json` is ahead.

CI (both fire on push and PR to `main`/`staging`):

| Workflow | Gate |
|---|---|
| `.github/workflows/theme-check.yml` | Theme Check, `--fail-level error`, node 22, `npm ci` + `npx shopify` (version pinned in `package-lock.json`) |
| `.github/workflows/quality.yml` | weight / request / DOM / image budgets from `scripts/budgets.json`, measured against the **staging theme preview on the CDN** |

`quality.yml` needs three repository secrets — `SHOPIFY_STORE`, `STAGING_THEME_ID`,
`SHOPIFY_FLAG_STORE_PASSWORD` — and fails without them. The fine-grained PAT cannot create
them (see `auth.md`); Alex adds them in the repo settings UI.

**Never budget against `shopify theme dev`.** Measured 2026-08-19: the same homepage is
5015 KB through the dev server and 433 KB through the CDN. The dev server serves assets
uncompressed; budgeting against it measures the dev server.

### The second clone — `~/Projects/yoursaunas-theme`

Same repo, outside iCloud. It held `quality.yml` for two days while the iCloud clone held the
CLI pin, and neither was on GitHub. Merged and pushed 2026-08-20 (`8cbfeef`); every ref,
the stash and the working tree were checked before declaring it redundant. **It can be
deleted** — that is task `T6` in `Sauna/STATUS.md`. Until it is, treat it as a place work
can hide.

---

## yoursaunas-site — the v1 lead-generation site (Astro, Cloudflare)

- `$ROOT/yoursaunas-site` · remote HTTPS `alexlevnikov/yoursaunas-site` · deploy config
  `wrangler.jsonc`
- `main` is current on GitHub. `feat/lead-form-actions` is **6 commits local by choice**
  (`GIT-3`) — Alex decided 2026-08-19 to push only `main`. Do not "fix" it silently.
- Its remote was SSH and was converted to HTTPS on 2026-08-19; 39 commits went out in that
  one push, and 14 iCloud conflict copies (`«file 2.ts»`) were deleted in the same pass.
- `yoursaunas.com` still serves this site. The Shopify storefront has not taken the domain.

---

## design-studio — design bake-off

- `$ROOT/design-studio` · **no remote at all.** One commit (`d24b4a4`, 7 848 files) created
  2026-08-19; before that the repo had zero commits and every file existed only in iCloud.
- To publish it (`GIT-1`), when Alex asks:
  `gh repo create alexlevnikov/design-studio --private --source "$ROOT/design-studio" --push`
- Scanned for secrets before that commit: `.mcp.json` clean, `.env.example` empty, the only
  `sk-` matches were the substring inside "ri**sk-**management".

---

## Agents OS — the umbrella for the personal Agentic OS

- `$ROOT/Agents OS` is a **symlink** to `$ROOT/Agents OS.nosync`. The `.nosync` suffix is how
  a folder is kept out of iCloud sync; the symlink preserves the familiar path. One repo,
  not two — a `git status` in either is the same repository.
- Remote HTTPS `alexlevnikov/agentic-os`, branch `main`, three submodules:
  `financial-agent`, `meditation-agent`, `coding-agent` (each its own GitHub repo).
- In a submodule, `git rev-parse --show-superproject-working-tree` returns the umbrella —
  and returns an *empty string with exit 0* when run in the umbrella itself, so test for
  emptiness, not for failure.
- For anything about what runs on the box, use the `agents-os:hetzner-server` skill.

---

## claude_plugins — the plugin marketplace (this repo)

- `$ROOT/claude_plugins` · remote HTTPS `alexlevnikov/alex_claude_marketplace` · `main`
- Claude Code installs the marketplace **from GitHub**, so an edit here does nothing until it
  is committed *and pushed*, followed by `claude plugin marketplace update` and a session
  restart. The full loop and the authoring rules are in `docs/AUTHORING.md`.
- Never commit keys here: it is iCloud-synced *and* public-facing on GitHub.

---

## Finances

- `$ROOT/Finances` · remote `git@github.com:alexlevnikov/finances.git` (SSH) · `main`, clean.
- Its bot clones this repo; `__pycache__` was tracked once and froze that clone for 13 days.
  Keep generated files out.
