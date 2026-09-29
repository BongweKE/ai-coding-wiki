#!/usr/bin/env bash
# Build the site and publish it to https://vibe.bongwe.space (Cloudflare Worker).
#
#   bash scripts/deploy_cloudflare.sh
#
# Auth: `wrangler login` (OAuth) or CLOUDFLARE_API_TOKEN + CLOUDFLARE_ACCOUNT_ID
# in the environment. In CI the docs site workflow runs this automatically when
# the repository has a CLOUDFLARE_API_TOKEN secret; without it, the step is
# skipped and only the GitHub Pages mirror updates.
#
# GitHub Pages (bongweke.github.io/ai-coding-wiki) stays as a fallback mirror
# and is deployed by .github/workflows/docs.yml on every push to main.

set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

bash scripts/build_site.sh

# Prefer the installed binary; fall back to a pinned npx copy so the script
# works on a machine that has never run wrangler.
if command -v wrangler >/dev/null 2>&1; then
  wrangler deploy
else
  npx --yes wrangler@4 deploy
fi
