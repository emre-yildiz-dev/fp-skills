# Effect backend scenario record

This is a reproducible, disposable validation record for the FP suite. It uses
`$EFFECT_TEMPLATE` (default: `~/code/test/effect-backend`) and **never** edits
that checkout. The synthetic changes below are validation fixtures, not product
decisions or deliverables. Reset the validation worktree after every scenario.

## Setup and shared evidence

```bash
EFFECT_TEMPLATE="${EFFECT_TEMPLATE:-$HOME/code/test/effect-backend}"
SUITE_ROOT="${SUITE_ROOT:-$HOME/code/projects/fplearn/fpuniversity/.worktrees/fcis-effect-skills}"
VALIDATION_WT="$(mktemp -d)/effect-backend-fp-skill-validation"
git -C "$EFFECT_TEMPLATE" worktree add --detach "$VALIDATION_WT" HEAD
(cd "$VALIDATION_WT" && bun install --frozen-lockfile)
```

Run read-only planning/review before modifications. In each skill run, read
`.claude/CLAUDE.md`, its referenced `.claude/rules/`, manifests, lockfiles,
source, tests, and `repos/effect` before proposing a change. Load the generic
FCIS guidance for every run, then the Effect guidance only after detection.
The observed preflight on 2026-09-23 passed: `apps/server/package.json` and
`packages/auth/package.json` record `effect@4.0.0-rc.111`; `.claude/CLAUDE.md`
requires local rules and says vendored `repos/effect` is the authority for
pinned pre-release APIs. This establishes `effect_mode: effect-4`, exact
version `4.0.0-rc.111`, and no version ambiguity.

Use Pi only as explicit file composition; do not use a Call-the-Skill tool.
For an agent run, load the selected directory explicitly (and preserve template
context files), capture its transcript, and constrain it to the listed files:

```bash
(cd "$VALIDATION_WT" && pi --no-extensions --no-skills \
  --skill "$SUITE_ROOT/.agents/skills/fp/<skill>" -p '<scenario prompt>')
```

For a manual run, follow the named skill's staged reads and gates exactly. The
commands below are the only verification commands for their scenario. Before
the next scenario (including after a failed expected-red command), run:

```bash
git -C "$VALIDATION_WT" reset --hard HEAD
git -C "$VALIDATION_WT" clean -fd
```

## 1. Pure password policy

- **Skill:** `fp-tdd`.
- **Prompt:** Add the disposable `contains_nul` password-policy branch: reject
  U+0000 with ordinary unit tests. Keep it pure; do not import Effect.
- **Anchors / allowed files:** `packages/auth/src/policy/password.ts` and
  `packages/auth/test/password.test.ts` only.
- **Expected artifact:** a `PasswordViolation` arm and a behavioral ordinary
  test; no service, Layer, I/O, or Effect import in the policy.
- **Verification:** `bunx vitest run --project=unit packages/auth/test/password.test.ts`.
- **Cleanup:** shared hard reset and clean.
- **Observed evidence:** PASS. The added expectation first failed with
  `expected [] to deeply equal [ 'contains_nul' ]` (1 failed, 9 passed), then
  passed after the minimal branch (10 passed). The diff was limited to the two
  allowed files and `git diff --check` passed.

## 2. Effect shell around an existing pure decision

- **Skill:** `fp-tdd` followed by `fp-implement` for the shell slice.
- **Prompt:** Add disposable `OAuthLinkingService` around `decideLinking`. It
  must depend on a narrow `LinkingFacts` `Context.Service`, acquire facts in
  the shell, call the existing pure policy, and use an explicit test Layer.
  Do not change the policy.
- **Required read anchors:** `packages/auth/src/policy/linking.ts`, plus
  `apps/server/src/service/TodoService.ts`,
  `apps/server/src/repo/TodosRepository.ts`,
  `apps/server/src/handler/TodosHandler.ts`, and
  `apps/server/src/infra/server.ts`.
- **Allowed mutation files:** new
  `packages/auth/src/service/OAuthLinkingService.ts` and
  `packages/auth/test/OAuthLinkingService.test.ts` only; do not modify
  `linking.ts`.
- **Expected artifact:** substituted `LinkingFacts`, explicit test Layer, and
  an Effect-aware service test; the policy remains ordinary and unchanged.
- **Verification:** `bunx vitest run --project=unit packages/auth/test/OAuthLinkingService.test.ts`.
- **Cleanup:** shared hard reset and clean.
- **Observed evidence:** PASS. The new test first failed because the service
  package did not exist; after adding the narrow capability and
  `Layer.effect` service, the one Effect-aware test passed. `git diff --check`
  passed and the policy file was untouched.

