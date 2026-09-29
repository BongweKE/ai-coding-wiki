> **Section 10 · Lesson 7** · Level: intermediate · ~25 min · Prereq: [Definition of done](10-Definition-Of-Done)

## Why this matters

Reading about verification does not build the reflex. These four exercises do. You write a suite small enough to finish in an hour, then deliberately break the code to prove the suite bites. You build an eval with a threshold. You smoke a deployed environment. You bisect a regression to one commit. Two hours, four artefacts you keep and reuse.

## Exercise 1 — The smallest suite that catches a real bug

Build a toy repo with one function and one route: the function computes a fee (`amount * rate`, rounded to two decimals) and the route stores a fee and returns it. Then write:

- one unit test for rounding at a boundary — pick an amount that lands on a half-cent;
- one integration test that stores the row and reads it back;
- one test for an invalid input, such as a negative amount or a missing currency.

Now break the code three ways, one at a time, restoring it after each, and confirm the suite fails every time:

1. Change the rounding to truncate instead of round.
2. Return the fee from memory instead of reading the stored row back.
3. Remove the input validation, so a negative amount is accepted.

If any break passes silently, the suite has a hole. Fix the hole, not the break.

## Exercise 2 — A 20-example eval with a threshold

Pick one small AI feature you can run locally: a summariser, an answer bot over five documents, or a classifier driven by a prompt. Build `evals/cases.jsonl` with twenty real inputs:

```jsonl
{"id":"c01","input":"how do I export my data?","expected":"Settings then Export","must_cite":"help-export"}
```

Write `evals/run.py` that calls the feature, scores each case (exact match, containment, or a judge against a short fixed rubric) and prints per-case results plus an average. Then:

1. Run it once and record the score as your baseline.
2. Set the threshold slightly below the baseline, so ordinary variation does not fail the run.
3. Add three canary cases whose answer and required source you know exactly.
4. Change one prompt instruction, re-run, and confirm the score moves in the direction you expected. If it does not move at all, your scorer measures nothing — fix the scorer before trusting the feature.

## Exercise 3 — A smoke test for a deployed environment

Take any service you have deployed (a free tier is fine). Write `smoke.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
BASE="${BASE_URL:?set BASE_URL}"
curl -fsS "$BASE/health" | grep -q '"status":"ok"'
TOKEN=$(curl -fsS -X POST "$BASE/auth/login" \
  -H 'content-type: application/json' \
  -d "{\"email\":\"$SMOKE_EMAIL\",\"password\":\"$SMOKE_PASSWORD\"}" | jq -r .token)
curl -fsS "$BASE/orders" -H "authorization: Bearer $TOKEN" | jq -e 'length >= 1' >/dev/null
echo "smoke ok"
```

Never hardcode credentials: pass them from your CI secret store and use a dedicated read-only smoke account. Run the script after a deploy and print the elapsed time. If it takes more than a minute, cut cases until it does not. Then add one canary assertion — a call whose answer you already know, for example that the seeded account returns exactly one order.

## Exercise 4 — Bisect a bug to the exact commit

In a repo with real history, plant a regression (or find one), then:

```bash
git bisect start
git bisect bad HEAD
git bisect good "$(git rev-list --max-count=1 --before='30 days ago' HEAD)"
git bisect run ./scripts/repro.sh
git bisect reset
```

`repro.sh` exits non-zero while the bug is present. Record three things: the culprit commit hash, its diff, and the test that would have caught it. Add that test. The commit is a curiosity; the missing test is the lesson.

## Try it

Run the four exercises in order and keep what each one produces:

1. The test suite, plus a note listing the three breaks it caught.
2. `evals/cases.jsonl` and the run script, with the baseline score and threshold written down.
3. `smoke.sh`, with a timing line in its output.
4. A bisect log: bad commit, good commit, culprit commit, and the guard test you added.

Grade yourself with one question per exercise: can a stranger re-run your artefact and get the same result from the README alone? If not, the artefact is not finished.

## Common mistakes

- **Writing tests after deciding the code is correct.** You will write tests that agree with the bug. Write the test from the requirement, then break the code to check that it bites.
- **An eval whose scorer you never sanity-checked.** Feed it an obviously wrong answer. If the score stays high, the scorer is broken.
- **A smoke test a human has to interpret.** Print a verdict and exit non-zero on failure, or nothing will ever run it.
- **Hardcoded smoke credentials.** Use CI secrets and a dedicated account. A password in a repository is a leaked password.
- **Bisecting with a flaky repro.** A script that passes one time in five sends you to a random commit. Make it deterministic first.
- **Deleting the artefact once the exercise is done.** The suite, the eval and the smoke test are the deliverable, not the lesson.
- **Raising the threshold instead of fixing the feature.** A threshold you lower whenever it fails is a decoration.

## Key takeaways

- A suite you have never seen fail is a suite you do not trust. Break the code on purpose.
- An eval needs a baseline, a threshold and at least one canary case before it counts as a gate.
- A smoke test is health, one critical flow and one canary — under a minute, safe to run on every deploy.
- Bisect beats guessing: about ten steps for a thousand commits, and it names the missing test.
- Keep the artefacts. They are the beginning of your real suite.

## Further learning

- [Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) — datasets, scorers and iteration in detail.
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/) — the risks your eval cases should include.
- [The test pyramid in practice](10-Test-Pyramid) — which layer a new test belongs in.
- [Railway Docs](https://docs.railway.com/) — a place to deploy the service you smoke test.
