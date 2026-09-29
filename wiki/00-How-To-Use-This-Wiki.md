> **Section 00 · Lesson 4** · Level: beginner · ~6 min · Prereq: none

## Why this matters

This wiki is 135 lessons. Read in order, it is a long march; read badly, it is entertainment. Five minutes here tells you which path to take, what a lesson page looks like, and the one rule that turns reading into skill.

## Four learning paths

You do not have to read everything. Pick the path that matches what you are trying to do, and follow it start to finish; the numbered lessons within a path are already in order.

**Just shipping.** You want one real thing online.

1. [Set up your workbench](00-Setup-Your-Workbench)
2. [How LLMs work for coders](01-How-LLMs-Work-For-Coders)
3. [Prompting fundamentals](02-Prompting-Fundamentals)
4. [The feature loop](03-The-Feature-Loop)
5. [Git essentials](05-Git-Essentials)
6. [Your first CI pipeline](05-Your-First-CI-Pipeline)
7. [Deploy on Railway](07-Deploy-On-Railway)
8. [Capstone 1: ship a tiny app](15-Capstone-1-Ship-A-Tiny-App)

**Professional engineering.** You want work that survives review, teammates and a bad Tuesday.

1. [Git essentials](05-Git-Essentials)
2. [Branching and pull requests](05-Branching-And-Pull-Requests)
3. [Checks that actually matter](05-Checks-That-Actually-Matter)
4. [Branch protection and required checks](05-Branch-Protection-And-Required-Checks)
5. [The test pyramid in practice](10-Test-Pyramid)
6. [Code review for AI code](13-Code-Review-For-AI-Code)
7. [Architecture decision records](06-Architecture-Decision-Records)
8. [Rules of operation: the full stack](12-Rules-Of-Operation-Overview)

**AI-product builder.** You want to build features where the model does the work, safely.

1. [How LLMs work for coders](01-How-LLMs-Work-For-Coders)
2. [Context engineering](02-Context-Engineering)
3. [What is MCP?](08-What-Is-MCP)
4. [Evaluating AI features](10-Evaluating-AI-Features)
5. [Token and cost discipline](03-Token-And-Cost-Discipline)
6. [OWASP LLM Top 10 in plain English](09-OWASP-LLM-Top-10)
7. [Prompt injection and exfiltration](09-Prompt-Injection-And-Exfiltration)
8. [Capstone 2: add an AI feature](15-Capstone-2-Add-An-AI-Feature)

**Team lead.** You are setting standards other people (and their agents) will follow.

1. [Rules of operation](12-Rules-Of-Operation-Overview)
2. [Writing SOPs](12-Writing-SOPs)
3. [Issue-driven development](13-Issue-Driven-Development)
4. [Team ownership and CODEOWNERS](13-Team-Ownership-CODEOWNERS)
5. [Human accountability](09-Human-Accountability)
6. [Token economics and budgets](13-Token-Economics-And-Budgets)
7. [Managing a skill library](04-Managing-A-Skill-Library)
8. [Case study synthesis: the patterns that repeat](14-Case-Study-Synthesis)

## How a lesson page is shaped

Every page follows the same skeleton, so you always know where to look:

- **The metadata line** at the top: section, lesson number, level, reading time and prerequisites. If you have not done the prerequisite, do it first — the lesson will assume it.
- **Why this matters** — the concrete pain the lesson removes.
- **The body** — two to five sections, with commands, code and diagrams.
- **Try it** — numbered, runnable steps. This is the lesson.
- **Common mistakes** — real failures, not hypotheticals.
- **Key takeaways** — rules you can act on.
- **Further learning** — links and the next page.

Do the exercises properly: run every command yourself, read the error messages before searching for them, and change one thing to break it on purpose. A command you did not run is a fact you did not learn. If you are short on time, do step one of *Try it* rather than skipping it entirely.

## Never read two lessons without running one command

This is the rule the whole book is built around. Reading produces recognition; running produces evidence. Recognition feels like knowing and evaporates in a week. Evidence — a repository that exists, a test you saw fail then pass, an error you fixed — is what you actually keep.

Practically: after each lesson, before opening the next, run at least one command from it and look at the output. If it worked, note what you saw. If it failed, you have just had the more valuable lesson. This is also how agents are evaluated in this book: a claim without a run behind it is a guess.

## Contributing, and why the repo and the wiki are the same content

The wiki pages are generated from the markdown files in the repository. That means a typo you fix on a wiki page is a change to a markdown file, and every improvement travels as an ordinary pull request with an ordinary review. Nothing is published only in a web editor.

So if a page is wrong, unclear, or missing the exact thing that blocked you, fix it: open an issue or send a pull request. You will be using the same branch, commit and review loop this wiki teaches, which is a fitting first contribution. See [Contributing to this wiki](15-Contributing-To-This-Wiki).

## Try it

1. Choose one path above and write it at the top of a notes file, with today's date.
2. Open the first lesson in that path and run its first command within ten minutes of starting.
3. Do one full *Try it* exercise and paste the real output into your notes file. Not a summary — the output.
4. Break something small on purpose (delete the README, run the test with a wrong argument) and read the error without searching for it first.
5. Find one sentence in this section you think is unclear, and open an issue about it. That is your first contribution.

## Common mistakes

- **Reading paths like a book list** — finishing four lessons in an evening with no repository to show for it.
- **Skipping Section 00** — then hitting a lesson that assumes you have git, `gh` and a runtime installed.
- **Pasting commands you do not read** — you get the output but not the model of what happened, which is the actual lesson.
- **Treating *Try it* as optional** — it is the part the rest of the page exists to set up.
- **Doing every exercise perfectly** — break things deliberately; a command that fails teaches the failure mode you will meet for real.
- **Not keeping notes** — six months later the difference between "I read about migrations" and "I ran a migration" is a note file with output in it.

## Key takeaways

- Pick one of the four paths and finish it before browsing.
- Every page has the same skeleton: metadata, why it matters, body, try it, mistakes, takeaways, further learning.
- Never read two lessons without running one command.
- Keep one notes file with dates and real command output.
- The wiki and the repo are the same markdown. Fix what blocks you and open a pull request.
- Prerequisites are real; the metadata line tells you what you need.

## Further learning

- [Contributing to this wiki](15-Contributing-To-This-Wiki) — how to fix a page or propose one, using the branch and PR loop.
- [The 30-day learning plan](15-30-Day-Learning-Plan) — the just-shipping path spread over a month with checkpoints.
- [Further learning](15-Further-Learning) — where to go after this wiki ends.
- [Capstone 1: ship a tiny app](15-Capstone-1-Ship-A-Tiny-App) — the first end-to-end project, if you want to start at the end and work backwards.
