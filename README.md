# Defrag blog

Engineering notes from Defrag — Cardano tooling, Rust at the edge, Workers/R2 pipelines, and tech demonstrators.

Built with [Zola](https://www.getzola.org/) **0.23.6**, deployed on Cloudflare Pages.

Some posts are AI-authored on Damon Oehlman’s behalf (e.g. drafted by Promoter Bot) and credited in front matter / byline.

## Local development

Install Zola 0.23.6 (or set `ZOLA_VERSION=0.23.6` in CI — see below), then:

```bash
zola serve
```

Open the URL Zola prints (usually `http://127.0.0.1:1111`).

- Drafts (`draft = true` in front matter) are **excluded** from `zola build` and from a plain `zola serve`.
- To preview drafts locally: `zola serve --drafts`

```bash
zola build          # production output → public/
zola build --drafts # include drafts
```

Before first deploy, edit `config.toml` and set `base_url` to the real Pages hostname (replace the `https://blog.example.invalid` placeholder).

## Cloudflare Pages setup

Create a Pages project linked to this repo (`defrag-au/blog`), production branch `main`.

| Setting | Value |
|---|---|
| Framework preset | None (or “Zola” if offered — still override build/output below) |
| Build command | `zola build` |
| Build output directory | `public` |
| Root directory | `/` (repo root) |
| Environment variable | `ZOLA_VERSION` = `0.23.6` |

Cloudflare’s Zola build image reads `ZOLA_VERSION` and installs that release before running the build command. Without it, Pages may use an older Zola and fail on `config.toml` / markdown features used here.

After the first successful deploy, copy the `*.pages.dev` URL (or custom domain) into `config.toml` `base_url`, commit, and redeploy so Atom/RSS and canonical links are correct.

## Content layout

```
content/
  _index.md          # home → post list
  about/             # authorship note
  posts/             # articles (TOML +++ front matter)
templates/           # self-contained HTML (no theme submodule)
static/css/site.css
static/js/mermaid-init.js   # turns ```mermaid fences into diagrams
```

Taxonomy: `tags`. Feeds: `/atom.xml`, `/rss.xml`.

## License

Content © Damon Oehlman unless noted. Code/templates in this repo: use freely for the Defrag site.
