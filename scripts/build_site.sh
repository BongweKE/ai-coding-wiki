#!/usr/bin/env bash
# Build the documentation site from wiki/ without modifying it.
#
# wiki/ stays byte-identical so scripts/push_wiki.sh keeps syncing the
# GitHub wiki. The site builds from a prepared copy:
#   - every wiki/*.md page is copied into site-src/
#   - wiki/00-Home.md is also copied as site-src/index.md (the landing page)
#   - mkdocs.yml excludes the wiki-only files from the build
#
# Usage:
#   bash scripts/build_site.sh          # build into site/
# Then open site/index.html, or let CI deploy it to GitHub Pages.

set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

rm -rf site-src
mkdir -p site-src
cp wiki/*.md site-src/
cp wiki/00-Home.md site-src/index.md

# --strict: an unresolved link or missing anchor fails the build rather than
# printing an INFO line nobody reads (the levels are set in mkdocs.yml).
mkdocs build --strict

# Then check the output: MkDocs validates source links, this validates that
# every link it actually wrote resolves. It is the gate that would have caught
# scripts/site_hook.py leaving all 828 internal links unrewritten.
python3 scripts/check_site.py site

echo "site built -> site/index.html"
