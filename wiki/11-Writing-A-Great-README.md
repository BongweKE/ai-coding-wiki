> **Section 11 · Lesson 2** · Level: beginner · ~12 min · Prereq: [Docs as code](11-Docs-As-Code)

## Why this matters

The README is the only document every visitor reads, human or agent, before deciding whether your project is worth their time. A reader who cannot answer "what is this, and can I run it" within two minutes leaves. A cheap README is also the highest-leverage file in the repository: an agent that reads it starts with correct commands instead of guessing your test runner.

## The first screen

Design the part visible without scrolling. It carries four things and nothing else:

1. **What it is** — one sentence, concrete nouns. "A CLI that turns a folder of CSV exports into a Postgres schema and loader." Not "a next-generation data platform".
2. **Who it is for** — the reader who should stay, and the reader who should leave.
3. **Why it exists** — the problem, in one sentence. If your system replaces a manual process, say what the manual process cost.
4. **One command that shows it working** — the smallest end-to-end path. Not install-and-configure-then-pray; one command with visible output.

```text
# orderbook-sync

Copies order data from a local export folder into Postgres, idempotently.
For developers who already have Postgres running; not for production payment data.

    docker compose up -d db && ./run.sh --dry-run

Expected: "12 files scanned, 340 rows staged, 0 written (dry run)".
```

That block is a whole specification. A reader knows in five seconds whether the tool is for them, and can copy one line.

## Setup that works on a clean machine

Your machine is contaminated: shells with old exports set, a database from last month, a language version you keep forgetting you upgraded. The section that matters is the one that runs on a fresh clone — a new laptop, a container, a colleague's desktop.

Write it as numbered steps with the expected output after each command, and test it by deleting your checkout and following your own text literally. Include the boring prerequisites (runtime version, database, environment variables) and say how to check each one:

```bash
node --version            # expect v22.x or newer
psql --version            # expect 16.x
cp .env.example .env      # then fill DATABASE_URL; keys never go in the repo
```

Two rules keep this section honest. First, no secrets and no real credentials — placeholders and `os.environ["DATABASE_URL"]` only. Second, if a step needs a service you cannot share, say how to fake it (a docker-compose service, a fixture, a stub) rather than leaving the reader stuck.

## Where to go next

Close the README with a small map so depth is reachable without being mandatory. Link the wiki pages and repository docs by name and purpose: architecture, conventions, deployment, contributing. Four links, one clause each. Everything a first-time reader does not need at 11pm belongs behind a link, not in the README body.

![Doc map: the question in your head and the file that answers it](https://raw.githubusercontent.com/BongweKE/ai-coding-wiki/main/assets/11-docs-map.png)

## Status honesty

State plainly what is finished. A short line near the top is enough: "Used in production by one team since March; billing is a prototype; multi-tenant isolation is not implemented." Readers plan around what you tell them. Overclaiming costs you a bug report you will not enjoy, and it costs an agent real damage — it will assume handlers exist because the README implies they do. Pair each caveat with the risk in one clause, and put the date on the assessment so it can age visibly.

## The README is an onboarding test

Set a target: a new contributor, given repository access and nothing else, should reach a working local run and one green test within an hour. Every minute past that is a README bug, not a contributor bug. The cheap way to find those bugs is to watch someone do it — or to run a fresh agent session with only the repository and see where it stalls and what it invents. Every invented command is a missing line in your README.

## Try it

1. Clone your project into a fresh directory (`git clone <url> /tmp/fresh && cd /tmp/fresh`) and delete any local config.
2. Time yourself following only the README until the app runs. Write down the minute where you had to guess.
3. Fix the README at that exact line: add the missing command or the expected output.
4. Add a "Status" section with today's date and one honest sentence per unfinished area.
5. Give the repository to an agent session with the prompt `Follow the README and get the app running. Stop and tell me at the first step that fails.` Fix what it reports.

## Common mistakes

- **The untested setup section** — written once on a machine full of old state, so it omits a prerequisite or a version bump. Fix: follow it literally on a fresh clone every time you touch dependencies.
- **A command list with no expected output** — the reader cannot tell success from silence. Fix: paste the line you expect to see, including an obviously fake error example if the error path matters.
- **Marketing prose in the first screen** — three paragraphs of vision before the run command. Fix: nouns, one sentence, one command; move the vision to the bottom or delete it.
- **A README that hides the rough edges** — no status, so an agent builds on an unfinished path. Fix: say what is a prototype, in the same breath as what works.
- **Stale installation steps after a tooling change** — the README still tells people to install a package manager you dropped. Fix: make the README part of the definition of done for dependency and setup changes ([Definition of done](10-Definition-Of-Done)).

## Key takeaways

- The first screen answers: what, who for, why, and one command that works.
- Test the setup section on a clean clone, with expected output after every command.
- Never put secrets in a README; placeholders and environment variables only.
- State maturity explicitly, with a date, so nobody plans on a prototype.
- Target an hour from clone to green test; every stalled minute is a README bug.

## Further learning

- [Best practices for Claude Code](https://www.anthropic.com/engineering/claude-code-best-practices) — why a short, accurate project file changes agent behaviour.
- [Docs as code](11-Docs-As-Code) — the doc map and single-source-of-truth rules this page assumes.
- [Writing for future you](11-Writing-For-Future-You) — the same honesty and specificity, applied to notes and runbooks.
- [Documentation per feature](11-Documentation-Per-Feature) — deciding which doc a change must update.
