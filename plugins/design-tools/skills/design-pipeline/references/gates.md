# Gate specifications

Authoritative. Every gate has a precondition, an owner, an exact invocation, an isolation mode, an
artifact, a checkable bar, a skip cost, and a fallback. A gate that cannot state its bar as a
yes/no question is not closed.

Isolation values: `inline` = run in the current context · `subagent` = dispatch a fresh agent told
to use exactly one named skill (`isolation.md`) · `subagent-if-large` = inline while the built
artifact is under 25 KB, subagent above it (see *Isolation is decided by what a gate reads*).

---

## Global rules — read before any gate

### Precedence between artifacts

Gates write documents that overlap, and two of them will eventually disagree. The order, highest
first:

1. Accessibility and correctness floor.
2. `BRAND-CONTRACT.md` §1 tokens, §3 forbidden, §5 e-commerce laws.
3. `.ui-craft/brief.md` §6 learned constraints.
4. `00-intake.md` — what was actually asked for.
5. `03-DIRECTION.md` — **how it looks**: type scale, colour, composition, the signature detail.
6. `.ui-craft/spec.md` — **what is on it**: content inventory, regions, states, acceptance bar.
7. The vendor skill's own defaults.

**G3 outranks G4 on every aesthetic question, and G4 outranks G3 on every content question.** When
they collide on the same value — a type size, a colour, a spacing step — the direction wins, because
G4 exists to structure content and G3 exists to decide appearance.

**The root fix is not to adjudicate but to not duplicate.** G4 must reference the direction's values,
never restate them: write "display size per `03-DIRECTION.md` §3", not the number. A spec that copies
a number has created a second source of truth that will drift the moment the direction is revised.

Tie-break when duplication happens anyway: **a rule stated as a mechanical check beats a rule stated
as a preference**, whichever gate wrote it. "`--text-4xl` appears exactly once, on the commit total"
is checkable; "title is `--text-4xl`" is not.

*Found by the 07-product-page acceptance run: `spec.md` assigned the title `--text-4xl` while
`03-DIRECTION.md` §3 reserved `--text-4xl` for the commit total. The build gate had to adjudicate on
its own and picked the direction, correctly, but nothing in this file told it to.*

### Isolation is decided by what a gate reads, not by what class its owner is

The first version of this file isolated orchestrators and ran every pass inline. That is the wrong
axis. A pass that reads a 100 KB built surface costs the orchestrator as much context as an
orchestrator does.

- **Owner is orchestrator-class** → `subagent`, always. G3, G5.
- **Gate reads the built artifact** → `subagent-if-large`. G6, G8, G9. Inline under 25 KB; above it,
  dispatch — the orchestrator needs its context for the remaining gates, and a gate that runs out of
  room mid-run is worse than one that costs a dispatch.
- **Gate reads only its own small inputs** → `inline`. G0, G1, G4.

Measure the artifact, do not estimate it.

### Unattended runs: gates carry their answers in

Several ui-craft lenses are interactive by design — `brief` asks five questions and shows the draft
before writing, `tokens` asks which file to write and confirms before overwriting, `shape` opens with
three to five clarifying questions and offers the spec persist as opt-in. A pipeline run that
dispatches them bare will stall waiting for a human.

**Every gate invocation must therefore carry:** the answers its owner is going to ask for, drawn from
`00-intake.md` and the brand contract; an explicit statement that this is an unattended pipeline run;
and the instruction to write its artifact without asking for confirmation. `vendors.md` records what
each interactive lens asks. A gate that stalls has failed, not paused.

### A gate closes on a verified artifact, never on a vendor's report

The vendor reports what it believes it did. The orchestrator closes the gate on what is actually on
disk. Before marking any gate `done`:

1. The artifact **exists** at the declared path.
2. Its size is **measured**, not quoted from the report.
3. It is **structurally complete** — for markdown, the required sections; for a built surface,
   balanced tags and no placeholder text.
4. At least **one substantive claim is spot-checked** independently. If the vendor says the
   acceptance bar is green, verify one item yourself.

*Found by the 07-product-page acceptance run: the build gate reported an 80,711-byte file and left a
100,293-byte one, having continued to edit after computing the size. Its substantive claims all held
up, but the discrepancy was found by measuring rather than reading.*

### Status vocabulary

