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

# Strip CR and every kind of whitespace from a captured secret.
# WHY: bash's `read -s` keeps a trailing CR as data, so a paste from a GUI
# clipboard (CRLF) or a stray keypress can yield a value that is non-empty to
# the shell but whitespace-only in reality. `gh secret set` accepts an empty
# value from a pipe with exit status 0, so that lands as a secret that exists
# and is empty — and the CI guard then treats the token as unset.
normalise() { printf '%s' "$1" | tr -d '[:space:]'; }

# Cloudflare API tokens are long (40 chars today, and they are not always that
# shape). Refuse anything implausibly short rather than storing garbage.
MIN_TOKEN_CHARS=20

read_token() {
  local raw attempt=0
  TOKEN="$(normalise "${CLOUDFLARE_API_TOKEN:-}")"
  [ -n "$TOKEN" ] && { ok "using CLOUDFLARE_API_TOKEN from the environment (${#TOKEN} chars)"; return 0; }

  say "Create an API token (30 seconds)"
  cat <<'INSTRUCTIONS'
Cloudflare dashboard -> My Profile -> API Tokens -> Create Token
  Permissions:       Account / Workers Scripts / Edit     (upload the Worker)
                     Account / Workers Routes  / Edit     (own the hostname)
                     Zone    / Zone            / Read     (safety margin)
  Account resources: include your account
Copy the token, then paste it below. Input is hidden while you type.
INSTRUCTIONS

  [ -t 0 ] || { bad "no token given and stdin is not a terminal — export CLOUDFLARE_API_TOKEN instead"; exit 1; }

  while [ "$attempt" -lt 3 ]; do
    attempt=$((attempt + 1))
    printf '\nPaste the token (attempt %s/3, input hidden): ' "$attempt"
    read -rs raw; echo
    TOKEN="$(normalise "$raw")"
    unset raw
    if [ -z "$TOKEN" ]; then
      bad "nothing usable read — paste the token itself, not a blank line"
    elif [ "${#TOKEN}" -lt "$MIN_TOKEN_CHARS" ]; then
      bad "only ${#TOKEN} characters read; a Cloudflare token is much longer — copy it again from the dashboard"
      TOKEN=""
    else
      ok "read ${#TOKEN} characters"
      return 0
    fi
  done
  bad "no usable token after 3 attempts"
  exit 1
}

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

  # Lengths the runner saw (never the values): a secret that exists but reads
  # as zero characters is an empty value — gh accepts an empty paste with exit
  # status 0, so this is the only place that is visible.
  local lengths
  lengths="$(gh run view "$id" --log 2>/dev/null | grep -o "secret lengths:.*" | tail -1 || true)"
  [ -n "$lengths" ] && echo "  runner saw: $lengths"

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

    read_token

    say "Storing secrets in $REPO"
    TOKEN_LEN="${#TOKEN}"
    printf '%s' "$TOKEN" | gh secret set CLOUDFLARE_API_TOKEN
    unset TOKEN
    gh secret set CLOUDFLARE_ACCOUNT_ID --body "$ACCOUNT_ID"
    ok "CLOUDFLARE_API_TOKEN: ${TOKEN_LEN} characters stored"
    ok "CLOUDFLARE_ACCOUNT_ID: ${#ACCOUNT_ID} characters stored"
    echo "  gh stores whatever it is handed; only the run below proves it is right."
    unset TOKEN_LEN
    gh secret list | grep -E 'CLOUDFLARE' | sed 's/^/  /'

    run_and_report
    ;;
  *) echo "usage: $0 [enable|status]" >&2; exit 2 ;;
esac
