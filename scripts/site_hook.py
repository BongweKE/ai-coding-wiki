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

Infographics: wiki/ embeds them as raw.githubusercontent.com URLs
(the form check_wiki.py's asset check expects). This hook rewrites those
embeds to the first-party copies under assets/ that
scripts/build_site.sh stages: same origin as the page (no extra
DNS+TLS hop to a third party), edge-cached for far longer than the five
minutes raw.githubusercontent.com allows, and resolvable by MkDocs'
validator. on_post_page then adds width/height (reserved layout space,
so no shift when the image arrives), async decoding, and lazy loading
for every image after the first — the first stays eager because it is
usually the largest thing on the page.
"""
import os
import re

LINK = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)\s]+)\)")
META = re.compile(r"^> \*\*(?P<label>[^*]+)\*\*(?P<rest>.*)$")
WHY = re.compile(r"^## Why this matters\s*\n+(?P<para>.+?)(?:\n\s*\n|\Z)", re.S | re.M)

# The raw-asset embeds wiki/ uses (see check_wiki.py's ASSET_URL).
RAW_ASSET = re.compile(
    r"!\[([^\]]*)\]\(https://raw\.githubusercontent\.com/"
    r"BongweKE/ai-coding-wiki/main/assets/([A-Za-z0-9._-]+)\)"
)
# <img> tags in built HTML whose src points at a staged first-party asset.
IMG_TAG = re.compile(r"<img\b[^>]*>")
IMG_ASSET_SRC = re.compile(r'\bsrc="[^"]*assets/([A-Za-z0-9._-]+)"')

_PNG_SIZE = {}


def _png_size(name):
    """(width, height) of assets/<name>, parsed straight from the PNG header.

    Returns None when the file is missing or not a PNG — the annotation is
    then skipped rather than the build broken (check_wiki.py already gates
    that every embedded asset exists).
    """
    if name not in _PNG_SIZE:
        _PNG_SIZE[name] = None
        try:
            with open(os.path.join("assets", name), "rb") as f:
                header = f.read(24)
        except OSError:
            return None
        if len(header) == 24 and header[:8] == b"\x89PNG\r\n\x1a\n":
            import struct

            _PNG_SIZE[name] = struct.unpack(">II", header[16:24])
    return _PNG_SIZE[name]


def _annotate_images(output):
    """Add dimensions and loading hints to first-party content images.

    width/height on the <img> reserves the layout box before the image
    arrives (the CLS fix); decoding="async" keeps decode off the main
    thread; images after the first also load="lazy". The first image on
    a page stays eager: it is commonly the LCP element, and lazy-loading
    the LCP is a regression, not an optimisation.
    """
    seen = 0

    def repl(m):
        nonlocal seen
        tag = m.group(0)
        src = IMG_ASSET_SRC.search(tag)
        if not src or "width=" in tag or "loading=" in tag:
            return tag
        seen += 1
        size = _png_size(src.group(1))
        extra = ' decoding="async"'
        if seen > 1:
            extra += ' loading="lazy"'
        if size:
            extra = f' width="{size[0]}" height="{size[1]}"' + extra
        end = re.search(r"\s*/?>$", tag)
        if not end:
            return tag
        return tag[: end.start()] + extra + end.group(0)

    return IMG_TAG.sub(repl, output)


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

    # Infographics: third-party raw URLs -> the staged first-party copies.
    markdown = RAW_ASSET.sub(
        lambda m: f"![{m.group(1)}](assets/{m.group(2)})", markdown
    )

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
    """Output-side fixes: image annotations, then opt-in analytics.

    Analytics: one script tag, no cookies, no third parties by default.
    Set `extra.analytics_code` in mkdocs.yml (the GoatCounter site code) to
    switch it on; empty means nothing is injected at all.
    """
    output = _annotate_images(output)

    code = (config.get("extra") or {}).get("analytics_code") or ""
    code = str(code).strip()
    if not code or "</body>" not in output:
        return output
    snippet = (
        f'<script data-goatcounter="https://{code}.goatcounter.com/count" '
        'async src="https://gc.zgo.at/count.js"></script>\n'
    )
    return output.replace("</body>", snippet + "</body>", 1)
