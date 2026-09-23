---
name: fp-domain-modeling
description: Resolve or model domain vocabulary, invariants, state transitions, policy contradictions, and durable design decisions. Use only when a request requires resolving a term, modeling a domain rule or state, reconciling a semantic contradiction, or recording a durable decision—not for prerequisite reads, summaries, spelling, headings, or renames in domain artifacts or code.
---

# FP Domain Modeling

Before changing the domain model, read:

- `../references/project-detection.md`
- `../references/fcis-architecture.md`
- `../references/artifact-contracts.md`

If any required reference is missing, stop and name it.

## Discover before asking

Build the project profile required by project detection. Read repository instructions, the
existing `CONTEXT.md`, decision ledger, ADRs, and relevant code and tests before asking the
user for facts that the repository can answer. Follow existing artifact locations and formats;
use the artifact-contract defaults only when the repository has none.

Treat tests and observed behavior as stronger evidence than source, and source as stronger than
memory. Treat direct user instructions, repository policy, and accepted ADRs as stronger than
generic guidance. Surface contradictions with their evidence rather than silently selecting one.
When Effect is present, establish its exact version and release channel before relying on an
Effect-specific claim; stop on unresolved version ambiguity rather than applying another version
by analogy.

## Model the language

1. Inspect the current glossary, ledger, ADRs, code, and tests. Ask only the smallest question
   that remains necessary.
2. Challenge overloaded terms. Name which words are domain concepts and which are infrastructure
   concepts; do not let a transport, database, Effect, or Layer name stand in for a business
   concept.
3. Use concrete, representative scenarios. For each, identify the values involved, invariant,
   legal and illegal states, trigger, transition, outcome, and the owner of the policy.
4. Cross-check each user claim against code and tests. Mark confirmed facts, deliberate changes,
   and contradictions separately. Keep the pure decision visible: if external facts were already
   values, state the remaining domain decision without I/O.
5. Prefer explicit states and transitions over ambiguous flags or hidden mutation. State the
   result algebra or failure outcome needed for a caller to distinguish meaningful branches.

## Persist only durable domain knowledge

As soon as vocabulary is resolved, update `CONTEXT.md` inline with terms, definitions, states,
transitions, and essential distinctions. Do not add unresolved proposals. Keep Effect, database,
HTTP, and Layer details out of `CONTEXT.md`; record those at their owning shell or boundary
artifact unless they are themselves domain language.

Append every settled design decision to the decision ledger immediately. Use the complete entry
contract: question, decision, constraints, rejected alternatives, core/shell/boundary impact,
contract impact, test implication, and ADR qualification. A decision must not survive only in
conversation.

Apply the three-part ADR gate before creating an ADR: create one only when the decision is hard
to reverse, surprising without context, **and** resulted from a real trade-off. An ADR records
context, decision, alternatives, consequences, and links to its ledger entry and specification.
Ordinary settled decisions stay in the ledger. For an architecture exception, also record the
violated rule, rationale, smallest exception boundary, compensating controls, and revisit
condition; promote it through the same ADR gate when it qualifies.

## Finish

Report the changed artifacts, unresolved contradictions or open vocabulary, and the next
recommended skill. Recommend `fp-codebase-design` when the core/shell ownership or capability
boundaries need design; otherwise recommend the workflow that can act on the settled decision.
