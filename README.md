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

## Local development

Install [Zola 0.23.6](https://github.com/getzola/zola/releases/tag/v0.23.6) and Node 20+.

```bash
zola serve                 # http://127.0.0.1:1111 — content only
zola serve --drafts        # include draft = true posts
npm ci
npm run build              # zola build → public/
npx wrangler dev --env production   # Worker + assets locally (needs build first)
```

Drafts are excluded from `zola build` / plain `zola serve`. Preview them with `--drafts`.

Before go-live, set `config.toml` `base_url` to the real https origin (must match the production route).

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

### One-time setup (Damon)

1. **Edit placeholders in `wrangler.toml`**
   - Uncomment / set `account_id`, **or** rely on `CLOUDFLARE_ACCOUNT_ID` (preferred for CI).
   - Replace `[env.dev].routes` / `[env.production].routes` patterns (e.g. `dev.blog.defrag.au`, `blog.defrag.au`) — same `{ pattern, custom_domain = true }` form as the monorepo sites. Do **not** commit someone else’s account id.
2. **Set `config.toml` `base_url`** to `https://<production-host>`.
3. **API token** with permission to edit Workers scripts and routes (Account → Workers Scripts:Edit, Workers Routes:Edit; zone DNS/route as needed for the custom domain).
4. **GitHub Actions secrets** on `defrag-au/blog` (for `.github/workflows/deploy.yml`):
   - `CLOUDFLARE_API_TOKEN`
   - `CLOUDFLARE_ACCOUNT_ID`

### Local / manual deploy

```bash
npm ci
export CLOUDFLARE_API_TOKEN=…          # or wrangler login
export CLOUDFLARE_ACCOUNT_ID=…         # if account_id unset in wrangler.toml
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

Push to `main` (or **Actions → Deploy → Run workflow**) runs `.github/workflows/deploy.yml`: installs Zola 0.23.6, `npm ci`, then `wrangler deploy --env production` via `cloudflare/wrangler-action@v3` (wrangler **4.43.0**, same pin as cnft.dev-workers’ deploy-worker action default).

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