## 3. Typed database-backed preview endpoint

- **Skill:** `fp-implement` (core-first checks and real wire test).
- **Prompt:** Add disposable `GET /v1/todos/:id/preview`, backed by the
  existing repository/service. Return the Todo on success and the existing
  typed `TodoNotFound` 404 on absence; put Layer composition only at the
  existing root.
- **Required read anchors:** `apps/server/src/service/TodoService.ts`,
  `apps/server/src/repo/TodosRepository.ts`,
  `apps/server/src/handler/TodosHandler.ts`, and
  `apps/server/src/infra/server.ts`.
- **Allowed mutation files:** the domain API contract
  `packages/domain/src/api/TodosApi.ts`,
  `apps/server/src/handler/TodosHandler.ts`, and the fixture test
  `apps/server/test/handler/errorRecovery.integration.test.ts`; leave the
  repository, service, and root wiring unchanged.
- **Expected artifact:** domain endpoint contract with `TodoNotFound`, thin
  handler delegation to `TodoService.getById`, and a real success/404 wire
  test. Do not alter repository error narrowing or create Layer wiring outside
  `apps/server/src/infra/server.ts`.
- **Verification:** `bunx vitest run --project=integration apps/server/test/handler/errorRecovery.integration.test.ts`.
- **Cleanup:** shared hard reset and clean.
- **Observed evidence:** PASS. The new real wire test was red before handler
  registration (`RouteNotFound`, expected 404 to be 200), then green with 3
  passing tests after the domain contract and one thin handler were added.
  The integration environment was available.

## 4. Diagnose a wrong error translation

- **Skill:** `fp-diagnosing-bugs`.
- **Prompt:** Make a disposable handler mutation that converts the declared
  `TodoNotFound` path into a defect, then diagnose why the wire response is
  500 instead of the declared status. Demonstrate the red-capable command
  before hypotheses; do not retain the mutation.
- **Required read anchors:** `apps/server/src/service/TodoService.ts`,
  `apps/server/src/repo/TodosRepository.ts`,
  `apps/server/src/handler/TodosHandler.ts`, and
  `apps/server/src/infra/server.ts`.
- **Allowed mutation files:** `apps/server/src/handler/TodosHandler.ts` and
  `apps/server/test/handler/errorRecovery.integration.test.ts`, based on the
  handler's typed error path.
- **Expected finding:** the handler must preserve the typed `TodoNotFound` E
  channel rather than `Effect.die` it; the real wire test is the probe.
- **Verification:** `bunx vitest run --project=integration apps/server/test/handler/errorRecovery.integration.test.ts`.
- **Cleanup:** shared hard reset and clean.
- **Observed evidence:** PASS. The required pre-hypothesis command was run
  first and went red: `getTodoById returns 404` reported `expected 500 to be
  404`. The mutation was reset, not fixed in the template.

## 5. Review retry above the narrowing seam

- **Skill:** `fp-code-review` (read-only).
- **Prompt:** Review a disposable mutation that adds `Effect.retry` in
  `TodosHandler` above the `TodosRepository` narrowing seam. Keep Standards,
  Spec, and FCIS/Effect findings separate.
- **Required read anchors:** `apps/server/src/service/TodoService.ts`,
  `apps/server/src/repo/TodosRepository.ts`,
  `apps/server/src/handler/TodosHandler.ts`, and
  `apps/server/src/infra/server.ts`.
- **Allowed mutation files:** `apps/server/src/handler/TodosHandler.ts` only.
- **Expected finding:** FCIS/Effect reports retry above foreign-error
  translation (and potentially replaying caller-actionable work); the smallest
  correction is to remove it and retain replay-safe retry at the repository.
- **Verification:** `bun run check` followed by the review's three independent
  finding lists.
- **Cleanup:** shared hard reset and clean.
- **Observed evidence:** PASS. `bun run check` exited 0, demonstrating that
  type checking is insufficient. The FCIS/Effect review gate identified the
  handler retry above `TodosRepository`'s `retryTransient`/`narrow` seam; it
  does not become a Standards or Spec finding by inference.

## 6. Review a raw failure crossing a serialized sink

- **Skill:** `fp-code-review` (read-only).
- **Prompt:** Replace the projected `runFailureFrom(err)` value with raw `err`
  in `FlowRunFailed`, then review the event/persisted-payload path. Do not
  retain the mutation.
- **Required read anchors:** `apps/server/src/service/TodoService.ts`,
  `apps/server/src/repo/TodosRepository.ts`,
  `apps/server/src/handler/TodosHandler.ts`, and
  `apps/server/src/infra/server.ts`.
