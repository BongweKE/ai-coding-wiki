#!/usr/bin/env python3
"""Build the wiki's infographics.

Each infographic is a self-contained dark-theme HTML card rendered to PNG with headless
Chrome, so the wiki can embed real images (GitHub renders mermaid natively, but PNGs work
everywhere, including offline readers and the printed PDF).

Usage:  python3 scripts/build_infographics.py [output_dir]
Requires: google-chrome (or chromium) on PATH.
"""
import os, subprocess, sys, shutil, tempfile

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
OUT = os.path.abspath(OUT)
W, H = 1600, 900

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:__W__px;height:__H__px;background:#0d1117;color:#e6edf3;
 font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
 padding:44px 52px;display:flex;flex-direction:column;gap:22px}
h1{font-size:34px;font-weight:700;letter-spacing:-.4px}
h1 .tag{font-size:15px;font-weight:600;color:#0d1117;background:#2dd4bf;border-radius:999px;
 padding:4px 12px;margin-left:14px;vertical-align:middle}
.sub{font-size:17px;color:#8b949e;line-height:1.45;max-width:1350px}
.body{flex:1;display:flex;flex-direction:column;justify-content:center;gap:16px}
.row{display:flex;gap:16px;align-items:stretch}
.col{display:flex;flex-direction:column;gap:12px;flex:1}
.card{background:#161b22;border:1px solid #30363d;border-radius:12px;padding:16px 18px;flex:1}
.card h3{font-size:17px;margin-bottom:6px}
.card p{font-size:14px;color:#8b949e;line-height:1.45}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
.arrow{display:flex;align-items:center;justify-content:center;font-size:26px;color:#484f58;min-width:34px}
.pill{display:inline-block;font-size:13px;font-weight:600;border-radius:999px;padding:3px 10px;
 border:1px solid #30363d;color:#8b949e;margin-right:6px}
.bar{display:flex;align-items:center;gap:12px;margin-bottom:9px}
.bar .lab{width:330px;font-size:15px;color:#c9d1d9;text-align:right}
.bar .track{flex:1;background:#161b22;border:1px solid #30363d;border-radius:8px;height:34px;position:relative;overflow:hidden}
.bar .fill{height:100%;display:flex;align-items:center;padding-left:12px;font-size:13px;font-weight:600;color:#0d1117}
.foot{font-size:13px;color:#6e7681;border-top:1px solid #21262d;padding-top:12px}
.t{b:1px solid #30363d}.tt{border-top:1px solid #30363d}
table{width:100%!;border-collapse:collapse;font-size:14px}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid #21262d}
th{color:#8b949e;font-weight:600;font-size:13px;text-transform:uppercase;letter-spacing:.5px}
.teal{color:#2dd4bf}.blue{color:#58a6ff}.amber{color:#d29922}.red{color:#f85149}
.purple{color:#bc8cff}.green{color:#3fb950}.dim{color:#8b949e}
.bt{background:#2dd4bf}.bb{background:#58a6ff}.ba{background:#d29922}.br{background:#f85149}
.bp{background:#bc8cff}.bg{background:#3fb950}
.node{background:#161b22;border:1px solid #30363d;border-radius:10px;padding:12px 16px;text-align:center;flex:1}
.node b{display:block;font-size:16px;margin-bottom:4px}
.node span{font-size:13px;color:#8b949e}
.node.accent{border-color:#2dd4bf}.node.warn{border-color:#d29922}.node.bad{border-color:#f85149}
.stackrow{display:flex;align-items:center;gap:14px}
.lvl{font-size:13px;color:#8b949e;width:60px;text-align:right}
""".replace("__W__", str(W)).replace("__H__", str(H)).replace("100%!", "100%")


def page(title, tag, sub, body, foot):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<h1>{title}{f'<span class="tag">{tag}</span>' if tag else ''}</h1>
<div class="sub">{sub}</div><div class="body">{body}</div><div class="foot">{foot}</div>
</body></html>"""


def card(t, p, cls=""):
    return f'<div class="card {cls}"><h3>{t}</h3><p>{p}</p></div>'


def arrow():
    return '<div class="arrow">&#8594;</div>'


def bars(items):
    out = []
    for lab, pct, cls, note in items:
        out.append(f'<div class="bar"><div class="lab">{lab}</div>'
                   f'<div class="track"><div class="fill {cls}" style="width:{pct}%">{note}</div></div></div>')
    return "".join(out)


def nodes(items):
    out = []
    for i, (b, s, cls) in enumerate(items):
        if i:
            out.append(arrow())
        out.append(f'<div class="node {cls}"><b>{b}</b><span>{s}</span></div>')
    return f'<div class="row">{"".join(out)}</div>'


def table(headers, rows):
    th = "".join(f"<th>{h}</th>" for h in headers)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>"


FOOT = "Coding With AI in the New Age · github.com/BongweKE/ai-coding-wiki"

# Social/Open Graph card. 1200x630 is the size link previews expect, so it is
# rendered separately from the 1600x900 infographics rather than added to CARDS.
SOCIAL_W, SOCIAL_H = 1200, 630
OG_HTML = """<!doctype html><html><head><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0;padding:0}
body{width:1200px;height:630px;background:#0d1117;color:#e6edf3;
 font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
 padding:64px 72px;display:flex;flex-direction:column;justify-content:space-between}
.kicker{font-size:18px;color:#2dd4bf;font-weight:700;letter-spacing:1.6px;text-transform:uppercase}
h1{font-size:64px;line-height:1.05;font-weight:800;letter-spacing:-1.4px;margin-top:16px}
h1 em{color:#2dd4bf;font-style:normal}
p{font-size:23px;color:#8b949e;line-height:1.42;max-width:960px;margin-top:18px}
.row{display:flex;gap:10px;margin-top:24px}
.pill{font-size:17px;font-weight:600;border-radius:999px;padding:6px 14px;border:1px solid #30363d;color:#c9d1d9}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:18px;color:#6e7681;
 border-top:1px solid #21262d;padding-top:18px}
</style></head><body>
<div>
<div class="kicker">Free &middot; technical &middot; beginner to advanced</div>
<h1>Coding With AI<br>in the <em>New Age</em></h1>
<p>A bite-sized wiki for building real things with AI coding agents &mdash; prompting, agentic
workflows, CI/CD, security, evals and shipping. 135+ short lessons, four learning paths.</p>
<div class="row"><span class="pill">Start here</span><span class="pill">30-day plan</span>
<span class="pill">Three capstones</span><span class="pill">Cheat sheets</span></div>
</div>
<div class="foot"><span>vibe.bongwe.space</span><span>github.com/BongweKE/ai-coding-wiki</span></div>
</body></html>"""

CARDS = {}

# ---- 00
CARDS["00-ai-ladder"] = page(
    "The autonomy ladder", "Section 0",
    "Every step up hands the agent more judgement and takes away your chance to catch it early. "
    "Climb as high as your verification allows — no higher.",
    "".join([
        nodes([("Type it","you decide, you write",""),
               ("Autocomplete","suggests the next line",""),
               ("Inline edit","rewrites a selection you approve",""),
               ("Chat","explains, drafts, reviews",""),
               ("Terminal agent","reads, edits, runs tests","accent"),
               ("Async / cloud agent","opens the PR while you sleep","warn")]),
        '<div class="sub" style="margin-top:14px">Blast radius grows to the right &#8594; so must your gates: '
        'diff review, tests in CI, branch protection, no production credentials in the sandbox, and a human on the merge button.</div>',
        '<div class="row" style="margin-top:6px">' +
        card("Cheap to reverse", "Autocomplete, a draft answer, a file you can <span class='mono'>git restore</span>. Let it be fast.", "accent") +
        card("Expensive to reverse", "A migration on real data, a deploy, a payment, a force-push. Require a plan and an approval.", "warn") +
        "</div>"]),
    FOOT)

CARDS["00-workbench"] = page(
    "Your workbench", "Section 0",
    "Six moving parts. Four are local, two hold credentials. Know which is which before you point an agent at them.",
    table(["Piece", "Job", "Holds secrets?", "Typical install"], [
        ["Editor", "Read and review code; agents live here too", "no", "<span class='mono'>VS Code / Zed / Neovim</span>"],
        ["Shell", "Run everything, including agents", "env vars only", "<span class='mono'>bash / zsh</span>"],
        ["git", "Undo button, review surface, audit trail", "no", "<span class='mono'>git --version</span>"],
        ["gh CLI", "Repos, issues, PRs, CI runs, releases", "yes (OAuth token)", "<span class='mono'>gh auth login</span>"],
        ["Runtime", "Runs your app and tests", "no", "<span class='mono'>node / python3</span>"],
        ["Agent CLI", "Reads files, edits, runs commands", "inherits both &#9888;", "<span class='mono'>npm i -g &lt;agent&gt;</span>"],
    ]) + '<div class="foot" style="border:none;padding-top:6px">Rule: the agent inherits every credential your shell has. Put the dangerous ones in a platform (Railway / Cloudflare / GitHub secrets), not in your profile.</div>',
    FOOT)

# ---- 01
CARDS["01-agent-loop"] = page(
    "The agent loop", "Section 1",
    "An agent is a loop around a model. The loop only closes when a tool returns evidence — otherwise it is guessing at the same speed it writes.",
    "".join([
        nodes([("1 Gather","read the right files, rules, docs",""),
               ("2 Plan","state the steps and the files",""),
               ("3 Act","edit, run a command, call a tool","accent"),
               ("4 Verify","test output, build log, diff","green"),
               ("5 Repeat or stop","small step, or hand back","warn")]),
        '<div class="row" style="margin-top:8px">' +
        card("Evidence > opinion", "&ldquo;Tests pass&rdquo; is a claim. <span class='mono'>pytest -q</span> output is evidence. Ask for the second one.", "accent") +
        card("Stop conditions", "Tests green, types clean, budget spent, or a decision only you can make. Write them into the rules file.", "") +
        card("Steering", "Interrupt, re-scope to one file, add a rule, or raise a gate. You are the loop's supervisor, not its passenger.", "warn") +
        "</div>"]),
    FOOT)

CARDS["01-context-window"] = page(
    "One context window, five tenants", "Section 1",
    "Everything the model knows in a single call is in here. Every token you spend on noise is a token it cannot spend on your task — and quality degrades as the window fills.",
    bars([("System prompt + tool definitions", 14, "bb", "fixed cost of the harness"),
          ("Rules file (AGENTS.md)", 8, "bg", "you control this"),
          ("Conversation history", 26, "ba", "rotting: stale plans, dead ends"),
          ("Files and tool results", 30, "bt", "the actual work"),
          ("Room left to think", 22, "bp", "reserve it")]) +
    '<div class="row" style="margin-top:10px">' +
    card("Cheapest fixes", "Shorter rules file, <span class='mono'>/clear</span> between tasks, targeted file reads, narrower tools, a docs index instead of a repo dump.", "accent") +
    card("Expensive fixes", "Retrieval, compaction, sub-agents with isolated context, and a durable skill library.", "warn") +
    "</div>",
    FOOT)

# ---- 02
CARDS["02-prompt-anatomy"] = page(
    "Anatomy of a prompt that works", "Section 2",
    "Six parts. Beginners write part 3 and wonder why the answer is wrong. The verification line is the one that saves you.",
    table(["Part", "What it is", "Example"], [
        ["1 Context", "Where we are, what exists", "<span class='mono'>FastAPI service, Postgres via SQLAlchemy, tests in pytest</span>"],
        ["2 Task", "One outcome, one sentence", "<span class='mono'>Add a GET /invoices/{id} endpoint</span>"],
        ["3 Constraints", "What must not change", "<span class='mono'>Do not touch the auth layer or the money helpers</span>"],
        ["4 Inputs", "Delimited data, not commands", "<span class='mono'>&lt;schema&gt;...&lt;/schema&gt; &lt;issue&gt;...&lt;/issue&gt;</span>"],
        ["5 Output format", "Shape of the answer", "<span class='mono'>Minimal diff + the exact test command</span>"],
        ["6 Verification", "How to prove it worked", "<span class='mono'>Run pytest tests/test_invoices.py and paste output</span>"],
    ]) + '<div class="foot" style="border:none;padding-top:6px">Long-lived parts (context, constraints) belong in AGENTS.md. Only parts 2–6 change per task.</div>',
    FOOT)

CARDS["02-context-engineering"] = page(
    "Context engineering: gather, curate, compact, hand off", "Section 2",
    "A task is not one prompt. It is a series of decisions about what the model gets to see next.",
    "".join([
        nodes([("Gather","point at files and docs, not the repo",""),
               ("Curate","keep constraints and decisions, drop transcripts","accent"),
               ("Work","small verified steps, commit checkpoints","green"),
               ("Compact","summarise state into a hand-off note","warn"),
               ("Hand off","fresh session or sub-agent starts clean","purple")]),
        '<div class="row" style="margin-top:8px">' +
        card("Keep", "Decisions made, constraints discovered, the commands that work, the next step, open questions.", "accent") +
        card("Drop", "Exploration transcripts, failed attempts, re-reads of files you already understand, the coffee-break chat.", "") +
        card("Never rely on", "What the model remembers. Files outlive sessions; conversations do not.", "warn") +
        "</div>"]),
    FOOT)

# ---- 03
CARDS["03-feature-loop"] = page(
    "The feature loop", "Section 3",
    "Explore, plan, implement in small steps, verify with evidence, commit, review. The inner cycle is where quality is made.",
    "".join([
        nodes([("Explore","read before writing",""),
               ("Plan","files, interfaces, tests, risk",""),
               ("Implement","one small step","accent"),
               ("Verify","tests, types, diff","green"),
               ("Commit","a checkpoint you can revert",""),
               ("Review","you, or a fresh reviewer","warn")]),
        '<div class="row" style="margin-top:8px">' +
        card("Why explore first", "Agents that write before reading reinvent helpers, break conventions, and touch files you did not want touched.", "accent") +
        card("Why small steps", "Each verified step is a place you can stop, revert, or hand to a human without losing the afternoon.", "") +
        card("Why commit often", "git is the undo button for agent work. A commit before a risky step turns a disaster into a reset.", "warn") +
        "</div>"]),
    FOOT)

CARDS["03-diff-size"] = page(
    "Diff size is blast radius", "Section 3",
    "Review quality falls faster than your reading speed rises. Past a few hundred lines you are approving, not reviewing.",
    bars([("1&#8211;50 lines", 22, "bg", "read every line, real review"),
          ("50&#8211;200 lines", 42, "bt", "read carefully, spot-check tests"),
          ("200&#8211;500 lines", 68, "ba", "skim &#8594; rubber stamp risk"),
          ("500+ lines", 96, "br", "&ldquo;looks fine&rdquo; &#8594; incident")]) +
    '<div class="row" style="margin-top:10px">' +
    card("How diffs get big", "One prompt for a whole feature, drive-by formatting, refactor + behaviour change in one commit, &ldquo;while I was in there&rdquo;.", "warn") +
    card("How to keep them small", "One concern per commit, forbid reformatting unrelated files, split by layer (schema, API, UI, tests), ask for the minimal patch explicitly.", "accent") +
    "</div>",
    FOOT)

# ---- 04
CARDS["04-skill-anatomy"] = page(
    "A skill: loaded only when it matters", "Section 4",
    "Progressive disclosure is the whole trick. The agent always sees the one-line description; it opens the rest only when the task matches.",
    "".join([
        '<div class="row">' +
        card("Level 1 &mdash; always visible", "<span class='mono'>name</span> + <span class='mono'>description</span> (~40 words). This is the trigger, so write it for retrieval, not for humans.", "accent") +
        card("Level 2 &mdash; loaded on match", "<span class='mono'>SKILL.md</span> body: when to use it, the procedure, the pitfalls, how to verify.", "") +
        card("Level 3 &mdash; opened on demand", "<span class='mono'>references/</span> deep docs, <span class='mono'>scripts/</span> runnable tools, <span class='mono'>templates/</span> boilerplate.", "purple") +
        "</div>",
        '<div class="card mono" style="font-size:14px;line-height:1.6"><h3 style="font-family:inherit">deploy-to-staging/</h3>'
        '&#9500;&#9472; SKILL.md &nbsp;<span class="dim">&#8592; frontmatter + steps + pitfalls</span><br>'
        '&#9500;&#9472; references/gotchas.md<br>'
        '&#9500;&#9472; scripts/smoke_test.sh &nbsp;<span class="dim">&#8592; the verification step</span><br>'
        '&#9492;&#9472; templates/rollback-plan.md</div>',
        '<div class="sub">A skill that always loads everything defeats the point; a skill whose description is vague never loads at all.</div>']),
    FOOT)

# ---- 05
CARDS["05-pipeline-gates"] = page(
    "Gates, cheapest first", "Section 5",
    "Run the fast, dumb checks on every push. Reserve the slow, expensive ones for pull requests into main and for promotion.",
    table(["Gate", "Catches", "Cost", "Run on"], [
        ["Format", "argument-by-mail review noise", "seconds", "every push"],
        ["Lint", "dead code, obvious bugs, unused imports", "seconds", "every push"],
        ["Type check", "contract drift, invented APIs", "~1 min", "every push"],
        ["Unit tests", "logic regressions", "minutes", "every push"],
        ["Secret scan", "the key someone pasted", "seconds", "every push"],
        ["Migration lint", "destructive or non-idempotent schema change", "seconds", "PRs touching SQL"],
        ["Dependency review", "known-vulnerable and hallucinated packages", "seconds", "PRs"],
        ["Integration tests", "wire formats, real database behaviour", "minutes", "PRs to main"],
        ["Build", "it compiles where you deploy", "minutes", "PRs to main"],
        ["Smoke test", "the deploy that succeeded but the app is down", "~1 min", "after every deploy"],
        ["Evals (AI features)", "quality regression after a prompt/model change", "minutes", "PRs + nightly"],
    ]),
    FOOT)

CARDS["05-promotion-flow"] = page(
    "One artefact, three environments", "Section 5",
    "Staging deploys itself. Production is a deliberate, approved act — and the database always moves before the code that needs it.",
    "".join([
        nodes([("Merge to main","reviewed + green","accent"),
               ("Auto-deploy staging","migrate &#8594; API &#8594; web &#8594; smoke",""),
               ("Verify on staging","click the real flow","green"),
               ("Approve promotion","human gate","warn"),
               ("Migrate prod DB","schema first, backward compatible","purple"),
               ("Deploy prod","same artefact, prod config",""),
               ("Verify + watch","health, logs, one real flow","green")]),
        '<div class="foot" style="border:none;padding-top:8px">The trap worth memorising: if the production service also auto-deploys from a git branch, '
        'it will race your gated pipeline and ship code ahead of its database. Pick one trigger per environment.</div>']),
    FOOT)

# ---- 06
CARDS["06-boundaries"] = page(
    "Boundaries are where bugs stop", "Section 6",
    "A boundary is a place you can change one side without breaking the other. Agents duplicate logic across missing boundaries faster than humans do.",
    "".join([
        '<div class="row">' +
        card("Edge / frontend", "Presentation only. No business rules, no direct database access, no secrets.", "") +
        card("API layer", "Auth, validation, one choke point for every response and error.", "accent") +
        card("Service layer", "Business rules, transactions, idempotency, third-party calls.", "accent") +
        card("Data layer", "Schema, constraints, migrations, row-level security.", "") +
        "</div>",
        '<div class="row" style="margin-top:8px">' +
        card("Smells", "A &ldquo;service&rdquo; file that owns everything &#183; business rules in widgets &#183; the same helper reimplemented three ways &#183; two places that format errors.", "warn") +
        card("The single-choke-point pattern", "Route every response, query and error through one function. Fix it once and every endpoint heals. Bypass it once and drift begins.", "accent") +
        "</div>"]),
    FOOT)

CARDS["06-adr-lifecycle"] = page(
    "An ADR is a decision with its reasons attached", "Section 6",
    "Written while you decide, not after. The rejected options are the valuable part — they stop the same debate from happening every quarter.",
    "".join([
        nodes([("Draft","context, options, trade-offs",""),
               ("Review in the PR","shipped with the code it governs","accent"),
               ("Accepted","immutable from here on","green"),
               ("Superseded","a new ADR replaces it","warn")]),
        '<div class="row" style="margin-top:8px">' +
        card("Write one when", "New dependency or service &#183; data model or contract change &#183; auth mechanism &#183; payment rail &#183; CI/CD pattern &#183; hosting choice.", "accent") +
        card("Skip it for", "Bug fixes, copy, minor refactors, dependency bumps, adding tests.", "") +
        card("Why agents need them", "A settled decision written down stops a fresh session from re-litigating it — and stops &ldquo;helpful&rdquo; rewrites of deliberate choices.", "purple") +
        "</div>"]),
    FOOT)

# ---- 07
CARDS["07-topology"] = page(
    "The stack that ships a small product", "Section 7",
    "Four moving parts, three providers, one rule: configuration lives outside the code, and the database moves before the API.",
    "".join([
        nodes([("Browser / app","static bundle or client",""),
               ("Edge worker","headers, routing, light auth","accent"),
               ("API service","your code, health check","accent"),
               ("Serverless Postgres","branches per environment","green"),
               ("Object storage","artefacts, downloads, backups","purple")]),
        '<div class="row" style="margin-top:8px">' +
        card("Environment variables", "Per environment, never in the repo. The deployed service holds them; your laptop does not need them.", "accent") +
        card("Migrations", "Versioned, idempotent, forward-only, applied before the deploy that needs them.", "") +
        card("Health endpoint", "First thing you write, last thing you remember to write. It is what a smoke test and a platform probe call.", "warn") +
        "</div>"]),
    FOOT)

CARDS["07-cost-tiers"] = page(
    "Where the money actually goes", "Section 7",
    "For a small product the bill is dominated by model tokens and compute, not storage. Measure cost per request before optimising anything.",
    bars([("Model tokens (input re-read each turn)", 34, "bt", "the biggest lever: context hygiene, caching, routing"),
          ("Compute / hosting", 26, "bb", "one instance, scale to zero"),
          ("GPU / batch jobs", 14, "bp", "size the GPU to the job; batch the work"),
          ("Database", 12, "bg", "storage is cheap, always-on compute is not"),
          ("Storage + egress", 8, "ba", "watch egress on files and media"),
          ("CI minutes", 6, "br", "cache, path filters, cancel stale runs")]) +
    '<div class="row" style="margin-top:10px">' +
    card("Set before you scale", "Spend alerts, hard caps, per-user quotas. A workspace that quietly meets its budget limit can have every service in it disabled at once.", "warn") +
    card("Prices change", "Free tiers, model names and per-token rates move constantly. Check the provider page the week you decide, not a blog post from last year.", "accent") +
    "</div>",
    FOOT)

# ---- 08
CARDS["08-mcp-topology"] = page(
    "MCP: a host, some clients, many servers", "Section 8",
    "MCP standardises how a model gets capabilities. It does not make those capabilities safe — the trust boundary is the part you draw yourself.",
    "".join([
        '<div class="row">' +
        card("Host", "The agent application you are talking to. Owns the conversation, the permissions and the model.", "accent") +
        arrow() +
        card("Client", "One connection per server, inside the host. Where credentials are held.", "accent") +
        arrow() +
        card("Servers", "Tools (actions), resources (readable data), prompts (templates). Local process over stdio, or a remote HTTP service.", "warn") +
        "</div>",
        '<div class="row" style="margin-top:10px">' +
        card("stdio server", "Runs on your machine with your user's permissions. Fast, simple, and as dangerous as your shell.", "warn") +
        card("Remote server", "Someone else's process holds your token. Your data leaves your network; their uptime is your problem.", "warn") +
        card("What MCP is not", "Not a sandbox, not an audit trail, not a guarantee of trust. Treat every server as third-party code with your credentials.", "bad") +
        "</div>"]),
    FOOT)

CARDS["08-mcp-risk-map"] = page(
    "MCP risk map", "Section 8",
    "Four ways a server hurts you. Each has a mitigation you can implement today — none of them is &ldquo;add a line to the system prompt&rdquo;.",
    table(["Risk", "How it works", "Mitigation"], [
        ["Tool poisoning", "Hidden instructions inside a tool's description that the model reads as orders", "Read every description; only install vetted servers; keep approval prompts on"],
        ["Rug pull / shadowing", "A server changes behaviour after approval, or impersonates another tool", "Pin versions, review updates, disable unknown tools, keep one source per capability"],
        ["Indirect injection", "Untrusted content (issue, page, row) arrives as instructions through a tool result", "Treat tool output as data; require approval for network writes and destructive calls"],
        ["Over-permission", "The server holds broad credentials and acts as a confused deputy", "Scoped, revocable tokens; read-only first; never give a server production credentials"],
    ]) + '<div class="foot" style="border:none;padding-top:8px">Blast radius = what the server can read + what it can write + what it can reach on the network. Shrink all three before you install.</div>',
    FOOT)

# ---- 09
CARDS["09-defense-in-depth"] = page(
    "Defence in depth for an agent workflow", "Section 9",
    "Assume each layer will fail once. That is not pessimism; it is why you can move fast without gambling the company.",
    table(["Layer", "Control", "Fails when"], [
        ["Input", "Treat external content as data, delimit it, never trust instructions inside it", "you paste an issue body as an order"],
        ["Identity", "Scoped, revocable, per-environment credentials", "one token opens everything"],
        ["Permission", "Read-only defaults, allow-lists, approval prompts on writes", "network and filesystem are wide open"],
        ["Execution", "Sandbox, no prod keys in the agent's shell, egress limits", "the agent runs on the box that can deploy"],
        ["Change", "Small diffs, human review, branch protection, required checks", "a green pipeline is treated as proof"],
        ["Data", "Sensitive data out of context, PII out of logs, RLS deny-by-default", "a customer row lands in a prompt"],
        ["Detection", "Audit logs of tool calls, spend alerts, anomaly review", "nobody notices for three weeks"],
        ["Recovery", "Rotation runbook, rollback plan, restore drill", "a leaked key lives for months"],
    ]),
    FOOT)

CARDS["09-supply-chain"] = page(
    "The generated-code supply chain", "Section 9",
    "A confident suggestion is not a verified dependency. Every arrow below is a place where something you did not write ends up running as you.",
    "".join([
        nodes([("Model suggests","plausible API or package name","warn"),
               ("You accept","copy, paste, install","accent"),
               ("Registry","typosquats, hallucinated names, hijacked maintainers","bad"),
               ("Your build","lockfile, transitive deps, postinstall scripts","warn"),
               ("CI","actions with mutable tags, secrets in env","bad"),
               ("Production","runs with your credentials and your data","")]),
        '<div class="row" style="margin-top:8px">' +
        card("Verify every dependency", "Does it exist, is it the one you meant, who maintains it, when was the last release, does the licence fit?", "accent") +
        card("Pin and lock", "Lockfiles committed, actions pinned to a commit SHA, versions pinned in the build.", "") +
        card("Least privilege in CI", "Read-only default token, no secrets on fork PRs, review workflow changes like code that runs as you.", "warn") +
        "</div>"]),
    FOOT)

# ---- 10
_pyramid = bars([("Smoke (deployed env)", 8, "ba", "is it up? 60 seconds"),
                 ("End-to-end (critical flows)", 14, "br", "expensive, brittle, few"),
                 ("Integration (real DB, real wire)", 30, "bt", "where the real bugs live"),
                 ("Unit (logic, fast, many)", 48, "bg", "cheap, fast, most of the suite")])
CARDS["10-test-pyramid"] = page(
    "The test pyramid, priced", "Section 10",
    "More unit tests, fewer end-to-end tests, and one smoke test that proves the deployed thing is alive.",
    "".join([_pyramid,
             '<div class="row" style="margin-top:10px">' +
             card("Test behaviour, not implementation", "Tests that break on every refactor train you to delete tests. Assert on what the user or caller observes.", "accent") +
             card("Fixtures that lie", "Never mock the database you actually use or the format you actually send — that is how a green suite hides a broken contract.", "warn") +
             "</div>"]),
    FOOT)

CARDS["10-eval-loop"] = page(
    "The eval loop for AI features", "Section 10",
    "Non-deterministic features need a different harness: a dataset, a scorer, a threshold, and a trend you actually look at.",
    "".join([
        nodes([("Collect failures","real questions users asked",""),
               ("Label","what a good answer looks like",""),
               ("Score","faithfulness, relevance, retrieval","accent"),
               ("Gate CI","must not drop below baseline","green"),
               ("Monitor prod","sample, log, alert","warn"),
               ("Re-collect","new failures become new cases","purple")]),
        '<div class="row" style="margin-top:8px">' +
        card("30&#8211;100 cases", "A small, maintained eval set beats thousands of examples nobody updates. Re-run it whenever the prompt or model changes.", "accent") +
        card("Canaries", "Questions with a known correct answer that the system must not hallucinate — the cheapest hallucination alarm there is.", "") +
        card("Cost is a quality metric", "Track latency and tokens per request alongside accuracy; a brilliant answer in 40 seconds that costs a dollar may still be a failure.", "warn") +
        "</div>"]),
    FOOT)

# ---- 11
CARDS["11-docs-map"] = page(
    "Which document answers which question", "Section 11",
    "If you cannot say where a fact lives, it will live in three places and be wrong in two of them.",
    table(["Question", "Document"], [
        ["What is this and how do I run it?", "README"],
        ["How do I set up, test and ship?", "docs/developer-guide.md"],
        ["What are the parts and how do they talk?", "docs/architecture.md + diagrams"],
        ["Is there an endpoint for X?", "docs/api.md"],
        ["What columns does that table have?", "docs/database.md"],
        ["Why is it built this way?", "docs/decisions/ (ADRs)"],
        ["Why did the deploy fail at 2am?", "docs/runbooks/ + docs/gotchas.md"],
        ["What changed in v1.4?", "CHANGELOG + releases"],
        ["What should the agent never do here?", "AGENTS.md + skills"],
    ]) + '<div class="foot" style="border:none;padding-top:6px">A feature is not done until the row that would have confused someone has been updated.</div>',
    FOOT)

# ---- 12
CARDS["12-rules-stack"] = page(
    "The rules stack: put each instruction in the cheapest layer that works", "Section 12",
    "Same instruction, five possible homes. Choosing wrong is why rules get ignored, skills bloat, and mistakes repeat.",
    table(["Layer", "Loaded", "Cost of a mistake here", "Use it for"], [
        ["AGENTS.md / CLAUDE.md", "every session", "always occupies context", "stack facts, real commands, conventions, hard never-dos"],
        ["Skill (SKILL.md)", "when relevant", "invisible if the description is vague", "procedures: deploy, migrate, review, release"],
        ["Hook / pre-commit", "deterministically, every time", "friction if too aggressive", "formatting, protected paths, secret scanning"],
        ["CI gate", "on every push/PR", "slow pipelines if overused", "tests, types, build, dependency and migration checks"],
        ["ADR", "when a human or agent asks why", "none until someone re-litigates", "settled decisions and their trade-offs"],
        ["SOP / runbook", "when the operation happens", "stale steps are worse than none", "rare, risky procedures with an owner and a review date"],
    ]) + '<div class="foot" style="border:none;padding-top:8px">Escalation rule: if a rule is violated twice, move it down the stack — into a hook or a gate that cannot be forgotten.</div>',
    FOOT)

# ---- 13
CARDS["13-issue-flow"] = page(
    "From idea to released change, linked end to end", "Section 13",
    "Every artefact points at the one before it. Six months later that chain is the only reliable answer to &ldquo;why is this here?&rdquo;",
    "".join([
        nodes([("Idea / bug","reported, triaged",""),
               ("Issue","problem + acceptance criteria","accent"),
               ("ADR","if it is expensive to reverse","purple"),
               ("Branch + PR","small, reviewed, checks green",""),
               ("Changelog","human words, newest first",""),
               ("Tag / release","one version, one artefact",""),
               ("Deploy","staging, then gated production","green")]),
        '<div class="row" style="margin-top:8px">' +
        card("What links what", "PR says <span class='mono'>Closes #12</span>; the ADR is named in the PR body; the changelog names the release; the release names the tag.", "accent") +
        card("Why it pays", "Bisecting a regression, answering audit questions, onboarding, and giving an agent the exact spec it should implement against.", "") +
        "</div>"]),
    FOOT)


def build():
    chrome = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    if not chrome:
        sys.exit("No Chrome/Chromium found on PATH.")
    os.makedirs(OUT, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="infographic-")
    ok = 0
    for name, html in sorted(CARDS.items()):
        hp = os.path.join(tmp, name + ".html")
        open(hp, "w").write(html)
        png = os.path.join(OUT, name + ".png")
        r = subprocess.run([chrome, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                            f"--window-size={W},{H}", "--force-device-scale-factor=1",
                            f"--screenshot={png}", "file://" + hp],
                           capture_output=True, text=True, timeout=120)
        if os.path.exists(png) and os.path.getsize(png) > 5000:
            ok += 1
            print(f"  ok   {name}.png  {os.path.getsize(png)//1024} KB")
        else:
            print(f"  FAIL {name}: {r.stderr.strip()[:200]}")
    print(f"{ok}/{len(CARDS)} infographics written to {OUT}")

    # The social card: same renderer, different canvas.
    hp = os.path.join(tmp, "og-card.html")
    open(hp, "w").write(OG_HTML)
    png = os.path.join(OUT, "og-card.png")
    r = subprocess.run([chrome, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                        f"--window-size={SOCIAL_W},{SOCIAL_H}", "--force-device-scale-factor=1",
                        f"--screenshot={png}", "file://" + hp],
                       capture_output=True, text=True, timeout=120)
    social_ok = os.path.exists(png) and os.path.getsize(png) > 5000
    print(f"  {'ok  ' if social_ok else 'FAIL'} og-card.png (social preview)")
    return 0 if ok == len(CARDS) and social_ok else 1


if __name__ == "__main__":
    sys.exit(build())