`pending` · `running` · `done` · `skipped` (always with a `cost`) · `done-by-verification` — the
gate's own owner did not run, but the orchestrator verified that the work exists and holds. It
carries a `cost` string like a skip, because what was not run is not known to be unnecessary.

---

## G0 — INTAKE

- **Owner:** this skill (no vendor)
- **Precondition:** none. Always first.
- **Isolation:** inline
- **Produces:** `.studio/<surface>/00-intake.md`

Ask, do not guess. Six answers, and no gate runs until they exist:

1. **Surface** — one name, kebab-case. Becomes the directory and the spec section key.
2. **Job** — what the visitor must be able to do, as one verb and one object ("choose a heater",
   "book a site visit"). Not a feeling, not a list.
3. **Sale mode** — `priced` · `quote-only` · `both`. Drives §5 of the brand contract.
4. **Data** — is there real content and imagery, and where? If no real data exists, say so now;
   the contract forbids inventing product content, so the surface will be built against empty and
   loading states instead of fabricated ones.
5. **DESIGN_VARIANCE 1–10** — layout risk. Dashboards ~4, commerce pages 5–6, landings 7,
   brand/story surfaces 8. This selects the G3 vendor.
6. **Mode** — `full` (all gates) · `ship-fast` (CRAFT_LEVEL 5, G2 and G7 forced off).

Also record: build target detected at G5, whether G2/G7 were requested, and the resolved path of
`BRAND-CONTRACT.md`.

- **Bar:** all six answers recorded, brand contract resolved.
- **On skip:** cannot be skipped. Without intake there is nothing to check the ship verdict against.

---

## G1 — FOUNDATION

- **Owner:** ui-craft — `brief`, then `tokens`
- **Precondition:** G0 closed
- **Isolation:** inline
- **Produces:** `.ui-craft/brief.md`, a token spine in the project

Project-level, not surface-level: runs once per project and is `[✓]` by detection thereafter.

1. Does `.ui-craft/brief.md` exist? If not, run `brief`. Feed it the brand contract — the brief
   must import §1 tokens and §4 anti-slop laws rather than re-deriving a design system.
2. Does a token spine exist (CSS custom properties `--color-*` / `--font-*`, a Tailwind theme
   extension, or a token file)? If not, run `tokens`.

**Never re-open the palette.** The eleven colours and two families in brand contract §1 are canon.
`tokens` establishes the *spine* — primitive → semantic → component — using those values. If it
proposes different hues, the contract wins and the proposal is discarded.

**Unattended.** `brief` will ask five questions and show its draft before writing; `tokens` will ask
which file to write to and confirm before it does. Carry both sets of answers in: product purpose,
primary user, principles, success metric and out-of-scope from `00-intake.md` and the brand contract,
and the target token file resolved from the build target. State that this is an unattended run.

- **Bar:** brief file exists AND a token spine resolves to the contract's values.
- **On skip:** "no brief → the build falls back to skill defaults; composition will not be anchored
  to project principles."

---

## G2 — REFERENCE *(optional, default off)*

- **Owner:** taste-skill — `imagegen-frontend-web` (surfaces) or `brandkit` (identity work)
- **Precondition:** G1 closed; image generation actually available
- **Isolation:** subagent
- **Produces:** `.studio/<surface>/refs/*.png` + `02-refs.md`

**Check the tool first.** If no image generation is available in this session, mark `[–]` and move
on. Do not describe images in prose and call the gate closed — that is the gate lying.

Vendor rule that must survive into the prompt: **one horizontal image per section**, never a
compressed board. A page with eight sections produces eight images, one palette across all of them.

`02-refs.md` records, per image: file, which section, and the one thing the build must take from it.

- **Bar:** one image per planned section, plus `02-refs.md` linking each to a section.
- **On skip:** "direction inferred from text only; no visual target for the build to hit."

---

## G3 — DIRECTION

- **Owner:** `design-taste-frontend` (VARIANCE ≤6) **or** `impeccable` (VARIANCE ≥7)
- **Precondition:** G1 closed
- **Isolation:** **subagent — mandatory**
- **Produces:** `.studio/<surface>/03-DIRECTION.md`

The one gate that decides how the surface looks. It outputs a **document, not code**. Building here
is the most common failure: the agent gets excited, writes markup, and G4/G5 inherit an unexamined
layout with no spec behind it.

