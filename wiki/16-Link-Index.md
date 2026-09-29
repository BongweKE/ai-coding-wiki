> **Section 16 · Lesson 6** · Level: beginner · ~10 min · Prereq: none (start here)

## Why this matters

Every external source this wiki cites is on this page, grouped by topic, with a sentence on what it actually covers. It exists so you can stop trusting a search result and start trusting a source someone has read.

This is also the page that keeps the rest of the wiki honest. A handbook of 135 lessons written over months accumulates links, and links rot. An index that names every one of them is the only place where a broken link is visible in one pass instead of surfacing in the middle of a lesson.

## How to read it

The index is grouped by topic, and inside each group **official documentation comes first, then repositories and papers, then articles and courses**. If you are new to a topic, read the documentation entry at the top of the group; it is the one written by the people who build the thing. The rest is interpretation.

One rule applies everywhere in this wiki: **a deep link you have not opened is a bug**. When a source has no page that covers the exact point, the index points at the documentation root and tells you what to search for, because a root always resolves and a guessed path does not.

## How this index is maintained

The index is maintained by hand and checked by machine:

1. Every time a lesson adds an external source, the source is added here with a one-line description, in the same pull request.
2. A link check runs as part of the release process. A scheduled job fetches every URL on this page, reports the ones that fail, and the release notes say how many were checked.
3. A failed link is replaced, not deleted: follow it to the surviving page, or step back to the documentation root so the reader can search.
4. Descriptions are re-read when a link changes. A stale description is almost as bad as a dead link, because it makes the reader trust the wrong source.

The honest caveat: **this field moves fast and links rot.** Behaviour, free tiers, model names, spec versions and file paths all change, and a page that was accurate when it was written can be wrong a quarter later. Treat this index as a starting point, not a guarantee — and when something here contradicts the source, the source wins. Anything numeric in this wiki is marked with the date it was true, or it is omitted.

## Agent engineering and prompting

