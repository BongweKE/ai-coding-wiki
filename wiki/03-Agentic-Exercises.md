> **Section 03 · Lesson 12** · Level: beginner · ~25 min · Prereq: [Reviewing agent output](03-Reviewing-Agent-Output)

## Why this matters

You have read the workflow lessons. Reading is not practice. The eight exercises below run the same loop at eight different scales, in a toy repo you can throw away. Do them in order; each one drills a habit the next one assumes. Budget about two hours for the set.

## Set up a toy repo

Make a small project with something to get wrong: a package with a function that computes a total from a list of items, a test folder, and a `README.md`. Keep it deliberately imperfect — one function longer than it should be, and one behaviour with no test. Commit the starting point so `git diff` always has a clean baseline.

## Try it

Work the eight exercises in order. For each one, record three things: the starting commit hash, the exact prompt you sent, and what you did with the output. That log is the real artifact — the prompts you keep are the ones you will reuse.

## Exercise 1: Explore first

**Do:** Ask only for a map: *"Describe how data flows from entry to output. List the files, the functions, and one thing that looks fragile. Do not edit."*

**Success criteria:** No file is modified (`git status` is clean), and the map names at least one fragility you verify by reading the code.

**A good answer looks like:** a short, specific report naming real functions, not a generic tour. If it invents a function that does not exist, that is the lesson — read-only exploration still needs checking.

## Exercise 2: Plan then implement

**Do:** Ask for a plan for a small feature (a `--dry-run` flag, say). Require files touched, interfaces, tests, risks, rollback. Approve or revise in writing. Only then implement.

**Success criteria:** A written plan exists before any code; the final diff matches the plan's file list; nothing off-list changed.

**A good answer looks like:** a plan you corrected at least once. An unreviewed plan means you skipped the exercise.

## Exercise 3: The TDD loop

**Do:** For one behaviour, have the agent write a failing test first, show the red output, then implement the minimum to pass.

**Success criteria:** You saw the failing output before the implementation; the test file is unchanged by the implementation (`git diff` on the test file is empty).

**A good answer looks like:** a test asserting a specific value, and a red run that fails for the reason you expect.

## Exercise 4: A small-diff refactor

**Do:** Extract one long function into two, as a pure mechanical refactor.

**Success criteria:** Suite green before and after; the commit message says "no behaviour change"; `git diff --stat` touches only the refactored file and its imports.

**A good answer looks like:** a boring diff. If the agent fixed a bug "while it was in there", you have found the exercise's point — split it.

## Exercise 5: A reproducible bug fix

**Do:** Introduce a bug on a throwaway branch. Fix it properly: reproduction first, hypothesis, root cause, regression test.

**Success criteria:** A committed test that failed before the fix and passes after; the fix targets the cause; no suppressed exceptions.

**A good answer looks like:** the reproduction failing with the exact error you planted, then a two-line fix and a test that locks it.

## Exercise 6: Review a deliberately bad diff

**Do:** Ask the agent for a plausible-looking change that is subtly wrong — a weakened assertion, an unused import, a TODO, and a call to a method that does not exist. Then review it with the five questions.

**Success criteria:** You find all four defects, and you can say which question caught each one.

**A good answer looks like:** "Q4 caught the weakened assertion, Q5 caught the invented method." If the invented method survives your review, that is the one to remember.

## Exercise 7: Add a hook

**Do:** Add a pre-commit hook that blocks edits to one protected path (a `migrations/` folder, say), then try to violate it.

**Success criteria:** The violation is refused with a message naming the rule; a legitimate edit still commits.

**A good answer looks like:** a refusal you can read, and the knowledge that the block happened before anything was committed.

## Exercise 8: Hand off a session

**Do:** End a session with a four-line hand-off note: goal, state, next step, pointers. Clear or start a new session and continue from the note alone.

**Success criteria:** The new session reaches the next step without re-exploring the repo, and you did not re-answer a settled question.

**A good answer looks like:** a note short enough to paste in one message and specific enough that the first reply is useful.

## Common mistakes

- **Skipping the log** — you cannot learn from a prompt you did not write down. Keep the log per exercise.
- **Doing the good version by accident** — if a diff came out clean because the task was trivial, it proved nothing. Use a task with room to go wrong.
- **Fixing the bad diff instead of reviewing it** — in exercise 6, the goal is to *find* the defects. Fixing teaches you nothing about the tell list.
- **A hook that only warns** — in exercise 7, a warning is not a pass. Make sure the violation is blocked.
- **A ten-line hand-off** — that is a session summary, not a pointer for the next one. Four lines.
- **Doing them all in one session** — you will be testing session hygiene with a rotted window. Start fresh per exercise.

## Key takeaways

- Practice each habit in isolation before combining them.
- Read-only exploration still needs checking; a map can be wrong.
- The test that defines the requirement stays fixed; only the implementation moves.
- Small, boring, single-intent commits are the goal, not a compromise.
- A guardrail is only real if it blocks something.
- A four-line hand-off beats a long summary for starting the next session.

## Further learning

- [Best practices for Claude Code](https://www.anthropic.com/engineering/claude-code-best-practices) — the workflow these exercises drill.
- [The feature loop](03-The-Feature-Loop) — the full loop the eight exercises fragment.
- [Git essentials for the AI era](05-Git-Essentials) — the commands you will use throughout.
