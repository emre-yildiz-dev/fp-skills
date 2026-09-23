# Functional Core / Imperative Shell

## Functional core

The core owns decisions, not effects: domain values, invariants, policies, calculations,
state transitions, exhaustive decision tables, tagged result unions, and domain events as values.
External facts arrive as values. No service acquisition, I/O, logging, tracing, queue access,
or runtime launch belongs here.

Ask: "If every external fact were already available, what pure decision remains?"

## Imperative shell

The shell acquires facts, invokes pure decisions, executes capabilities, manages resources,
translates errors, and exposes transports. Effect is one implementation of this shell, not a
reason to make pure policy effectful.

## Capability boundaries

Name capabilities by what the application can do, not by vendor or transport. A capability earns
an interface when implementations vary, external effects must be controlled, or ownership must be
kept behind a public seam. Do not create a service merely to hold functions.

## Boundary map

For every feature identify: ingress decoder, pure decision, required facts, capability ports,
adapters, error translation, serialized egress, composition root, and test seams.

## Architecture exception

Record the violated rule, why the normal shape fails, the smallest exception boundary,
compensating controls, and a revisit condition. Promote it to an ADR only when it is hard to
reverse, surprising, and the result of a real trade-off.

## Vocabulary

| Upstream term | FCIS term |
|---|---|
| Module | Cohesive package or domain capability |
| Interface | Domain algebra or capability port |
| Implementation | Pure function or interpreter |
| Seam | Public behavior or capability boundary |
| Adapter | Interpreter connected at the shell |
| Depth | Behavior and policy hidden behind a small algebra |
| Locality | Decisions and effects owned in one discoverable place |
