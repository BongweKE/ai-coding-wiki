> **Section 07 · Lesson 10** · Level: intermediate · ~25 min · Prereq: [Local to cloud walkthrough](07-Local-To-Cloud-Walkthrough)

## Why this matters

You can read about rollback for an hour and still freeze the first time production breaks. The knowledge that helps under pressure is the kind you have already used with your hands. These five exercises are deliberately small and deliberately unpleasant: you break a working deploy three ways, recover it twice, and finish by writing the runbook you would have wanted on day one. Do them on a throwaway project — never on anything real.

## Exercise 1 — break it three ways, fix it from logs alone

Deploy the toy API from the walkthrough. Then break it, once per symptom, reading **only** logs and the response body — no code changes until you have written down the cause.

**1a. A bad environment variable.** Set `DATABASE_URL` to a value with one character changed.

```bash
railway variable set DATABASE_URL="postgres://...wrong" --service hello-cloud --skip-deploys
railway redeploy --service hello-cloud
curl -s https://<your-host>/health      # {"status":"degraded","db":"unreachable"}
curl -s https://<your-host>/greetings   # 500
```

Write down: which log line told you it was the credential rather than the network, and how you knew the process was alive. Fix it, then confirm both endpoints.

**1b. A missing migration.** Add a route that reads a column which does not exist yet, deploy it *without* running the migration, and capture the exact database error code the API returns. Then run the migration and re-check without redeploying.

```bash
psql "$DATABASE_URL" -f infra/migrations/0002_add_greeting_lang.sql
curl -s https://<your-host>/greetings
```

Write down which layer reported the failure, and how staging would have caught it.

**1c. The wrong port.** Hard-code the listen port to `3000` and deploy.

```bash
curl -sS -m 5 https://<your-host>/health
# curl: (28) Operation timed out   (or a platform 502 page)
```

The build succeeded and the process is running; nothing answers the probe. Fix it to read `process.env.PORT || 8080`, redeploy, and note how differently this failure presented from 1a.

**Acceptance:** three written entries, each with symptom, the one log line or response that identified it, and the fix. Under 100 words each.

## Exercise 2 — a rollback against the clock

1. Note the current working state: `curl -s https://<your-host>/health`.
2. Deploy a change that visibly breaks one route.
3. Roll back with the *lowest* level that works: a feature flag, then a redeploy of the previous artefact.
4. Time it from "I noticed" to "the symptom is gone". Write the number down.
5. Repeat once, aiming to beat your own time by removing one step from the path.

**Acceptance:** both times recorded, plus one sentence naming the step you removed.

## Exercise 3 — restore a database into a branch

Never restore in place the first time you do this. Restore into a branch, verify, then decide.

1. Take a restore point or snapshot of the production branch.
2. Insert a distinctive row *after* the point.
3. Create a branch from that restore point.
4. Connect to the branch and prove two things: an older table state is visible, and the distinctive row is absent.
5. Run your migration runner against the branch and confirm it applies cleanly.
6. Write the drill into your runbook, then delete the branch.

**Acceptance:** a pasted command transcript, plus the sentence you would say to a colleague explaining what a restore would lose.

## Exercise 4 — budget alert and the cost of 100 requests

1. Set a spend limit and a 50% alert on the account you are using. Screenshot the setting for your own records.
2. Fire 100 requests at the deployed API:

   ```bash
   for i in $(seq 1 100); do curl -s -o /dev/null https://<your-host>/greetings; done
   ```

3. Open the platform's usage page and compute cost per 100 requests. Convert it to cost per 1,000 and per 100,000.
4. Do the same for one AI call: record tokens and cost per request, not a monthly total.
5. Add both numbers, with today's date, to `docs/cost.md`.

**Acceptance:** two per-request figures with dates, and the monthly cost extrapolated at 10× your current traffic.

## Exercise 5 — write the runbook you wish you had on day one

One page, four sections, all commands real:

```markdown
# Runbook: hello-cloud

## Deploy
- staging: merge to main (auto)
- production: dispatch "Promote" workflow; approvers: <names>

## Verify
- curl -fsS https://<staging-host>/health
- log in, load /greetings, confirm the new row appears

## Roll back
- flag: <name> (off = previous path)
- code: railway redeploy --service hello-cloud
- data: restore into a new branch; never in place without a second person

## When something breaks
- stop the bleeding, post an update every 15 minutes, keep a timeline
- after: one checkable change in the post-mortem
```

**Acceptance:** somebody who has never deployed this project follows it and deploys without asking you a question. If they ask one, the runbook has a gap — fix the gap, not the person.

## Try it

1. Run Exercise 1 first — it teaches the failure signatures the later exercises assume.
2. Do Exercises 2 and 3 against a throwaway project and a database branch, never production data.
3. Keep `docs/deploy-log.md` open and paste each command with its output straight after you run it.
4. Finish with Exercise 5, then hand the runbook to somebody who has never deployed this project.

## Common mistakes

- **Doing this on production data.** Use a throwaway project and a database branch. A restore drill that deletes real rows is not a drill.
- **Fixing 1a by adding a fallback value in code.** You have hidden the next occurrence instead of handling it.
- **Skipping the timing in Exercise 2.** A rollback you have never timed is a hope with a plan attached.
- **Restoring in place on the first attempt.** You lose every write since the snapshot and create a reconciliation job.
- **Confusing a rollback with a data restore.** Old code and a new schema usually work; old code and a restored schema may not.
- **Writing a runbook with placeholder commands.** Untested commands fail exactly when they are needed.

## Key takeaways

- Three failure signatures to recognise by sight: refused credentials (503 on health, process alive), missing schema (500 from the API), unprobed port (nothing answers).
- Practise rollback until the number is a fact you know, not an estimate.
- Restore into a branch, verify, decide — never in place, never alone.
- Know your per-request cost; that is the number that scales, not the monthly total.
- A runbook is finished when a second person can deploy from it without asking you anything.

## Further learning

- [Deploying with the CLI](https://docs.railway.com/cli/deploying) — redeploy and log commands used in every exercise.
- [Neon documentation](https://neon.com/docs/introduction) — branching and restore points for Exercise 3.
- [GitHub Actions documentation](https://docs.github.com/en/actions) — the promotion workflow the runbook dispatches.
- [Railway and Neon cheat sheet](16-Railway-And-Neon-Cheat-Sheet) — commands to paste into the runbook.
- [Rollbacks and incidents](07-Rollbacks-And-Incidents) — the theory these exercises make physical.
