> **Section 7 · Shipping & Deploy** — Railway, Neon, edge workers, environments, promotion, rollback and cost control.

*10 lessons.*

## By the end of this section you can

- Deploy an API and a database to the internet and keep them running.
- Use environments properly: staging automatic, production deliberate, migrations before code.
- Write a rollback plan before you need it, and run an incident without thrashing.
- Know where the money goes, and set limits before you scale.

### [Deployment Concepts](07-Deployment-Concepts)
`beginner` · ~15 min — Your laptop has your files, your .env, your Python version and your half-installed packages on it. A server has none of that.

### [Deploy On Railway](07-Deploy-On-Railway)
`beginner` · ~20 min — Railway is the shortest path from a folder on your laptop to a URL someone else can open. It builds your code, runs it, injects your variables and gives you logs.

### [Postgres On Neon](07-Postgres-On-Neon)
`intermediate` · ~20 min — A database that runs on your laptop and one that runs for users are different problems.

### [Edge With Cloudflare Workers](07-Edge-With-Cloudflare-Workers)
`intermediate` · ~15 min — Some requests should be answered before they reach your server: a redirect, a cache miss, a security header, a check that the caller is allowed to see this at all.

### [Object Storage And Artifacts](07-Object-Storage-And-Artifacts)
`intermediate` · ~12 min — Two things do not belong in git and do not belong on a container's disk: large files your users download, and build outputs your pipeline produces.

### [Environments And Promotion](07-Environments-And-Promotion)
`advanced` · ~20 min — main is not production. If merging a pull request ships straight to real users, the only review that matters happens after the damage.

### [Rollbacks And Incidents](07-Rollbacks-And-Incidents)
`intermediate` · ~18 min — Every deploy bets that the new version is better than the one running. Sometimes the bet loses, and the only question left is how long users stay affected.

### [Cost Control For Side Projects](07-Cost-Control)
`intermediate` · ~15 min — Small projects do not die from a bill they saw coming.

### [Local To Cloud Walkthrough](07-Local-To-Cloud-Walkthrough)
`beginner` · ~25 min — You have read about builds, variables, migrations, staging and gates.

### [Deployment Exercises](07-Deployment-Exercises)
`intermediate` · ~25 min — You can read about rollback for an hour and still freeze the first time production breaks. The knowledge that helps under pressure is the kind you have already used with your hands.

### [Deploy For Free](07-Deploy-For-Free)
`beginner` · ~20 min — Free tiers have failure modes — sleeping instances, quota cliffs, expiring storage — so pick the layer that hurts least and cap the spend before you ship.

### [Accept Payments In Kenya](07-Accept-Payments-In-Kenya)
`intermediate` · ~25 min — Stripe is not directly available in Kenya, so the work goes through Paystack, Flutterwave, Pesapal or Daraja — the same webhook-shaped problem every time.

### [Local Models When Code Cannot Leave](07-Local-Models-When-Code-Cannot-Leave)
`intermediate` · ~18 min — When the code cannot leave the machine, a local model behind an OpenAI-compatible endpoint on localhost gives you a working agent and no per-token bill.

---

← [6. System Design](06-System-Design) · [Home](Home) · [Sidebar](_Sidebar) · [8. MCP](08-MCP) →

