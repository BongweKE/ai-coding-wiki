#!/usr/bin/env python3
"""Generate llms.txt — a crawlable index of every lesson, for AI agents.

    python3 scripts/gen_llms_txt.py > site-src/llms.txt

A good share of this wiki's readers are AI agents fetching pages on a
person's behalf. llmstxt.org defines the file they read first: an H1, a
one-line blockquote summary, then sections of `- [label](url)` links.

Everything is derived from existing sources, so it cannot drift:
  * title and summary come from site_name / site_description in mkdocs.yml
  * sections and lessons come from wiki/_Sidebar.md — the wiki navigation,
    in the same order readers see
  * each link's description is the level and reading time from the page's
    own metadata blockquote

Wiki page names map to URLs the way the site serves them
(use_directory_urls): Page-Name -> <base>/Page-Name/, Home -> the root.
"""
import os
import re

FALLBACK_BASE = "https://vibe.bongwe.space/"

H1 = re.compile(r"^#+\s")
SECTION = re.compile(r"^\*\*\[([^\]]+)\]\(([^)]+)\)\*\*$")
LESSON = re.compile(r"^-\s+\[([^\]]+)\]\(([^)]+)\)$")
ANY_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
META_LINE = re.compile(r"^>\s*\*\*(?P<label>[^*]+)\*\*(?P<rest>.*)$")


def mkdocs_string(key):
    """A top-level `key: value` (or folded `>-` block) from mkdocs.yml.

    Read with a regex rather than a YAML parser: mkdocs.yml uses
    `!!python/name:` tags, which a safe loader refuses.
    """
    try:
        text = open("mkdocs.yml", encoding="utf-8").read()
    except OSError:
        return ""
    m = re.search(rf"^{key}:\s*(.*)$", text, re.M)
    if not m:
        return ""
    value = m.group(1).strip()
    if value in (">-", ">", "|", "|-"):
        # Folded scalar: the indented lines that follow, up to the next
        # top-level key, joined with single spaces.
        lines = []
        for line in text[m.end():].splitlines():
            if line and not line.startswith((" ", "\t")):
                break
            lines.append(line.strip())
        return " ".join(lines).strip()
    return value.strip("'\"")


def page_url(base, target):
    if target in ("Home", "00-Home"):
        return base
    return base + target + "/"


def page_description(name):
    """'beginner, ~12 min read' from the page's metadata blockquote, or ''."""
    if name in ("Home", "00-Home"):
        name = "00-Home"
    try:
        with open(os.path.join("wiki", name + ".md"), encoding="utf-8") as f:
            first = f.readline()
    except OSError:
        return ""
    m = META_LINE.match(first)
    if not m:
        return ""
    parts = []
    level = re.search(r"Level:\s*(\w+)", m.group("rest"))
    minutes = re.search(r"~(\d+)\s*min", m.group("rest"))
    if level:
        parts.append(level.group(1))
    if minutes:
        parts.append(f"~{minutes.group(1)} min read")
    if parts:
        return ", ".join(parts)
    # Overview pages have no level or reading time, but their metadata line
    # carries a one-line subtitle after an em dash:
    #   > **Section 0 · Start Here** — What AI coding actually is, …
    subtitle = re.match(r"\s*[—–-]\s*(.+?)\s*$", m.group("rest"))
    if subtitle:
        text = subtitle.group(1)
        if len(text) > 120:
            text = text[:120].rsplit(" ", 1)[0].rstrip(",;:") + "…"
        return text
    return ""


def parse_sidebar(base, sidebar):
    """(orientation links, [(heading, [(label, url, name), ...]), ...]).

    The sidebar's shape, fixed by check_wiki.py:
      ### Title                       <- the site name, not a section
      **[Home](Home)** · [a](A) · …   <- orientation line
      ---                             <- separator
      **[0. Start Here](00-Start-Here)**   <- a section (a page too)
      - [Lesson](01-Lesson)           <- lessons
    """
    orientation, sections = [], []
    for line in sidebar.splitlines():
        line = line.rstrip()
        if not line or line == "---" or H1.match(line):
            continue
        m = SECTION.match(line)
        if m:
            # The section line links the section's own overview page —
            # the same page mkdocs.yml's nav labels "Overview".
            sections.append((m.group(1), []))
            sections[-1][1].append(("Overview", page_url(base, m.group(2)), m.group(2)))
            continue
        m = LESSON.match(line)
        if m and sections:
            sections[-1][1].append((m.group(1), page_url(base, m.group(2)), m.group(2)))
            continue
        if line.startswith("**[") and not sections:
            # The orientation line above the first section.
            for label, target in ANY_LINK.findall(line):
                orientation.append((label, page_url(base, target), target))
    return orientation, sections


def main():
    base = mkdocs_string("site_url") or FALLBACK_BASE
    if not base.endswith("/"):
        base += "/"
    title = mkdocs_string("site_name") or "Coding With AI in the New Age"
    summary = mkdocs_string("site_description")
    repo = mkdocs_string("repo_url")

    with open(os.path.join("wiki", "_Sidebar.md"), encoding="utf-8") as f:
        sidebar = f.read()
    orientation, sections = parse_sidebar(base, sidebar)

    out = [f"# {title}", ""]
    if summary:
        out += [f"> {summary}", ""]
    if repo:
        out += [f"Repo: {repo}"]
    out += [f"Site: {base}", ""]

    def emit(links):
        for label, url, name in links:
            desc = page_description(name)
            suffix = f": {desc}" if desc else ""
            out.append(f"- [{label}]({url}){suffix}")
        out.append("")

    if orientation:
        out += ["## Orientation", ""]
        emit(orientation)
    for heading, links in sections:
        out += [f"## {heading}", ""]
        emit(links)

    print("\n".join(out).rstrip() + "\n")


if __name__ == "__main__":
    main()
