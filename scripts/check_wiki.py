#!/usr/bin/env python3
"""Check the wiki before it ships.

This is the gate the wiki describes in its own CI section: cheap, deterministic, and
specific about what it catches. It runs offline (no network), so it is safe in CI.

    python3 scripts/check_wiki.py            # report, exit 1 on errors
    python3 scripts/check_wiki.py --strict   # also fail on warnings

Checks
  1. Every page listed in WIKI-MANIFEST.md exists, and no orphan lesson pages exist.
  2. No H1 in a page body (the wiki renders the page title itself).
  3. The metadata blockquote is present, and Key takeaways / Further learning are present.
  4. Prose word count is inside the house budget (400-1400 words, code fences excluded).
  5. Every internal link [text](Page-Name) resolves to a real page.
  6. Every embedded asset URL points at a file that exists in assets/.
  7. Mermaid blocks are balanced, use an allowed diagram type, and are not empty.
  8. No banned hype words, and no accidental secrets.
"""
import os, re, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIKI = os.path.join(ROOT, "wiki")
ASSETS = os.path.join(ROOT, "assets")
MANIFEST = os.path.join(ROOT, "WIKI-MANIFEST.md")

BANNED = ["delve", "leverage", "seamless", "game-changer", "supercharge", "empower",
          "unlock the", "in today's fast-paced"]
SECRET_PATTERNS = [
    (r"\bsk-[A-Za-z0-9]{16,}", "looks like an API key"),
    (r"\bgh[pousr]_[A-Za-z0-9]{20,}", "looks like a GitHub token"),
    (r"\bAKIA[0-9A-Z]{12,}", "looks like an AWS access key id"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "private key block"),
    (r"\beyJ[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{20,}\.", "looks like a JWT"),
    (r"\bwhsec_[A-Za-z0-9]{16,}", "looks like a webhook signing secret"),
]
MERMAID_OK = {"flowchart", "graph", "sequencediagram", "statediagram-v2", "erdiagram",
              "classdiagram", "gantt", "timeline", "pie", "journey", "gitgraph"}
ASSET_URL = re.compile(r"raw\.githubusercontent\.com/BongweKE/ai-coding-wiki/main/assets/([A-Za-z0-9._-]+)")
LINK = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)\s]+)\)")
# Pages that exist in the wiki under a different name than in wiki/ (the wiki landing page).
ALIASES = {"Home": "00-Home.md", "_Sidebar": "_Sidebar.md", "_Footer": "_Footer.md"}

# Pages where a diagram would be decoration rather than teaching: exercises
# (they drive the reader through the lessons that already have the diagrams)
# and pure lookup/reference pages. Keep this list short and justified.
DIAGRAM_EXEMPT_SUFFIXES = ("-Exercises.md",)
DIAGRAM_EXEMPT_PAGES = {
    "00-Glossary.md",              # definitions lookup
    "00-How-To-Use-This-Wiki.md",  # orientation page
    "15-Further-Learning.md",      # link list
    "16-Link-Index.md",            # link list
}


def DIAGRAM_EXEMPT(name):
    return name in DIAGRAM_EXEMPT_PAGES or name.endswith(DIAGRAM_EXEMPT_SUFFIXES)


errors, warnings = [], []


def err(page, msg):
    errors.append(f"{page}: {msg}")


def warn(page, msg):
    warnings.append(f"{page}: {msg}")


def manifest_pages():
    """Lesson filenames from the manifest table rows."""
    out = set()
    if not os.path.exists(MANIFEST):
        return out
    for line in open(MANIFEST, encoding="utf-8"):
        m = re.match(r"\|\s*\d+\s*\|.*?`([A-Za-z0-9._-]+\.md)`", line)
        if m:
            out.add(m.group(1))
    return out


SECTION_INDEX = re.compile(r"^> \*\*Section \d+ · (?![^ ]*Lesson)[^*]*\*\* —")


