---
name: fp-diagnosing-bugs
description: Diagnose a known observed bug or regression through a tight reproduction loop, layer classification, falsifiable hypotheses, and regression evidence. Use only to investigate a broken, failing, flaky, slow, or wrong behavior/Effect outcome—not to explain or summarize, review hypothetical improvements without a symptom, or build a new feature (including test-first).
---

# FP Diagnosing Bugs

Diagnose one reported symptom through evidence, not intuition. This discipline is self-contained; read
files directly rather than invoking another skill mechanism.

## Load the applicable guidance

First confirm these five references exist; stop and name any missing file:

- `../references/project-detection.md`
- `../references/fcis-architecture.md`
- `../references/effect-4.md`
- `../references/error-model.md`
- `../references/testing.md`

Read repository instructions, manifests, lockfiles, relevant source and tests, existing commands,
`project-detection.md`, `fcis-architecture.md`, and `testing.md`. Always apply the generic FCIS
guidance. Detect Effect from resolved project evidence and record `effect_mode`, exact version, and
release channel. Only when that evidence proves `effect_mode: effect-4`, read `effect-4.md` and
`error-model.md`; otherwise do not add Effect ceremony. Stop on an ambiguous Effect major, exact
version, or RC; never apply Effect 3 or another Effect 4 RC by analogy.

For behavioral/API facts, prefer tests and observed behavior, project source, vendored source for
the installed dependency, version-matched official documentation, shared references, then memory.
For project policy, prefer direct user instructions, repository instructions and accepted ADRs,
established conventions, shared references, then memory. Surface contradictions rather than
silently choosing one.

## Classify before hypotheses

After reproducing but before proposing causes, assign exactly one primary failure class at the
public seam where the reported symptom is observed, then choose its probe. Do not reclassify a wrong
wire status as orchestration merely because an upstream Effect operation may explain it; that
operation is a hypothesis about the cause. A request returning the wrong status is a **Wire
boundary / error-translation** failure until probe evidence establishes the cause.

| Class | Probe |
|---|---|
| Core decision | table/property test with explicit values |
| Effect orchestration | `Effect.exit`, test Layer, TestClock, controlled capability |
| Adapter | real integration harness and projected foreign error |
| Layer graph | minimal Layer build/service acquisition |
| Runtime/concurrency | Scope, fiber, interruption, schedule, resource-lifetime probe |
| Wire boundary | real decode/encode or request/response test |

Use ordinary tests for core decisions. For Effect orchestration, use Effect-aware tests and test
capabilities. Keep retries below foreign-error translation and only around replay-safe work.

Every hypothesis must name this class and predict one observable `A`, `E`, `R`, `Exit`, or
serialized result. Never render a production `Cause`. Redact credentials, tokens, query parameters,
personal data, and arbitrary failure payloads from commands, probes, logs, artifacts, and reports.

## Complete the diagnosis loop

### 1. Build the feedback loop

Create and run a named command for the exact symptom. It must be fast, deterministic,
agent-runnable, and red-capable: its output, exit status, assertion, or measured threshold must
distinguish the reported broken behavior from the expected behavior. Record the command and its
observed red evidence before hypotheses.

**Complete when:** the already-run command reproduces the exact symptom with safe output. If no
red-capable command can be built, list each attempted command and why it failed, then stop and
request environment access or a redacted artifact. Do not hypothesize anyway.

### 2. Reproduce and minimize

Reduce the command, inputs, fixtures, timing, capabilities, Layer graph, or request to the smallest
reliable case. Remove one element at a time and rerun the loop; retain only elements whose removal
changes the result.

**Complete when:** the minimized reproduction remains red and every remaining element is
load-bearing.

### 3. Rank falsifiable hypotheses

Show three to five ranked hypotheses before testing any of them. For each, state the implicated
layer/class, why the minimized evidence supports its rank, one safe targeted probe, and its predicted
observable `A`, `E`, `R`, `Exit`, or serialized result. Include a prediction that could disprove it.

**Complete when:** three to five ranked, falsifiable hypotheses are visible and each has a distinct,
observable prediction.

### 4. Instrument one prediction

Test only the highest-value unresolved prediction at a time. Add a uniquely tagged temporary probe
(for example, `FPDBG-<issue>-<n>`) at the classified seam, rerun the minimized loop, and compare the
safe observed result with the prediction. Remove or revise the hypothesis before moving to the next
probe; do not turn probes into production telemetry.

**Complete when:** probe evidence confirms or falsifies hypotheses without exposing prohibited data,
and the confirmed cause has a direct causal path to the symptom.

### 5. Prove the regression and fix

Write and run a failing regression test at the class's correct public seam: a table/property test for
a core decision, Effect-aware test with controlled capabilities for orchestration, real integration
for an adapter, minimal build for a Layer graph, lifetime/interruption probe for runtime behavior, or
real request/decode/encode test for a wire boundary. Implement the smallest fix, run the regression
green, rerun the original red-capable command, and run the relevant focused and project gates.

**Complete when:** the regression is green, the original loop now demonstrates the expected result,
and all named verification results are recorded.

### 6. Clean up and report

Remove every temporary probe, prototype, fixture alteration, and diagnostic-only dependency. Rerun
the original loop after cleanup. The final report must retain the primary symptom class, the complete
three-to-five ranked hypothesis list with each predicted observable, and the regression-before-fix
and original-command-after-fix gates even when an earlier probe already confirmed the cause. If the
user prohibits edits, mark fix evidence as not run, but still name those required future commands and
gates; do not omit them. Also report the confirmed cause, affected seam, minimized case, failed and
passing commands, regression location, cleanup evidence, and remaining risk.

**Complete when:** no diagnostic instrumentation remains, the post-cleanup loop passes, and the
report ties the confirmed cause to the observed symptom without raw failure data.