`03-DIRECTION.md` must contain, and nothing else:

1. **Thesis** — one paragraph. What point of view is this surface taking, and what is it refusing?
2. **Palette in use** — which contract tokens carry the page, and the one accent's placement budget.
3. **Type pair** — Newsreader × Hanken Grotesk with the actual scale: display size, body size,
   tracking above 24px.
4. **Composition principle** — how the page is organised, stated as a rule the build can check
   ("every section breaks the grid on the opposite side from the one before it").
5. **The signature detail** — one. Named, described precisely enough to build, and built in G5's
   first pass, not deferred to polish.
6. **Forbidden for this surface** — the anti-slop laws that this direction is most likely to
   violate, named explicitly so G9 can check them.

If the direction wants to break a brand-contract §4 law, it names the law and argues for it here.
§1, §3, and §5 cannot be broken by any direction.

- **Bar:** all six sections present; no code produced.
- **On skip:** "no direction document → `craft-intent.md` defaults apply; safe, generic result."
- **Fallback:** if the chosen vendor is unavailable, use `high-end-visual-design`, and record the
  substitution in the artifact.

---

## G4 — SHAPE

- **Owner:** ui-craft — `shape`
- **Precondition:** G3 closed (or explicitly skipped)
- **Isolation:** inline
- **Produces:** `.ui-craft/spec.md` — a `## Surface: <name>` section

Wireframe before code: content inventory with P0/P1/P2 priority, ASCII layout for desktop and
mobile, the state list, and open questions.

**Unattended.** `shape` opens with three to five clarifying questions and treats the spec persist as
opt-in. Carry the answers in — primary action, what is visible by default versus disclosed, what
success looks like, who the user is — and state that the persist is auto-confirmed.

**Do not restate the direction's values.** Reference them. The typography and motion sections of the
spec point at `03-DIRECTION.md`; they do not copy its numbers. See *Precedence between artifacts*.

**Guard:** if `spec.md` already holds a section for this surface, do not append a duplicate — update
it or skip the gate.

Feed `shape` the direction document. Its composition principle constrains the layout; the state
list must already include everything brand-contract §5.8 names (out of stock, quote-only, nothing
selected, shipping unknown, incompatible option).

- **Bar:** spec section exists with an acceptance bar and a state list covering §5.8.
- **On skip:** "no spec → the build has no persisted acceptance bar; G9 checks against nothing."

---

## G5 — BUILD

- **Owner:** ui-craft — `craft <surface>`, with `full-output-enforcement` active
- **Precondition:** G4 closed (or direction present)
- **Isolation:** **subagent — mandatory**
- **Produces:** the surface itself

**Detect the build target first**, do not assume:

- `astro.config.mjs` present → Astro components in the project's existing patterns and Tailwind
  version. Match the neighbours; do not introduce a second styling system.
- `package.json` with a framework → that framework's idiom.
- Neither → one self-contained `index.html`, Tailwind via CDN, GSAP/Three via jsDelivr.

**Recipe coverage is partial.** `craft` ships recipes for `dashboard`, `landing` and `auth` only.
There is **no e-commerce recipe**, and `craft` is explicit that it will not improvise one — it falls
back to standard build mode with the closest reference. For a commerce surface that fallback is
correct, and the gate must supply what the missing recipe would have: **the G4 acceptance bar is the
recipe.** Name the fallback in the build report so the ship gate knows the acceptance bar was the
only contract in force. If the same surface class comes round a third time, author a local recipe
rather than re-deriving it per run.

The subagent receives: brand contract, `03-DIRECTION.md`, the spec section, the reference images if
G2 ran, and the instruction to use `craft` only. The direction's **signature detail is built in this
pass** — the acceptance bar is not green without it.

- **Bar:** every acceptance-bar item from the spec section is green, signature detail present,
  no placeholder comments anywhere in the output. **Verify, do not accept the report** — measure the
  file, check the tags balance, and spot-check at least one acceptance item yourself.
- **On skip:** cannot be skipped.

---

## G6 — STATES

- **Owner:** ui-craft — `unhappy`, then `harden`
- **Precondition:** G5 closed
- **Isolation:** `subagent-if-large` — this gate reads and edits the built surface
- **Produces:** states implemented in the surface

