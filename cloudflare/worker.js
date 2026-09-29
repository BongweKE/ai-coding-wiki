/**
 * vibe.bongwe.space front door.
 *
 * Almost everything is handled by the static assets layer, configured in
 * wrangler.jsonc: directory URLs (/Foo/ -> Foo/index.html), "/" -> index.html
 * and 404.html for a miss. This script adds two things on top:
 *
 *   1. Security headers on every response. The assets layer sends none, and
 *      the GitHub Pages mirror already sends HSTS — without these, the
 *      custom domain would be the weaker of the two origins the site is
 *      reachable at.
 *   2. A cached-miss guard: a 404 that gets cached anywhere is sticky and
 *      invisible — the path may exist a minute later and the cached miss
 *      keeps being served. That is not hypothetical: the root path served a
 *      cached 404 on some edges after a deploy that briefly had no root
 *      handling. Misses are therefore re-sent with `no-store`, so only real
 *      pages are ever cached.
 *
 * Deliberately no path rewriting here: the homepage must not depend on this
 * script running. If the script were stale or absent, "/" and every /Foo/
 * still resolve at the asset layer.
 */

// Standard, cheap, and the one place headers can be set for the whole site
// without touching mkdocs. No CSP on purpose: the theme and Mermaid rely on
// inline scripts, and a CSP strong enough to matter would need testing
// against every page first.
const SECURITY_HEADERS = {
  // HTTPS for a year, including any future subdomain.
  "strict-transport-security": "max-age=31536000; includeSubDomains",
  // Never let a browser sniff a text file into an executable download.
  "x-content-type-options": "nosniff",
  // Only the origin is told where a reader came from when they leave.
  "referrer-policy": "strict-origin-when-cross-origin",
  // Nobody frames the site (clickjacking, preview-jacking).
  "x-frame-options": "DENY",
  // The site uses none of these powers; say so.
  "permissions-policy": "camera=(), microphone=(), geolocation=()",
};

export default {
  async fetch(request, env) {
    const response = await env.ASSETS.fetch(request);
    const headers = new Headers(response.headers);
    for (const [name, value] of Object.entries(SECURITY_HEADERS)) {
      headers.set(name, value);
    }
    if (response.status !== 404) {
      return new Response(response.body, { status: response.status, headers });
    }
    headers.set("cache-control", "no-store");
    return new Response(response.body, { status: 404, headers });
  },
};
