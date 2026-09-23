import { Effect } from "effect";

declare class DbFailure { readonly _tag: "DbFailure" }
declare class SaveConflict { readonly _tag: "SaveConflict" }
declare const rawSave: Effect.Effect<void, DbFailure>;
declare const narrowDb: <A>(effect: Effect.Effect<A, DbFailure>) => Effect.Effect<A, SaveConflict>;

export const repositorySave = narrowDb(rawSave);

// MUTATION: retry is above translation and retries caller-actionable SaveConflict.
export const saveHandler = repositorySave.pipe(Effect.retry({ times: 2 }));
