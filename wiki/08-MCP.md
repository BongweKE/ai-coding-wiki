> **Section 8 · MCP: Connecting Tools Safely** — Understand the Model Context Protocol, use it, and adopt it without handing an attacker your machine.

Connect agents to real tools with the Model Context Protocol — and the risks that come with it.

*6 lessons in this section.*

### [What Is MCP?](08-What-Is-MCP)
`beginner` · ~12 min — every agent tool had a bespoke integration; MCP standardises 'the model can call capabilities'.

### [MCP Architecture And Transports](08-MCP-Architecture)
`advanced` · ~18 min — stdio (a local process) vs HTTP (remote servers), and what each implies for trust and for credentials.

### [Using MCP In Practice](08-Using-MCP-In-Practice)
`beginner` · ~20 min — Configuring a server in a client (config file, command/args or URL, env for credentials) with a generic example.

### [MCP Security Risks](08-MCP-Security-Risks)
`advanced` · ~20 min — malicious or hidden instructions inside tool descriptions that the model reads and obeys.

### [Safe MCP Adoption Checklist](08-Safe-MCP-Checklist)
`intermediate` · ~15 min — provenance, source review, pinned versions, read-only scopes, narrowly scoped tokens, no prod credentials, approval prompts kept on, egress limits, sa

### [MCP Exercises](08-MCP-Exercises)
`intermediate` · ~25 min — Run one read-only server locally and inspect every tool it exposes.

---

Section 8 of 16 · [Home](Home) · [Sidebar index](_Sidebar)
