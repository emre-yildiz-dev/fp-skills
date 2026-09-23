# Settled Decisions

1. Existing accounts are never auto-linked by matching email. Rejected: trust a provider's verified-email claim. Rationale: prevents account takeover.
2. OAuth linking policy remains a pure decision over already-acquired facts. Rejected: query inside the decision function.
3. Provider HTTP and persistence are separate capabilities owned by the shell. Rejected: expose vendor clients through the public auth facade.

Out of scope: redesigning the browser account-settings UI.

## Former handler contradiction and settlement

The current handler behavior auto-links a matching email, while decision 1 forbids it. This contradiction is explicit and settled: decision 1 is authoritative, and the current auto-link behavior is a defect to replace rather than a competing requirement. The implementation must route already-acquired facts through the pure linking decision; a matching existing email without an existing provider link produces `RejectNotLinked` and must not link the account. Pure-policy and wire-contract tests must preserve that outcome.

## Confirmed public test seams

During the completed interview, the following public test seams were reviewed and confirmed: ordinary pure-policy tests for the linking decision; Effect-orchestration tests with substituted capabilities or test Layers; real adapter-integration tests that exercise foreign-error projection; and real wire-contract tests for status translation and serialization. No further test-seam confirmation is outstanding.

## Settled synthetic wire contract

For this synthesis case, the callback wire mappings are settled: invalid callback is HTTP 400 with `{ "code": "INVALID_CALLBACK" }`; provider unavailable is HTTP 502 with `{ "code": "PROVIDER_UNAVAILABLE" }`; an unlinked identity whose email has an existing owner is HTTP 409 with `{ "code": "ACCOUNT_NOT_LINKED" }`; and account-store unavailable is HTTP 503 with `{ "code": "ACCOUNT_STORE_UNAVAILABLE" }`. Error bodies contain only the listed safe code—no message, email, account or provider identifier, foreign error, credentials, or `Cause`. Successful `SignIn` and `CreateUser` outcomes hand the resolved user ID to the existing session mechanism and preserve its existing success response, redirect, and cookie behavior; this case introduces no new success status or body schema.
