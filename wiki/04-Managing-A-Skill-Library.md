> **Section 04 · Lesson 5** · Level: advanced · ~15 min · Prereq: [Skill quality](04-Skill-Quality-And-Anti-Patterns)

## Why this matters

Five skills is a folder. Fifty is a system with its own failure modes: nobody knows who owns the deployment runbook, two skills answer the same question, one has been broken since a framework upgrade, and the agent's trigger list has grown long enough that activation gets noisy. Managing a library keeps the answer to "how does this project work?" in one place, and correct.

## Layout and naming

One skill per capability. A skill named `engineering` is a drawer, not a skill — if it loads, it loads everything. Name by the action, not the technology: `reconcile-ledger`, `flutter-web-release`, `rotate-database-credential`. Categories are folders by domain, one level deep:

```
skills/
├── payments/
│   ├── reconcile-ledger/
│   └── refund-a-transaction/
├── frontend/
│   └── flutter-web-release/
└── shared/
    ├── release-notes-from-git/
    └── rotate-database-credential/
```

Keep the library in the project repository, not only in the agent's local skills directory. Anything that exists solely on one laptop cannot be reviewed, restored, or handed over.

Record the library in one index file:

| Skill | Category | Owner | Last verified | Trigger boundary |
|---|---|---|---|---|
| `reconcile-ledger` | payments | platform team | 2026-09-12 | reconcile or audit ledger entries |
| `rotate-database-credential` | shared | platform team | 2026-08-30 | rotate a DB credential, not app secrets |

The last column prevents duplicate triggers: writing down what a skill does *not* cover keeps two skills from fighting over one request.

![Anatomy of a skill folder](https://raw.githubusercontent.com/BongweKE/ai-coding-wiki/main/assets/04-skill-anatomy.png)

## Versioning, ownership, review

Skills are code, so they get code's treatment: version control, a pull request, and a reviewer who will run the command. Three rules make this concrete:

- **Every skill has an owner.** A name or team, in the index. Unowned skills rot silently, because nobody notices when their commands go stale.
- **Third-party skills are pinned to a commit.** Vetting a folder once tells you nothing about what it contains next month — the reasoning behind pinning CI dependencies to a full commit hash rather than a moving tag, as the [secure use reference for GitHub Actions](https://docs.github.com/en/actions/reference/security/secure-use) sets out.
- **A change to the tooling is a change to the skill.** When a command, path or flag moves, the skill moves in the same pull request; one that cannot be fixed now gets marked unverified at the top of the body.

Enforce the rest with a script in CI that fails the build when a `SKILL.md` is missing frontmatter, exceeds the word budget, or names a file that does not exist. One team found that a rule living only in prose drifts, while a rule enforced by a check with an exit code does not.

## Vetting third-party skills

Before you trust a folder you did not write:

1. Read every file, not just `SKILL.md`. Bundled scripts, fixtures and templates are where the surprises are.
2. Check the dependencies the folder pulls in, and that every package name is real. A generated setup step can name a package that does not exist, and the empty name gets registered by someone else — see [Supply Chain Security](09-Supply-Chain-Security).
3. Look for instructions that reach the network, or tell the agent to fetch and execute something from an unrecognised host.
4. Record the revision you vetted, and where it came from.
5. Run it in a scratch repository or a container first. A skill that goes wrong in a throwaway checkout costs nothing.

Provenance beats popularity: a reviewed twenty-line rule from someone you can name is worth more than a large unread bundle.

## Retirement

Deleting a skill is a maintenance duty. A wrong skill is worse than a missing one: the agent follows it confidently, reports success, and moves on.

Review the library quarterly. For each skill, ask:

- Has anything in it been used since the last review? A skill nobody triggers is a description nobody matches — a fixable bug, not a reason to keep it.
- Does every command still run? Run the ones the skill depends on, not the ones you remember.
- Is it still the right procedure?
- Does its trigger still differ from its neighbours'?

Then do one of three things: update it, mark it unverified, or delete it. Deletion is not a loss; git history keeps the old version, and a clean library is one where every trigger means something.

## Try it

1. Restructure your skills into `skills/<category>/<skill>/` and move the folder into the project repository.
2. Write `skills/README.md` as the index table above, with owner, last-verified date and trigger boundary for each entry.
3. Run a name-agreement check over every folder:

```bash
for d in skills/*/*/; do
  n=$(grep -m1 '^name:' "$d/SKILL.md" | cut -d' ' -f2)
  [ "$n" = "$(basename "$d")" ] || echo "MISMATCH: $d vs name '$n'"
done
```

4. Pick the oldest skill and run its commands. Fix the skill in the commit that fixes the documentation.
5. Delete one skill you cannot justify.

## Common mistakes

- **One giant skill per project** — it loads as a wall, the agent skims it, and nothing in it is reliably followed.
- **A library that only exists in the agent's local directory** — invisible to review, absent from the repo, gone when the machine dies.
- **Vetting a third-party skill once and then letting it update** — your review applied to a revision, not a name.
- **No owner** — every skill looks maintained until the day it breaks.
- **Never retiring anything** — the trigger list grows, descriptions collide, activation gets unreliable, and nobody trusts the library enough to fix it.

## Key takeaways

- One skill per capability, named by action, filed under a domain category, kept in the project repository.
- Keep an index with owner, last-verified date and trigger boundary — the boundary is what prevents duplicate triggers.
- Treat skills as code: reviewed changes, pinned third-party revisions, and CI checks for the rules a machine can enforce.
- Vet a third-party folder by reading every file and checking its dependencies, then run it somewhere disposable.
- Retire deliberately. A confidently wrong skill costs more than a missing one.

## Further learning

- [Agent Skills overview](https://agentskills.io/home) — the format, plus guidance on leading a skill collection.
- [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) — the security guidance on auditing skills you did not author.
- [Secure use reference for GitHub Actions](https://docs.github.com/en/actions/reference/security/secure-use) — pinning dependencies to a revision, the same discipline for skills.
- [Agent Skills on the Claude platform](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) — how one product installs and organises skills.
