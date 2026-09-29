#!/usr/bin/env bash
# vibe.bongwe.space: publish the wiki site and verify it.
#
#   bash scripts/vibe-deploy.sh            # build, deploy to Cloudflare, verify everything
#   bash scripts/vibe-deploy.sh check      # verify only (no build, no deploy)
#   bash scripts/vibe-deploy.sh secrets    # store the Cloudflare token in GitHub so CI deploys too
#
# Why this exists: the site is served twice from one build — GitHub Pages
# (automatic, no secrets) and https://vibe.bongwe.space (a Cloudflare Worker,
# config in wrangler.jsonc). The Worker copy only publishes if CI has a
# CLOUDFLARE_API_TOKEN secret, so without `secrets` the two copies drift and
# you have to run this by hand after each content change.
#
# Auth, whichever you have:
#   * wrangler login            (an OAuth token, what this machine uses)
#   * CLOUDFLARE_API_TOKEN + CLOUDFLARE_ACCOUNT_ID in the environment
#
# The token is never echoed, never written to a file, and never typed into a
# chat: the `secrets` subcommand reads it with `read -s` and pipes it to gh.

set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
REPO_ROOT="$(pwd)"

DOMAIN="vibe.bongwe.space"
MIRROR="https://bongweke.github.io/ai-coding-wiki"
ACCOUNT_ID="${CLOUDFLARE_ACCOUNT_ID:-5a8fcb0172160f4cb5479d5fb4cb62cd}"

say() { printf '\n\033[1m%s\033[0m\n' "$*"; }
ok()  { printf '  \033[32mok\033[0m   %s\n' "$*"; }
bad() { printf '  \033[31mFAIL\033[0m %s\n' "$*"; }

# ---------------------------------------------------------------- mkdocs
ensure_mkdocs() {
  if command -v mkdocs >/dev/null 2>&1; then
    ok "mkdocs on PATH ($(mkdocs --version | head -1))"
  elif [ -x "$REPO_ROOT/.venv/bin/mkdocs" ]; then
    ok "using $REPO_ROOT/.venv"
  else
    say "Creating .venv and installing Material for MkDocs (one time)"
    python3 -m venv "$REPO_ROOT/.venv"
    "$REPO_ROOT/.venv/bin/pip" install --quiet --upgrade pip
    "$REPO_ROOT/.venv/bin/pip" install --quiet "mkdocs-material>=9.5,<10"
    ok "installed into $REPO_ROOT/.venv"
  fi
  export PATH="$REPO_ROOT/.venv/bin:$PATH"
}

# ---------------------------------------------------------------- verify
# Curl the domain through a pinned address when the local resolver has not
# picked the record up yet, so a fresh deploy can still be checked. Both
# helpers go through this: a plain `curl https://vibe.bongwe.space` fails on a
# machine whose resolver is cold, which looks exactly like a broken site.
RESOLVE_ARGS=()
_resolve_args() {
  RESOLVE_ARGS=()
  if [ "$1" = "https://$DOMAIN" ]; then
    local ip
    ip="$(dig +short @1.1.1.1 "$DOMAIN" A 2>/dev/null | head -1 || true)"
    if [ -z "$ip" ]; then
      bad "no A record for $DOMAIN yet (DNS not live)"
    else
      RESOLVE_ARGS=(--resolve "$DOMAIN:443:$ip")
    fi
  fi
}

http() {   # http <base> <path>  -> status code
  _resolve_args "$1"
  curl -s -o /dev/null -w '%{http_code}' --max-time 30 ${RESOLVE_ARGS[@]+"${RESOLVE_ARGS[@]}"} "$1$2"
}

fetch() {  # fetch <base> <path>  -> body
  _resolve_args "$1"
  curl -s --max-time 30 ${RESOLVE_ARGS[@]+"${RESOLVE_ARGS[@]}"} "$1$2"
}

verify() {
  say "Verifying the published site"
  local fail=0
  for path in "/" "/07-Deploy-For-Free.html" "/16-Zero-Dollar-Stack.html" "/10-Regression-Testing-Your-Agent-Harness.html" "/og-card.png" "/sitemap.xml"; do
    code="$(http "https://$DOMAIN" "$path")"
    if [ "$code" = "200" ]; then ok "$DOMAIN$path 200"; else bad "$DOMAIN$path $code"; fail=1; fi
  done

  # A missing page must return the wiki's own 404, not a blank one.
  if fetch "https://$DOMAIN" "/this-page-does-not-exist.html" | grep -q "Common starting points"; then
    ok "404 page served on a miss"
  else
    bad "404 page is missing or blank"; fail=1
  fi

  # GitHub Pages mirror.
  for path in "/" "/16-Zero-Dollar-Stack.html"; do
    code="$(http "$MIRROR" "$path")"
    if [ "$code" = "200" ]; then ok "$MIRROR$path 200"; else bad "$MIRROR$path $code"; fail=1; fi
  done

  # Both copies must be the same commit's build: the Home page carries the link
  # to the domain, so it is a cheap content fingerprint.
  local d m
  d="$(fetch "https://$DOMAIN" "/" | grep -c "vibe.bongwe.space</a>" || true)"
  m="$(fetch "$MIRROR" "/" | grep -c "vibe.bongwe.space</a>" || true)"
  if [ "$d" = "$m" ]; then ok "domain and mirror are in sync"; else
    bad "domain and mirror differ (domain=$d mirror=$m) — run without 'check' to republish"; fail=1
  fi
  return "$fail"
}

# ---------------------------------------------------------------- secrets
secrets() {
  command -v gh >/dev/null || { bad "gh CLI is required"; exit 1; }
  gh auth status >/dev/null 2>&1 || { bad "run 'gh auth login' first"; exit 1; }

  say "Store the Cloudflare credentials for CI"
  cat <<'TOKEN'
Create a token at: Cloudflare dashboard -> My Profile -> API Tokens -> Create Token
  Permissions:  Account / Workers Scripts / Edit
                Account / Workers Routes  / Edit
  Account Resources: include your account
Copy it, then paste it below (input is hidden, it is never printed or saved).
TOKEN
  printf '\nPaste the token: '
  read -rs CF_TOKEN; echo
  [ -n "${CF_TOKEN:-}" ] || { bad "no token entered"; exit 1; }

  printf '%s' "$CF_TOKEN" | gh secret set CLOUDFLARE_API_TOKEN
  gh secret set CLOUDFLARE_ACCOUNT_ID --body "$ACCOUNT_ID"
  unset CF_TOKEN
  ok "secrets stored for $(gh repo view --json nameWithOwner -q .nameWithOwner)"
  gh secret list | grep -E 'CLOUDFLARE' || true
  say "From now on every push to main publishes both copies automatically."
}

# ---------------------------------------------------------------- deploy
deploy() {
  ensure_mkdocs
  say "Gates"
  python3 scripts/check_wiki.py --strict   # structure, links, assets, mermaid, secrets, manifest counts
  say "Build (mkdocs --strict, then check the output's links)"
  bash scripts/build_site.sh

  command -v wrangler >/dev/null || { bad "wrangler is not installed: npm i -g wrangler"; exit 1; }
  say "Deploying site/ to $DOMAIN"
  wrangler deploy

  verify
  say "Done. Canonical: https://$DOMAIN  ·  mirror: $MIRROR"
}

case "${1:-deploy}" in
  deploy) deploy ;;
  check)  verify ;;
  secrets) secrets ;;
  *) echo "usage: $0 [deploy|check|secrets]" >&2; exit 2 ;;
esac
