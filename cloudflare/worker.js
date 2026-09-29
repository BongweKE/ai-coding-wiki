/**
 * vibe.bongwe.space front door.
 *
 * The site is built with `use_directory_urls: false`, so every page is a real
 * /Foo.html file and those are the canonical URLs (sitemap, canonical tags).
 * `html_handling: "none"` in wrangler.jsonc serves those paths exactly, with no
 * redirect to an extensionless form — which also means "/" no longer falls back
 * to index.html. That single mapping is all this script does.
 *
 * It also makes the 404 explicit: MkDocs writes 404.html, and returning it for
 * a miss is friendlier than an empty body. (not_found_handling: "404-page"
 * does the same thing; doing it here keeps the behaviour visible.)
 */
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/") {
      url.pathname = "/index.html";
    }

    const response = await env.ASSETS.fetch(new Request(url.toString(), request));
    if (response.status !== 404) {
      return response;
    }

    const notFound = await env.ASSETS.fetch(
      new Request(new URL("/404.html", url.origin).toString(), request),
    );
    if (notFound.status !== 200) {
      return response;
    }
    return new Response(notFound.body, { status: 404, headers: notFound.headers });
  },
};
