#!/usr/bin/env python3
"""Migrate property pages to SEO paths and inject gallery + share blocks."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://chiassondefrancesco.ca"

GALLERY_BLOCK = """          <section class="property-media bg-white border border-gray-200 rounded-2xl overflow-hidden"
            data-uls="{uls}"
            data-share-title="{share_title}"
            data-share-url="{canonical}"
            data-share-image="{og_image}"
            data-fallback-image="/src/assets/images/proprietes/{fallback_image}">
            <div class="property-gallery">
              <div class="relative bg-gray-100 group">
                <img id="property-gallery-main" src="/src/assets/images/proprietes/{fallback_image}" alt="{title}" class="w-full h-[280px] sm:h-[380px] md:h-[520px] object-cover transition-opacity duration-300">
                <button type="button" id="property-gallery-prev" class="absolute left-3 top-1/2 -translate-y-1/2 rounded-full bg-white/90 p-2 shadow-md hover:bg-white" aria-label="Photo précédente">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-brand-navy" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
                </button>
                <button type="button" id="property-gallery-next" class="absolute right-3 top-1/2 -translate-y-1/2 rounded-full bg-white/90 p-2 shadow-md hover:bg-white" aria-label="Photo suivante">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-brand-navy" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
                </button>
                <span id="property-gallery-counter" class="absolute bottom-3 right-3 rounded-full bg-black/60 px-3 py-1 text-xs font-medium text-white">1 / 1</span>
              </div>
              <div id="property-gallery-thumbs" class="grid grid-cols-4 sm:grid-cols-6 md:grid-cols-8 gap-2 p-4 max-h-52 overflow-y-auto bg-white"></div>
            </div>
            <div class="border-t border-gray-200 px-4 py-3 bg-gray-50">
              <p class="text-sm font-medium text-gray-700 mb-2">Partager cette propriété</p>
              <div id="property-share-buttons" class="flex flex-wrap gap-2"></div>
            </div>
          </section>"""

REDIRECT_TEMPLATE = """<!DOCTYPE html>
<html lang="fr-CA">
<head>
  <meta charset="utf-8">
  <title>Redirection…</title>
  <link rel="canonical" href="{canonical}">
  <meta http-equiv="refresh" content="0; url={canonical}">
  <script>window.location.replace("{canonical}");</script>
</head>
<body>
  <p>Cette fiche a déménagé. <a href="{canonical}">Continuer vers la nouvelle adresse</a>.</p>
