#!/usr/bin/env python3
"""Refresh site inventory from live RE/MAX listings for P-O Chiasson.

Uses data/properties.json (SEO paths) + RE/MAX inscription details to:
- generate missing SEO detail pages + legacy redirect stubs
- rebuild proprietes.html cards
- update King O 304 rental price on its existing page
- regenerate sitemap.xml + vercel redirects
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://chiassondefrancesco.ca"
REMAX_API = "https://api.remax-quebec.com/api/"
DEFAULT_REMAX_API_KEY = "c4dWcBkE#RL78Y@zg4Y06M$qrOJAeh7Fwv!Z9T4Q1f@zZ"
DEFAULT_BROKER_IDAGENT = 24115

SOLD_REDIRECT = """<!DOCTYPE html>
<html lang="fr-CA">
<head>
  <meta charset="utf-8">
  <title>Propriété vendue : redirection…</title>
  <meta name="robots" content="noindex, follow">
  <link rel="canonical" href="{canonical}">
  <meta http-equiv="refresh" content="0; url={canonical}">
  <script>window.location.replace("{canonical}");</script>
</head>
<body>
  <p>Cette propriété a été vendue. <a href="{canonical}">Voir nos propriétés disponibles</a>.</p>
</body>
</html>
"""

LEGACY_REDIRECT = """<!DOCTYPE html>
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

BED_SVG = (
    '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">'
    '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" '
    'd="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 '
    '01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6">'
    "</path></svg>"
)
BATH_SVG = (
    '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">'
    '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" '
    'd="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z">'
    "</path></svg>"
)


def api_key() -> str:
    import os

    return os.environ.get("REMAX_API_KEY") or DEFAULT_REMAX_API_KEY


def slugify(value: str) -> str:
    text = unicodedata.normalize("NFKD", value or "")
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower().replace("&", " et ")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "centre"


def city_and_sector_from_address(addr: dict) -> tuple[str, str]:
    muni = (addr.get("municipalite") or "").strip()
    city_raw = muni.split("(")[0].strip() or "quebec"
    sector = "centre"
    paren = re.findall(r"\(([^)]+)\)", muni)
    if paren:
        sector = slugify(paren[-1])
    return slugify(city_raw), sector


def street_slug_from_address(addr: dict) -> str:
    civ = (addr.get("noCiviqueDebut") or "").strip()
    rue = (addr.get("nomRueComplet") or "").strip()
    apt = (addr.get("appartement") or "").strip()
    base = f"{civ} {rue}".strip()
    if apt:
        base = f"{base} app {apt}"
    return slugify(base) or "propriete"


def public_path(listing: dict) -> str:
    return (
        f"/{listing['country']}/{listing['province']}/{listing['city']}/"
        f"{listing['sector']}/{listing['street']}/"
    )


def canonical_url(listing: dict) -> str:
    return BASE_URL + public_path(listing)


def sector_label(sector: str) -> str:
    return sector.replace("-", " ").title().replace("La Cite Limoilou", "La Cité-Limoilou")


def badge_for(detail: dict) -> tuple[str, str]:
    if detail.get("is_rental"):
        return "Location", "bg-purple-700"
    cat = (detail.get("category") or {}).get("fr") or ""
    kind = (detail.get("property_kind") or {}).get("fr") or ""
    if "Terrain" in cat or "Terrain" in kind:
        return "Terrain", "bg-green-600"
    if "Ferme" in cat or "Fermette" in kind:
        return "Résidentiel", "bg-brand-navy"
    if "Multi" in cat or "Plex" in kind:
        return "Multi-Plex", "bg-brand-navy"
    if "Commercial" in cat or "Industriel" in kind or "Fonds" in kind or "Co-propriété" in kind:
        return "Commercial", "bg-brand-navy"
    return "Résidentiel", "bg-brand-navy"


