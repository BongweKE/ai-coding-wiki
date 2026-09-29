> **Section 15 · Lesson 5** · Level: beginner · ~12 min · Prereq: none

## Why this matters

This wiki is deliberately shallow in one direction: it covers a lot quickly and stops where the field becomes a moving target. This page is the handoff — a grouped index of sources worth your next hour, with who each one is for and what to read first. None of them will stay current, which is why the last two sections exist.

## Courses, and the order that works

- [Anthropic's courses](https://github.com/anthropics/courses) — exercises rather than prose, in a recommended order: API fundamentals, the prompt engineering interactive tutorial, real-world prompting, prompt evaluations, then tool use. Do the evaluations course before you build a model feature. Prefer clicking to notebooks? There is a [web version](https://github.com/idsulik/apeit).
- [Agent Skills with Anthropic](https://www.deeplearning.ai/courses/agent-skills-with-anthropic) — for the reader who has written one skill and wants the shape of a library.
- [Spec-driven development with coding agents](https://www.deeplearning.ai/courses/spec-driven-development-with-coding-agents) — for the reader whose agent keeps solving the wrong problem precisely.

## Agent engineering, from the people building it

- [Anthropic Engineering](https://www.anthropic.com/engineering) — browse the root, and read in this order: [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) for the vocabulary, [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), then [Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills). [Best practices for Claude Code](https://www.anthropic.com/engineering/claude-code-best-practices) is the most immediately useful, and [Steering Claude Code](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more) answers "rules file, skill, hook or subagent?". Vendor write-ups: good mental models, worth verifying on your own repo.

## Specification-driven development

- [Understanding spec-driven development: Kiro, spec-kit and Tessl](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) — vendor-neutral and the best first read.
- [Spec-driven development with AI (GitHub blog)](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/) — the workflow with a real toolkit.

## CI/CD, Actions and hardening

- [GitHub Actions documentation](https://docs.github.com/en/actions) and [workflow syntax](https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions) — the two pages you will return to most.
- [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use) — read it after your first green pipeline and before your first third-party action.
- [Pinning GitHub Actions for security](https://www.stepsecurity.io/blog/pinning-github-actions-for-enhanced-security-a-complete-guide) — why `@v3` is a promise and a commit SHA is a fact.

## Deployment and databases

- [Railway docs](https://docs.railway.com/) and [deploying with the CLI](https://docs.railway.com/cli/deploying) — for Capstone 1; `railway up --ci` and project tokens are the parts that matter.
- [Neon documentation](https://neon.com/docs/introduction) — read the branching material before you build environments.

## MCP

- [Model Context Protocol](https://modelcontextprotocol.io/) and the [specification](https://modelcontextprotocol.io/specification/2025-06-18) — read the architecture once, then skim tools, resources and prompts.
- [github/github-mcp-server](https://github.com/github/github-mcp-server) — read one server's code before you install five.
- Read [MCP security risks](08-MCP-Security-Risks) first; a server is code you invite to act for you.

## Security: OWASP first

- [genai.owasp.org](https://genai.owasp.org/) and the [LLM Top 10 archive](https://genai.owasp.org/llm-top-10/) — the editions differ, so check which one you are reading; the [2026 list](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/) is current. For a model feature, start with LLM01 prompt injection, LLM05 improper output handling, LLM06 excessive agency and LLM10 unbounded consumption.
- [Agentic AI — threats and mitigations](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/) — the same failures once the model can act.
- [LLM prompt injection prevention cheat sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) and [MCP tool poisoning](https://owasp.org/www-community/attacks/MCP_Tool_Poisoning) — the two checklists to work against.
- [Slopsquatting: hallucinated package names](https://www.aikido.dev/blog/slopsquatting-ai-package-hallucination-attacks) — check that a dependency exists before you install it.

## Evals

- [Evaluation best practices (OpenAI)](https://developers.openai.com/api/docs/guides/evaluation-best-practices) — best first read.
- [Eval-driven development (DeepEval)](https://deepeval.com/blog/eval-driven-development) — the loop, with examples.
- [Best practices for LLM evaluation (Databricks)](https://www.databricks.com/blog/best-practices-and-methods-llm-evaluation) — when your eval set gets real.

## System design

Start with this wiki's own Section 06: [Why architecture before code](06-Why-Architecture-Before-Code), [Thinking in boundaries](06-Thinking-In-Boundaries), [Reliability patterns](06-Reliability-Patterns). Beyond that, prefer writing that states its date and the versions it tested.

## Open skill and server collections

- [anthropics/skills](https://github.com/anthropics/skills) — read the simplest skill end to end; it is ten minutes and it recalibrates yours.
- [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) — what other people have plugged in, and what they had to write to do it.

## How to judge a resource, and what will rot

Four questions: does it carry a date, a version or a commit hash; is it vendor-neutral or a product page; does it ship code you can run; does it say what it tested against? Three yeses earns an hour; none earns a closed tab.

This field moves fast and links rot. Every number in this wiki — free-tier limits, model names, action versions, spec revisions — is either marked "as of" or left out, and the same rule applies to everything above. Check the date before you trust a figure, and expect a 2025 answer to be wrong about a 2026 product. Dead link? Search the title: docs are reorganised far more often than deleted. If a page here has rotted, that is a contribution, not a complaint.

## Try it

1. Pick one group above and read only its first item, start to finish. Note its date.
2. Run the code in it. No code? Note where it was tested.
3. Take two sources on the same topic from different vendors and write down one claim they disagree on.
4. Add the three sources you finished to your notes file with dates. Not the ten you bookmarked.

## Common mistakes

- **Treating a vendor blog as neutral** — a good mental model and a biased comparison. Verify on your own repo.
- **Starting three courses at once** — finishing one beats sampling four.
- **Trusting a number with no date** — quota, price and version answers expire quietly.
- **Installing an MCP server before reading about tool poisoning** — a server is code acting with your credentials.
- **Collecting links instead of running code** — an unread bookmarked course teaches nothing.

## Key takeaways

- Read one source to the end and run its code; a bibliography is not knowledge.
- The OWASP GenAI pages are the only group to read before shipping anything model-facing.
- Prefer documentation roots over deep links you cannot verify, and check a page's date before trusting its numbers.
- Everything here will age; the four-question test ages much more slowly.
- When you find the better source, add it here through a pull request.

## Further learning

- [Link index](16-Link-Index) — every verified link used across this wiki, in one place.
- [Contributing to this wiki](15-Contributing-To-This-Wiki) — how to add the source that should have been on this page.
- [The 30-day learning plan](15-30-Day-Learning-Plan) — where these sources fit into practice.
- [Capstone 2](15-Capstone-2-Add-An-AI-Feature) — the exercise that will tell you whether you understood the security group.
