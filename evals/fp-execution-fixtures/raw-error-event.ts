import { Schema } from "effect";

export class JobFailed extends Schema.TaggedClass<JobFailed>()("JobFailed", {
  jobId: Schema.String,
  // MUTATION: arbitrary foreign errors cross a persisted event boundary.
  error: Schema.Unknown,
}) {}

export const toFailureEvent = (jobId: string, rawDriverError: unknown) =>
  new JobFailed({ jobId, error: rawDriverError });
