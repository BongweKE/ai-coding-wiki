#!/usr/bin/env bash
# Sync wiki/*.md into the repository's GitHub wiki.
#
# Why a script: GitHub does not create the wiki's git repository until someone
# creates the first page in the web UI, and the page list must stay flat and
# idempotent. This script is safe to re-run: it re-copies every page, commits,
# and pushes. Deletions are handled with `git rm` for pages that no longer exist
# in wiki/.
#
#   scripts/push_wiki.sh            # sync and push
#   scripts/push_wiki.sh --dry-run  # show what would change
#
# Prerequisite (once, in the browser): open
#   https://github.com/<owner>/<repo>/wiki
# click "Create the first page", save anything, and come back here.

set -euo pipefail

OWNER_REPO="${OWNER_REPO:-BongweKE/ai-coding-wiki}"
BRANCH="${BRANCH:-main}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$REPO_ROOT/wiki"
WORK="$(mktemp -d)"
DRY="${1:-}"

die() { echo "error: $*" >&2; exit 1; }

command -v git >/dev/null || die "git is required"
[ -d "$SRC" ] || die "no wiki/ directory in $REPO_ROOT"

# Prefer SSH if the user's gh auth uses it; fall back to the gh credential helper.
# WIKI_REMOTE overrides the URL entirely, which is how this script is tested against a local
# bare repository in CI or by hand:
#   WIKI_REMOTE=/tmp/fake-wiki.git scripts/push_wiki.sh
REMOTE="${WIKI_REMOTE:-https://github.com/$OWNER_REPO.wiki.git}"
if git -c credential.helper='!gh auth git-credential' clone --depth 1 \
      "$REMOTE" "$WORK/wiki" 2>/dev/null; then
  :
else
  die "could not clone $REMOTE
GitHub only creates the wiki repository after the first page exists.
Open https://github.com/$OWNER_REPO/wiki, click 'Create the first page', save it, then re-run this script.
(To test this script against a local repository, set WIKI_REMOTE=/path/to/bare.git)"
fi

cd "$WORK/wiki"
git config user.name  "$(git -C "$REPO_ROOT" config user.name)"
git config user.email "$(git -C "$REPO_ROOT" config user.email)"
# The clone used `-c credential.helper=...`, which applies only to that one command. Persist it
# in the clone's config so the push below is authenticated too (GitHub's wiki repo is not SSH-routed
# by gh by default, and an unauthenticated push fails with "could not read Username").
git config credential.helper '!gh auth git-credential'

# 1. copy every page from wiki/ (flat namespace: GitHub wiki has no directories)
shopt -s nullglob
for f in "$SRC"/*.md; do
  cp "$f" "./$(basename "$f")"
done
shopt -u nullglob

# 1b. the wiki's landing page must be named Home.md
if [ -f "$SRC/00-Home.md" ]; then
  cp "$SRC/00-Home.md" ./Home.md
fi

# 2. remove wiki pages whose source no longer exists (except GitHub's Home stub)
for f in ./*.md; do
  b="$(basename "$f")"
  [ "$b" = "Home.md" ] && continue
  if [ ! -f "$SRC/$b" ]; then
    echo "removing $b (no longer in wiki/)"
    rm -f "$f"
  fi
done

git add -A
if git diff --cached --quiet; then
  echo "wiki already in sync — nothing to push"
  exit 0
fi

echo "--- staged changes ---"
git diff --cached --stat

if [ "$DRY" = "--dry-run" ]; then
  echo "(dry run: not committing)"
  exit 0
fi

git commit -m "Sync wiki from $OWNER_REPO@$BRANCH ($(date -u +%Y-%m-%d))"
git push origin master 2>/dev/null || git push origin HEAD
echo "wiki pushed: https://github.com/$OWNER_REPO/wiki"
