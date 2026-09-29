> **Section 02 · Lesson 9** · Level: beginner · ~20 min · Prereq: [Prompt anti-patterns](02-Prompt-Anti-Patterns)

## Why this matters

Reading about prompting changes nothing. Six exercises on one tiny repo will change your default prompt for good — and each one is graded, so you cannot talk yourself past a vague answer.

## Build the toy repo

Five minutes of setup. The bug is deliberate; do not fix it yet.

```bash
mkdir toy-repo && cd toy-repo && git init
python3 -m venv .venv && . .venv/bin/activate && pip install pytest
```

Save this as `invoices.py`:

```python
def total(rows):
    """Sum amount_cents across invoice rows."""
    return sum(r["amount_cents"] for r in rows)

def format_kes(cents):
    return f"KES {cents / 100:,.2f}"
```

Save this as `test_invoices.py`:

```python
from invoices import format_kes, total

def test_total_sums_amounts():
    assert total([{"amount_cents": 250}, {"amount_cents": 150}]) == 400

def test_format_kes():
    assert format_kes(400) == "KES 4.00"
```

```bash
pytest -q   # 2 passed
```

The bug: `total` counts rows marked `{"voided": True}`, which should not be billed. Every exercise targets this repo.

## Exercise 1 — Rewrite a vague prompt

**Bad prompt:** "the total function is wrong, fix it"

**Task.** Rewrite it using the four moves from [Prompting fundamentals](02-Prompting-Fundamentals): specific, goal, constraints, definition of done. Send both versions in fresh sessions.

**Rubric.** Your rewrite names the file and function, states the behaviour you expect, says what must not change, and finishes with a command. If the agent asked you a clarifying question, the prompt was still vague.

## Exercise 2 — Add constraints

**Bad prompt:** "add a late fee feature"

**Task.** Rewrite it with at least four constraints: money stays in integer cents, no new dependencies, no change to the `total` signature, a test is required, and this must work for a zero-amount invoice. Send it and read the diff against each constraint.

**Rubric.** Count how many constraints the diff honoured without you repeating them. Fewer than four means they were buried in prose instead of listed one per line.

## Exercise 3 — Ask for a plan

**Bad prompt:** "implement late fees now"

**Task.** Send a plan-only prompt: files, order, risks, open questions, no edits. Read the plan and change one thing before approving.

**Rubric.** No file was modified during the plan turn. The plan names real files. It asks at least one question you had not thought about. Bonus: save the plan to `PLAN.md` and review the implementation against it afterwards.

## Exercise 4 — Add a verification step

**Bad prompt:** "make sure it works"

**Task.** Reproduce the voided-row bug first: ask for the smallest failing test, run it, keep the output. Then ask for the fix, with the instruction to run the suite and paste the result.

**Rubric.** You have a failure output before any fix. The final answer includes the test command and its real output. The assertion was not weakened or moved. If the agent edited the test, the exercise failed — say so in a fresh session and start again.

## Exercise 5 — Add an example

**Bad prompt:** "format the money properly"

**Task.** Write a prompt that includes two labelled examples of the exact output you want, including a negative case: `format_kes(0)` should return `"KES 0.00"`, never `"KES 0"` or a `None`. Ask for the change plus a test.

**Rubric.** The produced output matches your example character for character, including the thousands separator on `format_kes(123456789)`. If the output drifted, your examples were inconsistent with each other.

## Exercise 6 — Turn a repeat into a rule

**Bad prompt:** the third time you have typed "money is integer cents, never float"

**Task.** Open `AGENTS.md` (create it) and write the rule as one line under a `## Conventions` heading. Add a `## Commands` section with `pytest -q`. Then start a fresh session and ask for a small change involving money — without mentioning cents at all.

**Rubric.** The agent follows the convention with no reminder, and can tell you which context file it loaded. If it did not load the file, check the filename and location; a rules file in the wrong place is silently ignored.

## Reflect

Answer in two sentences: which single instruction changed the answer most?

Then write it into the rules file as a rule, in imperative form. That sentence is worth more than the other five exercises combined, because it will still be working for you next month.

## Try it

The six rewrites are done. Now run the whole loop once on real work.

1. Pick a small change in a repo you actually own and open a fresh session with only your rules file loaded.
2. Run exercises 3, 4 and 5 in order on that one change: plan, failing test, then example-driven output.
3. Before you merge, grade your own final prompt with exercise 1's rubric: does it name the file, the goal, the constraints and the command?
4. Save the prompt into `prompts/` and add any new constraint to `AGENTS.md`.

The repetition is the point. When you can grade a prompt in ten seconds and know which line is missing, this section has done its job.

## Common mistakes

- **Sending one version and stopping.** Sending both and comparing diffs is the exercise. The comparison is the lesson.
- **Fixing the bug before exercise 3.** Now every plan is informed by the fix, and you learn nothing about planning.
- **Grading your own rewrite generously.** Run the rubric literally: did the answer ask you anything? Then the prompt was vague.
- **Accepting a green suite as proof.** Check the test diff. If the assertion moved, the exercise failed.
- **Writing a rules-file entry in prose.** "We generally prefer cents" is a suggestion. "Money is integer cents; never float" is a rule.
- **Skipping the reflection.** One rule you wrote yourself beats six you copied.

## Key takeaways

- Six rewrites on one toy repo build a habit that transfers to every real prompt.
- Constraints you list get honoured; constraints buried in prose get dropped.
- A failing test before a fix is what makes "done" checkable.
- Examples pin down format faster than any adjective.
- A prompt you have typed three times belongs in the rules file.

## Further learning

- [Anthropic's prompt engineering tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial) — the full exercise-driven course this section condenses.
- [Anthropic's courses index](https://github.com/anthropics/courses) — prompt evaluations and tool use, the natural next steps after this material.
- [Best practices for Claude Code](https://www.anthropic.com/engineering/claude-code-best-practices) — the workflows these exercises are miniatures of.
