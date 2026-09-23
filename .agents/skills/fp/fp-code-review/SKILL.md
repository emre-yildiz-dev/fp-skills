---
name: fp-code-review
description: Review a diff independently against repository standards, its originating specification, and FCIS/Effect architecture. Use only when the user explicitly asks to assess a branch, pull request, or fixed change set—not to implement review fixes, explain code, run tests, or refactor.
---

# FP Code Review

Review a completed change without modifying it. This discipline is self-contained: read files directly
rather than invoking another skill mechanism. Produce three independent finding lists: Standards, Spec,
and FCIS/Effect. Do not merge or rerank findings across those axes.

## Load the review guidance

First confirm all six declared references exist; stop and name any missing file:

- `../references/project-detection.md`
- `../references/fcis-architecture.md`
- `../references/effect-4.md`
- `../references/error-model.md`
- `../references/testing.md`
- `../references/artifact-contracts.md`

Read repository instructions, manifests, lockfiles, relevant source and tests,
`project-detection.md`, `fcis-architecture.md`, `testing.md`, and `artifact-contracts.md`. Always
apply generic FCIS guidance. Detect Effect from resolved project evidence and record `effect_mode`,
exact version, and release channel. Only when that evidence proves `effect_mode: effect-4`, read
`effect-4.md` and `error-model.md`; otherwise do not add Effect ceremony. Stop on an ambiguous
Effect major, exact version, or RC; never apply Effect 3 or another Effect 4 RC by analogy.

For behavioral/API facts, prefer tests and observed behavior, project source, vendored installed
source, version-matched official documentation, shared references, then memory. For project policy,
prefer direct user instructions, repository instructions and accepted ADRs, established conventions,
shared references, then memory. Surface contradictions rather than silently choosing one.

## Establish a reviewable diff

Require a user-supplied fixed point (commit, branch, tag, or other immutable revision); ask for one
if absent. Resolve it, calculate the merge base, and inspect only the three-dot diff
`<fixed-point>...HEAD`. Reject an empty diff. Do not substitute a two-dot diff or review unrelated
history.

Locate the originating specification from user input, commit references, or repository conventions.
If none is available, mark the Spec axis unavailable rather than inventing a requirement. Read the
documented repository standards that apply to the changed paths. Remain read-only: do not edit files,
format, generate artifacts, stage changes, commit, push, or create a pull request.

## Review each axis independently

Keep separate notes and produce one list for each axis.

### Standards

Compare every relevant changed hunk to the documented repository standards. Each finding cites the
exact repository rule and changed hunk; do not treat generic preference as a repository rule.

### Spec

Compare changed behavior to the originating specification. Quote the requirement and classify each
finding as `missing/partial`, `wrong behavior`, or `scope creep`. When no originating specification
is available, output `Spec: unavailable` with the search evidence and do not infer requirements.

### FCIS/Effect

Review the diff against FCIS guidance regardless of project type; apply Effect-specific checks only
when Effect 4 was established. Check at least:

```text
hidden effects in policy; partial decisions; infrastructure types in domain contracts;
adapter-shaped services; accidental R; actionable errors converted to defects;
foreign errors retained in failed values; catch-all recovery; retry above narrowing;
non-idempotent replay; interrupts counted as failures; unowned detached fibers;
Layer construction outside roots; scattered run* bridges; unsafe serialized sinks;
wrong test seam or missing control.
```

For applicable findings, identify the smallest corrective action. In particular, keep pure decisions
ordinary-testable and require Effect-aware tests with test capabilities for Effect orchestration.
Retry must stay below foreign-error translation and wrap replay-safe work only. Treat raw `Cause`,
foreign errors, credentials, and arbitrary unknown values at serialized sinks as unsafe. Require an
architecture deviation to record the violated rule, rationale, smallest boundary, compensating
controls, and revisit condition.

## Delegate only by explicit request

When the operator explicitly requested delegation and a subagent capability is installed,
run the three axes in independent read-only contexts. Otherwise run them sequentially,
clearing working notes between axes and preserving the same output separation.

## Report findings

For every finding, use this shape:

```json
{
  "axis": "standards | spec | fcis-effect",
  "severity": "critical | high | medium | low",
  "location": "path:line",
  "evidence": "changed behavior and cited rule",
  "recommendation": "smallest corrective action"
}
```

Output `## Standards`, `## Spec`, and `## FCIS/Effect` independently, including explicit empty
lists. Within an axis, rank only that axis's findings by severity and evidence. State the fixed point,
merge base, reviewed three-dot range, standards sources, specification source or unavailability, and
Effect detection evidence. Report no finding without a changed-hunk location and cited evidence.
