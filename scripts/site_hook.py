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


def on_page_markdown(markdown, page, config, files):
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
