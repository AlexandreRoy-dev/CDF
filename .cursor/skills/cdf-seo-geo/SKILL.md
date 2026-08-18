---
name: cdf-seo-geo
description: SEO and GEO rules for the Chiasson De Francesco static site (chiassondefrancesco.ca). Use when editing HTML pages, listings, region pages, meta tags, JSON-LD, sitemap, robots.txt, or llms.txt.
---

# CDF SEO + GEO

French-Canadian real-estate brokerage site. Stack: static HTML, Tailwind CDN, Vercel. Listings at `/ca/qc/{city}/{sector}/{street}/`.

## Language and NAP

- `html lang="fr-CA"`, `og:locale` `fr_CA`
- Brand: Équipe Chiasson de Francesco, RE/MAX D'ABORD
- Address: 157 boul. Jacques-Cartier Sud, Sherbrooke, QC J1J 2Z4
- Phones: P-O 819-919-4631 · Marco 819-562-0656 · Jade 819-434-2652
- Measurement ID: `G-VBQPR5ZNV0` via `/src/assets/js/ga.js`

## Meta

- One `<title>`, one `<meta name="description">` per page. Never inject a second description.
- Title ~50–60 characters, intent first, brand at the end.
- Description ~140–160 characters, unique, no cloned prefix (`Équipe Chiasson de Francesco, courtiers… {title}`).
- Self-canonical. `merci.html` is `noindex` and must stay out of `sitemap.xml`.
- Do not add sitewide `hreflang` except the homepage `fr-CA` / `en-CA` pair.

## JSON-LD

Must match visible copy. Do not invent ratings, prices, or review counts.

| Page | Types |
|------|--------|
| Home | RealEstateAgent + LocalBusiness + WebSite (reviews only if visible) |
| Listing | RealEstateListing + Offer (CAD) + PostalAddress + BreadcrumbList |
| Broker | Person + RealEstateAgent |
| Article | Article |
| Region pages | Place + BreadcrumbList + FAQPage |
| Service pages (`vendre`, `acheter`, `courtier-commercial`) | FAQPage + BreadcrumbList |

## GEO

- Answer-first first paragraph (who + where + what).
- Visible FAQ + FAQPage JSON-LD on all `regions/*.html` pages and on `vendre.html`, `acheter.html`, `courtier-commercial.html`.
- Keep `/llms.txt` and AI crawlers allowed in `robots.txt`.
- Descriptive French internal anchors.

## Generators

- [`scripts/apply_seo_geo.py`](../../../scripts/apply_seo_geo.py) is the maintainable SEO pass.
- [`scripts/write_top_regions.py`](../../../scripts/write_top_regions.py) writes the five highest-intent region pages.
- [`scripts/write_geo_batch.py`](../../../scripts/write_geo_batch.py) writes 16 region pages, service pages, and GEO articles.
- [`scripts/write_geo_batch2.py`](../../../scripts/write_geo_batch2.py) writes Sherbrooke quartiers, extra towns, and product pages.
- [`scripts/write_quoi_savoir.py`](../../../scripts/write_quoi_savoir.py) writes city guides "Vendre ou acheter à [ville] : quoi savoir" (En bref, QAE, FAQ, named brokers). No em dashes in site copy.
- [`scripts/write_documents_vente.py`](../../../scripts/write_documents_vente.py) writes sale-document checklists (maison, terrain, plex) with En bref, numbered lists, FAQ + HowTo schema. No em dashes.
- [`scripts/patch-cdf-seo.py`](../../../scripts/patch-cdf-seo.py) must **not** inject a second description or put `merci.html` in the sitemap.
- New listings inherit schema from `apply_seo_geo.py` / Centris sync. Do not recreate the duplicate-meta pattern.

## Analytics MCP

Do not commit ADC JSON. Copy [`.cursor/mcp.json.example`](../../mcp.json.example) locally after `gcloud auth application-default login` with `analytics.readonly`.
