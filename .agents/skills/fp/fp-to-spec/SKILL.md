---
name: fp-to-spec
description: Synthesize the current conversation and project evidence into an FCIS and Effect-aware implementation specification without repeating the interview.
disable-model-invocation: true
---

# FP To Spec

## Stage the evidence

First confirm that all six declared reference files exist; stop and name any missing file:

- `../references/project-detection.md`
- `../references/fcis-architecture.md`
- `../references/effect-4.md`
- `../references/error-model.md`
- `../references/testing.md`
- `../references/artifact-contracts.md`

Read `project-detection.md`, `fcis-architecture.md`, and `artifact-contracts.md`. Read repository
instructions, the current conversation, glossary, decision ledger, ADRs, relevant artifact
contracts, manifests, lockfiles, source, and tests. Establish `effect_mode`, the exact installed
Effect version, and release channel. Stop on an ambiguous major, version, or RC. Only when
`effect_mode` is `effect-4`, then read `effect-4.md`, `error-model.md`, and `testing.md`. Always
apply FCIS guidance; when Effect is absent, do not add Effect-specific ceremony or apply Effect 3
or another Effect 4 RC by analogy.

Use behavioral/API facts in this order: tests and observed behavior, project source, vendored
installed source, version-matched official documentation, shared references, then memory. For
policy use: direct user instructions, repository instructions and accepted ADRs, established
conventions, shared references, then memory. Detect contradictions between the conversation,
artifacts, policy, and code evidence. Stop and report the conflicting claims and source paths;
do not smooth them into specification prose.

## Synthesize; do not rediscover

This skill is not a discovery interview. Do not repeat questions already settled in the current
conversation, glossary, ledger, ADRs, or repository evidence. Ask only for a missing source
artifact or confirmation of the proposed public test seams. Follow existing specification
locations and format; otherwise use the default from `artifact-contracts.md`.

Build a trace for every ledger decision: place it in the relevant specification section or state
explicitly why it is out of scope. Preserve settled constraints and rejected alternatives where
they constrain implementation. Reconcile no contradictions implicitly. Keep prose implementable
but do not include raw implementation snippets; a small input/output algebra or state-machine
shape is allowed only when prose would be less precise.

Write one complete specification with every section from `artifact-contracts.md`:

1. **User-visible behavior and scope** — outcomes, exclusions, and acceptance boundaries.
2. **Domain vocabulary, values, invariants, and state transitions** — glossary terms and legal
   state changes.
3. **Pure decision functions and their input/output algebras** — supplied external facts as values
   and explicit meaningful branches.
4. **Effect inventory** — actual time, randomness, persistence, network, queues, concurrency, and
   observability work.
5. **Capability ports and owning packages** — small capability algebras and their owners.
6. **A, E, and R contracts** — success, caller-actionable expected failures, and minimal required
   capabilities for each Effect workflow when Effect 4 is detected.
7. **Adapter and error-translation table** — ingress decode, foreign-error narrowing owner, typed
   result, recovery owner, and serialized egress.
8. **Layer dependency graph and composition root** — interpreters, edges, assembly, and runtime
   launch when Effect 4 is detected.
9. **Resource, retry, idempotency, interruption, and shutdown decisions** — lifecycle and replay
   ownership; state an explicit decision even when none applies.
10. **Security and serialization sinks** — decode/encode boundaries and redaction constraints for
    logs, spans, wire bodies, events, queues, and persisted JSON.
11. **Core-first test slices** — pure decision, substituted-capability service, adapter integration,
    and wire seams in implementation order.
12. **Architecture exceptions** — each exception's violated rule, rationale, smallest boundary,
    compensating controls, revisit condition, and qualifying ADR link.

For a non-Effect project, populate the same contract with actual shell ownership and mark only
Effect-specific `A`/`E`/`R` and Layer details as not applicable; do not invent services or Layers.

## Confirm and finalize

Before finalizing, present the proposed public test seams: pure decisions, capability ports,
adapter integrations, and wire contracts that apply. Ask the user only to confirm those seams;
if confirmation exposes a contradiction, stop and report it. After confirmation, finalize the one
approved specification and end with the source paths consulted, ledger-decision trace or explicit
out-of-scope placements, unresolved risks, and any unresolved contradictions.