def format_price_html(detail: dict) -> str:
    display = ((detail.get("display_price") or {}).get("fr") or "").strip()
    if detail.get("is_rental"):
        # "1 200$ par mois" -> "1 200 $ /mois"
        m = re.match(r"([\d\s]+)\s*\$", display)
        amount = m.group(1).strip() if m else display.replace("$", "").strip()
        return f'{amount} $ <span class="text-sm font-normal text-gray-600">/mois</span>'
    if "+TPS/TVQ" in display or "+ TPS/TVQ" in display:
        base = display.replace("+TPS/TVQ", "").replace("+ TPS/TVQ", "").replace("$", "").strip()
        return f'{base} $ <span class="text-xs text-gray-500 font-normal">+TPS/TVQ</span>'
    if display.endswith("$"):
        return display[:-1].strip() + " $"
    return display or "Sur demande"


def format_price_plain(detail: dict) -> str:
    display = ((detail.get("display_price") or {}).get("fr") or "").strip()
    if detail.get("is_rental"):
        m = re.match(r"([\d\s]+)\s*\$", display)
        return (m.group(1).strip() + " $") if m else display
    return display.replace("$", " $").replace("  $", " $") if display else "Sur demande"


def numeric_price(detail: dict) -> str:
    if detail.get("is_rental") and detail.get("price_rental"):
        return str(int(detail["price_rental"]))
    if detail.get("price_sale"):
        return str(int(detail["price_sale"]))
    return "0"


def fr_text(obj, default: str = "") -> str:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return (obj.get("fr") or obj.get("en") or default).strip()
    return str(obj).strip() or default


def address_display(detail: dict) -> str:
    addr = detail.get("address") or {}
    display = addr.get("display") if isinstance(addr, dict) else None
    if isinstance(display, dict):
        return fr_text(display)
    if isinstance(addr, dict) and addr.get("municipalite"):
        parts = []
        civ = addr.get("noCiviqueDebut") or ""
        rue = addr.get("nomRueComplet") or ""
        apt = addr.get("appartement") or ""
        street = f"{civ} {rue}".strip()
        if apt:
            street = f"{street}, app. {apt}"
        muni = addr.get("municipalite")
        return f"{street}, {muni}".strip(", ")
    return fr_text(display) or "Adresse sur demande"


def street_short(detail: dict, listing: dict) -> str:
    addr = detail.get("address") or {}
    if isinstance(addr, dict):
        civ = addr.get("noCiviqueDebut") or ""
        rue = addr.get("nomRueComplet") or ""
        apt = addr.get("appartement") or ""
        street = f"{civ} {rue}".strip()
        if apt:
            street = f"{street}, app. {apt}"
        if street:
            return street
    title = listing.get("title") or ""
    return title.split("—")[0].strip() if "—" in title else title


def description_text(detail: dict, listing: dict) -> str:
    content = detail.get("content") or {}
    desc = ""
    if isinstance(content, dict):
        desc = fr_text(content.get("description"))
        if not desc:
            desc = fr_text((content.get("addenda") or {}))
    if not desc:
        kind = fr_text(detail.get("property_kind"), "Propriété")
        addr = address_display(detail)
        verb = "à louer" if detail.get("is_rental") else "à vendre"
        desc = (
            f"{kind} {verb} : {addr}. "
            f"Inscrite par Pierre-Olivier Chiasson, courtier immobilier RE/MAX. "
            f"ULS {listing['uls']}. Contactez-nous pour une visite ou plus de détails."
        )
    return desc


def summary_stats(detail: dict) -> list[tuple[str, str]]:
    stats: list[tuple[str, str]] = []
    rooms = detail.get("nb_of_rooms")
    if rooms:
        stats.append((str(rooms), "Nb de pièces"))
    beds = detail.get("nb_of_bedrooms")
    if beds:
        label = "Chambre" if beds == 1 else "Chambres"
        stats.append((str(beds), label))
    baths = detail.get("nb_of_bathrooms")
    if baths:
        label = "Salle de bain" if baths == 1 else "Salles de bain"
        stats.append((str(baths), label))
    hab = detail.get("superficie_habitable")
    hab_fr = fr_text(hab)
    if hab_fr:
        stats.append((hab_fr, "Superficie habitable"))
    terrain = detail.get("superficie_terrain")
    if isinstance(terrain, dict):
        tip = terrain.get("tooltip_fr") or fr_text(terrain)
        if tip:
            stats.append((tip, "Superficie terrain"))
    year = (detail.get("date_construction") or {}).get("annee_construction")
    if year:
        stats.append((str(year), "Année"))
    return stats[:4]


