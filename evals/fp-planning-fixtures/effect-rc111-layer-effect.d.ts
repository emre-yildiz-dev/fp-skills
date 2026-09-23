export declare const effect: {
    /**
     * Constructs a layer from an effect that produces a single service.
     *
     * **When to use**
     *
     * Use when you need to construct a `Layer`-provided service with an `Effect`,
     * dependencies, or scoped resource acquisition.
     *
     * **Details**
     *
     * This allows you to create a `Layer` from an `Effect` that produces a service.
     * The `Effect` is executed in the scope of the layer, allowing for proper
     * resource management.
     *
     * **Example** (Creating a layer from an effect)
     *
     * ```ts import.meta.vitest
     * import { Context, Effect, Layer } from "effect"
     *
     * class Database extends Context.Service<Database, {
     *   readonly query: (sql: string) => Effect.Effect<string>
     * }>()("Database") {}
     *
     * const layer = Layer.effect(Database,
     *   Effect.sync(() => ({
     *     query: (sql: string) => Effect.succeed(`Query: ${sql}`)
     *   }))
     * )
     * const program = Database.use((database) => database.query("SELECT 1"))
     * Effect.runSync(Effect.provide(program, layer)) // => "Query: SELECT 1"
     * ```
     *
     * @see {@link effectContext} for effectfully providing multiple services
     * @see {@link effectDiscard} for running construction work without providing services
     *
     * @category constructors
     * @since 2.0.0
     */
    <I, S>(service: Context.Key<I, S>): <E, R>(effect: Effect<S, E, R>) => Layer<I, E, Exclude<R, Scope.Scope>>;
    /**
     * Constructs a layer from an effect that produces a single service.
     *
     * **When to use**
     *
     * Use when you need to construct a `Layer`-provided service with an `Effect`,
     * dependencies, or scoped resource acquisition.
     *
     * **Details**
     *
     * This allows you to create a `Layer` from an `Effect` that produces a service.
     * The `Effect` is executed in the scope of the layer, allowing for proper
     * resource management.
     *
     * **Example** (Creating a layer from an effect)
     *
     * ```ts import.meta.vitest
     * import { Context, Effect, Layer } from "effect"
     *
     * class Database extends Context.Service<Database, {
     *   readonly query: (sql: string) => Effect.Effect<string>
     * }>()("Database") {}
     *
     * const layer = Layer.effect(Database,
     *   Effect.sync(() => ({
     *     query: (sql: string) => Effect.succeed(`Query: ${sql}`)
     *   }))
     * )
     * const program = Database.use((database) => database.query("SELECT 1"))
     * Effect.runSync(Effect.provide(program, layer)) // => "Query: SELECT 1"
     * ```
     *
     * @see {@link effectContext} for effectfully providing multiple services
     * @see {@link effectDiscard} for running construction work without providing services
     *
     * @category constructors
     * @since 2.0.0
     */
    <I, S, E, R>(service: Context.Key<I, S>, effect: Effect<Types.NoInfer<S>, E, R>): Layer<I, E, Exclude<R, Scope.Scope>>;
};
