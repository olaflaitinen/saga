# Pull request

## Related issue

Closes #<!-- issue number -->

## Description

<!-- A concise description of what this pull request changes and why. -->

## Type of change

- [ ] Bug fix (non-breaking change that fixes an incorrect behavior)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that causes existing behavior to change)
- [ ] Documentation update
- [ ] Test addition or improvement
- [ ] Infrastructure or CI change

## Checklist

- [ ] An issue exists for this change (see above).
- [ ] `pre-commit run --all-files` passes with zero errors.
- [ ] `pytest tests/unit/ tests/integration/ tests/property/ -q` passes.
- [ ] `mypy --strict src/` passes.
- [ ] Docstrings are complete on all new public functions and classes.
- [ ] Documentation under `docs/` has been updated where applicable.
- [ ] `CHANGELOG.md` has been updated under `[Unreleased]`.
- [ ] No em-dash (U+2014) or en-dash (U+2013) characters appear in modified files.
- [ ] No emoji or pictographic Unicode characters appear in modified files.
- [ ] No numerical result has been introduced that is not sourced from the SAGA manuscript.
- [ ] No placeholder text (`TODO: replace`, `FIXME`, `XXX`, `foo`, `bar`, `baz`) appears.

## Testing notes

<!-- Describe any special testing considerations or manual verification steps. -->
