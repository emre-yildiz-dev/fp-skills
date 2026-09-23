# FCIS / Effect Skill Suite

This standalone Pi skill suite replaces equivalent BMAD and Superpowers workflows without
modifying those installed skills. Every skill name uses the `fp-` prefix to avoid collisions.

## Catalog

### Release 1: planning

- `fp-domain-modeling` — sharpen domain vocabulary, invariants, state transitions, and durable decisions.
- `fp-grill-with-docs` — interview for a design while maintaining glossary, decision ledger, and ADRs.
- `fp-codebase-design` — design functional cores, capability ports, adapters, package boundaries, and roots.
- `fp-to-spec` — synthesize project evidence into an approved implementation specification.

### Release 2: execution

- `fp-tdd` — implement one core-first, red/green vertical slice at a time.
- `fp-implement` — implement an approved specification through validated tracer slices.
- `fp-diagnosing-bugs` — reproduce, minimize, instrument, fix, and clean up by seam.
- `fp-code-review` — independently review Standards, Spec, and FCIS/Effect concerns.

## Workflow

```text
fp-grill-with-docs
  -> glossary + decision ledger + selective ADRs
  -> fp-codebase-design
  -> core/shell/boundary map
  -> fp-to-spec
  -> approved specification
  -> fp-implement + fp-tdd
  -> core-first vertical slices
  -> fp-code-review
  -> Standards | Spec | FCIS/Effect findings
```

`fp-domain-modeling` and `fp-diagnosing-bugs` are also available independently when their
respective workflows apply.

## FCIS and Effect behavior

All skills load the generic Functional Core / Imperative Shell guidance: pure policy belongs in
the core; fact acquisition, orchestration, adapters, error translation, and runtime wiring belong
in the shell. Skills inspect the repository first and load Effect-specific guidance only after
detecting an exact installed Effect 4 version. They stop on Effect version ambiguity rather than
applying Effect 3 or another release candidate by analogy.

## Invocation examples

```text
/skill:fp-grill-with-docs
/skill:fp-to-spec
/skill:fp-implement
```

## Full-suite validation

Run the deterministic structural gates for both releases:

```bash
python3 -m unittest discover -s .agents/skills/fp/scripts/tests -p 'test_*.py' -v
python3 .agents/skills/fp/scripts/validate_suite.py --suite-root .agents/skills/fp --through 2
uv lock --check
uv run --frozen ruff check .agents/skills/fp/scripts
```

The generic single-skill eval runner is not used unchanged because it stages only the target
skill directory and would omit this suite's sibling `references/` kernel. Use the suite-aware Pi
evaluation procedure and the disposable Effect template runbook at
`evals/fp-suite/effect-backend-scenarios.md` for behavioral validation.

Runtime-dependent evals require a configured Pi provider. Record unavailable provider or runtime
infrastructure as `skipped` or `infrastructure_error` as applicable; skipped runs are not evidence
of a passing evaluation.
