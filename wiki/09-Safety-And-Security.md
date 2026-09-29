> **Section 9 · Safety & Security** — Protect the machine, the credentials and the codebase you now share with an agent.

Secrets, generated-code risk, prompt injection, supply chain, OWASP catalogues, privacy, accountability.

*11 lessons in this section.*

## Safety & Security (Part 1: your workflow, secrets, generated code)

### [Threat-Modeling Your AI Workflow](09-Threat-Modeling-Your-Workflow)
`intermediate` · ~18 min — what am I protecting, who wants it, how would they get it, what happens if they do.

### [Secrets Hygiene](09-Secrets-Hygiene)
`beginner` · ~15 min — environment variables and a secret manager; never in code, config committed to git, or a chat message.

### [Secure Code Generation](09-Secure-Code-Generation)
`intermediate` · ~20 min — generated code has been found to carry a meaningful share of insecure patterns — treat it as an untrusted patch from a fast, confident stranger.

### [Prompt Injection And Exfiltration](09-Prompt-Injection-And-Exfiltration)
`advanced` · ~20 min — Direct vs indirect injection; why 'ignore previous instructions' is only the cartoon version.

### [Supply Chain Security](09-Supply-Chain-Security)
`advanced` · ~20 min — lockfiles, pinned versions, minimal dependency counts.

## Safety & Security (Part 2: OWASP, agents, privacy, accountability)

### [OWASP LLM Top 10 In Plain English](09-OWASP-LLM-Top-10)
`intermediate` · ~20 min — prompt injection, sensitive information disclosure, supply chain, data and model poisoning, improper output handling, excessive agency, system prompt 

### [OWASP Agentic Threats](09-OWASP-Agentic-Threats)
`advanced` · ~18 min — they plan, remember, and act with tools.

### [Privacy And Compliance Basics](09-Privacy-And-Compliance)
`intermediate` · ~20 min — what counts, why 'it is just a log line' is not a defence, and data minimisation as an engineering habit.

### [Human Accountability](09-Human-Accountability)
`beginner` · ~12 min — you own every line you commit, however it was produced.

### [Security Checklists](09-Security-Checklists)
`intermediate` · ~15 min — new repository, new API endpoint, new external integration, new AI feature.

### [Security Exercises](09-Security-Exercises)
`advanced` · ~25 min — plant a prompt injection in an issue body and see whether your agent obeys it.

---

Section 9 of 16 · [Home](Home) · [Sidebar index](_Sidebar)
