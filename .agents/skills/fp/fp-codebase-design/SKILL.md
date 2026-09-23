---
name: fp-codebase-design
description: Design functional cores, capability ports, adapters, package boundaries, and composition roots. Use when shaping architecture, interfaces, test seams, effect placement, or Effect services and Layers—not for package installation, API lookup, styling, or typo fixes.
---

# FP Codebase Design

Stage the required references before designing:

1. Read the generic guidance:
   - `../references/project-detection.md`
   - `../references/fcis-architecture.md`
2. Inspect repository instructions, manifests, lockfiles, source boundaries, tests, and the
   glossary, decision ledger, and ADRs. Establish `effect_mode`, exact installed Effect version,
   and release channel. Stop on an ambiguous Effect major or RC before loading Effect guidance.
3. Only when `effect_mode` is `effect-4`, read:
   - `../references/effect-4.md`
   - `../references/error-model.md`
   - `../references/testing.md`

These are exactly this skill's five declared references. If a reference required at its stage is
missing, stop and name it. Always use the generic FCIS guidance; for `effect_mode: none`, do not
load or introduce Effect-specific terminology. Never apply Effect 3 or a different Effect 4 RC by
analogy.

## Establish the design evidence

Consume the project profile, design question, domain artifacts, and existing source boundaries
before proposing a shape. Treat behavioral/API evidence in this order: tests and observed behavior,
project source, vendored installed source, version-matched official documentation, shared
references, then memory. For policy, use direct user instructions, repository instructions and
accepted ADRs, established conventions, shared references, then memory. Surface contradictions with
their evidence instead of smoothing them over.

Identify the smallest feature slice and the public behavior it must preserve. Keep domain language
separate from transport, persistence, vendor, and runtime names. A package should own a coherent
policy or capability, not a directory-shaped collection of files.

## Produce the design map

Return a map with these sections and name the owning module or package for every element:

## Core
- domain values and invariants
- pure decisions and signatures
- state transitions and events

State every external fact as an input value. Make meaningful branches explicit in a return algebra;
do not hide them in mutation, exceptions, or service acquisition. The core contains no I/O, clock,
randomness, logging, vendor types, `Context.Service`, `Layer`, or runtime launch.

## Shell
- external facts and effects
- capability ports and owners
- adapters/interpreters

Name a capability for what the application can do, give it a clear owner, and keep its algebra
small. Introduce a service only for a real capability boundary with varying interpreters, controlled
external effects, or a public test seam; reject service objects that merely group functions. Keep
adapters at the shell and reject domain contracts that leak database, HTTP, SDK, or other vendor
types.

## Boundaries
- ingress decoding
- error translation
- serialized egress
- public test seams

Decode unknown input at ingress, project each foreign failure once at its owning adapter boundary,
and encode known values at egress. Provide an error map from source failure to typed domain or
application error, recovery owner, and serialized representation. Do not serialize raw foreign
errors, `Cause`, credentials, or arbitrary unknown values. Identify pure-decision, capability,
adapter-integration, and wire-contract seams.

## Effect graph (Effect projects only)
- Effect<A, E, R> signatures
- Context.Service capabilities
- Layer dependencies
- composition root
- resource and concurrency ownership

For each workflow, show its `A`, caller-actionable `E`, and minimal `R`. Draw capability and Layer
dependency edges, name each interpreter, and identify the one composition root that assembles the
complete graph and launches the runtime. Assign scope/finalizer, concurrency, interruption,
durability, and shutdown ownership; do not scatter Layer construction or `run*` bridges.

## Favor deep, deletable boundaries

Preserve the deep-interface goal in functional terms: hide coordinated policy and interpreter
details behind a small, meaningful domain algebra or capability port, not behind a wide facade that
mirrors its implementation. Apply the deletion test: mentally delete an internal module,
interpreter, or adapter and ask whether callers retain enough implementation detail to recreate it.
If they do, shrink the public algebra and move that detail behind its owner. Do not use this test to
hide domain decisions that callers genuinely need to choose among.

## Compare material shapes

For an architectural decision, lead with a recommendation, then present two or three materially
different shapes rather than superficial renames. Compare each on purity, algebra size, capability
ownership, error locality, Layer complexity when applicable, testing cost, and migration cost.
Explain why the recommendation best fits repository evidence and settled decisions.

If a proposed shape violates an architectural rule, stop until its decision record states the
violated rule, rationale, smallest exception boundary, compensating controls, and revisit condition.
Use the ADR gate for hard-to-reverse, surprising trade-offs.

## Finish

Report the core/shell/boundary map, capability graph, error map, Effect graph when applicable,
public test seams, recommended shape and alternatives, open contradictions, and any recorded
architecture exceptions. Recommend `fp-to-spec` when the design is settled; otherwise name the
specific unresolved decision.
