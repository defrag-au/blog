+++
title = "About"
description = "What Defrag is, how this blog is authored, and where the work lives."
template = "section.html"
+++

**Defrag** is a small engineering studio working on tooling, infrastructure and preservation for the Cardano ecosystem — operated by Defrag Pty Ltd (New South Wales, Australia). The studio front door is [defrag.au](https://defrag.au); this site is the engineering notebook.

Most of the shipping surface area runs as **Rust on Cloudflare Workers** (plus R2, KV, and the odd Durable Object), with Zola for the static properties under `sites/` in [cnft.dev-workers](https://github.com/defrag-au/cnft.dev-workers). Public repos live under [`github.com/defrag-au`](https://github.com/defrag-au).

## Authorship

Most posts are written in Damon’s voice. Some are **AI-authored on Damon Oehlman’s behalf** (for example drafted by Promoter Bot or another assistant) and are credited as such in the byline or front matter (`drafted_by`, `authorship_note`). Treat those as collaborative drafts he has reviewed or will review before they leave draft status.

## Feeds

- [Atom](/atom.xml)
- [RSS](/rss.xml)

## Source

This blog is a [Zola](https://www.getzola.org/) project in [`defrag-au/blog`](https://github.com/defrag-au/blog), served by a Cloudflare Worker with a static assets binding.
