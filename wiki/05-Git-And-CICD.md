> **Section 5 · Git & CI/CD** — Git, the GitHub CLI, workflows, the checks that matter, hardening, releases and deploys.

*13 lessons in two parts.* Part 1: 1: git, gh, and your first pipeline. Part 2: 2: gates, secrets, releases, troubleshooting.

## By the end of this section you can

- Branch, commit, push and open a reviewed pull request with the GitHub CLI.
- Write a workflow file that lints, tests and fails loudly on every pull request.
- Choose the checks worth their CI minutes, and know what each one catches.
- Protect the main branch, manage secrets, harden third-party actions, and release deliberately.

## Git & CI/CD with gh (Part 1: git, gh, and your first pipeline)

### [Git Essentials For The AI Era](05-Git-Essentials)
`beginner` · ~20 min — An AI coding agent can rewrite forty files in ninety seconds. That speed is only safe because of one boring tool: git.

### [GitHub CLI Quickstart](05-GitHub-CLI-Quickstart)
`beginner` · ~15 min — Every task that sends you to a browser tab breaks your flow. The GitHub CLI (gh) puts issues, pull requests, and CI runs in the same terminal where you already work.

### [Branching And Pull Requests](05-Branching-And-Pull-Requests)
`beginner` · ~15 min — A branch plus a pull request costs you two minutes and buys four things: a diff someone else can review, a place for CI to run before the code reaches main, a record you can point to when something breaks, and a clean way to abandon work that turned out wrong.

### [Writing GitHub Actions](05-Writing-GitHub-Actions)
`beginner` · ~20 min — CI/CD means continuous integration and continuous delivery: a machine that runs your checks on every change so a broken commit never reaches main by accident.

### [Your First CI Pipeline](05-Your-First-CI-Pipeline)
`beginner` · ~20 min — A pipeline that runs your checks but never fails is worse than no pipeline, because it teaches you to trust a green tick that means nothing.

### [Checks That Actually Matter](05-Checks-That-Actually-Matter)
`intermediate` · ~20 min — A pipeline can hold ten checks and still miss the bug that costs you a weekend.

### [Fast And Reliable Checks](05-Fast-And-Reliable-Checks)
`intermediate` · ~18 min — A pipeline that takes twenty minutes will be bypassed. People stop waiting, merge on a hunch, and the checks become theatre. Speed is what keeps the gate in the loop.

## Git & CI/CD with gh (Part 2: gates, secrets, releases, troubleshooting)

### [Branch Protection And Required Checks](05-Branch-Protection-And-Required-Checks)
`intermediate` · ~15 min — A workflow file that nothing enforces is a suggestion.

### [Secrets In CI](05-Secrets-In-CI)
`intermediate` · ~15 min — Your pipeline needs credentials: a database URL to run migrations, a deploy token, an API key for an integration test.

### [Hardening GitHub Actions](05-Hardening-GitHub-Actions)
`advanced` · ~20 min — A workflow file is code that runs with your repository's credentials, on a machine that can reach your secrets.

### [Releases, Tags And Versioning](05-Releases-Tags-And-Versioning)
`intermediate` · ~15 min — A commit hash is a perfect identifier and a terrible announcement. Nobody says "we shipped 4f9c2ab".

### [Deployment Pipelines](05-Deployment-Pipelines)
`advanced` · ~20 min — A release workflow that builds one artefact does not yet tell you how it reaches users.

### [CI Troubleshooting](05-CI-Troubleshooting)
`beginner` · ~15 min — A red pipeline is not a wall, it is a message: something you cannot yet see would have broken for a user.

---

← [4. Agent Skills](04-Agent-Skills) · [Home](Home) · [Sidebar](_Sidebar) · [6. System Design](06-System-Design) →

