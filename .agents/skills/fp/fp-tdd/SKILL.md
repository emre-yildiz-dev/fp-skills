---
name: fp-tdd
description: Develop one behavior at a time with core-first vertical slices. Use when asked to build behavior test-first or to fix a bug explicitly by writing its regression test before implementation. Do not use to explain TDD, diagnose an existing test, review whether tests are implementation-coupled, or merely run tests.
---

# FP Test-Driven Development

## Stage the guidance

Before choosing a test seam:

1. Read the generic guidance:
   - `../references/project-detection.md`
   - `../references/fcis-architecture.md`
   - `../references/testing.md`
2. Read repository instructions, manifests, lockfiles, source, tests, the agreed feature slice,
   project profile, public seams, and verification commands. Establish `effect_mode`, exact
   installed Effect version, and release channel from project evidence.
3. Only when `effect_mode` is `effect-4`, read the Effect guidance:
   - `../references/effect-4.md`
   - `../references/error-model.md`

If a reference required at its stage is missing, stop and name it. Always load and apply the generic
FCIS and testing guidance. Apply the Effect-specific testing examples in `effect-4.md` only when
`effect_mode` is `effect-4`; otherwise do not add Effect ceremony. Stop on an ambiguous Effect
major, version, or RC. Never apply Effect 3 or another Effect 4 RC by analogy.

For behavioral/API facts, use tests and observed behavior, project source, vendored installed
source, version-matched official documentation, shared references, then memory. For project policy,
use direct user instructions, repository instructions and accepted ADRs, established conventions,
shared references, then memory. Stop and report contradictions rather than silently resolving them.

## State the slice before editing

Write down:

```text
Behavior:
Pure decision:
Successful result:
Expected failures:
Capabilities:
Foreign-error seam:
Public test seams:
Smallest verification command:
```

Stop and ask for a decision when any applicable field cannot be stated. Do not invent a pure
decision for glue-only changes; record `Pure decision: none` with the reason and begin at the first
real shell seam. After exact Effect 4 detection, label the successful result `A`, expected caller-actionable
failures `E`, and capabilities `R`; acquire only narrow capabilities in `R`, narrow foreign errors
once at the owning adapter boundary, and retry only replay-safe work below that translation. In
`effect_mode: none`, keep the generic result, failure, and capability fields above and do not add
Effect notation.

## Make one core-first vertical slice

Use this exact order:

```text
1. Model one value, invariant, event, or state transition.
2. Write one failing ordinary test for the pure decision.
3. Run it and verify failure for the intended reason.
4. Implement the minimum pure decision.
5. Run it green.
6. Write one failing Effect orchestration test with substituted capabilities/test services.
7. Implement the minimum Effect workflow.
8. Add a real adapter integration test when a foreign boundary changes.
9. Add a real wire-contract test when serialization/status behavior changes.
10. Wire the Layer at the composition root.
11. Run the smallest checks after every step and the project gate at the end.
```

For non-Effect work, apply the applicable steps without inventing services or Layers. For glue-only
work, start at the recorded first real shell seam and use the applicable integration or wire test.
Keep ingress decode and egress encoding at their boundaries; do not let raw foreign errors or
unknown values cross serialized sinks.

Keep tests behavioral and independent: reject implementation-coupled tests, tautological expected
values, and horizontal test batches. Ordinary tests prove pure decisions. Effect-aware tests with
substituted capabilities or test services prove orchestration. Real adapter integration tests prove
foreign-boundary behavior, and real wire-contract tests prove serialization and status behavior.
Refactor architecture during review unless a local cleanup is required to keep the just-added slice
understandable.

## Finish the slice

After each red and green transition, retain the smallest command and its result as evidence. In a
planning-only or no-edit response, print the completed slice fields before the numbered red/green
sequence; do not defer that contract to the summary. With exact Effect 4 evidence, use explicit
`A`, `E`, and `R` labels. In `effect_mode: none`, use the generic successful-result, expected-failures,
and capabilities labels without Effect notation. At the end, run the project gate and report the
behavior, A/E/R contract where applicable, test seams, commands, results, and any remaining boundary
or architecture risk. An architecture deviation may
proceed only when its record states the violated rule, rationale, smallest boundary, compensating
controls, and revisit condition; otherwise stop for a decision.
