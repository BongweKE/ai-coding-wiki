> **Section 11 · Lesson 6** · Level: beginner · ~20 min · Prereq: [Writing for future you](11-Writing-For-Future-You)

## Why this matters

Documentation is a skill, and skills come from reps against a clock. These four exercises are small and finishable in one sitting each. Each one has a test you can fail honestly: a clean checkout that refuses to run, a runbook you cannot follow without improvising, a gotcha entry that does not help you next time. Do them once and the format is yours.

## Exercise 1 — README in 20 minutes, tested on a clean checkout

Pick a toy project you already wrote: a script, a small CLI, a scraper. Set a 20-minute timer. Write the first screen (what it is, who it is for, why, one command), a numbered setup section with expected output, and a status line saying what is unfinished.

Deliverable: `README.md`, plus the exact command that shows the project working.

Test it by cloning to a location your machine has never seen:

```bash
git clone ./readme-lab /tmp/readme-fresh   # or a real remote
cd /tmp/readme-fresh
# now follow the README only, no memory allowed
```

Pass condition: you reach the working command with no improvisation, and every step produced the output the README promised. Fail honestly — write down the minute and the line where you guessed — then fix that line and repeat once.

## Exercise 2 — A runbook you follow literally

Write `docs/runbooks/deploy.md` for a deployment you can actually perform: a static site, a worker, a container. Use numbered steps, the command for each, the output you expect, a failure section, and a "Do not" list.

Deliverable: a runbook with preconditions, 5–8 steps, a rollback or failure path, and a verified date.

Then run it on a clean shell with your own history cleared, following the text as if someone else wrote it. Every place you typed something the runbook did not say is a bug in the runbook, not in you. Expect to find two or three — people reliably omit the working directory, an environment variable, and the "wait for it to be healthy" step.

```markdown
## Steps
1. `cd ~/projects/<app>`                       → expect the repo root (has `.git`)
2. `./scripts/check-gates.sh`                  → expect "all green" and exit 0
3. `railway up --service <svc>`                → expect "build complete" then a deploy URL
4. `curl -fsS https://<svc>.example.com/health` → expect `{"status":"ok"}`
```

## Exercise 3 — Three gotcha entries from bugs you have hit

Think of three bugs that cost you an hour or more. Write one entry each in the four-part format: **symptom**, **cause**, **fix**, **detection next time**. The first three lines come easily; the fourth is the exercise.

Deliverable: three entries in `docs/gotchas.md`, grouped under a component heading.

Test: read each entry as the person who has not seen the bug. Does the symptom line let them recognise their situation in ten seconds, including the exact error text? Does the detection line name a specific check — a test, a probe, an assertion — rather than "be careful"? If an entry fails, rewrite it; if you cannot name a detection, that is the finding: you do not yet understand the bug well enough to prevent it.

Good symptom lines are quoted, not paraphrased. "The call succeeds locally and fails in the container with `CERTIFICATE_VERIFY_FAILED`" beats "TLS problems after deploy".

## Exercise 4 — A hand-off note for a stranger

Take one unfinished piece of work — ideally something half-done and slightly messy, which is the realistic case — and write the six-field note from [Writing for future you](11-Writing-For-Future-You): state, gates, decisions, next step, open questions, traps.

Deliverable: the note in the pull request description or a `handoff.md` on the branch.

Test: hand it to someone with no context, or open a fresh agent session with only the repository and the note. Give one instruction — "continue this work" — and watch where they stall or guess. The stall is a missing fact; the guess is an ambiguity. Both go back into the note. A note that produces zero questions is the pass.

## Try it

Run all four in one sitting like a workshop, roughly 60–75 minutes total:

1. Set up a scratch repo with a toy project and commit it: `mkdir readme-lab && cd readme-lab && git init`.
2. Exercises 1 and 2 first — they are the ones you can test mechanically.
3. Exercise 3 next, with a 15-minute cap so you do not polish entries nobody will read.
4. Exercise 4 last, on your real unfinished work, because it is the one that pays back tomorrow.
5. Commit the four artefacts together. From now on, treat them as the definition of done for a small task (see [Definition of done](10-Definition-Of-Done)).

## Common mistakes

- **Writing documentation as a summary of the code** — telling the reader what the functions do instead of how to use the thing. Fix: write for the reader's next action, not for completeness.
- **Never running the clean-checkout test** — the README is "obviously fine" because your machine has state. Fix: clone to `/tmp`, delete your personal config, and follow it literally.
- **Polishing instead of testing** — twenty minutes spent on wording, zero on the failing step. Fix: timestamp the test, not the prose.
- **Gotcha entries with no error text** — future readers cannot match their situation to yours. Fix: paste the actual error line.
- **Writing exercise 4 for a tidy task** — the note looks competent and teaches nothing, because the tidy case has no open questions or traps. Fix: use the messiest unfinished work you have.
- **Stopping at one rotation** — each exercise improves sharply on the second pass, once you know where your assumption breaks. Fix: repeat the runbook and the README test at least twice.

## Key takeaways

- Every documentation exercise ends in a test you can fail: a clean checkout, a literal run-through, a stranger's question, a fresh agent that stalls.
- The README test is a fresh clone; the runbook test is following your own text without improvising.
- The fourth field of a gotcha entry — detection — is the one that turns a story into prevention.
- The hand-off note is done when a reader needs to ask you nothing.
- Expect two or three discoveries per exercise. Finding none usually means the test was too gentle.

## Further learning

- [Docs as code](11-Docs-As-Code) — the doc map these artefacts slot into.
- [Writing a great README](11-Writing-A-Great-README) — the first-screen and setup rules used in exercise 1.
- [Documentation per feature](11-Documentation-Per-Feature) — the gotcha format and the change → document table behind exercise 3.
- [Lesson banks and retros](11-Lesson-Banks-And-Retros) — where lessons from these exercises should end up.
- [Best practices for Claude Code](https://www.anthropic.com/engineering/claude-code-best-practices) — checking your docs by watching an agent use them.
