# Existing Decisions

1. Existing accounts are never auto-linked by matching email. Rejected: trust a provider's verified-email claim. Rationale: prevents account takeover.
2. OAuth linking policy remains a pure decision over already-acquired facts. Rejected: query inside the decision function.
3. Provider HTTP and persistence are separate capabilities owned by the shell. Rejected: expose vendor clients through the public auth facade.

Out of scope: redesigning the browser account-settings UI.

Unresolved contradiction: the current handler still auto-links a matching email, while decision 1 forbids it.
