> **Section 5 · Git & CI/CD with gh** — From a terminal to a green CI run on your first pull request.

Git, the GitHub CLI, workflows, the checks that matter, hardening, releases and deploys.

*13 lessons in this section.*

## Git & CI/CD with gh (Part 1: git, gh, and your first pipeline)

### [Git Essentials For The AI Era](05-Git-Essentials)
`beginner` · ~20 min — it is the undo button, the review surface, and the audit trail.

### [GitHub CLI Quickstart](05-GitHub-CLI-Quickstart)
`beginner` · ~15 min — gh auth login, gh auth status, the scopes you need.

### [Branching And Pull Requests](05-Branching-And-Pull-Requests)
`beginner` · ~15 min — review, CI, rollback, history.

### [Writing GitHub Actions](05-Writing-GitHub-Actions)
`beginner` · ~20 min — workflow (a YAML file in .github/workflows), event (on:), job (runner + steps), step (uses: or run:), action, runner, artefact.

### [Your First CI Pipeline](05-Your-First-CI-Pipeline)
`beginner` · ~20 min — checkout, set up runtime with caching, install, lint, test.

### [Checks That Actually Matter](05-Checks-That-Actually-Matter)
`intermediate` · ~20 min — format, lint, type check, unit tests, build, migration lint, dependency/secret scan, integration tests, coverage threshold, smoke test against a deplo

### [Fast And Reliable Checks](05-Fast-And-Reliable-Checks)
`intermediate` · ~18 min — caching, parallel jobs, matrix builds, path filters, fail-fast, cancel-in-progress.

## Git & CI/CD with gh (Part 2: gates, secrets, releases, troubleshooting)

### [Branch Protection And Required Checks](05-Branch-Protection-And-Required-Checks)
`intermediate` · ~15 min — required status checks, review requirements, no force-push, linear history.

### [Secrets In CI](05-Secrets-In-CI)
`intermediate` · ~15 min — repository secrets, environment secrets, organisation secrets, and short-lived OIDC tokens instead of long-lived keys.

### [Hardening GitHub Actions](05-Hardening-GitHub-Actions)
`advanced` · ~20 min — Pin third-party actions to a full commit SHA; tags are mutable and a compromised dependency becomes your credential.

### [Releases, Tags And Versioning](05-Releases-Tags-And-Versioning)
`intermediate` · ~15 min — Semantic versioning in one paragraph, and what counts as breaking for an API, a CLI, and a mobile app.

### [Deployment Pipelines](05-Deployment-Pipelines)
`advanced` · ~20 min — Continuous delivery vs continuous deployment; why most teams want deploy-to-staging automatic and promotion-to-production manual.

### [CI Troubleshooting](05-CI-Troubleshooting)
`beginner` · ~15 min — Read the failing step, not the whole log; the last error before exit is usually the cause.

---

Section 5 of 16 · [Home](Home) · [Sidebar index](_Sidebar)
