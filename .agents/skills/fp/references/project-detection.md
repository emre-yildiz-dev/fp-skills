# Project Detection

## Required inspection

1. Read repository-level AGENTS.md or CLAUDE.md and every directly referenced rule relevant to the task.
2. Read the package manifest and lockfile entry for `effect`.
3. Inspect existing core, service, adapter, Layer, and test examples before proposing a pattern.
4. Record existing artifact and command conventions.

## Effect detection

Set `effect_mode: effect-4` only when the installed dependency resolves to 4.x.
Record the exact version string and whether it is stable, beta, or RC.
The exact installed version must be recorded from the resolved dependency.
Set `effect_mode: none` only when Effect is absent. If Effect is installed but does not resolve to 4.x,
stop; do not classify it as `none`. Stop when the exact installed version or release channel cannot be resolved.
Never infer Effect from TypeScript alone. Never apply Effect 3 or another Effect 4 RC by analogy.
If only facts for a different Effect 4 RC or version are available, stop.

## Evidence order

Behavior/API facts: tests and observed behavior, project source, vendored installed source,
version-matched official documentation, shared references, model memory.

Project policy: direct user instructions, repository instructions and accepted ADRs,
established conventions, shared references, model memory.

## Contradictions

A policy document cannot redefine dependency behavior. Surface the contradiction and cite both sources.

## Stop conditions

Stop before design or code when Effect is installed but is not 4.x, the exact installed version or
release channel cannot be resolved, only facts for a different Effect 4 RC or version are available,
the Effect major/RC cannot be established, local instructions point to missing authority, or the
requested pattern conflicts with observed project behavior.

## Project profile

```yaml
effect_mode: none | effect-4
effect_version: string | null
evidence:
  instructions: []
  manifests: []
  examples: []
  vendored_sources: []
artifact_conventions: {}
verification_commands: []
open_contradictions: []
```
