export declare const Service: {
    /**
     * Creates a `Context` service key.
     *
     * **When to use**
     *
     * Use when you need to define a context service key for a dependency that must
     * be provided by the surrounding context.
     *
     * **Details**
     *
     * Call `Context.Service("Key")` for a function-style key, or use the two-stage
     * form `Context.Service<Self, Shape>()("Key")` for class-style service
     * declarations. The returned key can be yielded as an Effect and passed to
     * `Context.make`, `Context.add`, and the Context getter functions.
     *
     * **Gotchas**
     *
     * The string key is the runtime identity of the service. Reusing the same key
     * string for unrelated services makes them occupy the same slot in a
     * `Context`.
     *
     * **Example** (Creating service keys)
     *
     * ```ts import.meta.vitest
     * import { Context } from "effect"
     *
     * // Create a simple service
     * const Database = Context.Service<{
     *   query: (sql: string) => string
     * }>("Database")
     *
     * // Create a service class
     * class Config extends Context.Service<Config, {
     *   port: number
     * }>()("Config") {}
     *
     * // Use the services to create contexts
     * const db = Context.make(Database, {
     *   query: (sql) => `Result: ${sql}`
     * })
     * const config = Context.make(Config, { port: 8080 })
     * Context.get(db, Database).query("SELECT 1") // => "Result: SELECT 1"
     * Context.get(config, Config).port // => 8080
     * ```
     *
     * @see {@link Reference} for service keys with default values
     *
     * @category services
     * @since 4.0.0
     */
    <Identifier, Shape = Identifier>(key: string, options?: {} | undefined): Service<Identifier, Shape>;
    /**
     * Creates a `Context` service key.
     *
     * **When to use**
     *
     * Use when you need to define a context service key for a dependency that must
     * be provided by the surrounding context.
     *
     * **Details**
     *
     * Call `Context.Service("Key")` for a function-style key, or use the two-stage
     * form `Context.Service<Self, Shape>()("Key")` for class-style service
     * declarations. The returned key can be yielded as an Effect and passed to
     * `Context.make`, `Context.add`, and the Context getter functions.
     *
     * **Gotchas**
     *
     * The string key is the runtime identity of the service. Reusing the same key
     * string for unrelated services makes them occupy the same slot in a
     * `Context`.
     *
     * **Example** (Creating service keys)
     *
     * ```ts import.meta.vitest
     * import { Context } from "effect"
     *
     * // Create a simple service
     * const Database = Context.Service<{
     *   query: (sql: string) => string
     * }>("Database")
     *
     * // Create a service class
     * class Config extends Context.Service<Config, {
     *   port: number
     * }>()("Config") {}
     *
     * // Use the services to create contexts
     * const db = Context.make(Database, {
     *   query: (sql) => `Result: ${sql}`
     * })
     * const config = Context.make(Config, { port: 8080 })
     * Context.get(db, Database).query("SELECT 1") // => "Result: SELECT 1"
     * Context.get(config, Config).port // => 8080
     * ```
     *
     * @see {@link Reference} for service keys with default values
     *
     * @category services
     * @since 4.0.0
     */
    <Self, Shape>(): <const Identifier extends string, E, R = Types.unassigned, Args extends ReadonlyArray<any> = never>(id: Identifier, options?: {
        readonly make?: ((...args: Args) => Effect<Shape, E, R>) | Effect<Shape, E, R> | undefined;
    } | undefined) => ServiceClass<Self, Identifier, Shape> & ([Types.unassigned] extends [R] ? unknown : {
        readonly make: [Args] extends [never] ? Effect<Shape, E, R> : (...args: Args) => Effect<Shape, E, R>;
    });
    /**
     * Creates a `Context` service key.
     *
     * **When to use**
     *
     * Use when you need to define a context service key for a dependency that must
     * be provided by the surrounding context.
     *
     * **Details**
     *
     * Call `Context.Service("Key")` for a function-style key, or use the two-stage
     * form `Context.Service<Self, Shape>()("Key")` for class-style service
     * declarations. The returned key can be yielded as an Effect and passed to
     * `Context.make`, `Context.add`, and the Context getter functions.
     *
     * **Gotchas**
     *
     * The string key is the runtime identity of the service. Reusing the same key
     * string for unrelated services makes them occupy the same slot in a
     * `Context`.
     *
     * **Example** (Creating service keys)
     *
     * ```ts import.meta.vitest
     * import { Context } from "effect"
     *
     * // Create a simple service
     * const Database = Context.Service<{
     *   query: (sql: string) => string
     * }>("Database")
     *
     * // Create a service class
     * class Config extends Context.Service<Config, {
     *   port: number
     * }>()("Config") {}
     *
     * // Use the services to create contexts
     * const db = Context.make(Database, {
     *   query: (sql) => `Result: ${sql}`
     * })
     * const config = Context.make(Config, { port: 8080 })
     * Context.get(db, Database).query("SELECT 1") // => "Result: SELECT 1"
     * Context.get(config, Config).port // => 8080
     * ```
     *
     * @see {@link Reference} for service keys with default values
     *
     * @category services
     * @since 4.0.0
     */
    <Self>(): <const Identifier extends string, Make extends Effect<any, any, any> | ((...args: any) => Effect<any, any, any>)>(id: Identifier, options: {
        readonly make: Make;
    }) => ServiceClass<Self, Identifier, Make extends Effect<infer _A, infer _E, infer _R> | ((...args: infer _Args) => Effect<infer _A, infer _E, infer _R>) ? _A : never> & {
        readonly make: Make;
    };
};
