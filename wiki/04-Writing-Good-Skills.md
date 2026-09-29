> **Section 04 · Lesson 3** · Level: intermediate · ~15 min · Prereq: [Anatomy of a SKILL.md](04-Anatomy-Of-A-Skill-File)

## Why this matters

A skill that reads well and changes nothing is worse than no skill at all, because the agent now performs confidence about a procedure it only half-follows. Good skills are short, imperative, and built from failures that actually happened to somebody. This lesson is the difference between a skill folder that sits in the repository and a skill that fixes behaviour.

## Rule-shaped, not essay-shaped

Every line should be an instruction with the reason attached, one rule per line:

Bad: "Generally speaking, when working in this codebase, it is often preferable to consider running the linter before committing changes."

Good: "Run `make lint` before every commit. CI rejects unformatted code, so skipping it only moves the failure to the pull request."

The reason is not decoration. An agent that knows *why* a step exists can handle the case your rule did not anticipate. An agent given a bare command with no reason either stops when the situation shifts or improvises something you did not ask for.

## Keep it small enough to load

Progressive disclosure only pays off if the top level stays thin. A body of 900 lines burns the context the skill was meant to save, and gets skimmed instead of read.

Split, but verify the split. One maintainer split a bloated skill from roughly 11,000 words down to about a third of that by moving whole sections into `references/`, then checked the result by diffing the surviving headings and tokens against the original. Their rule, now enforced across a library of skills: keep every skill under about 5,000 words. Before moving a section out, list the headings it contained, paste them into the reference file's top comment, and confirm the count afterwards.

## Encode failures, not theory

Every pitfall in a skill should be one that cost someone real time. Two shapes worth recognising, both generalised from shipped projects:

- An integration's callback endpoint replied with the literal string `ok` even when the underlying operation had failed. The skill written afterwards does not say "always check the response". It says: "after the callback returns, read the transaction row and assert its state; the HTTP body is not evidence."
- An integration renamed a bulk-transfer path without removing the old one. The old name still existed and still returned a server error. The skill lists the current path and adds: "the old SDK-copied name is an endpoint-drift trap — never call it."

Theory belongs in the wiki, not in the skill. "Concurrency is hard" is not a pitfall. "This endpoint can be called twice with the same idempotency key; check before you retry" is.

## Write the description for retrieval

The description is not a title. Treat the first 60-odd characters as the only ones guaranteed to be read at decision time:

- Start with "Use when ...".
- Front-load the nouns a user would type: "release notes", "database migration", "staging deploy".
- Cut adjectives and any phrase that would also fit a different skill.
- If two skills could plausibly match the same request, their descriptions are both wrong — sharpen the boundary and say what each one does *not* cover.

Test it cheaply: paste the description alone into a fresh session and ask whether it would open the skill for the request "add a database column".

## Maintain it when the code moves

When a command inside a skill goes stale, fix the skill in the same change that fixed the code. A skill is not documentation that can wait for a docs sprint; it is an instruction an agent will follow confidently and then report as done. If you cannot fix it now, mark the body as unverified at the top rather than leaving a command you know is wrong. When the fix taught you something, append it to your lesson bank — see [Lesson Banks And Retros](11-Lesson-Banks-And-Retros).

## Try it

1. Run a hedge check over a skill you have written, or one from a public collection:

```bash
grep -nE '\b(should|consider|generally|usually|might want to|perhaps)\b' SKILL.md
```

Each hit is a rule that has not made up its mind. Rewrite it as an imperative with a reason, or delete it.

2. Count the words: `wc -w SKILL.md`. If the count is high, list the headings that are reference material rather than steps and move the largest into `references/`.
3. Pick one failure from your own history — a command that returned success while the work failed, a renamed endpoint, a flag that silently changed behaviour — and add it as a pitfall with the check that would have caught it.
4. Rewrite your description so the first six words contain the trigger. Re-read it as though you were the retrieval step.

## Common mistakes

- **Hedged instructions** — "you should probably consider running the tests" gives the agent nothing to decide with. Say what to run, and why.
- **A rule with no reason** — when a case falls just outside it, the agent cannot tell which part was the point.
- **Theory in the pitfalls section** — general truths about software are not the same as traps in this project. Keep the specific one.
- **A description written as a title** — "Deployment" will never be matched against "ship this to production". Start with "Use when".
- **Fixing the code but not the skill** — the next session follows the stale command, gets a confusing error, and blames the code.

## Key takeaways

- Imperative plus reason, one rule per line. Cut everything else.
- Keep the always-loaded part small; move reference material into `references/` and verify nothing was lost.
- A pitfall is only worth keeping if it cost someone time. Encode the check that catches it.
- The description is a retrieval trigger. Front-load the words a user would type.
- When a command changes, the skill changes in the same edit — or it is marked unverified.

## Further learning

- [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) — guidance on iterating with the agent and watching how a skill is actually used.
- [Agent Skills overview](https://agentskills.io/home) — includes dedicated pages on optimising descriptions and evaluating skills.
- [Agent Skills on the Claude platform](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) — format and authoring reference for one implementation.