- **Allowed mutation files:** template event/error projection patterns in
  `apps/server/src/events/GraphEventBridgeLive.ts` only.
- **Expected finding:** FCIS/Effect identifies an unprojected foreign failure
  crossing the event and pg-boss serialized payload; restore the single
  projection before either sink.
- **Verification:** `bunx vitest run --project=unit apps/server/test/events/flowRunFailedRedaction.test.ts`.
- **Cleanup:** shared hard reset and clean.
- **Observed evidence:** PASS. The deliberate raw-value mutation made the
  redaction suite fail (8 failed, 3 passed); its failures name the
  `FlowRunFailed` serialized path. Reset restored the template.

## 7. Non-Effect FCIS-only planning

- **Skill:** `fp-to-spec` planning case.
- **Prompt:** Plan a small pure-package change from the Plan 1
  `plain-package.json` fixture outside the Effect template. Apply FCIS
  guidance, but do not introduce Effect services, Layers, `Effect<A,E,R>`, or
  Effect-specific test ceremony.
- **Anchors / allowed files:**
  `$SUITE_ROOT/evals/fp-planning-fixtures/plain-package.json` and its sibling
  planning fixtures only; no file in `$VALIDATION_WT`.
- **Expected artifact:** ordinary pure decision/test seams and explicit
  non-Effect detection.
- **Verification:** manually run `fp-to-spec` after reading its declared
  references and the fixture sources; then run
  `python3 -c 'import json; d=json.load(open("evals/fp-planning-fixtures/plain-package.json")); assert "effect" not in d.get("dependencies", {})'`
  from `$SUITE_ROOT`.
- **Cleanup:** no template modification; remove any external planning scratch
  artifact.
- **Observed evidence:** PASS (expected stop). Manual `fp-to-spec` planning
  run on 2026-09-23 read `plain-package.json`, `project-rules.md`,
  `existing-decisions.md`, and `auth-policy.ts`, along with its generic
  detection, FCIS, and artifact-contract references. It recorded
  `effect_mode: none` because the manifest has no Effect dependency; it applied
  the pure-policy rule and proposed ordinary pure decision tests only. It did
  not propose an Effect service, Layer, `Effect<A,E,R>` contract, or
  Effect-specific test lane. It then stopped before specification finalization:
  `existing-decisions.md` says matching-email accounts are never auto-linked,
  while the same fixture records that the current handler auto-links them. The
  required contradiction report is the planning result, not a completed spec.

## 8. One-rule-at-a-time mutation matrix

- **Skills:** `fp-tdd` / `fp-implement` design gates where a change is made;
  `fp-code-review` for the final independent FCIS/Effect finding.
- **Prompt:** Apply exactly one disposable mutation, run its command, identify
  the gate that catches it, reset, then continue. Do not combine mutations.
- **Anchors / allowed files:** the relevant policy, adapter, handler,
  `apps/server/src/infra/server.ts`, or `GraphEventBridgeLive.ts` only.
- **Verification and observed evidence:**

  | Mutation | Verification | Gate that caught it | Observed evidence |
  | --- | --- | --- | --- |
  | Pure policy imports Effect | `bun run check` | `fp-code-review` FCIS/Effect; compiler may also reject the unused import | `check` exited 2; review independently rejects the hidden effect. |
  | Adapter leaks a foreign error | `bun run check` | `fp-code-review` FCIS/Effect | `check` exited 2 for the incompatible seam; review requires narrowing at the adapter even when a variant typechecks. |
  | Retry moves above translation | `bun run check` | `fp-code-review` FCIS/Effect | `check` exited 0; review caught the architectural violation. |
  | Layer wiring moves out of the entrypoint | `bun run check` | `fp-code-review` FCIS/Effect | `check` exited 2 for the incomplete synthetic Layer; review rejects the location independently. |
  | Raw failure crosses a serialized sink | `bunx vitest run --project=unit apps/server/test/events/flowRunFailedRedaction.test.ts` | redaction test and `fp-code-review` FCIS/Effect | exit 1; the payload-redaction suite failed. |

- **Cleanup:** shared hard reset and clean after every row.

## Teardown

```bash
git -C "$EFFECT_TEMPLATE" worktree remove --force "$VALIDATION_WT"
```

Observed teardown requirement: verify `git -C "$VALIDATION_WT" status --short`
is empty before removal. A skipped runtime-dependent scenario is not pass
 evidence: record it as `skipped` with the unavailable provider or infrastructure
reason, distinct from `fail` and `infrastructure_error`.
