---
name: fp-implement
description: Implement an approved specification as core-first functional slices with Effect-aware boundaries and verification.
disable-model-invocation: true
---

# FP Implement

Implement an approved specification through one completed tracer slice at a time. This workflow is
self-contained: do not invoke another skill mechanism.

## Stage the evidence

First confirm all six declared references exist; stop and name a missing file:

- `../references/project-detection.md`
- `../references/fcis-architecture.md`
- `../references/effect-4.md`
- `../references/error-model.md`
- `../references/testing.md`
- `../references/artifact-contracts.md`

Read the generic guidance before work: `project-detection.md`, `fcis-architecture.md`,
`testing.md`, and `artifact-contracts.md`. Read all relevant repository instructions, the approved
specification and every source it cites, decision ledger, ADRs, manifests, lockfiles, existing
source/tests, and project verification commands. Run project detection and record the artifact and
command conventions, `effect_mode`, exact installed Effect version, and release channel.

Only when detection proves `effect_mode: effect-4`, read `effect-4.md` and `error-model.md`.
Otherwise, do not add Effect ceremony. Stop on an ambiguous Effect major, exact version, or RC;
never apply Effect 3 or another Effect 4 RC by analogy.

For behavioral/API facts, prefer tests and observed behavior, project source, vendored installed
source, version-matched official documentation, shared references, then memory. For project policy,
prefer direct user instructions, repository instructions and accepted ADRs, established conventions,
shared references, then memory. Surface contradictions with their sources; do not silently choose.

## Preflight the approved contract

Before editing, verify the specification identifies the applicable:

- pure decisions, values, invariants, and explicit output algebras;
- capability ports and their owners;
- success, expected errors, and requirements (`A`, `E`, and `R`) for Effect workflows;
- ingress/egress adapters, foreign-error narrowing, and safe serialization;
- Layer dependencies, composition root, resource/retry/idempotency/interruption decisions; and
- pure, orchestration, adapter, wire, and Layer test seams with verification commands.

Stop for a decision if an applicable contract is absent, sources contradict it, or an architecture
deviation is undocumented. A permitted exception record must state the violated rule, rationale,
smallest boundary, compensating controls, and revisit condition; add an ADR only when the repository
criteria require one.

List tracer slices in dependency order from the specification. Select only the first unfinished
slice; do not batch horizontal work or start a later slice.

## Complete one core-first slice

State the selected behavior, pure decision, `A`/`E`/`R` where applicable, foreign-error seam,
public test seams, and smallest verification command. Then use this loop, retaining each command
and observed red/green result:

```text
model -> pure red/green -> orchestration red/green -> adapter evidence
-> wire evidence -> Layer wiring -> focused checks -> project gate
```

Model one value, invariant, event, or transition. Write and run one failing ordinary behavioral test
for the pure decision; implement the smallest pure change and run it green. For Effect work, write
and run a failing orchestration test with substituted capabilities or test Layers, then implement
the smallest workflow. Use ordinary tests for pure decisions and Effect-aware tests/test
capabilities for orchestration. Add real adapter integration evidence when a foreign boundary
changes, and real decode/encode or request/response evidence when a wire boundary changes. Wire
Layers only at the composition root.

Keep external facts as values in the core. Narrow foreign errors once at their owning adapter;
retain caller-actionable outcomes in typed `E`; preserve interruption; and keep raw failures,
`Cause`, credentials, and arbitrary unknown values out of serialized sinks. Retry only replay-safe
work below foreign-error translation. Run focused checks throughout, then the named project gate.

Do not refactor unrelated architecture while implementing a slice unless a local cleanup is needed
to keep that slice understandable. Do not run `git commit`, `git push`, or create a pull request
automatically.

## Report and continue deliberately

After the project gate, report exactly:

```md
## Implemented slices
## Pure-core changes
## Shell and capability changes
## Error/serialization changes
## Layer-graph changes
## Architecture exceptions
## Verification commands and observed results
## Remaining slices
```

Include red and green evidence, applicable `A`/`E`/`R` contracts, changed test seams, exception
records, and the next unfinished slice. Stop before that next slice unless asked to continue.