</body>
</html>
"""


def public_path(listing: dict) -> str:
    return (
        f"/{listing['country']}/{listing['province']}/{listing['city']}/"
        f"{listing['sector']}/{listing['street']}/"
    )


def canonical_url(listing: dict) -> str:
    return BASE_URL + public_path(listing)


def og_image_url(listing: dict) -> str:
    return f"{BASE_URL}/src/assets/images/proprietes/{listing['uls']}/og-share.jpg"


def fix_root_paths(content: str) -> str:
    content = content.replace('href="./src/', 'href="/src/')
    content = content.replace('src="./src/', 'src="/src/')
    content = content.replace('href="../src/', 'href="/src/')
    content = content.replace('src="../src/', 'src="/src/')
    content = content.replace('href="index.html"', 'href="/index.html"')
    content = content.replace('href="proprietes.html"', 'href="/proprietes.html"')
    content = content.replace('href="blog.html"', 'href="/blog.html"')
    content = content.replace('href="index.html#', 'href="/index.html#')
    return content


def inject_gallery(content: str, listing: dict) -> str:
    gallery = GALLERY_BLOCK.format(
        uls=listing["uls"],
        share_title=listing["shareTitle"],
        canonical=canonical_url(listing),
        og_image=og_image_url(listing),
        fallback_image=listing["fallbackImage"],
        title=listing["title"],
    )

    pattern = re.compile(
        r'<section class="bg-white border border-gray-200 rounded-2xl overflow-hidden">\s*'
        r'<img[^>]+class="w-full h-\[360px\] object-cover">\s*'
        r"</section>",
        re.DOTALL,
    )
    if pattern.search(content):
        content = pattern.sub(gallery, content, count=1)
    return content


def update_seo(content: str, listing: dict) -> str:
    canonical = canonical_url(listing)
    og_image = og_image_url(listing)
    share_title = listing["shareTitle"]

    content = re.sub(
        r'<link rel="canonical" href="[^"]+">',
        f'<link rel="canonical" href="{canonical}">',
        content,
    )
    content = re.sub(
        r'<meta property="og:url" content="[^"]+">',
        f'<meta property="og:url" content="{canonical}">',
        content,
    )
    content = re.sub(
        r'<meta property="og:image" content="[^"]+">',
        f'<meta property="og:image" content="{og_image}">',
        content,
    )
    content = re.sub(
        r'<meta property="og:title" content="[^"]+">',
        f'<meta property="og:title" content="{share_title}">',
        content,
    )

    if 'property="og:image:width"' not in content:
        content = content.replace(
            f'<meta property="og:image" content="{og_image}">',
            (
                f'<meta property="og:image" content="{og_image}">\n'
                f'    <meta property="og:image:width" content="1200">\n'
                f'    <meta property="og:image:height" content="630">\n'
                f'    <meta property="og:image:type" content="image/jpeg">\n'
                f'    <meta name="twitter:card" content="summary_large_image">\n'
                f'    <meta name="twitter:title" content="{share_title}">\n'
                f'    <meta name="twitter:image" content="{og_image}">'
            ),
        )

    city_label = listing["city"].replace("-", " ").title()
    sector_label = listing["sector"].replace("-", " ").title()
    breadcrumb = (
        f'<nav class="text-sm text-gray-500 mb-4">\n'
        f'        <a href="/proprietes.html" class="hover:text-brand-red">Propriétés</a>\n'
        f'        <span class="mx-1">/</span>\n'
        f'        <a href="{public_path(listing)}" class="hover:text-brand-red">{city_label}</a>\n'
        f'        <span class="mx-1">/</span>\n'
        f'        <span class="text-gray-700">{sector_label}</span>\n'
        f'      </nav>'
    )
    content = re.sub(
        r'<nav class="text-sm text-gray-500 mb-4">.*?</nav>',
        breadcrumb,
        content,
        count=1,
        flags=re.DOTALL,
    )
    return content


def inject_scripts(content: str) -> str:
    scripts = (
        '\n  <script src="/src/assets/js/property-gallery.js" defer></script>\n'
        '  <script src="/src/assets/js/property-share.js" defer></script>'
    )
    if "property-gallery.js" not in content:
        content = content.replace("</body>", scripts + "\n</body>")
    return content


def migrate_listing(listing: dict) -> None:
    legacy = ROOT / listing["legacyFile"]
    if not legacy.exists():
        print(f"SKIP missing legacy file: {listing['legacyFile']}")
        return

    dest_dir = (
        ROOT
        / listing["country"]
        / listing["province"]
        / listing["city"]
        / listing["sector"]
        / listing["street"]
    )
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "index.html"

    content = legacy.read_text(encoding="utf-8")
    content = fix_root_paths(content)
    content = inject_gallery(content, listing)
    content = update_seo(content, listing)
    content = inject_scripts(content)
    dest.write_text(content, encoding="utf-8")

    redirect_html = REDIRECT_TEMPLATE.format(canonical=canonical_url(listing))
    legacy.write_text(redirect_html, encoding="utf-8")
    print(f"migrated {listing['uls']} -> {dest.relative_to(ROOT)}")


def update_site_links(registry: dict) -> None:
    mapping = {
        listing["legacyFile"]: public_path(listing)
        for listing in registry["listings"]
    }

    files = [ROOT / "proprietes.html", ROOT / "index.html", ROOT / "sitemap.xml"]
    for path in files:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        original = text
        for legacy, new_path in mapping.items():
            text = text.replace(f'href="{legacy}"', f'href="{new_path}"')
            text = text.replace(
                f"<loc>{BASE_URL}/{legacy}</loc>",
                f"<loc>{BASE_URL}{new_path}</loc>",
            )
        if text != original:
            path.write_text(text, encoding="utf-8")
            print(f"updated links in {path.relative_to(ROOT)}")


def regenerate_sitemap(registry: dict) -> None:
    html_files = sorted(p for p in ROOT.rglob("*.html") if ".git" not in p.parts)
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path in html_files:
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith("prop-") and rel.endswith(".html"):
            continue
        if rel.endswith("/index.html"):
            url = BASE_URL + "/" + rel.replace("/index.html", "/")
        elif rel == "index.html":
            url = BASE_URL + "/"
        else:
            url = BASE_URL + "/" + rel
        priority = "1.0" if rel == "index.html" else "0.7"
        if rel == "merci.html":
            priority = "0.3"
        lines.append(f"  <url><loc>{url}</loc><priority>{priority}</priority></url>")
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("regenerated sitemap.xml")


def main() -> None:
    registry = json.loads((ROOT / "data" / "properties.json").read_text(encoding="utf-8"))
    for listing in registry["listings"]:
        migrate_listing(listing)
    update_site_links(registry)
    regenerate_sitemap(registry)


if __name__ == "__main__":
    main()