def index_pages():
    """Generated pages (Home + section indexes) that are exempt from the lesson skeleton.

    Detect them by content, not by filename. A section index opens with an overview
    blockquote ('> **Section 5 · Git & CI/CD** - ...'); a lesson page carries
    '> **Section 05 · Lesson 3** · Level: ...'. Matching on the filename instead
    exempted every page in the wiki (every lesson file also starts 'NN-Capital'),
    which silently disabled the skeleton, word-budget, internal-link, mermaid and
    banned-word checks for 138 of 141 lesson pages.
    """
    exempt = {"00-Home.md", "_Sidebar.md", "_Footer.md"}
    for f in os.listdir(WIKI) if os.path.isdir(WIKI) else []:
        if not f.endswith(".md"):
            continue
        with open(os.path.join(WIKI, f), encoding="utf-8") as fh:
            if SECTION_INDEX.match(fh.readline()):
                exempt.add(f)
    return exempt


def section_indexes(pages):
    """Pages that open with a section overview blockquote rather than a lesson one."""
    out = []
    for f in pages:
        if SECTION_INDEX.match(open(os.path.join(WIKI, f), encoding="utf-8").readline()):
            out.append(f)
    return out


def check_manifest_counts(mp, pages):
    """The manifest's own numbering line must match the tree (it drifted once:
    it claimed 20 section indexes when the tree had 17)."""
    line = None
    for l in open(MANIFEST, encoding="utf-8"):
        if l.startswith("Total pages:"):
            line = l.strip()
            break
    if line is None:
        err("WIKI-MANIFEST.md", "no 'Total pages:' line")
        return
    m = re.match(r"Total pages:\s*(\d+)\s+lessons\s*\+\s*(\d+)\s+section indexes", line)
    if not m:
        err("WIKI-MANIFEST.md", f"unrecognised page count line: {line!r}")
        return
    want_lessons, want_indexes = int(m.group(1)), int(m.group(2))
    have_lessons = len(mp)
    have_indexes = len(section_indexes(pages))
    if want_lessons != have_lessons:
        err("WIKI-MANIFEST.md", f"says {want_lessons} lessons, the manifest tables list {have_lessons}")
    if want_indexes != have_indexes:
        err("WIKI-MANIFEST.md", f"says {want_indexes} section indexes, the tree has {have_indexes}")
    if "Home" not in line:
        warn("WIKI-MANIFEST.md", f"page count line does not mention Home: {line!r}")


def prose_words(text):
    stripped = re.sub(r"```.*?```", "", text, flags=re.S)
    stripped = re.sub(r"^\s*\|.*$", "", stripped, flags=re.M)   # tables are not prose
    stripped = re.sub(r"^\s*[-#>\d]+[.)]?\s*", "", stripped, flags=re.M)
    return len([w for w in re.split(r"\s+", stripped) if w.strip()])


