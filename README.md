# Defrag blog

Engineering notes from Defrag — Cardano tooling, Rust at the edge, Workers/R2 pipelines, and tech demonstrators.

Built with [Zola](https://www.getzola.org/) **0.23.6**, served by a **Cloudflare Worker** via an `[assets]` binding (same shape as the Zola sites under [`cnft.dev-workers` `sites/`](https://github.com/defrag-au/cnft.dev-workers/tree/main/sites) — e.g. `sites/defrag`).

Some posts are AI-authored on Damon Oehlman’s behalf (e.g. drafted by Promoter Bot) and credited in front matter / byline.

## Layout

```
config.toml          # Zola (base_url, taxonomies, highlighting)
content/             # posts, about
templates/           # self-contained HTML (no theme submodule)
static/              # css, mermaid-init.js
public/              # zola build output (gitignored) — wrangler [assets] directory
src/worker.js        # thin Worker: /health only (run_worker_first)
wrangler.toml        # Worker name, assets binding, env routes
```


## Design & content features

- Dark bench theme aligned with defrag.au / `sites/defrag` (void/panel/signal palette, four-tile mark, mono labels).
- Landing hero + pillars grounded in the studio's published copy; intentional empty state when no posts are published.
- Live demo embeds via a Zola **Tera component** (shortcodes were removed in Zola 0.23). In Markdown:

      {{<demo src="https://example/demo" title="Demo" ratio="wide" />}}

  Click-to-load iframe, noscript fallback, open-in-new-tab, keyboard-focus tip.
- Share cards: `scripts/generate-og-cards.py` (Pillow) writes 1200×630 PNGs to `static/og/` before `zola build` (`scripts/build.sh`). Templates emit `og:` / `twitter:summary_large_image` meta.

## Local development

Install [Zola 0.23.6](https://github.com/getzola/zola/releases/tag/v0.23.6) and Node 20+.

```bash
npm ci
npm run serve              # generates OG cards, then zola serve
npm run serve:drafts       # include draft = true posts
npm run build              # scripts/build.sh → OG cards + zola → public/
npx wrangler dev --env production   # Worker + assets locally (needs build first)
```

`zola serve` alone still works if `static/og/*.png` already exist (committed or previously generated). Pillow is required for card generation (`pip install pillow`).

Drafts are excluded from `zola build` / plain `zola serve`. Preview them with `--drafts`.

`base_url` is already `https://blog.defrag.au` (keep it aligned with the production custom domain).

## Deploy (Cloudflare Worker + assets)

This is **not** Cloudflare Pages. Config mirrors `sites/defrag/wrangler.toml`:

| Knob | Value |
|---|---|
| Worker `name` | `defrag-blog` |
| Entry | `src/worker.js` |
| `compatibility_date` | `2026-04-28` |
| `[assets].directory` | `./public` |
| `[assets].binding` | `ASSETS` |
| `not_found_handling` | `404-page` |
| `run_worker_first` | `["/health"]` |
| `[build].command` | `zola build` |
| Production custom domain | `blog.defrag.au` (`custom_domain = true`) |
| Dev custom domain | `dev.blog.defrag.au` (same `dev.` prefix pattern as `sites/defrag`) |
| `config.toml` `base_url` | `https://blog.defrag.au` |

### Secrets (organisation)

`CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` live as **defrag-au organisation secrets** (same names the monorepo deploy actions use). The workflow reads them via `${{ secrets.CLOUDFLARE_API_TOKEN }}` / `${{ secrets.CLOUDFLARE_ACCOUNT_ID }}` — no per-repo secrets. If a run fails with empty credentials, the org secret’s repository access policy may not include this public repo yet (Damon: widen visibility / add `blog` under the secret’s selected repos).

### Local / manual deploy

```bash
npm ci
export CLOUDFLARE_API_TOKEN=…          # or wrangler login
export CLOUDFLARE_ACCOUNT_ID=…
npx wrangler deploy --env production   # runs `zola build`, then uploads
# or: npm run deploy
```

Always pass `--env production` (or `dev`). Top-level config has **no** routes — a bare `wrangler deploy` would publish a route-less worker (same footgun `deploy-target.sh` guards against in cnft.dev-workers).

Dry-run (bundle + config check, no upload):

```bash
npm run dry-run
# → wrangler deploy --env production --dry-run
```

### CI

Push to `main` (or **Actions → Deploy → Run workflow**) runs `.github/workflows/deploy.yml`: installs Zola 0.23.6, `npm ci`, then `wrangler deploy --env production` via `cloudflare/wrangler-action@v3` (wrangler **4.43.0**).

### Divergence from monorepo `sites/`

| | `cnft.dev-workers/sites/*` | this repo |
|---|---|---|
| Static out dir | `dist/` (`zola build --output-dir dist`) | `public/` (Zola default) |
| Worker entry | Rust cdylib → `build/worker/shim.mjs` | `src/worker.js` |
| CSS | Tailwind via `build-site.sh` | Hand-written `static/css/site.css` |
| Deploy | repo `scripts/deploy-target.sh` waves | GitHub Action / local wrangler |

Behaviour of `[assets]`, `/health`, and env-scoped custom domains matches.

## Content

```
content/
  _index.md
  about/             # authorship note
  posts/             # articles (TOML +++ front matter; drafts use draft = true)
```

Taxonomy: `tags`. Feeds: `/atom.xml`, `/rss.xml`.

## License

Content © Damon Oehlman unless noted. Code/templates in this repo: use freely for the Defrag site.
