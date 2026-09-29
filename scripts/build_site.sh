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

mkdocs build
echo "site built -> site/index.html"
