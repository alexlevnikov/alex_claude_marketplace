# Maintaining the Hermes architecture library

The Git checkout is the durable memory of Hermes design work. It holds reusable mechanics and research, not bot runtime state.

## Read and write cycle

1. Search `references/components/`, `references/decisions/`, `references/patterns/`, the deep research in `docs/`, and the official catalog before choosing a mechanism.
2. Separate claims from the current official site, the pinned `v2026.9.14` source, and the observed target bot. Record the evidence and date. Mark uncertain findings `provisional`; a documentation match is not runtime proof.
3. Add or update one component card for a reusable mechanism. Add a pattern for a repeatable design. Record an architecture decision as `accepted` only after the owner chooses it; otherwise use `proposed`. Link replacements with `supersedes` rather than rewriting history.
4. Store service-specific deployments in the bot repository or a private operations map. Do not put real host maps, addresses, tailnet names, profiles, secrets, sessions, user memory or raw API responses in this public plugin.
5. Run `python3 scripts/validate_knowledge.py`, inspect the diff and verify primary sources before publishing. The validator checks structure and obvious leaks; it cannot establish factual accuracy.

## Record format

Records under `references/components/`, `references/decisions/` and `references/patterns/` use simple YAML-style scalar frontmatter: `id`, `kind`, `status`, `pinned_tag`, and `verified_utc`. Component status is `verified`, `provisional`, or `retired`; decision status is `proposed`, `accepted`, or `superseded`; pattern status is `draft`, `verified`, or `retired`. Use a stable ID matching the filename. The body should state use conditions, boundaries, evidence, and review trigger. See existing records for examples.

Deep studies belong in `docs/`; the [component index](components/index.md) links their relevant mechanics. Do not duplicate full research in a short component card. `SKILL.md` remains a router, not an encyclopedia. Plain-text search is the default index; generated indexes may be added only when the corpus needs them.
