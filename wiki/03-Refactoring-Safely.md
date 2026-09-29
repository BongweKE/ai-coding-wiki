> **Section 03 · Lesson 6** · Level: intermediate · ~15 min · Prereq: [Keeping diffs small](03-Keeping-Diffs-Small)

## Why this matters

Refactoring changes the shape of code without changing what it does. That contract is only checkable if you have tests. Without them, "refactor" and "rewrite" are the same word, and the only thing telling you the behaviour survived is the agent's opinion.

## Tests are the permission slip

A test harness is what makes refactoring safe. Green before, green after, behaviour unchanged. If the suite is thin, the first job is not to refactor — it is to add the tests that would catch a change in behaviour.

Run the suite *before* you touch anything, and record the result. "All green" is the baseline. If it is already failing, you have no way to attribute the next failure, so fix or quarantine the red tests first.

## Characterisation tests before legacy code

Legacy code is code you do not understand and are afraid to change. The tool for it is the **characterisation test**: a test that pins down what the code *currently* does, including behaviour you suspect is wrong.

The method:

1. Call the function or hit the endpoint with a real input.
2. Capture the actual output.
3. Assert that output — even if it looks odd.
4. Repeat for the cases you care about.
5. Only then refactor.

You are not asserting what the code *should* do; you are taking a photograph of what it does. That photograph is your alarm. If a refactor changes the output in a case you did not intend, the test screams. If you think a behaviour is a bug, fix it in a *separate* commit after the refactor, so nobody confuses the two.

Useful prompt: *"Read `fee.ts`. Write characterisation tests that capture its current behaviour for a zero amount, a negative amount, and a very large amount. Do not change the implementation. If a case returns something surprising, assert the surprising value and add a comment."*

## Mechanical versus semantic refactors

Split refactors into two kinds and never mix them:

- **Mechanical** — rename a symbol, move a file, extract a function, change a formatter. Behaviour cannot change. These are safe to do in bulk, and tools can verify them.
- **Semantic** — change a data structure, replace a library, split a service, alter an algorithm. Behaviour may change subtly.

Mechanical refactors are cheap and broad. Semantic refactors are expensive and narrow. Doing a rename and an algorithm change in the same commit means the reviewer cannot tell which lines are the rename and which are the logic.

Ship them as separate commits, in this order: mechanical first (the suite proves it is inert), then the semantic change on top with its own tests. If the semantic change has to be reverted, the rename stays.

## Never mix a refactor with a behaviour change

This is the rule the whole lesson exists for. A single commit that both moves code and changes what it does destroys two things:

- **Reviewability** — the reviewer sees a sea of moved lines and cannot find the three that matter.
- **Bisectability** — when a bug appears next sprint, `git bisect` lands on "the refactor" and you cannot tell whether the move or the change caused it.

The refactor commit should be boring. Its commit message is "extract `parseFee` from `calculate` — no behaviour change, suite unchanged". If you cannot honestly write "no behaviour change", it is not a pure refactor.

Ask the agent to declare intent up front:

> "Do a pure mechanical refactor: move the fee logic into its own module. Do not change behaviour, do not fix anything you notice, do not touch tests unless imports must change. When done, show me `git diff --stat` and confirm the test results are unchanged."

Anything it notices along the way becomes the next ticket, not part of this commit.

## Try it

1. Pick a file with at least one test and one function you dislike.
2. Run the suite and paste the baseline result into your notes.
3. Write a characterisation test for the function's current behaviour, including one edge case. Commit it on its own.
4. Ask for a pure mechanical refactor with an explicit "no behaviour change" instruction.
5. Run the suite. Then `git diff` and confirm nothing outside the moved code changed.
6. Commit the refactor. Then, separately, make the behaviour change you actually wanted, with its own test.

## Common mistakes

- **Refactoring without a baseline run** — the suite was already red, so you cannot attribute the next failure. Run it first.
- **Rewriting instead of refactoring** — the agent "improves" the algorithm while moving code, and the tests were never strong enough to notice. Pin behaviour with characterisation tests before you start.
- **Mixing the rename with the fix** — one commit, two intentions, and an unreadable diff. Separate commits, mechanical first.
- **Trusting a green suite you did not see fail** — if the test could not have caught a change in behaviour, green means nothing. Check the assertions cover the paths you moved.
- **Aggressively refactoring legacy code you do not understand** — you replace a working quirk with a clean bug. Characterise it first; fix the quirk later, deliberately.

## Key takeaways

- No test harness, no refactor — that is a rewrite.
- Write characterisation tests to photograph legacy behaviour before changing shape.
- Separate mechanical refactors from semantic ones, mechanical first.
- Never put a refactor and a behaviour change in the same commit.
- A refactor commit should be boring and explicitly "no behaviour change".
- Anything you notice while refactoring is a task for the next commit.

## Further learning

- [Best practices for Claude Code](https://www.anthropic.com/engineering/claude-code-best-practices) — scoping a task and telling the agent what not to touch.
- [TDD with agents](03-TDD-With-Agents) — the red-green loop that gives refactoring its safety net.
- [Keeping diffs small](03-Keeping-Diffs-Small) — why a mixed commit cannot be reviewed or reverted.
