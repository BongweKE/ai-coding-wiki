> **Section 9 · Safety & Security** — Secrets, generated-code risk, prompt injection, supply chain, OWASP catalogues, privacy, accountability.

*11 lessons in two parts.* Part 1: 1: your workflow, secrets, generated code. Part 2: 2: OWASP, agents, privacy, accountability.

## By the end of this section you can

- Threat-model your own workflow, with the agent drawn inside the trust boundary.
- Keep secrets out of code, git history and prompts, and know the first five minutes after a leak.
- Review generated code for its specific traps: invented dependencies, insecure defaults, licence risk.
- Recognise prompt injection, install structural mitigations, and own what you commit.

## Safety & Security (Part 1: your workflow, secrets, generated code)

### [Threat-Modeling Your AI Workflow](09-Threat-Modeling-Your-Workflow)
`intermediate` · ~18 min — An agent is a new actor in your workflow. It reads files, runs shell commands, installs packages and calls APIs using credentials issued to you.

### [Secrets Hygiene](09-Secrets-Hygiene)
`beginner` · ~15 min — A leaked key is not a code bug you fix on Friday.

### [Secure Code Generation](09-Secure-Code-Generation)
`intermediate` · ~20 min — Generated code arrives looking finished. It is formatted, it names variables reasonably, and it often runs on the first try.

### [Prompt Injection And Exfiltration](09-Prompt-Injection-And-Exfiltration)
`advanced` · ~20 min — Prompt injection is the security problem that does not look like one.

### [Supply Chain Security](09-Supply-Chain-Security)
`advanced` · ~20 min — Your codebase is mostly other people's code. Every dependency, every action your pipeline calls and every base image your build pulls is a package someone else can change without asking you.

## Safety & Security (Part 2: OWASP, agents, privacy, accountability)

### [OWASP LLM Top 10 In Plain English](09-OWASP-LLM-Top-10)
`intermediate` · ~20 min — The OWASP LLM Top 10 is the shared vocabulary for "what goes wrong when you put a model inside a product". If you build an AI feature, it is your review checklist.

### [OWASP Agentic Threats](09-OWASP-Agentic-Threats)
`advanced` · ~18 min — An agent is not a chatbot with extra features.

### [Privacy And Compliance Basics](09-Privacy-And-Compliance)
`intermediate` · ~20 min — The moment your product handles a real person's name, phone number or payment detail, obligations attach — and AI blurs them, because data leaves your infrastructure in a prompt and returns as text nobody structured.

### [Human Accountability](09-Human-Accountability)
`beginner` · ~12 min — An agent can write a thousand lines in four minutes.

### [Security Checklists](09-Security-Checklists)
`intermediate` · ~15 min — Security advice is easy to read and impossible to remember at the moment it matters — three minutes before you push, with an agent asking whether it can also "tidy up the config".

### [Security Exercises](09-Security-Exercises)
`advanced` · ~25 min — Reading about prompt injection teaches you the vocabulary. Testing whether your agent obeys an injected instruction teaches you whether you have a problem, and it takes about ten minutes.

---

← [8. MCP](08-MCP) · [Home](Home) · [Sidebar](_Sidebar) · [10. Quality](10-Quality) →

