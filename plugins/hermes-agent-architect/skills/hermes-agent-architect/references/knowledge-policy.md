# Updating Hermes Architect

This Git directory is the durable memory of Hermes architecture work. Keep
platform facts, design decisions and operational observations distinct.

## During a task

1. Search existing references and `data/docs-catalog.json` before proposing a
   mechanism. Check the pinned source and the actual target bot when relevant.
2. Record a reusable finding only when its evidence, version and scope are
   clear. Keep a provisional claim explicitly provisional.
3. Record an architecture decision as **accepted** only after the owner chooses
   it. Before that, mark it **proposed**. Link a later replacement to the old
   decision rather than silently rewriting history.
4. Put service-specific deployment state in the service's source repository or
   `/srv/repos/agent-lab-mvp/docs/HERMES-SERVICES.md`. Do not store live profiles,
   secrets, user memory, sessions or API dumps in this plugin.

## Where to write

- `references/decision-guide.md`: concise routing guidance that affects many
  future designs.
- `references/decisions/<id>.md`: one accepted or proposed architecture choice;
  include problem, options, choice, rationale, scope, evidence, date and a
  review condition.
- `references/patterns/<id>.md`: a reusable bot recipe with prerequisites,
  configuration without secrets, validation and rollback.
- `docs/`: deep research and readable overviews. Label the evidence boundary
  between current documentation, pinned tag and observed runtime.
- `data/docs-catalog.json`: the generated index of official docs. Change it
  through `scripts/build_catalog.py` and review the diff.

An empty directory does not need to be created. Search the corpus with `rg`
and the docs script. Add a new index or database only when plain text search
becomes insufficient. Run the skill validator and targeted script checks before
committing. A Git commit changes this knowledge; it does not redeploy a bot.
