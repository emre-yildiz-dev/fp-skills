# Project Rules

- Vendored source matching the lockfile is the authority for dependency APIs.
- Pure policies contain no Effect, I/O, service acquisition, clock, or randomness.
- Effect services orchestrate capabilities; all Layer wiring lives at entrypoints.
- Expected caller-actionable outcomes remain typed failures.
