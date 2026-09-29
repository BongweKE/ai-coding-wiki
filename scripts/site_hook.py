#!/usr/bin/env python3
"""MkDocs hook: rewrite GitHub-wiki-style links so MkDocs can resolve them.

wiki/ pages link to each other by wiki page name, [label](Page-Name),
with no .md extension. That is the format check_wiki.py enforces and
the GitHub wiki expects — but MkDocs does not resolve it. This hook
rewrites the link target to the page's source filename at build time,
so wiki/ stays byte-identical to what scripts/push_wiki.sh syncs to
the GitHub wiki.

The rewrite stops at the source filename on purpose: MkDocs then
validates the link against the file list and generates the URL itself
(so use_directory_urls decides the shape), and the `validation:` block
in mkdocs.yml reports any target that really does not exist. Rewriting
straight to a .html URL instead makes MkDocs' validator report all 800+
links as "not found among documentation files", because it resolves
links against the source tree.

Special cases:
  Home, 00-Home  -> index.md, the site landing page (wiki/00-Home.md)
  _Sidebar, _Footer -> wiki-only chrome; rendered as plain text
"""
import os
import re

LINK = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)\s]+)\)")
META = re.compile(r"^> \*\*(?P<label>[^*]+)\*\*(?P<rest>.*)$")
WHY = re.compile(r"^## Why this matters\s*\n+(?P<para>.+?)(?:\n\s*\n|\Z)", re.S | re.M)


def _page_description(markdown, config):
    """A search-result-sized description for <meta name="description">.

    Built from the metadata blockquote (level + reading time) plus the first
    sentence of 'Why this matters', so every page gets a real description
    instead of the site-wide one.
    """
    first = (markdown.splitlines() or [""])[0]
    m = META.match(first)
    if not m:
        return None
    facts = [m.group("label").strip()]
    level = re.search(r"Level:\s*(beginner|intermediate|advanced)", m.group("rest"))
    minutes = re.search(r"~(\d+)\s*min", m.group("rest"))
    if level:
        facts.append(level.group(1))
    if minutes:
        facts.append(f"~{minutes.group(1)} min read")
    prefix = " · ".join(facts)

    why = WHY.search(markdown)
    sentence = ""
    if why:
        text = re.sub(r"\s+", " ", why.group("para")).strip()
        text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)   # links -> their label
        text = re.sub(r"[*`]", "", text)
        cut = text.find(". ")
        if cut > 0:
            text = text[: cut + 1]
        sentence = text

    description = f"{prefix}. {sentence}".strip() if sentence else prefix
    if len(description) > 158:
        description = description[:158].rsplit(" ", 1)[0].rstrip(",;:") + "…"
    return description


def on_page_markdown(markdown, page, config, files):
    # Markdown metadata is off in mkdocs.yml, so the per-page description is
    # set here, where the raw page text is still available.
    # overrides/main.html reads it for the search results and link previews.
    if page is not None and getattr(page, "meta", None) is not None:
        if not page.meta.get("description"):
            description = _page_description(markdown, config)
            if description:
                page.meta["description"] = description

    # MkDocs >= 1.5: File.name has no extension ("01-The-Agent-Loop"), so the
    # wiki page name has to come from src_uri ("01-The-Agent-Loop.md").
    pages = set()
    for f in files:
        if f.is_documentation_page() and f.src_uri.endswith(".md"):
            pages.add(os.path.basename(f.src_uri)[:-3])
    pages.update({"Home", "00-Home"})

    def repl(m):
        label, target = m.group(1), m.group(2)
        if target.startswith(("http://", "https://", "#", "mailto:")):
            return m.group(0)
        base, _, anchor = target.partition("#")
        if base in ("_Sidebar", "_Footer"):
            return label
        if base.endswith(".md") or base not in pages:
            # Already a filename, or not a wiki page: leave it for the
            # validator to judge rather than guessing a target.
            return m.group(0)
        name = "index.md" if base in ("Home", "00-Home") else base + ".md"
        suffix = "#" + anchor if anchor else ""
        return "[" + label + "](" + name + suffix + ")"

    return LINK.sub(repl, markdown)


def on_post_page(output, page, config):
    """Opt-in analytics: one script tag, no cookies, no third parties by default.

    Set `extra.analytics_code` in mkdocs.yml (the GoatCounter site code) to
    switch it on; empty means nothing is injected at all.
    """
    code = (config.get("extra") or {}).get("analytics_code") or ""
    code = str(code).strip()
    if not code or "</body>" not in output:
        return output
    snippet = (
        f'<script data-goatcounter="https://{code}.goatcounter.com/count" '
        'async src="https://gc.zgo.at/count.js"></script>\n'
    )
    return output.replace("</body>", snippet + "</body>", 1)
