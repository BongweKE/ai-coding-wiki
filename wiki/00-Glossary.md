> **Section 00 · Lesson 5** · Level: beginner · ~8 min · Prereq: none

## Why this matters

Most friction beginners hit is vocabulary, not difficulty. A term you half-know makes a whole page unreadable. Skim this once, then return whenever a lesson uses a word you cannot define out loud.

## How to use it

Each entry is one line: what it is, and where it is explained properly.

## A to Z

- **ADR (architecture decision record)** — a dated file recording one design decision and why. See [Architecture decision records](06-Architecture-Decision-Records).
- **AGENTS.md** — a rules file read by several agent tools at session start. See [AGENTS.md that works](12-AGENTS-md-That-Works).
- **Agent** — a model with tools in a loop, choosing its own steps. See [The agent loop](01-The-Agent-Loop).
- **API** — a defined way for one program to call another over HTTP. See [API design basics](06-API-Design-Basics).
- **Artifact** — a file a build produces: a bundle, an image, a report. See [Object storage and artifacts](07-Object-Storage-And-Artifacts).
- **Blast radius** — the worst thing that can happen if this action is wrong. See [Threat-modeling](09-Threat-Modeling-Your-Workflow).
- **Branch** — a named line of commits, letting you work without touching `main`. See [Branching and pull requests](05-Branching-And-Pull-Requests).
- **Branch protection** — rules blocking merges until checks pass and reviews happen. See [Branch protection](05-Branch-Protection-And-Required-Checks).
- **CD (continuous delivery)** — automatically getting merged code onto a server. See [Deployment pipelines](05-Deployment-Pipelines).
- **Checks** — automated jobs (tests, linters, builds) that must pass on a pull request. See [Checks that actually matter](05-Checks-That-Actually-Matter).
- **CI (continuous integration)** — a service running your checks on every push, before review. See [Your first CI pipeline](05-Your-First-CI-Pipeline).
- **Commit** — a saved snapshot of your files with a message and hash. See [Git essentials](05-Git-Essentials).
- **Context engineering** — deciding what goes in the context window, and what stays out. See [Context engineering](02-Context-Engineering).
- **Context window** — every token one conversation can hold, including files and command output. See [A taxonomy of context](01-Taxonomy-Of-Context).
- **Coverage** — the share of your code the tests actually execute. See [The test pyramid](10-Test-Pyramid).
- **Determinism** — same input, same result, every time. Tests and hooks are deterministic; prompts are not. See [Hooks and guardrails](03-Hooks-And-Guardrails).
- **Diff** — the line-by-line difference between two versions of code. See [Keeping diffs small](03-Keeping-Diffs-Small).
- **Embedding** — numbers representing meaning, used to find similar text. See [A taxonomy of context](01-Taxonomy-Of-Context).
- **Environment variable** — a value the shell passes to a program; the safe home for keys. See [Secrets hygiene](09-Secrets-Hygiene).
- **Eval** — a repeatable, scored test of model output quality rather than a pass/fail test. See [Evaluating AI features](10-Evaluating-AI-Features).
- **Gate** — a checkpoint that stops progress unless a condition is met. See [Branch protection](05-Branch-Protection-And-Required-Checks).
- **Hallucination** — a confident, fluent, wrong statement, such as a package that does not exist. See [Supply chain security](09-Supply-Chain-Security).
- **Harness** — the program around a model: tools, permissions, rules and stopping conditions. See [The AI coding landscape](00-The-AI-Coding-Landscape).
- **Hook** — a script a harness runs at a fixed point, with no exceptions. See [Hooks and guardrails](03-Hooks-And-Guardrails).
- **Idempotency** — running the same operation twice has the same effect as running it once. See [Reliability patterns](06-Reliability-Patterns).
- **Idempotency key** — a unique id on a request so a retry cannot charge twice. See [API design basics](06-API-Design-Basics).
- **LLM (large language model)** — a text model trained to predict the next token. See [How LLMs work for coders](01-How-LLMs-Work-For-Coders).
- **Main** — the default branch; the version everyone treats as current. See [Git essentials](05-Git-Essentials).
- **MCP (Model Context Protocol)** — an open standard connecting agents to outside tools and data. See [What is MCP?](08-What-Is-MCP).
- **Migration** — a versioned change to a database schema, applied in order. See [Postgres on Neon](07-Postgres-On-Neon).
- **Model** — the trained system turning text in into text out; no memory between calls. See [Choosing a model](01-Choosing-Models).
- **Monorepo** — one repository holding several apps and packages. See [Thinking in boundaries](06-Thinking-In-Boundaries).
- **Plan mode** — an agent mode where it may read and propose but not change files. See [Plan mode and spec-driven development](03-Plan-Mode-And-Spec-Driven-Development).
- **PR (pull request)** — a proposal to merge one branch into another, with a diff and discussion. See [Branching and PRs](05-Branching-And-Pull-Requests).
- **Prompt** — everything you send the model: instructions, files, examples, error output. See [Prompting fundamentals](02-Prompting-Fundamentals).
- **Prompt injection** — hostile instructions hidden in content the agent reads, such as a web page. See [Prompt injection and exfiltration](09-Prompt-Injection-And-Exfiltration).
- **RAG (retrieval-augmented generation)** — fetching relevant text first, then answering from it. See [Evaluating AI features](10-Evaluating-AI-Features).
- **RLS (row-level security)** — database rules filtering which rows a user may read or write. See [Postgres on Neon](07-Postgres-On-Neon).
- **Rollback** — going back to the previous working version, deliberately and quickly. See [Rollbacks and incidents](07-Rollbacks-And-Incidents).
- **Rules file** — the markdown file an agent reads at session start with your conventions. See [Rules files](02-Rules-Files-AGENTS-and-CLAUDE-md).
- **Runner** — the machine (often GitHub-hosted) executing your CI jobs. See [Your first CI pipeline](05-Your-First-CI-Pipeline).
- **Sandbox** — OS-level isolation restricting what files and networks a process reaches. See [Threat-modeling your workflow](09-Threat-Modeling-Your-Workflow).
- **Secret** — any credential granting access: API keys, tokens, database passwords. See [Secrets hygiene](09-Secrets-Hygiene).
- **Serverless** — running code on managed infrastructure that scales to zero between requests. See [Edge with Cloudflare Workers](07-Edge-With-Cloudflare-Workers).
- **Skill** — a folder with a `SKILL.md` teaching an agent a procedure on demand. See [What are agent skills?](04-What-Are-Agent-Skills).
- **Smoke test** — a few fast checks that the app starts and the main path works. See [Smoke tests](10-Integration-And-Smoke-Tests).
- **SOP (standard operating procedure)** — a written, repeatable procedure for a recurring task. See [Writing SOPs](12-Writing-SOPs).
- **Staging** — an environment mirroring production closely enough to test a release. See [Environments and promotion](07-Environments-And-Promotion).
- **Token** — the unit models read and bill by, roughly three-quarters of a word. See [Token and cost discipline](03-Token-And-Cost-Discipline).
- **Tool call** — the model requesting an action and receiving the result. See [The agent loop](01-The-Agent-Loop).
- **Trunk** — the main development line everyone merges into frequently. See [Branching and pull requests](05-Branching-And-Pull-Requests).
- **Vector** — an embedding treated as a point in space, so distance means similarity. See [A taxonomy of context](01-Taxonomy-Of-Context).
- **Workflow** — steps orchestrated through paths you wrote, versus steps an agent picks. See [The AI coding landscape](00-The-AI-Coding-Landscape).
- **YAML** — the indentation-based format used for CI config; indentation errors break it. See [Writing GitHub Actions](05-Writing-GitHub-Actions).

