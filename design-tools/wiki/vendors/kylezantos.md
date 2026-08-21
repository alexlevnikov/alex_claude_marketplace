# design-motion-principles — kylezantos

**Repo:** https://github.com/kylezantos/design-motion-principles · **Install:** git clone; the repo is nested (`<repo>/skills/design-motion-principles`), so the inventory keeps the clone as `_repo-design-motion-principles` and symlinks the skill in (repaired 2026-08-20).
**In the set:** 1 tool — `design-motion-principles` (122 lines).

## What it is

Three motion lenses — Emil Kowalski, Jakub Krehel, Jhey Tompkins — in one skill with two modes:
**build** interactive components with purposeful motion, or **audit** existing animations for
AI-slop motion patterns. The audit mode emits an **HTML report with looping demos**, which is the
reason it is in the set: it is the one motion reviewer whose output the owner can *watch*.

## The contract

Use the audit mode when a visible review is wanted (`collisions.md` §3); use `improve-animations`
(Emil) when a text plan for other agents is wanted.

## Engage

- Router: "I want to see the motion review" → `design-motion-principles` (audit).
- Direct: `/design-tools:design-motion-principles audit <target>`.
