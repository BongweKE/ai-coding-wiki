> **Section 12 · Lesson 9** · Level: intermediate · ~25 min · Prereq: [Change tracking](12-Change-Tracking)

## Why this matters

Reading about operating rules changes nothing. Four short artifacts — one improved rule, one ADR, one tested SOP, one changelog entry and release note — are enough to change how the next month goes. Do these on the project that actually hurts, not a toy repo: exercise three only works when a step you assumed can actually fail.

## Exercise 1 — One instruction, four layers (8 min)

Take the instruction **"never push directly to `main`"**.

1. Write it as you would type it in chat.
2. Write it as one line in the rules file.
3. Write the full procedure as a skill: branch, local checks, PR, checks green, merge.
4. Decide what should be a hook and what should be a CI gate.

A worked answer, so you can compare:

- **Chat**: forgotten by tomorrow.
- **Rules file**: `Never push directly to main. All changes arrive via a reviewed pull request.` — one line, applies to every task. Correct layer.
- **Skill**: the whole branch-and-PR procedure, with the exact commands and the checks to run before pushing. Too long for the rules file, needed on every feature — correct layer.
- **Gate**: a local pre-push hook that refuses a push to `main` is *preventive* — it stops the mistake. A CI workflow that resolves the commit's pull request and fails the run if it did not arrive via a PR is *detective* — it fires after the fact. You need both, because the detective control cannot undo the push, and the hook can be skipped with a flag.

Then route two of your own instructions: one for the rules file, one for a gate.

## Exercise 2 — An ADR for a decision you already made (6 min)

1. Pick a decision from the last month that you never wrote down: a dependency, an auth method, a deploy pattern, a data format.
2. Copy the template from [ADRs in practice](12-ADRs-In-Practice) into `docs/decisions/0001-<slug>.md`.
3. Write the two or three alternatives you actually considered, the criterion that decided it, and the cost you accepted.
4. Add the row to the index.

The deliverable is not the file. It is noticing how much easier the *next* decision is, because you now have a written criterion instead of a memory — and how much harder it is for a future session to undo it.

## Exercise 3 — An SOP for your deploy, tested literally (8 min)

1. Write the six sections: trigger, prerequisites, steps, verification, rollback, owner and dates.
2. Put the rollback point in the *prerequisites*, not at the bottom — the tag, the archive, the config snapshot, created before you start.
3. Open a clean shell and run the SOP literally, copy-pasting exactly what it says, on staging. Do not improvise and do not "know what it means".
4. Every time you cannot continue, or you guess, write it down. That list is the actual output of this exercise.
5. Fix those steps, add `Tested on <date>`, and commit it.

The step you assumed is the whole point. In practice it is usually a variable exported in the wrong shell, a conversion step between two of your own formats, or a wait longer than it looks.

## Exercise 4 — A changelog entry and a release note (3 min)

Take your last change and write both:

```markdown
## [Unreleased]
### Fixed
- Duplicate callback events no longer create a second ledger row (#212)
```

Then the release note, for a reader who does not know your codebase:

> **Fixed:** duplicate payment callbacks no longer create a second ledger row. No action needed.

Notice the difference in audience: the changelog entry names the issue and cites a domain object, the release note says what happened to the reader. Both are required — they answer different questions.

## Try it

Set up once, then work through the four exercises in order:

1. Open the repo you actually ship from, at the root, in a clean shell.
2. Create a scratch file `rules-work.md` and answer each exercise there, then move the finished artifact to its real home (`AGENTS.md`, `docs/decisions/`, `docs/sops/`, `CHANGELOG.md`).
3. Timebox: 8, 6, 8, 3 minutes. When the timer runs out, stop and commit what you have — an imperfect ADR today beats a perfect one never.
4. Finish by re-reading your rules file and deleting anything the agent could derive from the code.

## Common mistakes

- **Writing the rules-file line as an essay** — three sentences of context around one rule. The agent reads one line; the context dilutes it. Keep the rule, move the story to the ADR.
- **Putting a gate in the rules file** — "always run the secret scan" as prose is a request. As a pre-commit hook it is enforced, and it works when nobody remembers.
- **An ADR with one option** — if there is nothing to reject, nothing was decided; you have written a memo.
- **Testing the SOP by reading it** — the whole exercise is that reading misses the step you assumed. Run it, with a clean shell, on the real target.
- **A changelog entry that says "fixes"** — no object, no PR link, no reader. Say what changed for whom.
- **Doing all four on a toy repo** — none of your real assumptions live there, so none of them get found.

## Key takeaways

- Route each instruction to the cheapest layer that produces the outcome; a gate beats prose for anything a machine can decide.
- Write the ADR for the decision you already made — the next one gets faster, and settled decisions stop being re-litigated.
- Test the SOP literally, from a clean shell; the step you assumed is the deliverable.
- Write both a changelog entry (for the team) and a release note (for the user) for your last change.
- Timebox each exercise and commit the imperfect artifact. Operating rules accrete; they are never finished in one sitting.

## Further learning

- [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) — start from the gap you observed, then build the skill that closes it.
- [Agent Skills Overview](https://agentskills.io/home) — the format for the skill you wrote in exercise 1.
- [Templates](16-Templates) — starter files for the ADR, SOP and changelog used here.
- [Capstone 3: Make a repo agent-proof](15-Capstone-3-Agent-Proof-Repository) — all four artifacts applied to one repository, end to end.