| Source | What it covers | Who it is for |
|---|---|---|
| [Anthropic engineering](https://www.anthropic.com/engineering) | The index of Anthropic's engineering posts on context, agents and tooling. Start here when a topic in this wiki points at "the engineering blog". | Anyone who wants the primary source behind the agent advice in Sections 01–03. |
| [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | The architecture patterns behind agent systems: workflows versus agents, when a loop is worth the cost. | Readers designing their own agent, not just driving one. |
| [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | What belongs in the context window, what to retrieve on demand, and how compaction changes behaviour. | Anyone whose agent loses the plot in long sessions. |
| [Best practices for Claude Code](https://www.anthropic.com/engineering/claude-code-best-practices) | Practical agent-driving habits, including what belongs in a rules file and what does not. | The reader writing their first `AGENTS.md`. |
| [Create custom subagents](https://code.claude.com/docs/en/sub-agents) | The product documentation for defining subagents, their tools and their instructions. | Section 03 readers splitting work across parallel agents. |
| [Steering agents: rules, skills, hooks and subagents](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more) | Which mechanism to use for which kind of rule — always-on, on-demand, deterministic. | Anyone unsure whether a rule belongs in a file, a skill or a hook. |

## Skills

| Source | What it covers | Who it is for |
|---|---|---|
| [Agent Skills](https://agentskills.io/) | The open standard: what a skill is, the folder layout, and the ports across tools. | The starting point for Section 04. |
| [Agent Skills overview](https://agentskills.io/home) | The same standard's overview page, with the canonical explanation of progressive disclosure. | Readers who want one page to send a colleague. |
| [Agent Skills on the Claude platform](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) | Vendor documentation for installing, bundling and scoping skills. | Anyone shipping a skill into a real agent. |
| [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) | The design rationale: metadata first, body second, bundled files only when needed, plus security notes on untrusted skills. | The reader writing a `SKILL.md` who wants the why. |
| [anthropics/skills](https://github.com/anthropics/skills) | Real skills you can read as examples, including document-handling ones. | Copying a structure that already works. |
| [Hermes Agent documentation](https://hermes-agent.nousresearch.com/docs) | Documentation for the agent runtime used in this wiki's skill lessons: configuration, skills, plugins. | Readers following [Creating skills with Hermes](12-Creating-Skills-With-Hermes). |

## Spec-driven development

| Source | What it covers | Who it is for |
|---|---|---|
| [Spec-driven development with AI: get started with a toolkit](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/) | GitHub's own introduction to writing a spec before code and wiring it to an agent workflow. | The reader starting Section 03's plan-mode lesson. |
| [Understanding spec-driven development: Kiro, spec-kit and Tessl](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) | A comparison of three tools and the different assumptions each makes about where the spec lives. | Anyone choosing a workflow rather than inventing one. |

## System design and architecture

| Source | What it covers | Who it is for |
|---|---|---|
| [Spec-driven development: from code to contract](https://arxiv.org/html/2602.00180v1) | A paper arguing that the durable artefact of agent-written software is the contract between components, not the code. | Readers who want the design theory behind Section 06's boundary lessons. |

## CI/CD and GitHub Actions

| Source | What it covers | Who it is for |
|---|---|---|
| [GitHub Docs](https://docs.github.com/) | The documentation root for everything GitHub, including search that beats guessing a URL. | Every Section 05 and 13 reader. |
| [GitHub Actions docs](https://docs.github.com/en/actions) | The Actions section root: workflows, runners, caching, artifacts. | The first workflow you write. |
| [Workflow syntax for GitHub Actions](https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions) | The reference for every key in a workflow file, including `permissions`, `timeout-minutes` and `continue-on-error`. | Debugging a workflow that will not run. |
| [Workflows](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows) | The conceptual model: what a workflow is, how jobs and steps relate, how triggers fire. | Readers who have copied YAML without knowing what it does. |
| [Workflow commands for GitHub Actions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands) | The `::error::` and `::warning::` lines that become annotations on a pull request, plus masking. | Making a failure legible to a reviewer. |
| [Secure use reference for GitHub Actions](https://docs.github.com/en/actions/reference/security/secure-use) | Pinning actions to a commit SHA, least-privilege tokens, and the risks of privileged triggers. | Anyone reviewing a third-party action. |
| [GitHub Actions policy now supports blocking and SHA pinning](https://github.blog/changelog/2025-08-15-github-actions-policy-now-supports-blocking-and-sha-pinning-actions/) | The changelog entry for repository and organisation policies that enforce SHA pinning. | Teams enforcing the habit rather than recommending it (as of 2025). |
| [Pinning GitHub Actions for enhanced security](https://www.stepsecurity.io/blog/pinning-github-actions-for-enhanced-security-a-complete-guide) | A vendor walkthrough of why a tag can move and how to pin and keep pins current. | Readers who want the mechanics after the official reference. |

## Deployment platforms

| Source | What it covers | Who it is for |
|---|---|---|
| [Railway docs](https://docs.railway.com/) | The root for services, environments, variables and deploys. | Section 07 readers shipping a first service. |
| [Railway CLI documentation](https://docs.railway.com/cli) | The command reference for linking, deploying, logs and variables from a terminal. | Running deploys by hand. |
| [Deploying with the CLI](https://docs.railway.com/cli/deploying) | The deploy flow specifically: what `up` does and what it prints. | Writing the deploy step of an SOP. |
| [Railway Quick Start](https://docs.railway.com/quick-start) | The shortest path from an empty account to a running service. | Absolute first deploy. |
| [Railway CLI on GitHub](https://github.com/railwayapp/cli) | The CLI source and issue tracker; useful when the docs and behaviour disagree. | Debugging a surprising command result. |
| [Cloudflare developer documentation](https://developers.cloudflare.com/) | The root for Workers, and the entry point for object storage and other platform services. | Section 07's edge and storage lessons. |
| [Environment variables](https://developers.cloudflare.com/workers/configuration/environment-variables/) | How configuration reaches a Worker at runtime, including per-environment values. | Wiring staging and production apart. |
| [Workers secrets](https://developers.cloudflare.com/workers/configuration/secrets/) | Storing secrets outside the repository and reading them in code. | Section 09's secrets lessons, in a concrete tool. |
| [Wrangler commands](https://developers.cloudflare.com/workers/wrangler/commands/) | The CLI reference for deploying, tailing logs and managing a Worker. | Everything you do from a terminal. |
| [Wrangler configuration](https://developers.cloudflare.com/workers/wrangler/configuration/) | The config file: bindings, routes, compatibility settings. | Understanding what a deploy actually changes. |

## Databases and storage

| Source | What it covers | Who it is for |
|---|---|---|
| [Neon documentation](https://neon.com/docs/introduction) | Serverless Postgres: branches, connection strings, pooled endpoints and restore points. | Section 07's database lesson and every migration you run against a branch. |
| [neondatabase/neon](https://github.com/neondatabase/neon) | The database source and changelog. | Confirming behaviour the docs describe loosely. |

## MCP (Model Context Protocol)

| Source | What it covers | Who it is for |
|---|---|---|
| [Model Context Protocol](https://modelcontextprotocol.io/) | The protocol's home: concepts, servers, clients and the current specification. | Section 08 from the first page. |
| [Model Context Protocol specification](https://modelcontextprotocol.io/specification/2025-06-18) | The dated specification — the version this wiki targets, so a later revision does not quietly invalidate the lesson (as of 2025). | Readers who need exact protocol behaviour. |
| [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | Reference servers to read and run before writing your own. | Building or auditing a server. |
| [github/github-mcp-server](https://github.com/github/github-mcp-server) | GitHub's own MCP server, including its tool surface and configuration. | Connecting an agent to GitHub with a maintained server. |

## Security and OWASP

| Source | What it covers | Who it is for |
|---|---|---|
| [OWASP GenAI Security Project](https://genai.owasp.org/) | The root for OWASP's AI security work: threat lists, guides and initiatives. | Section 09's starting point. |
| [OWASP Top 10 for LLM applications](https://genai.owasp.org/llm-top-10/) | The named risk list for LLM features: prompt injection, insecure output handling, and the rest. | Anyone shipping a feature that calls a model. |
| [OWASP GenAI: LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) | The single risk entry for prompt injection, with attack and mitigation detail. | Section 09's injection lesson. |
| [Agentic Security Initiative](https://genai.owasp.org/initiatives/agentic-security-initiative/) | The programme covering risks specific to agents that take actions, not just generate text. | Readers whose agent has tools and credentials. |
| [Agentic AI: threats and mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/) | The threat catalogue and the mitigations mapped to each one. | Building the guardrail list for a multi-step agent. |
| [OWASP GenAI LLM Top 10 (2026)](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/) | The revised edition of the LLM risk list. Compare with the older list before quoting a risk number (as of 2026). | Readers who cite risk IDs in a review. |
| [OWASP Top 10 for agentic applications (2026)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | The 2026 list aimed at agentic applications as a category. | Threat-modelling a product built on agents. |
| [Securing agentic applications guide 1.0](https://genai.owasp.org/resource/securing-agentic-applications-guide-1-0/) | A longer guide to designing, testing and operating agentic systems safely. | The deep read after the threat list. |
| [OWASP](https://owasp.org/) | The foundation's project root, including API security material. | Section 06 and 14 readers looking at API risk. |
| [OWASP Top 10 for Large Language Model Applications](https://owasp.org/projects/top-10-for-large-language-model-applications) | The project page behind the list, with the project's own framing. | Following the list's evolution. |
| [MCP tool poisoning](https://owasp.org/www-community/attacks/MCP_Tool_Poisoning) | OWASP's attack page for malicious or misleading MCP tool definitions. | Reading a server you are about to install. |
| [OWASP prompt injection prevention cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) | The defensive half: input handling, output handling, and what actually helps. | Turning an injection finding into a fix. |
| [Protecting against indirect prompt injection in MCP](https://developer.microsoft.com/blog/protecting-against-indirect-injection-attacks-mcp/) | Vendor guidance on injection that arrives through tool results and documents rather than the user. | Anyone whose agent reads untrusted files or web pages. |
| [CSA research note: slopsquatting](https://labs.cloudsecurityalliance.org/research/csa-research-note-slopsquatting-ai-supply-chain-20260419-csa/) | A research note on hallucinated package names and the supply-chain risk they create. | Explaining the risk to a reviewer or a manager. |
| [Slopsquatting and hallucinated packages](https://www.aikido.dev/blog/slopsquatting-ai-package-hallucination-attacks) | A vendor write-up of the same attack class with concrete examples. | Readers who want the worked cases. |
| [Trend Micro on slopsquatting](https://www.trendmicro.com/vinfo/us/security/news/cybercrime-and-digital-threats/slopsquatting-when-ai-agents-hallucinate-malicious-packages) | Industry reporting on the pattern, useful for the "is this real?" question. | Making the case for verifying every new dependency. |

## Evaluation

| Source | What it covers | Who it is for |
|---|---|---|
| [Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) | A vendor guide to building eval sets, scoring them and using them as a gate. | Section 10's evaluating AI features lesson. |
| [Best practices and methods for LLM evaluation](https://www.databricks.com/blog/best-practices-and-methods-llm-evaluation) | A second vendor take on methods and metrics, useful when the first guide's assumptions do not fit. | Readers designing a human-graded eval. |
| [Eval-driven development](https://deepeval.com/blog/eval-driven-development) | A practitioner framing of writing the eval before tuning the prompt, with an open-source tool as the example. | Anyone who has tuned a prompt without a scoreboard. |

## Courses and tutorials

| Source | What it covers | Who it is for |
|---|---|---|
| [Agent Skills with Anthropic](https://www.deeplearning.ai/courses/agent-skills-with-anthropic) | A short course on writing and using skills, with exercises. | Section 04 readers who want guided practice. |
| [Spec-driven development with coding agents](https://www.deeplearning.ai/courses/spec-driven-development-with-coding-agents) | A short course on writing specs an agent can execute. | Section 03 readers who learn faster with exercises. |
| [Anthropic courses](https://github.com/anthropics/courses) | The repository holding Anthropic's educational courses, in a suggested order. | Anyone following this wiki's prompting sections. |
| [Real world prompting](https://github.com/anthropics/courses/blob/master/real_world_prompting/README.md) | The course on composing prompting techniques into full prompts rather than isolated tricks. | Section 02 readers past the basics. |
| [Prompt engineering interactive tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial) | The notebook-based tutorial that walks through prompting techniques one at a time. | Complete beginners to prompting. |
| [Web version of the prompting tutorial](https://github.com/idsulik/apeit) | A community browser version of the same tutorial, for people who would rather click than run notebooks. | Readers without a local Python setup. |

## Try it

1. Pick three links that a lesson you have read cites, and open them. Confirm each one still covers what this index claims.
2. Add the link check to your own project: a scheduled workflow that fetches every URL on this page and fails when one returns an error.
3. When a link is dead, do not delete it silently. Find the surviving page, or step back to the documentation root, and update the description in the same pull request.
4. Note the date next to anything numeric you quote from a source — free tiers and model names are the fastest-moving facts in this index.

## Common mistakes

- **Linking a guessed deep path.** If you have not opened the URL, link the documentation root instead. A dead deep link wastes more of the reader's time than a search does.
- **Treating a vendor blog as documentation.** Articles explain and course notes teach, but behaviour comes from the official reference. The index marks which is which.
- **Deleting a rotted link instead of replacing it.** The reader loses the trail; a root link keeps it.
- **Updating the URL and leaving the description.** A description that no longer matches the page is worse than a 404, because nothing looks broken.
- **Quoting a number without its date.** Free tiers, quotas and spec versions change; say "as of the year you read it" or leave the number out.
- **Letting the index drift from the lessons.** A source cited in a lesson but missing here is invisible to the link check, so it rots unwatched.

## Key takeaways

- Every external source the wiki cites is on this page, grouped by topic, with an honest one-line description and an audience.
- Official documentation first, then repositories and papers, then articles and courses.
- A deep link you have not opened is a bug — link the docs root so the reader can search.
- A link check runs as part of the release process; a failed link is replaced or stepped back to a root, never silently dropped.
- The field moves fast and links rot. When this index disagrees with the source, the source wins.

## Further learning

- [How to use this wiki](00-How-To-Use-This-Wiki) — reading orders, sections, and where to start if you are new.
- [Further learning](15-Further-Learning) — the curated short list, once you have finished the handbook.
- [Contributing to this wiki](15-Contributing-To-This-Wiki) — how to add a source and keep the index complete.
- [GitHub Docs](https://docs.github.com/) — the documentation root used most often across this wiki, and a good example of how to search instead of guess.
- [Mermaid cookbook](16-Mermaid-Cookbook) — the diagram templates referenced throughout the lessons.
