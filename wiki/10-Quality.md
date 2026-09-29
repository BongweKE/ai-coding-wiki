> **Section 10 · Quality** — Tests, integration and smoke tests, evals for AI features, definition of done, debugging.

*7 lessons.*

## By the end of this section you can

- Build a test suite that fails when the product breaks, not when the code is refactored.
- Add smoke tests that exercise the deployed artefact, not just your laptop.
- Build a small eval set with a threshold for an AI feature, and gate CI on it.
- Write a definition of done you can actually check.

### [The Test Pyramid In Practice](10-Test-Pyramid)
`beginner` · ~18 min — Tests are what let you move quickly without reading every line an agent wrote. Without them, "the agent says it works" is your entire verification story.

### [Testing With Agents](10-Testing-With-Agents)
`intermediate` · ~18 min — An agent can write a test suite in seconds.

### [Integration And Smoke Tests](10-Integration-And-Smoke-Tests)
`intermediate` · ~18 min — A unit test runs in a process with no database, no environment variables and no network.

### [Evaluating AI Features](10-Evaluating-AI-Features)
`advanced` · ~20 min — A normal test asserts one exact output. A feature that calls a model returns different words every time, so assert answer == "the expected sentence" is either flaky or useless.

### [Definition Of Done](10-Definition-Of-Done)
`beginner` · ~12 min — "Done" drifts. You finish the code, the agent says it is done, the tests pass locally, and two days later production is missing a migration and nobody wrote the doc.

### [Debugging Discipline](10-Debugging-Discipline)
`intermediate` · ~18 min — The fastest way to waste an afternoon is to change code before you can reproduce the failure.

### [Quality Exercises](10-Quality-Exercises)
`intermediate` · ~25 min — Reading about verification does not build the reflex. These four exercises do. You write a suite small enough to finish in an hour, then deliberately break the code to prove the suite bites.

### [Regression Testing Your Agent Harness](10-Regression-Testing-Your-Agent-Harness)
`advanced` · ~20 min — Prompts, rules files, skills and tool schemas change weekly with no tests — a golden set captured from real traces catches the regression before your users do.

---

← [9. Safety & Security](09-Safety-And-Security) · [Home](Home) · [Sidebar](_Sidebar) · [11. Documentation](11-Documentation) →

