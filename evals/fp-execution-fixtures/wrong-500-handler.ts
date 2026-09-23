import { Effect, Schema } from "effect";

class NotFound extends Schema.TaggedError<NotFound>()("NotFound", {
  id: Schema.String,
}, { httpApiStatus: 404 }) {}

type Row = { id: string };

export const getById = (findRows: Effect.Effect<ReadonlyArray<Row>, Error>, id: string) =>
  findRows.pipe(
    Effect.flatMap((rows) => rows[0] ? Effect.succeed(rows[0]) : Effect.fail(new NotFound({ id }))),
    // MUTATION: converts the freshly-created caller-visible 404 into a defect/500.
    Effect.orDie,
  );
