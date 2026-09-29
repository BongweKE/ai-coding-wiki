> **Section 8 · MCP** — Connect agents to real tools with the Model Context Protocol — and manage the risks that come with it.

*6 lessons.*

## By the end of this section you can

- Explain hosts, clients and servers, and what a server may actually do on your behalf.
- Connect a server read-only, verify what it exposes, and scope its credentials.
- Name the MCP-specific attacks: tool poisoning, rug pulls, injection through tool output, confused deputy.
- Run a fifteen-point adoption checklist before you trust a server with anything.

### [What Is MCP?](08-What-Is-MCP)
`beginner` · ~12 min — An agent is only as useful as the things it can reach. Reading files in your repo is table stakes.

### [MCP Architecture And Transports](08-MCP-Architecture)
`advanced` · ~18 min — Two questions decide how much damage a server can do: how it connects to your machine, and what it was granted when it did. Transports answer the first.

### [Using MCP In Practice](08-Using-MCP-In-Practice)
`beginner` · ~20 min — Adding an MCP server is a five-line change to a config file. That is why it deserves care: it reads like configuration, but it gives a program your credentials and a route into your systems.

### [MCP Security Risks](08-MCP-Security-Risks)
`advanced` · ~20 min — An MCP server is a program with your access, and its output lands in the model's context as trusted text. That is the whole threat model.

### [Safe MCP Adoption Checklist](08-Safe-MCP-Checklist)
`intermediate` · ~15 min — You now know the risks.

### [MCP Exercises](08-MCP-Exercises)
`intermediate` · ~25 min — You have read the architecture and the checklist.

---

← [7. Shipping & Deploy](07-Shipping-And-Deploy) · [Home](Home) · [Sidebar](_Sidebar) · [9. Safety & Security](09-Safety-And-Security) →