def caracteristiques_items(detail: dict) -> list[tuple[str, str]]:
    items: list[tuple[str, str]] = []
    kind = fr_text(detail.get("property_kind"))
    ptype = fr_text(detail.get("property_type"))
    cat = fr_text(detail.get("category"))
    if kind:
        items.append(("Genre de propriété", kind))
    if ptype:
        items.append(("Type", ptype))
    if cat:
        items.append(("Catégorie", cat))
    year = (detail.get("date_construction") or {}).get("annee_construction")
    if year:
        items.append(("Année de construction", str(year)))
    if detail.get("dimensions_batiment"):
        items.append(("Dimensions du bâtiment", detail["dimensions_batiment"]))
    hab = fr_text(detail.get("superficie_habitable"))
    if hab:
        items.append(("Superficie habitable", hab))
    if detail.get("dimensions_terrain"):
        items.append(("Dimensions du terrain", detail["dimensions_terrain"]))
    terrain = detail.get("superficie_terrain")
    if isinstance(terrain, dict):
        tip = terrain.get("tooltip_fr") or fr_text(terrain)
        if tip:
            items.append(("Superficie du terrain", tip))
    beds = detail.get("nb_of_bedrooms")
    if beds:
        above = detail.get("nb_of_bedrooms_above")
        bas = detail.get("nb_of_bedrooms_basement")
        extra = ""
        if above or bas:
            parts = []
            if above:
                parts.append(f"{above} hors sol")
            if bas:
                parts.append(f"{bas} sous-sol")
            extra = f" ({', '.join(parts)})"
        items.append(("Chambres", f"{beds}{extra}"))
    baths = detail.get("nb_of_bathrooms")
    if baths:
        powder = detail.get("nb_of_powder_rooms") or 0
        val = str(baths)
        if powder:
            val += f" + {powder} salle(s) d'eau"
        items.append(("Salles de bain", val))
    if detail.get("is_without_warranty"):
        info = fr_text(detail.get("is_without_warranty_info"))
        items.append(("Garantie légale", info or "Exclusion(s) — voir courtier"))
    return items


def fetch_detail(session: requests.Session, uls: str) -> dict:
    url = f"{REMAX_API}inscriptions/{uls}"
    resp = session.get(url, timeout=60)
    resp.raise_for_status()
    return resp.json()


def registry_entry_from_detail(uls: str, detail: dict) -> dict:
    addr = detail.get("address") or {}
    city, sector = city_and_sector_from_address(addr if isinstance(addr, dict) else {})
    street = street_slug_from_address(addr if isinstance(addr, dict) else {})
    kind = fr_text(detail.get("property_kind"), "Propriété")
    verb = "à louer" if detail.get("is_rental") else "à vendre"
    short = street_short(detail, {"title": "", "uls": uls})
    city_label = (
        (addr.get("municipalite") or city).split("(")[0].strip()
        if isinstance(addr, dict)
        else city
    )
    title = f"{short} — {city_label}" if short else f"ULS {uls}"
    share = f"{kind} {verb} — {short}, {city_label}".strip(", ")
    legacy = f"prop-{street}-{city}-{uls}.html"
    return {
        "uls": str(uls),
        "country": "ca",
        "province": "qc",
        "city": city,
        "sector": sector,
        "street": street,
        "title": title,
        "shareTitle": share,
        "legacyFile": legacy,
        "fallbackImage": f"{uls}.jpg",
    }


def fetch_live_uls(session: requests.Session, broker_idagent: int = DEFAULT_BROKER_IDAGENT) -> list[str]:
    uls_list: list[str] = []
    page = 1
    while True:
        resp = session.get(
            f"{REMAX_API}inscriptions/search",
            params={"BrokerId": broker_idagent, "Sold": 0, "PageSize": 100, "Page": page},
            timeout=60,
        )
        resp.raise_for_status()
        payload = resp.json()
        batch = payload.get("data") or []
        for item in batch:
            uls = str(item.get("no_inscription") or "")
            if uls:
                uls_list.append(uls)
        meta = payload.get("meta") or {}
        last_page = meta.get("last_page") or page
        if page >= last_page or not batch:
            break
        page += 1
    return uls_list


