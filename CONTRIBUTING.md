# Contributing to SAGA

Thank you for your interest in contributing to the SAGA repository. This document describes
the contribution workflow, coding standards, and review process.

## Table of contents

- [Before you start](#before-you-start)
- [Development environment](#development-environment)
- [Contribution workflow](#contribution-workflow)
- [Coding standards](#coding-standards)
- [Testing requirements](#testing-requirements)
- [Documentation requirements](#documentation-requirements)
- [Pull request checklist](#pull-request-checklist)
- [Reporting bugs and reproducibility questions](#reporting-bugs-and-reproducibility-questions)

## Before you start

Open a GitHub Issue before beginning any non-trivial contribution. This avoids duplicated effort
and ensures the proposed change aligns with the repository's scope. Label your issue with one of:
`bug`, `enhancement`, `reproducibility`, `documentation`, or `question`.

For reproducibility questions related to the protected Statistics Sweden LISA microdata, see
`docs/data/mona-secure-environment.md` for the MONA access procedure. External contributors
cannot replicate bit-level results without independent MONA project approval from Statistics Sweden
under a new project separate from SCB-MONA-2026-147.

## Development environment

```bash
git clone https://github.com/olaflaitinen/saga.git
cd saga

conda env create -f environment.yaml
conda activate saga

pip install -e ".[dev]"

pre-commit install
```

Verify the setup by running the unit test suite:

```bash
pytest tests/unit/ -q --tb=short
```

The unit tests complete in under 5 minutes on a single CPU core using the tiny synthetic panel
fixture (`tests/fixtures/tiny_synthetic_panel.py`).

## Contribution workflow

1. Open an issue describing the change (see above).
2. Fork the repository and create a branch off `main`. Branch names follow the pattern
   `type/short-description`, where `type` is one of `fix`, `feat`, `docs`, `test`, `chore`.
3. Make your changes. Run `pre-commit run --all-files` before committing to enforce ruff, black,
   mypy, and the em-dash/en-dash prohibition hook.
4. Add or update tests to cover your change. All public functions must have at least one unit test.
5. Update the relevant documentation under `docs/` if your change affects a documented behavior,
   numerical claim, or public API.
6. Open a pull request against `main`. Fill out the pull request template completely.
7. Request review from `@olaflaitinen`. The CI pipeline must pass (ruff, black, mypy, pytest,
   reproducibility smoke test) before the pull request is eligible for merge.
8. Address review comments. The maintainer merges using squash-and-merge to maintain a linear
   history.

## Coding standards

- Python 3.11 or 3.12 only. No syntax or standard-library features from 3.13 or later.
- Full type annotations under PEP 604 union syntax (`X | Y` rather than `Optional[X]`).
- `black` formatter with line length 100.
- `ruff` with rules E, F, I, N, UP, B, C4, SIM, PT, RET, RUF. Zero warnings.
- `mypy` in strict mode. Zero errors.
- No em-dash (U+2014) or en-dash (U+2013) in any file. The pre-commit hook enforces this.
- No emoji or pictographic Unicode in any file.
- Google-style docstrings on all public functions and classes, with Args, Returns, Raises, and
  Examples sections where applicable.
- Module docstrings on every Python module.

## Testing requirements

- Every new public function must have at least one pytest unit test in `tests/unit/`.
- Parameterize tests where the same logic is tested at multiple input values.
- Use named fixtures from `tests/conftest.py` or `tests/fixtures/` rather than module-level
  globals.
- Integration tests for cross-module workflows belong in `tests/integration/`.
- Statistical property tests belong in `tests/property/` using the `hypothesis` package.
- The tiny synthetic panel fixture (`tests/fixtures/tiny_synthetic_panel.py`) must be used
  as the data source for all CI-runnable tests; do not depend on real LISA data in tests.

## Documentation requirements

- Markdown documents under `docs/` must use ATX-style headings.
- Every new feature that changes a public API must be documented in the relevant file under
  `docs/methodology/` or `docs/deployment/`.
- If your change corrects a numerical result, update the corresponding file under
  `docs/results/` and `docs/paper-mirror/` so that the repository remains a faithful mirror
  of the manuscript.
- No placeholder text (`TODO: replace`, `FIXME`, `XXX`, `Lorem ipsum`, `foo`, `bar`, `baz`).

## Pull request checklist

Before submitting your pull request, confirm that each item below is complete:

- [ ] An issue exists for this change.
- [ ] `pre-commit run --all-files` passes with zero errors.
- [ ] `pytest tests/unit/ tests/integration/ tests/property/ -q` passes.
- [ ] Type annotations are complete and `mypy --strict src/` passes.
- [ ] Docstrings are present on all new public functions and classes.
- [ ] Documentation under `docs/` has been updated where applicable.
- [ ] `CHANGELOG.md` has been updated under an `[Unreleased]` section.
- [ ] No em-dash or en-dash characters appear in any modified file.
- [ ] No emoji or pictographic Unicode characters appear in any modified file.

## Reporting bugs and reproducibility questions

Use the GitHub Issue templates:

- **Bug report**: for incorrect behavior in the code.
- **Reproducibility question**: for questions about replicating paper results, including
  questions about the synthetic mirror, the conformal calibration, or the training schedule.
- **Feature request**: for proposed enhancements to the model, evaluation, or documentation.

For private security disclosures, see `SECURITY.md`.
