/**
 * vibe.bongwe.space front door.
 *
 * Almost everything is handled by the static assets layer, configured in
 * wrangler.jsonc: directory URLs (/Foo/ -> Foo/index.html), "/" -> index.html
 * and 404.html for a miss. This script exists for one reason: a cached miss.
 *
 * A 404 that gets cached anywhere is sticky and invisible — the path may exist
 * a minute later and the cached miss keeps being served. That is not
 * hypothetical: the root path served a cached 404 on some edges after a deploy
 * that briefly had no root handling. Misses are therefore re-sent with
 * `no-store`, so only real pages are ever cached.
 *
 * Deliberately no path rewriting here: the homepage must not depend on this
 * script running. If the script were stale or absent, "/" and every /Foo/
 * still resolve at the asset layer.
 */
export default {
  async fetch(request, env) {
    const response = await env.ASSETS.fetch(request);
    if (response.status !== 404) {
      return response;
    }
    const headers = new Headers(response.headers);
    headers.set("cache-control", "no-store");
    return new Response(response.body, { status: 404, headers });
  },
};
