# Durable Artifact Contracts

Follow existing repository conventions first. When none exists, use these default paths:

```text
CONTEXT.md
docs/decisions/YYYY-MM-DD-<topic>.md
docs/adr/NNNN-<decision>.md
docs/specs/YYYY-MM-DD-<topic>.md
```

## Glossary

`CONTEXT.md` contains domain vocabulary only: terms, definitions, states, transitions, and distinctions needed to understand the domain. Do not turn it into a specification or implementation guide; keep Effect, database, HTTP, and Layer details out unless they are domain language.

## Decision ledger

Record every settled design decision in `docs/decisions/YYYY-MM-DD-<topic>.md`, even when it does not qualify for an ADR.

```md
## D<N>: <decision title>

- **Question:**
- **Decision:**
- **Constraints:**
- **Rejected alternatives:**
- **Architecture impact:** Core | Shell | Boundary | None
- **Contract impact:** A / E / R / schema / capability / adapter / none
- **Test implication:**
- **ADR:** no | proposed `<title>`
```

## ADR

Create `docs/adr/NNNN-<decision>.md` only for a hard-to-reverse decision that is surprising without context and resulted from a real trade-off. State context, decision, alternatives, consequences, and links to the decision-ledger entry and specification.

## Specification

Write `docs/specs/YYYY-MM-DD-<topic>.md` after discovery without repeating the interview. Use all twelve sections below:

```md
# <topic>

## 1. User-visible behavior and scope

## 2. Domain vocabulary, values, invariants, and state transitions

## 3. Pure decision functions and their input/output algebras

## 4. Effect inventory

## 5. Capability ports and owning packages

## 6. A, E, and R contracts

## 7. Adapter and error-translation table

## 8. Layer dependency graph and composition root

## 9. Resource, retry, idempotency, interruption, and shutdown decisions

## 10. Security and serialization sinks

## 11. Core-first test slices

## 12. Architecture exceptions
```

Architecture exceptions must state the violated rule, rationale, smallest boundary, compensating controls, and revisit condition. Link an ADR when the exception is hard to reverse, surprising, and based on a real trade-off.
