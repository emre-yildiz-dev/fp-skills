# Effect 4 Shell

Load this reference only after project detection proves Effect 4.

## Effect<A, E, R>

A is the successful domain result. E contains expected failures a caller can act on.
R contains capabilities the program requires. Review all three; a correct A with accidental E or R is an architecture defect.

## Services

Use Context.Service for narrow capabilities. The service shape describes what the application can do.
Acquire dependencies inside the construction Effect. Do not expose repositories or vendor clients through a public facade.

```ts
import { Context, Effect, Layer } from "effect"

class Greeting extends Context.Service<Greeting, {
  readonly greet: (name: string) => Effect.Effect<string>
}>()("app/Greeting", {
  make: Effect.gen(function*() {
    const formatter = yield* Formatter
    return { greet: (name) => Effect.succeed(formatter.format(name)) }
  })
}) {
  static readonly layer = Layer.effect(this, this.make)
}
```

`make` is an Effect, not an implicit global constructor. Its required capabilities remain visible in its R channel.

## Layers

Provide interpreters with explicit Layer values. Effect 4 does not imply an auto-derived Default layer.
Compose dependencies before providing the application layer. Keep Layer assembly at composition roots.

## Composition roots

Only entrypoints assemble the complete graph and launch a runtime. Keep `run*` bridges at genuine
framework or process boundaries. Do not scatter Effect.runPromise through application code.

```ts
const applicationLayer = Greeting.layer.pipe(Layer.provide(Formatter.layer))
const program = Effect.gen(function*() {
  const greeting = yield* Greeting
  return yield* greeting.greet("Ada")
})

// main.ts, the process composition root
Effect.runPromise(program.pipe(Effect.provide(applicationLayer)))
```

## Effect testing

Use this Effect-specific testing guidance only after project detection proves Effect 4. Within a
core-first vertical slice, follow this order:

```text
model -> failing pure test -> pure decision -> Effect orchestration test -> Effect service
-> adapter integration -> adapter -> wire contract -> Layer wiring
```

Keep ordinary pure functions in ordinary tests. Test an Effect workflow through its capability port
with test Layers. Use `it.effect` where the project test runner provides it, and inspect
`Effect.exit` when success, typed failure, defect, or interruption is itself the behavior. Use
`TestClock` for time rather than sleeping; provide controlled services for randomness, identity,
and external facts. Check Layer wiring only at the composition root.

## Resources and concurrency

Use Scope/finalizers for resources and structured fibers for concurrent work. A detached fiber requires
a written answer for durability, shutdown, interruption, reporting, and ownership.

## Version discipline

Read the installed or vendored API for RC builds. Never translate an Effect 3 example by name alone.