Order matters. `unhappy` is state-first design: it inventories loading, empty, error, partial,
conflict, and offline, and refactors impossible boolean combinations into a proper state machine.
`harden` then fills the production matrix — skeletons, error copy, partial data, i18n, permissions,
first-run guidance.

For commerce surfaces this gate is where the money is. Brand contract §5.8 is the minimum, not the
target.

- **Bar:** every state in the spec's state list renders; no state reachable only by editing code.
- **On skip:** "no state pass → the surface breaks on real data; on a commerce page this is a
  revenue defect, not a polish defect."

---

## G7 — MOTION *(optional, default off)*

- **Owner:** emil-kowalski — `motion-design`, then `emil-design-eng`, then ibelick
  `fixing-motion-performance`
- **Precondition:** G6 closed
- **Isolation:** inline
- **Produces:** motion in the surface

Off by default. Motion is added when there is something worth moving, and commercial surfaces buy
their LCP and INP back by not having it. Turn it on from intake, never by inference.

Sequence: `motion-design` sets timing, easing, and choreography · `emil-design-eng` reviews the
component-level feel and springs · `fixing-motion-performance` enforces compositor-only animation,
a perf budget, and `prefers-reduced-motion`.

`design-motion-principles` is an alternative auditor with an HTML report — use it when the user
wants to *see* the motion review rather than read it.

- **Bar:** reduced-motion path honoured; no animation on layout-triggering properties; INP not
  regressed at G8.
- **On skip:** "static surface — legitimate for v1; add later as a `design-tools` pass."

---

## G8 — AUDIT

- **Owner:** web-quality (Osmani) — `seo`, `core-web-vitals`, `accessibility`
- **Precondition:** G6 closed
- **Isolation:** `subagent-if-large` — three doctrines totalling ~1,460 lines plus the built surface
- **Produces:** `.studio/<surface>/08-AUDIT.md`

Three passes, one merged report, findings ranked by severity. This is the gate ui-craft explicitly
does not cover — it defers SEO strategy by design.

Required for any commerce surface: structured data for `Product` and `Offer`, and
`AggregateRating` **only where a real rating exists** (§5.6 — inventing one is fraud, not SEO).
Record measured LCP, INP, and CLS, or state plainly that they were not measured and why.

`web-quality-audit` is the umbrella version — use it when the surface is small enough that three
separate passes are overkill; note the substitution in the artifact.

- **Bar:** report exists; zero critical findings, or each critical finding has an explicit accepted-
  risk line.
- **On skip:** "not audited → invisible in search and unmeasured on performance."

---

## G9 — SHIP

- **Owner:** ui-craft — `finalize`
- **Precondition:** G5 closed at minimum
- **Isolation:** `subagent-if-large`
- **Produces:** `.studio/<surface>/09-SHIP.md`

`finalize` runs its detector, verifies brief and tokens, applies the ten-pass finish bar, ranks
findings by feedback hierarchy, and returns **READY / NOT READY / BLOCKED**. It produces findings
only — it does not edit code.

Add two checks `finalize` cannot know about:

1. **Brand contract compliance** — §1 tokens, §3 forbidden list, §4 laws the direction did not
   explicitly claim an exemption from, §5 commerce laws.
2. **Direction compliance** — is the signature detail present, and does the composition follow the
   principle stated in `03-DIRECTION.md`?

The verdict prints the full resolved checklist and every `[–]` gate with its downstream cost. A
verdict that hides a skipped gate is a failed verdict.

- **Bar:** a verdict exists with reasons. Silent success is failure. The verdict is written against
  the artifact the orchestrator measured, not the one the build gate described.

**After the verdict.** Findings can still arrive — a stop hook, a review, a fresh pair of eyes. Do
not silently amend the verdict. Append a `## Post-verdict fix` section to `09-SHIP.md` recording the
finding, whether it was assessed as real or as a false positive, the diff if it was fixed, the
re-verification, and whether the verdict changed. Record the same in `STATE.json` under
`post_verdict_fixes`. Suppressing a finding — an ignore rule or an inline waiver — requires the
user's explicit confirmation that it is intentional; the gate never suppresses on its own judgement.
- **On skip:** "no ship verdict — nothing certifies this surface as done."
