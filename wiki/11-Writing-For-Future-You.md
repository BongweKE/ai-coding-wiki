> **Section 11 · Lesson 5** · Level: beginner · ~12 min · Prereq: [Lesson banks and retros](11-Lesson-Banks-And-Retros)

## Why this matters

Everything you do rarely is something you will do badly next time — promoting a release, rotating a key, restoring a database from a backup. The gap is not knowledge, it is memory: the three commands that mattered, the order they had to run in, the output that means it worked. Writing for future you means writing a page that is boring and exact, so past-you is not needed to interpret it.

## Runbooks: steps and expected output

A runbook is the procedure for an operation you perform seldom enough to forget. It is not an essay about the operation. It is numbered steps, each with the command, and where output teaches something, the output you expect.

```markdown
# Runbook: promote <service> to production
Last verified: 2026-05-02 (by hand, following this text literally)

## Preconditions
- Staging has run the changed flow successfully.
- No migration is pending: `./tool/migrate --status` prints "up to date".

## Steps
1. Confirm the commit: `git rev-parse --short HEAD`  → expect the SHA from the PR.
2. Trigger the promotion:
   `gh workflow run "Promote to Production" --ref main`
3. Watch it: `gh run watch`  → expect every job green, ~6 min.
4. Verify the app answers: `curl -fsS <PROD_API_URL>/health`  → expect `{"status":"ok"}`.
5. Exercise the changed flow once, manually, with a test account.

## If it fails
- Build fails → nothing was deployed; fix on a branch, PR, merge, promote again.
- Migration step fails → do not patch by hand; roll back per `docs/runbooks/rollback.md`.
- Health check fails → revert to the previous deployment, then investigate offline.

## Do not
- Deploy from a feature branch.
- Run a migration by hand against production.
```

Four properties make the difference. Numbered steps, so a reader can skip ahead. Expected output, so "no response" is distinguishable from "success". A failure section, written while the calm version of you still remembers what could go wrong. A **Do not** list, because the expensive mistakes are usually somebody being helpful.

Write it the day you learn the operation, then verify it once by following your own words literally and fixing every point where you improvised. Note the "last verified" date — an unverified runbook is a hypothesis.

## Session hand-off notes

A hand-off note is state, not narrative. It exists so a stranger — a colleague tomorrow, or an agent in a fresh session with no history — can take the next step in thirty seconds.

```markdown
# Hand-off: payout retries (2026-05-04, ~14:20)

- **State**: handler implemented and tested; not deployed. Branch `feat/payout-retries`, PR #128, head `a1b2c3d`.
- **Gates**: `./scripts/check-gates.sh` → all green, 14s. Last run 14:05.
- **Decisions**: retries capped at 3 with a fixed 2s delay; chose fixed over exponential because the provider's status endpoint is cheap. Rationale in the PR description.
- **Next step**: `gh workflow run "Deploy Staging" --ref main`, then check `<STAGING_URL>/health` and the changed flow.
- **Open questions**: does the provider already deduplicate on its side? Settle it before raising the cap above 3.
- **Do not**: re-run migration `0042` by hand — it is not idempotent yet (tracked in issue #131).
```

Every field here answers a question the next person would otherwise have to ask: what changed, what is verified, why it was built that way, what happens next, what is unresolved, and what will hurt them. Note the honest last line — the fastest way to save someone an afternoon is to name the trap.

## Notes that survive

Three details decide whether a note is useful in a month:

- **Absolute paths and real commands.** `~/projects/<app>/backend` beats "the backend folder". Copy-pasteable beats descriptive.
- **Dates.** Environment variables, prices, endpoints and model versions change. "Verified 2026-05-02" tells the reader how much to trust the rest.
- **Links to the artefact.** The PR, the commit, the issue, the CI run. A note that points at the diff lets the next reader get the detail without you.

Avoid half-commands and mental shortcuts ("then the usual migration thing"). Whatever felt obvious while writing will be the exact place the next reader stops — including when that reader is an agent that has to guess.

![Doc map: the question in your head and the file that answers it](https://raw.githubusercontent.com/BongweKE/ai-coding-wiki/main/assets/11-docs-map.png)

## The five-minute habit

After any task that surprised you — a deploy that hung, a test that passed for the wrong reason, an error message that led nowhere — spend five minutes writing. Keep it under one screen. Choose the destination by audience:

- Someone repeating the operation → the runbook.
- Someone continuing the work → the hand-off note, in the repository, near the code or in the PR.
- A fact about the system → the doc that owns that fact.
- A lesson about how you learned it → the lesson bank.

The habit only holds if the cost is small. Five minutes, one artefact, no formatting ceremony.

## The wiki nobody reads

The classic failure is a beautiful knowledge base that nobody opens, because the information is not where the work happens. Put notes where the work happens: the runbook in the repository next to the pipeline file, the hand-off in the PR description or a `NOTES.md` in the branch, the gotcha in the gotchas file, the operational caveat as a comment beside the code it constrains. Then link from the doc map, so the person who does not know the file exists still finds it ([Docs as code](11-Docs-As-Code)).

A private wiki is where notes go to be forgotten. A file in the repository is reviewed, versioned, and readable by every future session.

## Try it

1. Pick an operation you have run fewer than five times. Write the runbook at `docs/runbooks/<name>.md` using the template above.
2. Follow your own runbook literally, from a clean shell. Fix every step where you improvised; add the expected output you actually saw.
3. End your next unfinished task with a hand-off note in the PR description, using all six fields.
4. Add a "Do not" line to one existing doc — the mistake you would warn a friend about.
5. Set a reminder for 30 days to re-read the hand-off and mark what was wrong. Fix the runbook from that.

## Common mistakes

- **A runbook without output** — steps only, so a hanging command and a successful one look identical. Fix: paste the expected line after each step that produces output.
- **Hand-off notes that narrate** — three paragraphs of what you tried, no state and no next step. Fix: the six fields, facts only, failed approaches mentioned only as traps to avoid.
- **Relative paths and "the usual"** — the note assumes a working directory you will not be in next month. Fix: absolute paths, full commands.
- **Notes outside the repository** — in chat, a personal file, a private wiki. Fix: move the durable part into the repo and link it from the doc map.
- **Writing it after the deadline** — the note gets skipped or written from memory. Fix: write the runbook during the learning, and the hand-off before you close the laptop.

## Key takeaways

- Runbooks: numbered steps, expected output, a failure section, and a "Do not" list.
- A hand-off note is six fields: state, gates, decisions, next step, open questions, traps.
- Notes survive on absolute paths, real commands, dates, and links to the diff.
- Five minutes after any task that surprised you; one artefact, no ceremony.
- Put the note where the work happens, then link it from the doc map.

## Further learning

- [Documentation per feature](11-Documentation-Per-Feature) — which document a change must update.
- [Rollbacks and incidents](07-Rollbacks-And-Incidents) — the operational section your runbook's failure path points at.
- [Environments and promotion](07-Environments-And-Promotion) — the pipeline a promotion runbook drives.
- [Agent memory and session hygiene](03-Agent-Memory-And-Session-Hygiene) — what to persist between sessions and what to discard.