def check_page(path, name, exempt):
    text = open(path, encoding="utf-8").read()
    # prose = the page minus fenced code blocks, so shell comments (# ...) are not read as headings
    prose = re.sub(r"```.*?```", "", text, flags=re.S)
    lines = prose.splitlines()

    # 2. no H1 (Home is the one page allowed a title, since it is the wiki landing page)
    if name != "00-Home.md":
        for i, l in enumerate(lines):
            if re.match(r"^#(?!#)\s", l):
                err(name, f"H1 found in prose (line {i+1} of the prose): the wiki renders the page title already")
                break

    if name not in exempt:
        # 3. metadata + closing sections
        if not lines or not lines[0].startswith("> **Section"):
            err(name, "first line must be the metadata blockquote starting with '> **Section'")
        for required in ("## Key takeaways", "## Further learning"):
            if required not in text:
                err(name, f"missing required section: {required}")
        if "## Try it" not in text:
            warn(name, "no '## Try it' section — every page should have one runnable step")
        if "## Common mistakes" not in text:
            warn(name, "no '## Common mistakes' section")
        # 4. length
        w = prose_words(text)
        if w < 400:
            err(name, f"only {w} words of prose (house minimum is 400)")
        elif w > 1400:
            warn(name, f"{w} words of prose (house maximum is 1400 — consider splitting)")
        # diagrams promised vs delivered. Exercise pages and lookup/reference
        # pages are exempt: they point at the lessons that carry the mental
        # model, and a diagram there is filler. Everything else must show one.
        if "```mermaid" not in text and "png)" not in text and not DIAGRAM_EXEMPT(name):
            warn(name, "no diagram and no infographic")

    # 5. internal links resolve
    for label, target in LINK.findall(text):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        if target.endswith(".md"):
            err(name, f"internal link must use the wiki page name, not a filename: {target}")
            continue
        if target.startswith("images/"):
            continue
        if target in ALIASES:
            continue
        if not os.path.exists(os.path.join(WIKI, target + ".md")):
            err(name, f"link to missing page: [{label}]({target})")

    # 6. assets exist
    for asset in ASSET_URL.findall(text):
        if not os.path.exists(os.path.join(ASSETS, asset)):
            err(name, f"embedded asset does not exist: assets/{asset}")

    # 7. mermaid blocks (ignore inline code spans so prose like ` ```mermaid ` is not counted)
    fences = re.sub(r"(?<!`)`{1,2}(?!`)[^`\n]*?`{1,2}(?!`)", "", text)  # inline spans only, not ``` fences
    blocks = re.findall(r"```mermaid\n(.*?)```", fences, flags=re.S)
    if fences.count("```mermaid") != len(blocks):
        err(name, "unbalanced ```mermaid fence (opened but never closed)")
    for b in blocks:
        first = b.strip().splitlines()[0].strip().lower() if b.strip() else ""
        kind = first.split()[0] if first else ""
        if kind not in MERMAID_OK:
            err(name, f"mermaid block starts with unsupported type '{first[:40]}'")
        if "%%{init" in b or re.search(r"^\s*click\s", b, flags=re.M):
            err(name, "mermaid uses an init directive or click handler (do not)")
        if len(re.findall(r"^\s*[A-Za-z_][A-Za-z0-9_]*\s*[\[\(]", b, flags=re.M)) > 20:
            warn(name, "mermaid diagram looks large (over 20 nodes)")

    # 8. banned words in prose + secrets anywhere (a secret in a code block is still a secret)
    low = prose.lower()
    for w in BANNED:
        if re.search(r"\b" + re.escape(w), low):
            warn(name, f"banned hype word: '{w}'")
    for pat, what in SECRET_PATTERNS:
        m = re.search(pat, text)
        if m:
            err(name, f"{what} — never commit anything resembling a real credential ({m.group(0)[:12]}…)")


def main():
    strict = "--strict" in sys.argv
    if not os.path.isdir(WIKI):
        sys.exit("no wiki/ directory found")
    mp, exempt = manifest_pages(), index_pages()
    pages = sorted(f for f in os.listdir(WIKI) if f.endswith(".md"))
    for p in pages:
        check_page(os.path.join(WIKI, p), p, exempt)

    # 1. manifest coverage (both ways)
    for missing in sorted(mp - set(pages)):
        errors.append(f"manifest lists {missing} but the file does not exist")
    for orphan in sorted(set(pages) - mp - exempt):
        if re.match(r"^\d\d-", orphan):
            errors.append(f"{orphan} is not in WIKI-MANIFEST.md (orphan page)")
        else:
            warnings.append(f"{orphan} is not in WIKI-MANIFEST.md")
    check_manifest_counts(mp, pages)

    print(f"checked {len(pages)} pages · {len(mp)} in manifest · {len(errors)} errors · {len(warnings)} warnings")
    for e in errors:
        print(f"  ERROR   {e}")
    for w in warnings:
        print(f"  warning {w}")
    if errors or (strict and warnings):
        return 1
    print("wiki OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
