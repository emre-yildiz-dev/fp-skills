# Project Rules

- Effect version: 4.0.0-rc.111.
- Pure policy modules contain no Effect, services, I/O, clock, or randomness.
- Foreign failures are projected once at the adapter boundary.
- Retry is below projection and wraps replay-safe work only.
- Layers are assembled only at process entrypoints.
- Raw failures and Cause values never cross serialized sinks.

## Eval verification commands

Run these from this fixture directory:

- `bun run test:approval-policy` is the ordinary public pure-policy test seam.
- `bun run test:wrong-500` makes a request to `http://127.0.0.1:<ephemeral-port>/items/missing`
  and expects the declared 404 contract. It is intentionally red while the `Effect.orDie` mutation
  is present.
- `bun run verify:wrong-500-mutation` expects the current 500 mutation so fixture validation can
  remain green without serializing a raw Cause or failure payload.