def sync_registry_to_live(session: requests.Session, registry: dict) -> list[str]:
    """Add missing live ULS to the registry; drop sold ones. Returns newly added ULS."""
    live_uls = fetch_live_uls(session)
    live_set = set(live_uls)
    existing = {str(item["uls"]): item for item in registry.get("listings", [])}
    added: list[str] = []

    kept = [existing[u] for u in live_uls if u in existing]
    for uls in live_uls:
        if uls in existing:
            continue
        print(f"adding new listing ULS {uls} to registry…")
        detail = fetch_detail(session, uls)
        entry = registry_entry_from_detail(uls, detail)
        kept.append(entry)
        added.append(uls)

    removed = sorted(set(existing) - live_set)
    for uls in removed:
        print(f"removing sold/inactive ULS {uls} from registry…")

    registry["listings"] = kept
    path = ROOT / "data" / "properties.json"
    path.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"registry now has {len(kept)} listings ({len(added)} added, {len(removed)} removed)")
    return added


def render_detail_page(listing: dict, detail: dict) -> str:
    path = public_path(listing)
    canonical = canonical_url(listing)
    og = f"{BASE_URL}/src/assets/images/proprietes/{listing['uls']}/og-share.jpg"
    fallback = listing["fallbackImage"]
    kind = fr_text(detail.get("property_kind"), "Propriété")
    verb = "à louer" if detail.get("is_rental") else "à vendre"
    headline = f"{kind} {verb}"
    addr = address_display(detail)
    share_title = listing.get("shareTitle") or f"{headline} — {street_short(detail, listing)}"
    page_title = f"{share_title} | Chiasson De Francesco"
    desc = description_text(detail, listing)
    meta_desc = desc[:155].rsplit(" ", 1)[0] + "…" if len(desc) > 160 else desc
    badge, badge_cls = badge_for(detail)
    price_html = format_price_html(detail)
    # For detail H1 price block, use larger styling for rentals
    if detail.get("is_rental"):
        m = re.match(r"([\d\s]+)", format_price_plain(detail))
        amount = m.group(1).strip() if m else ""
        price_block = (
            f'<div class="text-brand-red font-bold text-3xl">{amount} $ '
            f'<span class="text-lg font-semibold text-gray-600">/mois</span></div>'
        )
    else:
        price_block = f'<div class="text-brand-red font-bold text-3xl">{format_price_html(detail)}</div>'

    stats = summary_stats(detail)
    stats_html = ""
    if stats:
        cells = []
        for val, label in stats:
            cells.append(
                f'<div><div class="text-2xl font-bold text-brand-navy">{val}</div>'
                f'<div class="text-sm text-gray-500">{label}</div></div>'
            )
        stats_html = f"""
        <div class="lg:col-span-1">
          <div class="bg-gray-50 border border-gray-200 rounded-2xl p-5">
            <div class="text-sm font-medium text-gray-700 mb-3">Résumé</div>
            <div class="grid grid-cols-2 gap-4">
              {"".join(cells)}
            </div>
          </div>
        </div>"""

    chars = caracteristiques_items(detail)
    char_cells = []
    for label, value in chars:
        span = " md:col-span-2" if len(value) > 60 else ""
        char_cells.append(
            f'<div class="bg-gray-50 border border-gray-200 rounded-xl p-4{span}">'
            f'<span class="font-semibold">{label} :</span> {value}</div>'
        )
    chars_section = ""
    if char_cells:
        chars_section = f"""
          <section class="bg-white border border-gray-200 rounded-2xl p-8">
            <h2 class="font-heading text-2xl font-bold text-brand-navy mb-6">Caractéristiques</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-gray-700">
              {"".join(char_cells)}
            </div>
          </section>"""

    city = listing["city"].replace("-", " ").title()
    sector = sector_label(listing["sector"])
    cta_label = "cette location" if detail.get("is_rental") else "cette propriété"
    offer_price = numeric_price(detail)
    offer_extra = ""
    if detail.get("is_rental"):
        offer_extra = """,
        "priceSpecification": {
          "@type": "UnitPriceSpecification",
          "price": "%s",
          "priceCurrency": "CAD",
          "unitCode": "MON"
        }""" % offer_price

    street_addr = street_short(detail, listing)
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "RealEstateListing",
                "name": share_title,
                "description": meta_desc,
                "url": canonical,
                "image": og,
                "identifier": listing["uls"],
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": street_addr,
                    "addressLocality": city,
                    "addressRegion": "QC",
                    "addressCountry": "CA",
                },
                "offers": {
                    "@type": "Offer",
                    "price": offer_price,
                    "priceCurrency": "CAD",
                    "availability": "https://schema.org/InStock",
                    "url": canonical,
                },
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Accueil", "item": f"{BASE_URL}/"},
                    {"@type": "ListItem", "position": 2, "name": "Propriétés", "item": f"{BASE_URL}/proprietes.html"},
                    {"@type": "ListItem", "position": 3, "name": share_title, "item": canonical},
                ],
            },
        ],
    }
    # inject rental priceSpecification into JSON via string replace after dumps is messy;
    # build offers manually in the dumped JSON instead.
    if detail.get("is_rental"):
        ld["@graph"][0]["offers"]["priceSpecification"] = {
            "@type": "UnitPriceSpecification",
            "price": offer_price,
            "priceCurrency": "CAD",
            "unitCode": "MON",
        }

    ld_json = json.dumps(ld, ensure_ascii=False, indent=2)

    return f"""<!DOCTYPE html>
<html lang="fr-CA" class="scroll-smooth">
<head>
    <link rel="icon" type="image/svg+xml" href="/src/assets/favicon.svg">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-VBQPR5ZNV0"></script>
<script src="/src/assets/js/ga.js"></script>

  <title>{page_title}</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta name="description" content="{meta_desc.replace('"', '&quot;')}">
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
    <meta name="author" content="Équipe Chiasson de Francesco">
    <link rel="canonical" href="{canonical}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical}">
    <meta property="og:site_name" content="Chiasson de Francesco">
    <meta property="og:title" content="{page_title}">
    <meta property="og:description" content="{meta_desc.replace('"', '&quot;')}">
    <meta property="og:image" content="{og}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:type" content="image/jpeg">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{page_title}">
    <meta name="twitter:image" content="{og}">
    <meta property="og:locale" content="fr_CA">

  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Inter:400,500,600,700,800,900|Playfair+Display:400,500,600,700,800,900&amp;subset=latin">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          fontFamily: {{
            heading: ['"Playfair Display"', 'serif'],
            body: ['"Inter"', 'sans-serif'],
          }},
          colors: {{
            brand: {{ red: '#AA1120', navy: '#0c2749' }}
          }}
        }}
      }}
    }}
  </script>

<script type="application/ld+json">
{ld_json}
</script>
</head>

<body class="antialiased bg-gray-50 text-gray-900 font-body flex flex-col min-h-screen">

  <nav class="py-4 px-6 fixed w-full top-0 z-50 bg-brand-navy shadow-md">
    <div class="relative max-w-7xl mx-auto flex items-center justify-between">
      <a href="/index.html"><img src="/src/assets/logo.png" alt="Chiasson & De Francesco" class="h-10 md:h-12 w-auto"></a>
      <div class="hidden md:flex items-center gap-10">
        <a href="/index.html" class="text-white hover:text-brand-red transition-colors font-medium">Accueil</a>
        <a href="/index.html#about" class="text-white hover:text-brand-red transition-colors font-medium">Équipe</a>
        <a href="/proprietes.html" class="text-brand-red font-bold transition-colors">Propriétés</a>
        <a href="/blog.html" class="text-white hover:text-brand-red transition-colors font-medium">Blogue</a>
        <a href="/index.html#contact" class="text-white hover:text-brand-red transition-colors font-medium">Contact</a>
      </div>
      <button id="mobile-menu-btn" class="md:hidden text-white focus:outline-none">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" /></svg>
      </button>
    </div>
    <div id="mobile-menu" class="hidden md:hidden relative bg-brand-navy px-6 py-6 space-y-4 border-t border-white/10 mt-4">
      <a href="/index.html" class="block text-white hover:text-brand-red font-medium">Accueil</a>
      <a href="/index.html#about" class="block text-white hover:text-brand-red font-medium">Équipe</a>
      <a href="/proprietes.html" class="block text-brand-red font-bold">Propriétés</a>
      <a href="/blog.html" class="block text-white hover:text-brand-red font-medium">Blogue</a>
      <a href="/index.html#contact" class="block text-white hover:text-brand-red font-medium">Contact</a>
    </div>
  </nav>

  <header class="pt-32 pb-10 bg-white border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-6">
      <nav class="text-sm text-gray-500 mb-4">
        <a href="/proprietes.html" class="hover:text-brand-red">Propriétés</a>
        <span class="mx-1">/</span>
        <a href="{path}" class="hover:text-brand-red">{city}</a>
        <span class="mx-1">/</span>
        <span class="text-gray-700">{sector}</span>
      </nav>
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
        <div class="lg:col-span-2">
          <span class="inline-block {badge_cls} text-white text-xs font-bold uppercase tracking-wider px-3 py-1 rounded-full mb-3">{badge}</span>
          <h1 class="font-heading text-4xl md:text-5xl font-bold text-brand-navy leading-tight">{headline}</h1>
          <p class="text-gray-600 mt-3 text-lg">{addr}</p>
          <div class="mt-5 flex items-center gap-4 flex-wrap">
            {price_block}
            <div class="text-sm text-gray-500"><span class="font-semibold text-gray-700">ULS</span> : {listing['uls']}</div>
          </div>
        </div>
        {stats_html}
      </div>
    </div>
  </header>

  <main class="flex-grow py-12">
    <div class="max-w-7xl mx-auto px-6">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-10">
        <div class="lg:col-span-2 space-y-10">

          <section class="property-media bg-white border border-gray-200 rounded-2xl overflow-hidden"
            data-uls="{listing['uls']}"
            data-share-title="{share_title.replace('"', '&quot;')}"
            data-share-url="{canonical}"
            data-share-image="{og}"
            data-fallback-image="/src/assets/images/proprietes/{fallback}">
            <div class="property-gallery">
              <div class="relative bg-gray-100 group">
                <img id="property-gallery-main" src="/src/assets/images/proprietes/{fallback}" alt="{street_addr} — {city}" class="w-full h-[280px] sm:h-[380px] md:h-[520px] object-cover transition-opacity duration-300">
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
          </section>

          <section class="bg-white border border-gray-200 rounded-2xl p-8">
            <h2 class="font-heading text-2xl font-bold text-brand-navy mb-4">Description</h2>
            <p class="text-gray-600 leading-relaxed text-lg">
              {desc}
            </p>
          </section>
{chars_section}

        </div>

        <aside class="space-y-6">
          <section class="bg-white border border-gray-200 rounded-2xl p-7">
            <h2 class="font-heading text-xl font-bold text-brand-navy mb-4">Courtier(s)</h2>
            <div class="space-y-5">
              <div class="bg-gray-50 border border-gray-200 rounded-xl p-4">
                <div class="font-semibold text-gray-900">PIERRE-OLIVIER CHIASSON</div>
                <div class="text-sm text-gray-600 mt-1">Courtier immobilier résidentiel et commercial</div>
                <div class="text-sm text-gray-600 mt-1">RE/MAX D'ABORD INC.</div>
                <a href="tel:8199194631" class="mt-3 inline-flex items-center justify-center w-full bg-brand-navy text-white font-semibold py-2 rounded-lg hover:bg-brand-red transition-colors text-sm">819-919-4631</a>
              </div>
            </div>
          </section>
          <section class="bg-white border border-gray-200 rounded-2xl p-7">
            <h2 class="font-heading text-xl font-bold text-brand-navy mb-3">Intéressé par {cta_label}?</h2>
            <p class="text-gray-600 text-sm leading-relaxed mb-5">Contactez-nous pour planifier une visite ou obtenir plus d'informations.</p>
            <a href="/index.html#contact" class="inline-flex items-center justify-center w-full bg-brand-red text-white font-semibold py-3 rounded-lg hover:bg-brand-navy transition-colors text-sm">Nous contacter</a>
          </section>
        </aside>
      </div>
    </div>
  </main>

  <div class="relative z-50 -mt-2">
    <footer id="footer" class="bg-[#232323] text-gray-400 py-16 border-t-4 border-brand-red font-body">
      <div class="max-w-7xl mx-auto px-6">
        <div class="flex flex-wrap justify-center gap-x-4 gap-y-2 text-xs mb-6 text-gray-500">
          <a href="https://immobiliermaison.com/" target="_blank" rel="noopener noreferrer" class="hover:text-brand-red transition-colors">immobiliermaison.com</a>
          <a href="https://vendremamaisonsherbrooke.com/" target="_blank" rel="noopener noreferrer" class="hover:text-brand-red transition-colors">vendremamaisonsherbrooke.com</a>
          <a href="https://vendremamaisonestrie.com/" target="_blank" rel="noopener noreferrer" class="hover:text-brand-red transition-colors">vendremamaisonestrie.com</a>
          <a href="https://vendremonplex.com/" target="_blank" rel="noopener noreferrer" class="hover:text-brand-red transition-colors">vendremonplex.com</a>
          <a href="https://realestatesherbrooke.com/" target="_blank" rel="noopener noreferrer" class="hover:text-brand-red transition-colors">realestatesherbrooke.com</a>
        </div>
        <div class="border-t border-white/10 pt-8 text-center text-xs text-gray-500">
          <p>&copy; 2026 Équipe Chiasson & De Francesco. Tous droits réservés.</p>
        </div>
      </div>
    </footer>
  </div>
  <script>
    const btn = document.getElementById('mobile-menu-btn');
    const menu = document.getElementById('mobile-menu');
    if (btn && menu) btn.addEventListener('click', () => menu.classList.toggle('hidden'));
  </script>

  <script src="/src/assets/js/property-gallery.js" defer></script>
  <script src="/src/assets/js/property-share.js" defer></script>
</body>
</html>
"""


