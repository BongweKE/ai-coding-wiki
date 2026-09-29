> **Section 2 · Prompting & Context** — Instructions and context an agent can actually execute — including the rules file loaded every session.

*9 lessons.*

## By the end of this section you can

- Write an instruction with context, task, constraints, inputs, output format and a verification step.
- Write a rules file that loads every session and stays short enough to be read.
- Stop a session's context from rotting: what to keep, what to drop, when to start fresh.
- Reach for the right one of fourteen prompt patterns instead of starting from a blank box.

### [Prompting Fundamentals](02-Prompting-Fundamentals)
`beginner` · ~12 min — "Fix my code" gets you a guess. The agent cannot see your terminal, your intent, or the constraint that the old endpoint has to keep working.

### [Structuring Instructions](02-Structuring-Instructions)
`beginner` · ~12 min — A specific prompt still fails if the agent cannot tell which part is the task and which part is the material. Structured instructions fix that.

### [Showing Examples (Few-Shot)](02-Showing-Examples-Few-Shot)
`intermediate` · ~12 min — Describing a format in prose takes a paragraph and still leaves room for interpretation. One worked example pins it down in four lines.

### [Reasoning And Chain Of Thought](02-Reasoning-And-Chain-Of-Thought)
`intermediate` · ~12 min — An agent that starts editing on the first sentence spends your review budget on the wrong problem.

### [Context Engineering](02-Context-Engineering)
`intermediate` · ~15 min — The context window is the resource you actually manage. Every file the agent reads, every command output, every tangent you take stays in it and costs attention.

### [Rules Files: AGENTS.md And CLAUDE.md](02-Rules-Files-AGENTS-and-CLAUDE-md)
`beginner` · ~15 min — Every session you re-explain the same three things: how to run the tests, which folder is off-limits, and the convention that is not in the code.

### [Prompt Patterns Cookbook](02-Prompt-Patterns-Cookbook)
`beginner` · ~15 min — Most of your prompts are one of fourteen kinds. Naming them means you stop inventing prompts from scratch at 11pm and start reaching for a shape you already know works.

### [Prompt Anti-Patterns](02-Prompt-Anti-Patterns)
`beginner` · ~10 min — Bad prompts look productive. You get an answer, you paste another prompt, you get another answer. An hour later you have a large diff you do not understand and cannot safely review.

### [Prompting Exercises](02-Prompting-Exercises)
`beginner` · ~20 min — Reading about prompting changes nothing. Six exercises on one tiny repo will change your default prompt for good — and each one is graded, so you cannot talk yourself past a vague answer.

---

← [1. Foundations](01-Foundations) · [Home](Home) · [Sidebar](_Sidebar) · [3. Agentic Workflows](03-Agentic-Workflows) →

