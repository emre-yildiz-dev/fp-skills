# Testing Seams

This reference is runtime-agnostic. Load it for every project; load runtime-specific testing guidance only after project detection establishes the runtime and version.

## Core-first vertical slice

Work one public behavior at a time, with independent expected values and one red/green slice at a time. Confirm the public seam before moving to the next step:

```text
model -> failing pure test -> pure decision -> shell orchestration test -> shell workflow
-> adapter integration -> adapter -> wire contract -> composition-root wiring
```

## Pure decision tests

Ordinary pure functions use ordinary tests. Write a failing test against the decision's public input/output algebra; expected values must be computed independently, not copied from the implementation. Test invariants, meaningful branches, and illegal states without clocks, services, or runtime setup.

## Shell orchestration tests

Test shell workflows through capability ports with controlled substitutes. Assert successful results, expected failures, and requested capabilities as public behavior. Supply deterministic time, randomness, identity, and external facts instead of sleeping or using ambient state.

## Adapter integration tests

Exercise each adapter against its real foreign boundary or representative integration harness. Confirm the one projection/narrowing seam, resource behavior, and replay-safe retry policy. Do not substitute the adapter implementation when the question is its vendor behavior.

## Wire contract tests

Exercise real ingress decode and egress encode or request/response behavior. Assert the public schema, status/result mapping, and redaction; no raw foreign failure may cross the wire. Finish the slice by checking wiring at the composition root.
