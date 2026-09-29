#!/usr/bin/env python3
"""Check the built site: every internal link must resolve to a real file.

    python3 scripts/check_site.py           # check site/ (the default output dir)
    python3 scripts/check_site.py _out/     # check another directory

This is the output-side companion to scripts/check_wiki.py. check_wiki.py
validates the source pages (wiki-style links, assets, structure); this script
validates what MkDocs actually wrote, which is the only place a broken
rewrite is visible. It exists because the build shipped once with 828
internal links left unrewritten by scripts/site_hook.py — a
source-only check cannot see that.

Rules:
  * http(s), mailto, tel, javascript: and bare "#" links are skipped.
  * A relative target must exist in the output directory, with or without
    the fragment. A directory target must hold an index.html.
  * Fragments (#anchor) are not verified: MkDocs already validates anchors
    through the `validation:` block in mkdocs.yml.
  * Every local <img src> and <script src> must exist too.

Exits non-zero on the first failure set, so CI fails the build.
"""
import os
import re
import sys

SKIP_SCHEMES = ("http://", "https://", "mailto:", "tel:", "javascript:", "data:", "//")
ATTR = re.compile(r'<(?:a|img|script|link)\b[^>]*?\b(?:href|src)="([^"]*)"', re.I)


def local_targets(path):
    html = open(path, encoding="utf-8", errors="replace").read()
    for raw in ATTR.findall(html):
        url = raw.strip()
        if not url or url.startswith("#") or url.startswith(SKIP_SCHEMES):
            continue
        yield url


def resolves(site_dir, page_path, url, base_path="/"):
    target = url.split("#", 1)[0].split("?", 1)[0]
    if not target:
        return True
    if target.startswith("/"):
        # MkDocs writes site_url-absolute links (404.html, sitemap); strip the
        # base path the site is published under (e.g. /ai-coding-wiki/) before
        # looking the file up inside the output directory.
        rel = target[len(base_path):] if base_path != "/" and target.startswith(base_path) else target.lstrip("/")
        fs = os.path.join(site_dir, rel)
    else:
        fs = os.path.normpath(os.path.join(os.path.dirname(page_path), target))
    if os.path.isfile(fs):
        return True
    if os.path.isdir(fs) and os.path.isfile(os.path.join(fs, "index.html")):
        return True
    return False


def site_base_path():
    """The path prefix the site is published under, from site_url in mkdocs.yml.

    Read with a regex rather than a YAML parser: mkdocs.yml uses
    `!!python/name:` tags, which a safe loader refuses.
    """
    from urllib.parse import urlparse

    try:
        text = open("mkdocs.yml", encoding="utf-8").read()
    except OSError:
        return "/"
    m = re.search(r"^site_url:\s*(\S+)\s*$", text, re.M)
    if not m:
        return "/"
    path = urlparse(m.group(1)).path or "/"
    return path if path.endswith("/") else path + "/"


def main():
    site_dir = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "site")
    if not os.path.isdir(site_dir):
        print(f"no built site at {site_dir} — run scripts/build_site.sh first")
        return 2

    pages = []
    for dirpath, _, names in os.walk(site_dir):
        for n in names:
            if n.endswith(".html"):
                pages.append(os.path.join(dirpath, n))

    broken, checked = [], 0
    base_path = site_base_path()
    for page in sorted(pages):
        seen = set()
        for url in local_targets(page):
            checked += 1
            if (url) in seen:
                continue
            seen.add(url)
            if not resolves(site_dir, page, url, base_path):
                broken.append((os.path.relpath(page, site_dir), url))

    print(f"checked {checked} local links in {len(pages)} built pages · {len(broken)} broken")
    for page, url in broken[:40]:
        print(f"  BROKEN  {page} -> {url}")
    if len(broken) > 40:
        print(f"  … and {len(broken) - 40} more")
    if broken:
        return 1
    print("site links OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
