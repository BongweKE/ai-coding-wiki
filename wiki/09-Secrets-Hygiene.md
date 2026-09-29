> **Section 09 · Lesson 2** · Level: beginner · ~15 min · Prereq: [Setup your workbench](00-Setup-Your-Workbench)

## Why this matters
A leaked key is not a code bug you fix on Friday. It is a stranger holding your credentials, and the clock starts the second the value reaches git history, a CI log, a screenshot or a chat message. Once an agent works in your repo, that risk goes up: agents paste file contents into context, print environment variables while debugging, and happily commit whatever they find. The good news is that secrets hygiene is a short, mechanical routine, and once it is in place it protects you from your own mistakes too.

## Where secrets belong
There are exactly two acceptable homes for a secret.

- **On the machine that needs it**: an environment variable, loaded from a file that is never committed, or from your OS keychain.
- **In the platform that runs the code**: a secret store on your host or CI provider, injected into the process at runtime.

Everywhere else is wrong: never in source, never in a config file committed to git, never in a Docker image layer, never in a chat message or an issue, never in a prompt. "It is a private repo" is not protection — history is forever, collaborators change, and a fork or a mis-scoped token exposes it.

## The `.env` pattern
Gitignore the real file, commit a template, and load at runtime.

```bash
# .gitignore
.env
.env.*
!.env.example
```

```bash
# .env.example - committed, contains no real values
DATABASE_URL=postgres://user:password@localhost:5432/app
SERVICE_API_KEY=sk-...REDACTED
```

```python
import os

api_key = os.environ["SERVICE_API_KEY"]  # fails loudly if unset
```

Keep one file per environment, and never reuse a value across them. `.env.local`, `.env.staging` and the production values in the platform's secret store should be different credentials, so a mistake in development cannot spend production money. Giving each environment its own key is what makes rotation cheap later.

## Scanning, and what to do when a key leaks
A secret scanner catches the mistake before a human reviewer does. Pattern scanners look for known credential shapes in a diff; commit-history scanners look at everything already pushed. Add one as a required check on every pull request, and turn on your host's push protection so a known credential shape is rejected at push time. The tooling changes often — pick one, read its current docs, and make the scan a gate rather than a warning.

When a key leaks, the order matters:

1. **Rotate first.** Issue a new credential and revoke the old one. Assume it is compromised the moment it is visible. Do not start with cleanup.
2. **Then purge.** Removing the value from git history is worthwhile, but it is cleanup, not containment. Rotating already made the leaked value useless.
3. **Then scan.** Search the whole history, the CI logs and any build caches for the same value or a variant of it.
4. **Then add a gate.** A scanner on pull requests plus push protection stops the repeat.

Notice what is not on that list: waiting to see whether anyone uses the key. Assume they will.

## Why the platform's variables beat a file
A deployed service should be configured by the environment it runs in, not by a file your laptop carries. Platform variables are encrypted at rest, are injected only into the running process, are visible to the people who run the deploy, and can be scoped to an environment that requires approval to use. A `.env` file on your laptop is none of those things, and it is the copy most likely to end up in a backup, an editor sync folder or a screenshot. If your laptop does not hold the production key, your laptop cannot leak it.

## Rotation, scope and separation
Three habits keep the blast radius small.

- **Rotate on a schedule and on suspicion.** Pick a cadence you will actually keep — say annually for stable keys, sooner for anything exposed to a third party — and rotate immediately after any team change or suspected exposure. Write the procedure down as a runbook: generate, update staging, test end to end, update production, watch for failures.
- **Scope every token.** Grant the narrowest permissions that do the job: read-only where reading is all it does, one resource rather than the whole account, one environment rather than all of them.
- **Separate credentials per environment and per purpose.** One key for deploys, one for the API client, one for backups. A shared key means one leak is every leak.
- **Audit yearly.** Delete variables nobody can explain. Old sandbox credentials left set in production are a common finding, and they are free attack surface.

```mermaid
flowchart TD
    A["Code needs a secret"] --> B{"Where does it run?"}
    B -- "your laptop" --> C["Local .env file, gitignored"]
    B -- "CI or deployed" --> D["Platform secret store"]
    C --> E{"Was it ever committed?"}
    D --> E
    E -- "no" --> F["Keep it out of git"]
    E -- "yes" --> G["1. Rotate the key now"]
    G --> H["2. Purge history and logs"]
    H --> I["3. Add a scanner gate"]
    I --> J["4. Confirm the old value is dead"]
```

## Try it
1. Create `.gitignore` with the three lines above, then create `.env.example` containing placeholders only.
2. Move every real value in your project into environment variables read via `os.environ[...]`, and delete the committed copies.
3. Check your history for anything that looks like a key:

   ```bash
   git log --all -S 'SERVICE_API_KEY' --oneline
   git grep -nE '(api[_-]?key|secret|token)[[:space:]]*[:=][[:space:]]*[A-Za-z0-9_-]{16,}' -- ':!*.lock'
   ```

4. If either command returns a real value, rotate that credential today, then clean up.
5. Add a secret-scanning step to your pull-request workflow and make it required. See [Secrets in CI](05-Secrets-In-CI).

## Common mistakes
- **Cleaning history before rotating.** Rewriting the past does not un-leak a key. Rotate, then tidy.
- **Committing `.env.example` with real values.** It is the file people copy most, and it is the one most often accidentally filled in.
- **One key for every environment.** Then you cannot test rotation, cannot tell which environment caused an incident, and cannot revoke one without breaking the others.
- **Putting a secret in a URL query string.** URLs end up in access logs, browser history and error reports.
- **Asking the agent to "just set it up" without saying where secrets live.** It will write the value into the first file that works. Say the rule in your [AGENTS.md](12-AGENTS-md-That-Works).

## Key takeaways
- Two homes only: environment variables on the machine, or the platform's secret store. Never source, never config in git, never chat.
- Commit `.env.example` with placeholders and gitignore everything else.
- Rotate first, purge second, scan third, add a gate fourth.
- Prefer platform variables for anything deployed; a key your laptop never holds cannot leak from it.
- Give each environment and each purpose its own narrowly scoped credential, and rotate on a schedule.

## Further learning
- [GitHub Docs: secure use reference](https://docs.github.com/en/actions/reference/security/secure-use) — how CI handles secrets, masking and least privilege.
- [Cloudflare Workers: Secrets](https://developers.cloudflare.com/workers/configuration/secrets/) — a worked example of platform-held runtime secrets.
- [Railway Docs](https://docs.railway.com/) — environment variables and per-environment configuration for a deployed service.
- [GitHub Actions documentation](https://docs.github.com/en/actions) — where to add a scanning step in your workflow.
