# Governance

## Project maintainers

For v1.0.0, the sole maintainer is:

- **Gustav Olaf Yunus Laitinen-Fredriksson Lundstrom-Imanov** (@olaflaitinen)

All pull requests, issue triage, and release decisions are the responsibility of the
maintainer.

## Decision-making process

The project uses a "benevolent dictator" model for v1.0.0. All substantive technical
decisions are made by the maintainer. Community input is welcomed via GitHub Issues and
Discussions.

For major changes (new features, breaking changes, model retraining), the maintainer
will open a GitHub Discussion for community comment before merging.

## Release process

New releases are triggered by pushing a version tag (e.g., `v1.1.0`) to the main branch.
The `release.yaml` GitHub Actions workflow builds the Python wheel, Docker image, and
GitHub Release automatically. See [CHANGELOG.md](CHANGELOG.md) for the release history.

## Contributor license

By contributing to this repository, you agree that your contributions will be licensed
under the same Apache License 2.0 that covers the rest of the codebase. See
[LICENSE](LICENSE).