def card_html(listing: dict, detail: dict) -> str:
    badge, badge_cls = badge_for(detail)
    kind = fr_text(detail.get("property_kind"), "Propriété")
    verb = "à louer" if detail.get("is_rental") else "à vendre"
    street = street_short(detail, listing)
    addr = detail.get("address") or {}
    muni = ""
    if isinstance(addr, dict):
        muni = addr.get("municipalite") or ""
    # shorten municipality for card subtitle
    subtitle = muni or listing.get("title", "").split("—")[-1].strip()
    cat = fr_text(detail.get("category"))
    if cat and cat not in subtitle:
        subtitle = f"{subtitle} · {cat}" if subtitle else cat

    beds = detail.get("nb_of_bedrooms")
    baths = detail.get("nb_of_bathrooms")
    stats = ""
    if beds or baths:
        parts = []
        if beds:
            parts.append(
                f'<span class="flex items-center gap-1" title="Chambres">{BED_SVG} {beds}</span>'
            )
        if baths:
            parts.append(
                f'<span class="flex items-center gap-1" title="Salles de bain">{BATH_SVG} {baths}</span>'
            )
        stats = (
            '<div class="flex items-center gap-3 py-2 border-t border-gray-100 text-gray-600 text-sm">'
            + "".join(parts)
            + "</div>"
        )
        btn_pad = "pt-2"
    else:
        btn_pad = "pt-4"

    img = listing["fallbackImage"]
    path = public_path(listing)
    price = format_price_html(detail)
    alt = f"{kind} {street}".replace('"', "")

    return f"""
      <div class="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-xl transition-all duration-300 group flex flex-col">
        <div class="relative h-56 overflow-hidden">
          <img src="/src/assets/images/proprietes/{img}" alt="{alt}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
          <div class="absolute top-4 left-4 {badge_cls} text-white px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider shadow-sm">{badge}</div>
        </div>
        <div class="p-5 flex flex-col flex-grow">
          <p class="text-brand-red font-bold text-lg">{price}</p>
          <p class="text-sm font-medium text-brand-navy mt-1">{kind} {verb}</p>
          <p class="font-heading font-bold text-brand-navy">{street}</p>
          <p class="text-gray-500 text-sm">{subtitle}</p>
          {stats}
          <a href="{path}" class="block w-full text-center bg-gray-50 hover:bg-brand-navy hover:text-white text-brand-navy font-semibold py-2.5 rounded-lg transition-colors mt-auto {btn_pad} text-sm">Voir la fiche</a>
        </div>
      </div>
"""


