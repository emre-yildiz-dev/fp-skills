---
name: fp-grill-with-docs
description: Interview the user to resolve a design while maintaining domain vocabulary, a complete decision ledger, and selective ADRs.
disable-model-invocation: true
---

# FP Grill With Docs

Stage required references before the first question:

1. First read the generic guidance:
   - `../references/project-detection.md`
   - `../references/fcis-architecture.md`
   - `../references/artifact-contracts.md`
2. Inspect the repository and establish `effect_mode`, exact installed Effect version, and release
   channel. If the version or release channel is ambiguous, stop before loading Effect guidance.
3. Only when `effect_mode` is `effect-4`, then read the Effect guidance:
   - `../references/effect-4.md`
   - `../references/error-model.md`
   - `../references/testing.md`

If a reference required at its stage is missing, stop and name it. For `effect_mode: none`, do not
load Effect guidance.

## Establish the evidence base

Inspect before interviewing. Build the project profile from repository instructions, manifests and
lockfiles, existing source and tests, artifact conventions, decision ledgers, ADRs, and glossary.
Answer repository facts through that inspection; ask the user only for choices that evidence cannot
settle. Give behavioral/API evidence precedence to tests and observed behavior, then project source,
vendored installed source, version-matched official documentation, shared references, and memory.
Give policy precedence to direct user instructions, repository instructions and accepted ADRs,
established conventions, shared references, and memory. Surface contradictions with their evidence.

Always use the FCIS guidance. Do not use Effect 3 or a different Effect 4 RC by analogy. For
`effect_mode: none`, keep the interview useful without Effect-specific branches.

Choose existing artifact locations and formats first; otherwise use the artifact-contract defaults.
Locate or create the glossary and decision ledger before asking a decision question.

## Build and walk the design tree

Map each unsettled design choice as a node with its prerequisites, evidence, owner, and artifact
impact. Mark repository facts as inspected, user decisions as settled only after an answer, and
contradictions as unresolved. Build a dependency tree rather than a flat questionnaire:

1. Scope, users, outcomes, domain vocabulary, values, invariants, illegal states, and state
   transitions.
2. Pure decisions, their supplied inputs (including required external facts as values), explicit
   output algebra, and acceptance scenarios.
3. Effects needed to acquire facts or execute outcomes, boundary ownership, capabilities, and test
   seams.
4. Only when detection says `effect-4`, extend the tree with `Effect<A, E, R>` contracts;
   capability ownership; adapters and error translation; retry and idempotency; resources and
   finalizers; interruption; concurrency; serialized sinks and observability; the Layer graph;
   composition root; and core, service, adapter, and wire test seams. Revisit the domain
   invariants, pure decisions, and required external facts at these boundaries so every effectful
   branch has an explicit core/shell contract.

Ask only frontier nodes whose prerequisites are settled. In each round ask at most four frontier
questions because Pi's structured question tool has a four-question limit. For every question,
state the decision it unlocks, a recommended answer, and its trade-off. Do not ask a repository
fact as though it were a user preference. Wait for the user's answers after each round; do not
advance to a dependent question while an answer is pending.

## Persist answers as they land

After each answer, update the tree and immediately persist all settled knowledge:

- Update `CONTEXT.md` only with resolved domain terms, definitions, states, transitions, and
  essential distinctions. Do not put Effect, database, HTTP, or Layer implementation details there
  unless they are domain language.
- Append every settled decision to the ledger with its question, decision, constraints, rejected
  alternatives, core/shell/boundary impact, `A`/`E`/`R` or other contract impact, test implication,
  and ADR qualification. Do not leave an ordinary decision only in conversation.
- Create an ADR only if the decision is hard to reverse, surprising without context, **and** arose
  from a real trade-off. Otherwise record that ADR was declined in the ledger.
- For every architecture deviation, record the violated rule, rationale, smallest exception
  boundary, compensating controls, and revisit condition. Create an ADR too only when it passes
  the same three-part gate.

Cross-check new claims against repository evidence before recording them. Keep contradictions
visible rather than resolving them implicitly.

## Complete

End only when the frontier is empty **and** the user confirms shared understanding. Then report:

```text
Settled decisions
Changed glossary entries
Decision ledger path
ADRs created or declined
Architecture exceptions
Unresolved contradictions
Recommended next skill: fp-codebase-design or fp-to-spec
```

Recommend `fp-codebase-design` when ownership, ports, adapters, or composition need design;
recommend `fp-to-spec` when the design is settled and ready for synthesis.
