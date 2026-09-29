> **Section 6 · System Design** — Design before code: boundaries, diagrams, state machines, ADRs, schemas, APIs, scale.

*12 lessons in two parts.* Part 1: 1: thinking, diagrams, decisions, data. Part 2: 2: APIs, reliability, security, scale.

## By the end of this section you can

- Choose a system's boundaries before an agent writes a line of it.
- Draw diagrams as code: flow, sequence, state machine, schema.
- Write an ADR that records the options you rejected and why.
- Model data with the right constraints, design an API contract, and plan for failure and scale.

## System Design & Architecture (Part 1: thinking, diagrams, decisions, data)

### [Why Architecture Before Code](06-Why-Architecture-Before-Code)
`beginner` · ~12 min — An agent can write a working feature faster than you can read it. The slow, expensive part of software is no longer typing the code — it is choosing the shape the code lives in.

### [Thinking In Boundaries](06-Thinking-In-Boundaries)
`intermediate` · ~18 min — A boundary is a place where you can change what is inside without touching what is outside.

### [Diagrams As Code](06-Diagrams-As-Code)
`beginner` · ~18 min — A drawing in a design tool is a picture nobody can diff, so it goes stale the week after it is made.

### [State Machines For Real Features](06-State-Machines-For-Features)
`intermediate` · ~20 min — Every feature with a status column is a state machine, whether or not you admit it.

### [Architecture Decision Records](06-Architecture-Decision-Records)
`beginner` · ~15 min — Six months from now, someone will ask why the tenant key sits on every table, or why one provider call is queued and another is not.

### [Data Modeling Basics](06-Data-Modeling-Basics)
`intermediate` · ~20 min — Constraints are the cheapest correctness you will ever buy.

## System Design & Architecture (Part 2: APIs, reliability, security, scale)

### [API Design Basics](06-API-Design-Basics)
`intermediate` · ~20 min — An API is the contract between everything that calls your service and the data model beneath it.

### [Reliability Patterns](06-Reliability-Patterns)
`advanced` · ~20 min — Every dependency you call will eventually be slow, wrong, or absent: a database failover, a provider outage, a network partition, a deploy that half-rolled.

### [Security Architecture](06-Security-Architecture)
`advanced` · ~20 min — Security architecture is mostly a drawing plus the gates on it: what can talk to what, with which credential, and what happens when that credential leaks.

### [Observability](06-Observability)
`intermediate` · ~18 min — Without observability, a production problem reaches you as a support message: "the app is broken". With it, the problem arrives as an alert with a request id, a failing route and a timeline.

### [Scaling From One Instance](06-Scaling-From-One-Instance)
`advanced` · ~18 min — Scaling is usually described as adding machines.

### [Architecture Review With AI](06-Architecture-Review-With-AI)
`intermediate` · ~15 min — You have a diagram, a schema, an API table and a couple of ADRs. A model reads all of that in seconds and is genuinely good at one thing: finding the failure you did not think about.

---

← [5. Git & CI/CD](05-Git-And-CICD) · [Home](Home) · [Sidebar](_Sidebar) · [7. Shipping & Deploy](07-Shipping-And-Deploy) →

