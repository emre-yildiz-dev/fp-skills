# FCIS / Effect Skills for Pi

Eight composable Agent Skills for Functional Core / Imperative Shell architecture, with Effect 4 guidance activated only when the project evidence proves the exact installed Effect version.

## Skills

### Planning

- `fp-domain-modeling` — clarify domain terms, invariants, and transitions.
- `fp-grill-with-docs` — interview through design decisions and persist the glossary, decision ledger, and selective ADRs.
- `fp-codebase-design` — map functional cores, capability ports, adapters, package boundaries, and roots.
- `fp-to-spec` — synthesize approved evidence into an implementation contract.

### Execution

- `fp-tdd` — deliver one core-first vertical slice at a time.
- `fp-implement` — implement an approved spec through validated tracer slices.
- `fp-diagnosing-bugs` — reproduce, minimize, instrument, and fix bugs by boundary seam.
- `fp-code-review` — review Standards, Spec, and FCIS/Effect concerns independently.

The recommended workflow is `fp-grill-with-docs → fp-codebase-design → fp-to-spec → fp-implement` with `fp-tdd` for each slice, followed by `fp-code-review`. Domain modeling and bug diagnosis can also be used independently.

## Install with Pi

Install the npm package globally so the skills are available across your projects:

```bash
pi install npm:fp-skills@1.0.1
```

Or install it only for the current project:

```bash
pi install --local npm:fp-skills@1.0.1
```

The npm package includes the `pi-package` keyword used for Pi package gallery discovery. You can also install the same release directly from its Git tag:

```bash
pi install git:github.com/emre-yildiz-dev/fp-skills@v1.0.1
```

Project package declarations load only after Pi project trust is granted. Review the package and its skill instructions before trusting a project. Check configured packages with `pi list`; update the npm package with `pi update npm:fp-skills`, or the Git package with `pi update git:github.com/emre-yildiz-dev/fp-skills`; remove the source you installed with the corresponding `pi remove` command.

To update to a newer release, change the pinned npm version or Git tag in the install command. Pinned versions remain fixed until you install a newer version.

You can force a skill in Pi with `/skill:fp-codebase-design` or `/skill:fp-tdd`. The package contains standard `.agents/skills` directories and can also be copied into a compatible project's `.agents/skills/` directory for other Agent Skills implementations.

## Validation

From the repository root, run the deterministic release checks:

```bash
python3 -m unittest discover -s .agents/skills/fp/scripts/tests -p 'test_*.py' -v
python3 .agents/skills/fp/scripts/validate_suite.py --suite-root .agents/skills/fp --through 2
uv lock --check
uv run --frozen ruff check .agents/skills/fp/scripts
```

The repository also includes quality cases, trigger cases, fixtures, and an Effect-backend scenario runbook. Model/provider-dependent evaluations require a configured Pi provider and are not claimed as passing by the deterministic CI workflow; see `evals/fp-suite/effect-backend-scenarios.md` for the bounded template-validation scenarios.

## Distribution

The skills are published as the npm package [`fp-skills`](https://www.npmjs.com/package/fp-skills) and are eligible for Pi package gallery discovery through the `pi-package` keyword. The same source is also available from GitHub as a tagged Pi Git package.

## License and attribution

The upstream workflow source is adapted from [mattpocock/skills](https://github.com/mattpocock/skills) at commit [`c55ee46073ed923f86ce59a5eb3b6d895095d1b7`](https://github.com/mattpocock/skills/tree/c55ee46073ed923f86ce59a5eb3b6d895095d1b7). Its MIT notice is retained in `.agents/skills/fp/UPSTREAM-LICENSE.md`. The FCIS/Effect guidance and Pi integration are maintained in this repository and may diverge from upstream.
