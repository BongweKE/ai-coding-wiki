> **Section 13 · Lesson 6** · Level: beginner · ~20 min · Prereq: [Issue-driven development](13-Issue-Driven-Development)

## Why this matters

You have read about issues, boards, review, ownership and cost. Reading is not practice. The five exercises below run the same habits you will use on real work, in a toy repository you can throw away. Do them in order; each one assumes the artifact from the one before it. Budget about two hours for the set, and keep a log: what you produced, and what you would change next time.

## Set up a toy project

Make something small enough to understand completely and big enough to be wrong: a package with a function that totals a list of items, a command-line entry point, a test folder, and a `README.md`. Add one deliberate flaw — an untested behaviour, or a function that silently returns a default on bad input. Commit the starting point so every diff has a clean baseline, and put the repo on GitHub, because half of these exercises need the issue tracker and the settings.

## Try it

Work the five exercises in order, and record three things for each: the artifact you produced, the exact prompt you sent to any agent, and what you would change next time. That log is the deliverable — the artifacts you keep are the ones you will reuse.

## Exercise 1: Five issues, one filed through a template

**Do:** Write five issues in a text file, each with problem, current behaviour, expected behaviour, and two to four acceptance criteria. Then add `.github/ISSUE_TEMPLATE/1-bug_report.yml` and a `config.yml` with `blank_issues_enabled: false`, and file one of the five through the form.

**Success criteria:** All five issues have testable criteria — a reader could write the test from the criteria alone. The filed issue arrived with every required field populated, and blank issues are off.

**A good answer looks like:** a criterion you could turn into an assertion without asking a question, for example "a second submit within five seconds returns 409 and creates no second record". If you had to explain one to yourself out loud, rewrite it.

## Exercise 2: Two-person review of an AI-written PR

**Do:** Give an agent one of the five issues and let it implement the change on a branch. Before you look at the diff, ask a second agent — fresh session, only the issue text and the diff — to report gaps against the criteria, ignoring style. Then review the diff yourself with the seven-question checklist.

**Success criteria:** You diffed the test files first and can name any assertion that moved. You wrote down which of the seven checks found something, how long the review took, and where your findings and the reviewer agent's disagreed.

**A good answer looks like:** a review that finds at least one real gap, and a note saying which agent finding you rejected as noise. If both reviews came back clean first time, ask the agent for a deliberately sloppy variant — weakened assertion, invented method, unused import — and review that instead.

## Exercise 3: CODEOWNERS and a PR template

**Do:** Add `.github/CODEOWNERS` with a default owner on `*` and a strict owner on `src/auth/`, `db/migrations/` and `.github/workflows/`. Enable "Require review from Code Owners". Then add `pull_request_template.md` with: what changed, how I tested this (with an evidence line), and scope.

**Success criteria:** A PR that touches only `.github/workflows/` cannot merge without the owner. Every new PR arrives with the template sections, and the "how I tested this" line contains a real command and its output.

**A good answer looks like:** a screenshot of the blocked merge button, and a template short enough that you actually fill it in.

## Exercise 4: Estimate the monthly cost, then measure it

**Do:** Take the feature from exercise 1 and model its monthly cost: tokens in and out per request (measure them), requests per user per month (state an assumption), and a cache hit rate you would defend. Compute cost at 10, 100 and 500 users. Then set a hard cap and a per-user quota on the account before you run anything further, and write one sentence saying what the product does at the cap.

**Success criteria:** You have a written estimate with its assumptions visible, a measured cost for at least three real requests, and a platform-enforced cap. The estimate and the measurement are in the same file, with the difference between them noted.

**A good answer looks like:** numbers you can explain, plus one recorded surprise — a probe that cost more than the model predicted, with the reason (a longer answer, a bigger retrieval context).

## Exercise 5: One board review

**Do:** Put your five issues on a board with Backlog, Todo, In progress, Blocked, In review and Done, set *In progress* to a limit of two, and attach the next three to a milestone called "v0.1". Then run a fifteen-minute review: every item gets advanced, re-scoped, blocked with a note, or closed.

**Success criteria:** After the review, no item is untouched and every closed item has a reason. The milestone view and the backlog view disagree on what is in scope — that is the point of having both.

**A good answer looks like:** at least one deleted issue, and one item you split because you could not describe it in one sentence.

## Common mistakes

- **Vague acceptance criteria** — "make the CLI nicer" cannot be reviewed or tested. If you cannot write the assertion, you have not specified the issue.
- **Reviewing your own diff with your own agent** — a second pass in the same session shares the first pass's blind spots. Use a fresh context, then review as the human.
- **Fixing the bad diff instead of reviewing it** — in exercise 2 the goal is to *find* the gaps; note the finding first, then fix it.
- **A CODEOWNERS file with no enforcement** — it reads like policy and behaves like a comment. Turn on required code-owner review.
- **Skipping the cap because the estimate looks small** — small estimates are exactly the ones that hide a retry loop. Set the ceiling first.
- **A board review that advances everything** — if nothing gets closed or re-scoped, you moved cards, you did not review work.
- **No log** — you cannot learn from a prompt or a decision you did not write down.

## Key takeaways

- An issue is only specified once its acceptance criteria can be turned into assertions.
- Two reviews beat one: a second agent in a fresh context for gaps, then a human against the criteria.
- Ownership is only real with enforcement on; a template only helps if it is short enough to fill in.
- Estimate cost from measured tokens and stated assumptions, cap it before you scale, and decide what happens at the cap.
- A board review is a set of decisions — advance, re-scope, block, close — not a card shuffle.
- Keep the log. The prompts and decisions you wrote down are the reusable part.

## Further learning

- [Best practices for Claude Code](https://www.anthropic.com/engineering/claude-code-best-practices) — the verification and adversarial-review patterns exercise 2 leans on.
- [Issue-driven development](13-Issue-Driven-Development) — the six-part issue shape these exercises assume.
- [Code review for AI code](13-Code-Review-For-AI-Code) — the seven-question checklist for exercise 2.
- [Token economics and budgets](13-Token-Economics-And-Budgets) — the modelling method for exercise 4.
- [Team ownership and CODEOWNERS](13-Team-Ownership-CODEOWNERS) — the routing table for exercise 3.
