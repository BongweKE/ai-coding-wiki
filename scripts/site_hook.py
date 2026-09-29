#!/usr/bin/env python3
"""MkDocs hook: rewrite GitHub-wiki-style links to site URLs.

wiki/ pages link to each other by wiki page name, [label](Page-Name),
with no .md extension. That is the format check_wiki.py enforces and
the GitHub wiki expects — but MkDocs cannot resolve it. This hook
rewrites the links at build time, so wiki/ stays byte-identical to
what scripts/push_wiki.sh syncs to the GitHub wiki.

Special cases:
  Home, 00-Home -> the site landing page (index.html)
  _Sidebar, _Footer -> wiki chrome; rendered as plain text
"""
import re

LINK = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)\s]+)\)")


def on_page_markdown(markdown, page, config, files):
    urls = {}
    for f in files:
        if f.name.endswith(".md"):
            urls[f.name[:-3]] = f.url
    urls["Home"] = urls.get("index", "index.html")
    urls["00-Home"] = urls["Home"]

    def repl(m):
        label, target = m.group(1), m.group(2)
        if target.startswith(("http://", "https://", "#", "mailto:")):
            return m.group(0)
        base, _, anchor = target.partition("#")
        if base.endswith(".md"):
            base = base[:-3]
        if base in ("_Sidebar", "_Footer"):
            return label
        if base in urls:
            suffix = "#" + anchor if anchor else ""
            return "[" + label + "](" + urls[base] + suffix + ")"
        return m.group(0)

    return LINK.sub(repl, markdown)
