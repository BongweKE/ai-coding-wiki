#!/usr/bin/env bash
# Turn on the Cloudflare deploy in CI, using gh.
#
#   bash scripts/enable-cloudflare-ci.sh            # store the token, then prove the deploy works
#   bash scripts/enable-cloudflare-ci.sh status     # just check whether CI is currently deploying
#   CLOUDFLARE_API_TOKEN=xxx bash scripts/enable-cloudflare-ci.sh    # non-interactive
#
# What this does, in order:
#   1. checks gh is authenticated against the right repo
#   2. stores CLOUDFLARE_API_TOKEN + CLOUDFLARE_ACCOUNT_ID as repository secrets
#   3. triggers the docs site workflow and reads back the job results, so you
#      know the Cloudflare step actually ran instead of skipping
#
# The token is read with `read -s`, piped straight into gh, and never echoed,
# logged, written to disk, or shown in chat. If you would rather not type it,
# export it first (or wrap this call in `op run` / `pass show`).
#
# NOTE: `wrangler login` on your laptop cannot be reused here. That is a
# user-scoped OAuth token; Actions needs an account-scoped API token, which
# only you can create (dashboard -> My Profile -> API Tokens).

set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

DOMAIN="vibe.bongwe.space"
MIRROR="https://bongweke.github.io/ai-coding-wiki"
WORKFLOW="docs.yml"
ACCOUNT_ID="${CLOUDFLARE_ACCOUNT_ID:-5a8fcb0172160f4cb5479d5fb4cb62cd}"

say() { printf '\n\033[1m%s\033[0m\n' "$*"; }
ok()  { printf '  \033[32mok\033[0m   %s\n' "$*"; }
bad() { printf '  \033[31mFAIL\033[0m %s\n' "$*"; }

need_gh() {
  command -v gh >/dev/null || { bad "gh is not installed"; exit 1; }
  gh auth status >/dev/null 2>&1 || { bad "not logged in — run: gh auth login"; exit 1; }
  REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner)"
  say "Repository: $REPO"
}

# ---------------------------------------------------------------- status
# Runs the workflow and reports what each job did. `deploy to
# vibe.bongwe.space (optional)` reports "skipped" until the secret exists.
run_and_report() {
  say "Triggering $WORKFLOW"
  gh workflow run "$WORKFLOW" >/dev/null
  sleep 6
  local id
  id="$(gh run list --workflow="$WORKFLOW" --limit 1 --json databaseId -q '.[0].databaseId')"
  echo "  run $id — waiting for it to finish"
  gh run watch "$id" --exit-status >/dev/null 2>&1 || true

  say "Job results"
  gh run view "$id" --json jobs -q '.jobs[] | "\(.name)|\(.conclusion)"' \
    | while IFS='|' read -r name conclusion; do ok "$name — $conclusion"; done

  # The Cloudflare job succeeds whether or not it actually published: without a
  # token its publish step is skipped. Read the step, not the job, or the
  # script would report a deploy that never happened.
  local step
  step="$(gh run view "$id" --json jobs -q \
    '.jobs[] | select(.name|test("vibe\\.bongwe\\.space|Cloudflare";"i"))
     | .steps[] | select(.name=="Publish to Cloudflare") | .conclusion' 2>/dev/null | head -1)"
  local published=1
  case "$step" in
    success) ok "Publish to Cloudflare step ran — CI is deploying the domain"; published=0 ;;
    skipped) bad "Publish to Cloudflare step SKIPPED — the secret is not set, so CI only updates the mirror" ;;
    "")      bad "the Cloudflare job did not run at all" ;;
    *)       bad "Publish to Cloudflare step: $step" ;;
  esac

  # Are both copies the same build? Compare a fingerprint of each (the Home
  # page links to the domain, so it is a cheap content check).
  say "Published copies"
  local ip d m
  ip="$(dig +short @1.1.1.1 "$DOMAIN" A 2>/dev/null | head -1 || true)"
  local rargs=()
  [ -n "$ip" ] && rargs=(--resolve "$DOMAIN:443:$ip")
  d="$(curl -s --max-time 30 ${rargs[@]+"${rargs[@]}"} "https://$DOMAIN/" | grep -c "vibe.bongwe.space</a>" || true)"
  m="$(curl -s --max-time 30 "$MIRROR/" | grep -c "vibe.bongwe.space</a>" || true)"
  if [ "$d" = "1" ] && [ "$d" = "$m" ]; then
    ok "domain and mirror both serve the current build"
  else
    bad "out of sync (domain=$d mirror=$m)"
    echo "       keep the domain fresh by hand until CI publishes it:"
    echo "         bash scripts/vibe-deploy.sh"
  fi
  return "$published"
}

case "${1:-enable}" in
  status) need_gh; run_and_report ;;
  enable)
    need_gh

    TOKEN="${CLOUDFLARE_API_TOKEN:-}"
    if [ -z "$TOKEN" ]; then
      say "Create an API token (30 seconds)"
      cat <<'INSTRUCTIONS'
Cloudflare dashboard -> My Profile -> API Tokens -> Create Token
  Permissions:       Account / Workers Scripts / Edit
                     Account / Workers Routes  / Edit
  Account resources: include your account
Copy the token, then paste it below. Input is hidden while you type.
INSTRUCTIONS
      if [ -t 0 ]; then
        printf '\nPaste the token: '
        read -rs TOKEN; echo
      else
        bad "no token given and stdin is not a terminal — export CLOUDFLARE_API_TOKEN instead"
        exit 1
      fi
    fi
    [ -n "$TOKEN" ] || { bad "empty token"; exit 1; }

    say "Storing secrets in $REPO"
    printf '%s' "$TOKEN" | gh secret set CLOUDFLARE_API_TOKEN
    unset TOKEN
    gh secret set CLOUDFLARE_ACCOUNT_ID --body "$ACCOUNT_ID"
    gh secret list | grep -E 'CLOUDFLARE' | sed 's/^/  /'

    run_and_report
    ;;
  *) echo "usage: $0 [enable|status]" >&2; exit 2 ;;
esac
