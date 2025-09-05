# Git Flow Protocol: Project Genesis

## Branching Strategy
- `main`: Production-ready code. Only merges from `develop` or release branches.
- `develop`: Integration branch for new features. Merges from feature branches.
- `feature/<feature-name>`: For new features. Branch off `develop`.
- `bugfix/<bug-name>`: For bug fixes. Branch off `develop` or `main` (for hotfixes).
- `release/<version>`: For preparing new releases. Branch off `develop`.
- `hotfix/<bug-name>`: For critical production bugs. Branch off `main`.

## Commit Standards
- **Format:** `type(scope): subject`
  - `type`: feat, fix, docs, style, refactor, test, chore, perf, build, ci
  - `scope`: Optional; module, component, or area affected
  - `subject`: Concise, imperative mood, no period.
- **Body:** More detailed explanation if necessary.
- **Footer:** Reference issues (e.g., `Closes #123`), breaking changes.

## Pull Request (PR) Workflow
- All changes must go through a PR.
- Requires at least one approval.
- Automated checks (linting, tests, security scans) must pass.
- PR description must include:
  - Link to feature spec/bug report.
  - Summary of changes.
  - North Star alignment (which objectives it advances, principles it upholds).
  - Protocols followed.

## Merging
- Use squash and merge for feature branches into `develop`.
- Use merge commit for `develop` into `main`.