def rebuild_proprietes(cards: str) -> None:
    path = ROOT / "proprietes.html"
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(
        r'(<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">)\s*.*?(</div>\s*</div>\s*</main>)',
        re.DOTALL,
    )
    if not pattern.search(text):
        raise SystemExit("Could not find proprietes.html card grid")
    replacement = r"\1\n" + cards + "\n    " + r"\2"
    text = pattern.sub(replacement, text, count=1)
    path.write_text(text, encoding="utf-8")
    print("updated proprietes.html")


def update_king304_price() -> None:
    path = ROOT / "ca/qc/sherbrooke/les-nations/31-rue-king-o-app-304/index.html"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    text = text.replace("1 300 $", "1 200 $")
    text = text.replace('"price": "1300"', '"price": "1200"')
    text = text.replace("1 300$/mois", "1 200$/mois")
    path.write_text(text, encoding="utf-8")
    print("updated King O 304 price to 1 200$")


def ensure_legacy_redirect(listing: dict) -> None:
    legacy = listing.get("legacyFile")
    if not legacy:
        return
    dest = canonical_url(listing)
    path = ROOT / legacy
    path.write_text(LEGACY_REDIRECT.format(canonical=dest), encoding="utf-8")


def main() -> int:
    registry = json.loads((ROOT / "data" / "properties.json").read_text(encoding="utf-8"))
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (compatible; CDF-refresh/1.0)",
            "Accept": "application/json",
            "X-Header-Api": api_key(),
            "Origin": "https://www.remax-quebec.com",
            "Referer": "https://www.remax-quebec.com/fr/resultats?BrokerId=24115&Sold=0",
        }
    )

    added = sync_registry_to_live(session, registry)
    listings = registry["listings"]

    details: dict[str, dict] = {}
    for listing in listings:
        uls = listing["uls"]
        print(f"fetch {uls}…")
        details[uls] = fetch_detail(session, uls)

    # Generate missing SEO pages; always rewrite pages for newly added ULS.
    for listing in listings:
        dest = (
            ROOT
            / listing["country"]
            / listing["province"]
            / listing["city"]
            / listing["sector"]
            / listing["street"]
            / "index.html"
        )
        detail = details[listing["uls"]]
        if not dest.exists() or listing["uls"] in added:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(render_detail_page(listing, detail), encoding="utf-8")
            print(f"wrote {dest.relative_to(ROOT)}")
        ensure_legacy_redirect(listing)

    cards = "\n".join(card_html(l, details[l["uls"]]) for l in listings)
    rebuild_proprietes(cards)
    update_king304_price()

    sys.path.insert(0, str(ROOT / "scripts"))
    from apply_seo_geo import write_sitemap, write_vercel_redirects

    write_sitemap(listings)
    write_vercel_redirects(listings)

    vercel_path = ROOT / "vercel.json"
    if vercel_path.exists():
        data = json.loads(vercel_path.read_text(encoding="utf-8"))
        redirects = data.get("redirects") or []
        extras = [
            "/ca/qc/milan/centre/505-chemin-de-la-yard",
            "/ca/qc/milan/centre/505-chemin-de-la-yard/",
            "/prop-505-chemin-de-la-yard-milan-26831137.html",
        ]
        existing = {r.get("source") for r in redirects}
        for source in extras:
            if source not in existing:
                redirects.append(
                    {"source": source, "destination": "/proprietes.html", "permanent": True}
                )
        data["redirects"] = redirects
        vercel_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        print("extended vercel sold redirects")

    print(f"done — {len(listings)} listings ({len(added)} new)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
