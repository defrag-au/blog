/**
 * Thin worker for the Defrag blog static site.
 *
 * The Zola output in public/ is served directly by the [assets] binding.
 * Only `/health` reaches this worker (see `run_worker_first` in wrangler.toml);
 * posts, tags, feeds and the about page are all static.
 *
 * Same seam as cnft.dev-workers sites (e.g. sites/defrag/src/lib.rs): add future
 * `/api/*` here and list the prefix in `run_worker_first`. Until then there is
 * nothing to route.
 */
export default {
  async fetch(request, _env, _ctx) {
    const { pathname } = new URL(request.url);
    if (pathname === "/health") {
      return new Response("OK", {
        status: 200,
        headers: { "content-type": "text/plain; charset=utf-8" },
      });
    }
    return new Response("Not Found", { status: 404 });
  },
};
