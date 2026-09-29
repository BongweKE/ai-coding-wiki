> **Section 3 · Agentic Workflows** — The daily craft: plan, implement, test, review, and keep diffs small enough to read.

*12 lessons.*

## By the end of this section you can

- Run the loop: explore, plan, implement in small steps, verify with evidence, commit, review.
- Do red-green-refactor with an agent without letting it weaken the tests that define the work.
- Keep diffs reviewable, and explain why that is the biggest quality lever you have.
- Debug from a reproducible failure instead of a plausible story, and hand a session off cleanly.

### [The Feature Loop](03-The-Feature-Loop)
`beginner` · ~15 min — An agent writes a working feature and a broken one with exactly the same confidence. The difference is not the model; it is the loop you make it run.

### [Plan Mode And Spec-Driven Development](03-Plan-Mode-And-Spec-Driven-Development)
`intermediate` · ~15 min — A plan is the cheapest artifact in software. Ten minutes of planning can save a day of implementation, because you review a short document instead of a large diff.

### [TDD With Agents](03-TDD-With-Agents)
`intermediate` · ~18 min — Agents are good at making tests pass. That is the problem. An agent that cannot satisfy a test has a second, easier option: weaken the test.

### [Keeping Diffs Small](03-Keeping-Diffs-Small)
`beginner` · ~12 min — Small diffs are not an aesthetic preference. A diff is the unit of review, the unit of rollback, and the unit of blame.

### [Agentic Debugging](03-Agentic-Debugging)
`intermediate` · ~18 min — An agent debugging without a reproduction is speculating in code form. It reads a stack trace, guesses a cause, edits a file, and asks you to try again. Sometimes it works.

### [Refactoring Safely](03-Refactoring-Safely)
`intermediate` · ~15 min — Refactoring changes the shape of code without changing what it does. That contract is only checkable if you have tests.

### [Subagents And Parallel Work](03-Subagents-And-Parallel-Work)
`advanced` · ~18 min — One agent doing everything works until the task outgrows its context window — and by then it has forgotten the constraint you gave it at the start.

### [Agent Memory And Session Hygiene](03-Agent-Memory-And-Session-Hygiene)
`intermediate` · ~12 min — A long session rots.

### [Hooks And Guardrails](03-Hooks-And-Guardrails)
`advanced` · ~15 min — A rule in a prompt is a request. A hook is a mechanism. When you tell an agent "never commit secrets", you are hoping.

### [Reviewing Agent Output](03-Reviewing-Agent-Output)
`intermediate` · ~15 min — An agent's output is a claim until you check it.

### [Token And Cost Discipline](03-Token-And-Cost-Discipline)
`intermediate` · ~12 min — Agents cost money per token, and an agentic task spends tokens on things that are invisible in a chat: the context re-sent on every turn, the output of every command, the retries.

### [Agentic Exercises](03-Agentic-Exercises)
`beginner` · ~25 min — You have read the workflow lessons. Reading is not practice. The eight exercises below run the same loop at eight different scales, in a toy repo you can throw away.

---

← [2. Prompting & Context](02-Prompting-And-Context) · [Home](Home) · [Sidebar](_Sidebar) · [4. Agent Skills](04-Agent-Skills) →

