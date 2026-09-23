# Error Model

Load this reference only after project detection proves Effect 4. Apply its boundary rules to the FCIS boundary map.

| Failure | Representation | Recovery owner |
|---|---|---|
| Domain outcome | tagged value or typed `E` | application caller |
| Foreign recoverable failure | projected typed error | adapter/application seam |
| Deployment/programming fault | redacted defect | runtime/operator |
| Interrupt | interrupt reason | scope/runtime |

## Expected failures

Put expected domain failures in E as small tagged values with caller-actionable data. Model ordinary outcomes explicitly; callers decide recovery rather than inspect vendor details.

## Foreign failures

Each adapter boundary owns one foreign-error projection/narrowing seam. Translate a recoverable database, HTTP, filesystem, or SDK failure there into a typed error the application understands. Do not retain the foreign value under `cause` or another field after translation.

## Defects

Use defects only for deployment or programming faults, with a written rationale for why callers cannot recover. Record a redacted diagnostic for the runtime/operator; do not turn a caller-actionable expected failure into a defect.

## Interruptions

Preserve interruption as interruption. It is a scope/runtime concern, not an expected failure, and is excluded from failure metrics.

## Retry and idempotency

Place retry below translation at the adapter boundary and only around replay-safe work. Establish idempotency before retrying writes, dispatches, or external calls; do not retry a projected application error above its narrowing seam.

## Serialized sinks

Logs, spans, HTTP bodies, events, queues, and persisted JSON accept explicit safe schemas only. Never put raw errors or `Cause` values in serialized sinks. Do not use `Schema.Unknown` for arbitrary failure payloads without an explicit projection. Test redaction using the secret value itself, not merely a field name.
