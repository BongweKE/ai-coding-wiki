> **Section 04 · Lesson 6** · Level: intermediate · ~25 min · Prereq: [Managing a skill library](04-Managing-A-Skill-Library)

## Why this matters

Reading about skills does not produce a library. These three exercises do, because each one forces a skill out of a procedure you already perform but have never written down. Do them in one sitting, then audit and test what you produced.

## Exercise 1 — the local dev loop

Write `skills/shared/dev-loop/SKILL.md`. It must let a stranger start the project from a clean checkout.

Required content: prerequisites with versions; the exact commands in order; the port each service listens on; the seed step, because a server starting against an empty database looks broken; the test command and what a passing run prints; and one trap you have personally hit.

The trap earns its place. A real one: if the database is not running, the API still starts and fails later with an error that looks like a code bug. Write "start the database and wait for it to accept connections before starting the API", not "ensure the environment is ready".

Number every step. An agent follows a numbered list in order and skips steps buried in prose.

## Exercise 2 — the deployment runbook

Write `skills/<category>/deploy/SKILL.md` for one environment; staging is the right one to start with.

Required content:

- The exact promote or deploy command, with its flags and the branch it applies to.
- Who or what approves the step, and the gate that must be green first.
- What to check after it lands: the health endpoint, the log line proving the new revision is serving, the smoke test.
- The rollback command, written out. A runbook without a rollback is half a runbook.
- What not to do: never deploy straight to production, never hand-edit the running environment, never paste a credential into a command line.

Say which tool the steps assume. A runbook that silently assumes one CLI breaks when someone uses another.

## Exercise 3 — the code review checklist

Write `skills/shared/review-checklist/SKILL.md`. Keep it to eight items, ordered by what is most likely to hurt, because review attention is finite.

Required content, in priority order:

1. Does the change do what was asked, and only that?
2. Are secrets, keys and tokens absent from the diff — including fixtures?
3. Do the tests assert behaviour, or were they adjusted until they passed?
4. Do error paths surface loudly rather than as a green no-op?
5. Are exact values such as money handled without floating point?
6. Is the diff small enough to review in one sitting?
7. Do the new commands or endpoints actually run?
8. Is everything the change depends on documented — migration, environment variable, manual step?

Each item carries one clause saying why it is there: "check the assertion, not the exit code" tells a reader what to look for.

## Audit and test

Audit all three with the 12-item checklist from [Skill Quality And Anti-Patterns](04-Skill-Quality-And-Anti-Patterns), run every command, then test the only way that counts:

1. Open a **fresh session** with no history of writing them.
2. Ask the task in plain words: "how do I run this locally?", "how do I deploy this to staging?", "review this diff".
3. Watch which skill loads and whether it is followed. The first place the agent departs from your steps is the gap.
4. Break it deliberately: change a flag in the SKILL.md to something wrong and repeat step 2. If the agent now fails, the skill is genuinely being read.
5. Fix the gap, then record the lesson in your lesson bank — see [Lesson Banks And Retros](11-Lesson-Banks-And-Retros).

## Bonus — one skill, two agent tools

Take the review checklist and make it run under two agent products:

- Keep `SKILL.md` vendor-neutral: frontmatter, procedure, pitfalls, verification. No tool names in the body.
- Move anything tool-specific — install path, activation settings, script support — into a short `## Tool notes` section or a `references/tool-notes.md`, labelled with the product each note applies to.
- If a step only works in one product, say so in the step. Portability comes from stating assumptions, not hiding them.

Then run it in both. A version that needs no edits in the second tool answers whether the format is portable.

## Try it

1. Create the three folders and their `SKILL.md` files. Copy each command out of your shell history; do not write from memory.
2. Number the steps in exercises 1 and 2, and add the expected output where it teaches something.
3. Run the four automated checks from the previous lesson over the whole `skills/` tree.
4. Complete the fresh-session test for each skill and note the first departure point.
5. Add all three to your library index with an owner and a last-verified date.
6. Adapt the review checklist for a second agent tool and run it there.

## Common mistakes

- **Writing the runbook from memory** — a step that was never run is discovered missing at the worst moment. Copy from shell history and re-run each command.
- **A checklist with no priority order** — trivial items carry the same weight as important ones, and reviewers work top-down.
- **Testing in the session that wrote the skill** — the agent already has the context, so it looks like it works. Use a fresh session or a new directory.
- **Credentials and real hostnames in the runbook** — a skill gets copied, committed and shared. Refer to environment variable names, not values, and generalise internal hosts.

## Key takeaways

- Three skills cover most of a project's verbal repetition: the dev loop, the deploy runbook, the review checklist.
- Write from commands you actually ran, with numbered steps and expected output.
- Every runbook needs a rollback and a verification step; every checklist needs a priority order.
- The only test that matters is a fresh session getting it right without being told.
- Portability comes from keeping the body vendor-neutral and stating tool assumptions explicitly.

## Further learning

- [Agent Skills overview](https://agentskills.io/home) — quickstart and best-practice pages if you want a second reference while writing.
- [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) — how to capture successful approaches into a skill as you work.
- [Steering Claude Code: rules, skills, hooks, subagents](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more) — when a checklist should be a rule or a hook instead of a skill.
- [Rules Of Operation exercises](12-Rules-Exercises) — turning skills into operating rules for a team.