## Try it

1. Pick five terms you could not define out loud before reading. Write your own definition for each in one sentence, without looking.
2. Compare yours with the entry above. Where they differ is your actual gap.
3. Follow the "see also" link for the two terms that matter most to what you are building this week.

## Common mistakes

- **Assuming `main` is a backup** — it is the shared current version; rewriting it destroys other people's work.
- **Reading "idempotency" as "retry-safe" and stopping there** — the server must detect the duplicate, which usually needs an idempotency key.
- **Treating hallucination as random noise** — it is fluent and confident, so it looks exactly like a correct answer. Only a run tells them apart.
- **Confusing CI and CD** — CI verifies the code; CD puts it where people use it. A green CI is not a working deployment.
- **Using "agent" for autocomplete** — the distinction changes what you must review.

## Key takeaways

- Vocabulary is the cheapest thing to fix and the most common blocker.
- Each entry is one line plus a link; the link is the real content.
- CI verifies, CD deploys, and a gate only exists if something blocks on it.
- Hallucination and prompt injection are the words to look up before letting an agent install anything.
- Hooks are deterministic; prompts and rules files are advisory.

## Further learning

- [What is MCP?](08-What-Is-MCP) — the protocol behind most "connect this tool to my agent" questions.
- [How LLMs work for coders](01-How-LLMs-Work-For-Coders) — tokens, context and why the model forgets.
- [OWASP LLM Top 10 in plain English](09-OWASP-LLM-Top-10) — the named security risks without the jargon.
- [Model Context Protocol specification](https://modelcontextprotocol.io/specification/2025-06-18) — the authoritative definition of MCP architecture, transports and features.
