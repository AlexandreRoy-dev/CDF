#!/usr/bin/env python3
"""Apply CDF SEO/GEO hygiene: unique meta, one description, GA snippet, JSON-LD, sitemap."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://chiassondefrancesco.ca"
GA_MEASUREMENT = "G-VBQPR5ZNV0"
TODAY = date.today().isoformat()

GA_SNIPPET = f'''<script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT}"></script>
<script src="/src/assets/js/ga.js"></script>'''

GTAG_BLOCK = re.compile(
    r'(?:\s*<!--\s*Google tag \(gtag\.js\)\s*-->)?'
    r'\s*<script async src="https://www\.googletagmanager\.com/gtag/js\?id=G-VBQPR5ZNV0">\s*</script>\s*'
    r'<script>\s*window\.dataLayer[\s\S]*?gtag\(\s*[\'"]config[\'"]\s*,\s*[\'"]G-VBQPR5ZNV0[\'"]\s*\);\s*</script>',
    re.I,
)

GENERIC_PREFIX = "Équipe Chiasson de Francesco, courtiers immobiliers RE/MAX à Sherbrooke et en Estrie."

SKIP_DIRS = {".git", "node_modules", "emails", ".agents", ".cursor", "public"}

PAGE_META = {
    "index.html": None,  # keep hand-written homepage meta
    "proprietes.html": (
        "Propriétés à vendre en Estrie | Chiasson De Francesco",
        "Maisons, condos, terrains et immeubles commerciaux inscrits par l'équipe Chiasson de Francesco, courtiers RE/MAX à Sherbrooke.",
    ),
    "blog.html": (
        "Blogue immobilier Estrie | Chiasson De Francesco",
        "Conseils d'achat et de vente, prévisions 2026 et pièges à éviter. Blogue de l'équipe Chiasson de Francesco à Sherbrooke.",
    ),
    "evaluation.html": (
        "Vendre maintenant ou attendre ? | Chiasson de Francesco",
        "Questionnaire Estrie : durée de détention, projet de vie et secteur. L'équipe Chiasson de Francesco vous dit si une mise en marché a du sens.",
    ),
    "regions-desservies.html": (
        "Régions desservies en Estrie | Chiasson De Francesco",
        "Courtiers immobiliers à Sherbrooke, Magog, Bromont, Orford, North Hatley et 15 autres secteurs de l'Estrie. Équipe Chiasson de Francesco.",
    ),
    "confidentialite.html": (
        "Politique de confidentialité | Chiasson De Francesco",
        "Politique de confidentialité de l'équipe Chiasson de Francesco — courtiers immobiliers RE/MAX D'ABORD à Sherbrooke.",
    ),
    "pierre-olivier.html": (
        "Pierre-Olivier Chiasson, courtier Sherbrooke",
        "Pierre-Olivier Chiasson, courtier immobilier résidentiel et commercial RE/MAX à Sherbrooke. Achat, vente et investissement en Estrie.",
    ),
    "marco.html": (
        "Marco De Francesco, courtier Sherbrooke",
        "Marco De Francesco, courtier immobilier bilingue RE/MAX à Sherbrooke. Accompagnement à l'achat et à la vente en Estrie et à distance.",
    ),
    "jade.html": (
        "Jade Sirois, courtière immobilière Sherbrooke",
        "Jade Sirois, courtière immobilière résidentielle à Sherbrooke. Équipe Chiasson de Francesco, RE/MAX D'ABORD, pour l'achat et la vente en Estrie.",
    ),
    "article-previsions-2026.html": (
        "Prévisions immobilier Estrie 2026 | CDF",
        "Taux, prix et conseils pour acheter ou vendre en Estrie en 2026, par l'équipe Chiasson de Francesco à Sherbrooke.",
    ),
    "article-eviter-les-pieges.html": (
        "Pièges à éviter à l'achat | Chiasson De Francesco",
        "Inspection, financement et négociation : les erreurs fréquentes à l'achat d'une propriété en Estrie, expliquées par nos courtiers.",
    ),
    "article-frais-caches.html": (
        "Frais cachés à l'achat d'une maison | CDF",
        "Notaire, inspection, taxes et déménagement : les coûts souvent oubliés quand on achète une propriété à Sherbrooke et en Estrie.",
    ),
    "article-investir-sherbrooke.html": (
        "Investir en multi-logements à Sherbrooke",
        "Plex et immeubles locatifs à Sherbrooke : ce que les investisseurs doivent vérifier avant d'acheter, avec l'équipe Chiasson de Francesco.",
    ),
    "article-home-staging.html": (
        "Home staging à Sherbrooke | Chiasson De Francesco",
        "Préparer une maison à la vente en Estrie : mise en valeur, photos et première impression, par l'équipe Chiasson de Francesco.",
    ),
}

REGION_META = {
    "bromont": ("Courtier immobilier à Bromont | Chiasson De Francesco", "Acheter ou vendre à Bromont : ski, vélo et maisons de village. L'équipe Chiasson de Francesco vous accompagne en Estrie."),
    "coaticook": ("Courtier immobilier à Coaticook | CDF", "Acheter ou vendre une propriété à Coaticook, ville de services en Estrie. Équipe Chiasson de Francesco, courtiers RE/MAX."),
    "compton": ("Courtier immobilier à Compton | CDF", "Maisons et fermettes à Compton, en Estrie. L'équipe Chiasson de Francesco vous accompagne pour acheter ou vendre."),
    "cookshire-eaton": ("Courtier à Cookshire-Eaton | CDF", "Propriétés et terrains à Cookshire-Eaton. Courtiers Chiasson de Francesco pour un achat ou une vente en Estrie."),
    "danville": ("Courtier immobilier à Danville | CDF", "Acheter ou vendre à Danville, Estrie. Accompagnement par l'équipe Chiasson de Francesco, RE/MAX D'ABORD."),
    "eastman": ("Courtier immobilier à Eastman | CDF", "Maisons et chalets à Eastman, près d'Orford. L'équipe Chiasson de Francesco vous accompagne en Estrie."),
    "lac-aylmer": ("Propriétés au lac Aylmer | CDF", "Acheter ou vendre en bord du lac Aylmer, Estrie. Courtiers Chiasson de Francesco à Sherbrooke."),
    "lac-brome": ("Courtier à Lac-Brome et Knowlton | CDF", "Maisons et bord de lac à Lac-Brome (Knowlton). L'équipe Chiasson de Francesco vous accompagne."),
    "lac-massawippi": ("Propriétés au lac Massawippi | CDF", "Acheter ou vendre autour du lac Massawippi et North Hatley. Équipe Chiasson de Francesco, courtiers RE/MAX."),
    "lac-megantic": ("Courtier immobilier au lac Mégantic | CDF", "Acheter ou vendre une propriété au lac Mégantic, Estrie. Équipe Chiasson de Francesco."),
    "lac-memphremagog": ("Propriétés au lac Memphrémagog | CDF", "Bord de lac à Magog, Orford et Newport. L'équipe Chiasson de Francesco vous accompagne sur le Memphrémagog."),
    "magog": ("Courtier immobilier à Magog | lac Memphrémagog", "Acheter ou vendre à Magog, porte d'entrée du lac Memphrémagog. Maisons, condos et chalets avec Chiasson de Francesco."),
    "north-hatley": ("Courtier immobilier à North Hatley | CDF", "Acheter ou vendre à North Hatley et au lac Massawippi. L'équipe Chiasson de Francesco, courtiers RE/MAX en Estrie."),
    "orford": ("Courtier immobilier à Orford | mont Orford", "Maisons et chalets à Orford, au pied du mont et du parc national. Équipe Chiasson de Francesco en Estrie."),
    "richmond": ("Courtier immobilier à Richmond | CDF", "Acheter ou vendre à Richmond, sur la rivière Saint-François. Courtiers Chiasson de Francesco, RE/MAX."),
    "sherbrooke": ("Courtier immobilier à Sherbrooke | Chiasson De Francesco", "Acheter ou vendre à Sherbrooke : Les Nations, Fleurimont, Lennoxville, Mont-Bellevue. Équipe Chiasson de Francesco, RE/MAX."),
    "stanstead": ("Courtier immobilier à Stanstead | CDF", "Propriétés à Stanstead, à la frontière et près du lac Memphrémagog. Équipe Chiasson de Francesco."),
    "sutton": ("Courtier immobilier à Sutton | CDF", "Acheter ou vendre à Sutton, village de montagne en Estrie. L'équipe Chiasson de Francesco vous accompagne."),
    "val-des-sources": ("Courtier à Val-des-Sources | CDF", "Maisons à Val-des-Sources (Asbestos). Courtiers Chiasson de Francesco pour un achat ou une vente en Estrie."),
    "weedon": ("Courtier immobilier à Weedon | CDF", "Acheter ou vendre à Weedon, Estrie. Accompagnement par l'équipe Chiasson de Francesco, RE/MAX D'ABORD."),
    "windsor": ("Courtier immobilier à Windsor | CDF", "Propriétés à Windsor, Estrie. L'équipe Chiasson de Francesco vous accompagne pour acheter ou vendre."),
}

LISTING_OFFERS = {
    "25365838": {"price": "1300", "availability": "https://schema.org/InStock", "unitCode": "MON", "name": "Condo à louer — 31, Rue King O., app. 304, Sherbrooke"},
    "26831137": {"price": "234900", "availability": "https://schema.org/InStock", "name": "Maison à vendre — 505, Chemin de la Yard, Milan"},
    "23954624": {"price": "949900", "availability": "https://schema.org/InStock", "name": "Fermette à vendre — 251, 9e Rang, Saint-Isidore-de-Clifton"},
    "10043722": {"price": "100000", "availability": "https://schema.org/InStock", "name": "Fonds de commerce à vendre — 182, Rue Wellington N., Sherbrooke"},
    "13807137": {"price": "425000", "availability": "https://schema.org/InStock", "name": "Co-propriété à vendre — 760, Av. Honoré-Mercier, Québec"},
    "20828105": {"price": "650000", "availability": "https://schema.org/InStock", "name": "Bâtisse commerciale à vendre — 800, Rue Tessier, Sherbrooke"},
    "17958008": {"price": "1475000", "availability": "https://schema.org/InStock", "name": "Co-propriété commerciale à vendre — 1111, Rue Saint-Urbain, Montréal"},
    "27084256": {"price": "54000", "availability": "https://schema.org/InStock", "name": "Terrain à vendre — Boul. des Chasseurs, Saint-Alexis-des-Monts"},
    "11185705": {"price": "1275000", "availability": "https://schema.org/InStock", "name": "Terrain à vendre — Route 108, Cookshire-Eaton"},
}

ARTICLES = {
    "article-previsions-2026.html": ("2026-01-05", "Pierre-Olivier Chiasson", "pierre-olivier.html"),
    "article-eviter-les-pieges.html": ("2025-11-15", "Pierre-Olivier Chiasson", "pierre-olivier.html"),
    "article-frais-caches.html": ("2025-10-30", "Pierre-Olivier Chiasson", "pierre-olivier.html"),
    "article-investir-sherbrooke.html": ("2025-11-28", "Pierre-Olivier Chiasson", "pierre-olivier.html"),
    "article-home-staging.html": ("2025-12-12", "Pierre-Olivier Chiasson", "pierre-olivier.html"),
}

BROKERS = {
    "pierre-olivier.html": {
        "name": "Pierre-Olivier Chiasson",
        "job": "Courtier immobilier résidentiel et commercial",
        "tel": "+1-819-919-4631",
        "email": "p-o.chiasson@remax-quebec.com",
        "image": f"{BASE}/src/assets/pierre-olivier-chiasson.webp",
    },
    "marco.html": {
        "name": "Marco De Francesco",
        "job": "Courtier immobilier résidentiel et commercial",
        "tel": "+1-819-562-0656",
        "email": "",
        "image": f"{BASE}/src/assets/marco-de-francesco.webp",
    },
    "jade.html": {
        "name": "Jade Sirois",
        "job": "Courtière immobilière résidentielle",
        "tel": "+1-819-434-2652",
        "email": "",
        "image": f"{BASE}/src/assets/images/Jade.png",
    },
}

SOLD_PATHS = {
    "prop-16-rue-lisee-cookshire-eaton-16447016.html",
    "prop-251-rue-main-o-coaticook-10326178.html",
    "prop-31-rue-king-o-app-305-sherbrooke-10701075.html",
    "ca/qc/cookshire-eaton/sawyerville/16-rue-lisee/index.html",
    "ca/qc/coaticook/centre/251-rue-main-o/index.html",
    "ca/qc/sherbrooke/les-nations/31-rue-king-o-app-305/index.html",
}


def html_files() -> list[Path]:
    files = []
    for path in ROOT.rglob("*.html"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name.startswith("google") and path.name.endswith(".html"):
            continue
        files.append(path)
    return files


def rel_posix(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def page_url(path: Path) -> str:
    rel = rel_posix(path)
    if rel == "index.html":
        return f"{BASE}/"
    if rel.endswith("/index.html"):
        return f"{BASE}/{rel[:-10]}"
    return f"{BASE}/{rel}"


def is_redirect_stub(text: str) -> bool:
    return "window.location.replace" in text and "<body" in text and text.count("<p>") <= 2


def replace_gtag(text: str) -> str:
    if is_redirect_stub(text) or "noindex" in text and "window.location.replace" in text:
        return text
    if GTAG_BLOCK.search(text):
        text = GTAG_BLOCK.sub("\n" + GA_SNIPPET, text, count=1)
    elif f"gtag/js?id={GA_MEASUREMENT}" not in text:
        if "<head>" in text:
            text = text.replace("<head>", "<head>\n" + GA_SNIPPET, 1)
        elif "<head " in text:
            text = re.sub(r"<head[^>]*>", lambda m: m.group(0) + "\n" + GA_SNIPPET, text, count=1)
    # collapse accidental double GA
    if text.count("/src/assets/js/ga.js") > 1:
        first = True

        def keep_first(match: re.Match) -> str:
            nonlocal first
            if first:
                first = False
                return match.group(0)
            return ""

        text = re.sub(
            r'\s*<script async src="https://www\.googletagmanager\.com/gtag/js\?id=G-VBQPR5ZNV0"></script>\s*<script src="/src/assets/js/ga\.js"></script>',
            keep_first,
            text,
        )
    return text


def descriptions(text: str) -> list[str]:
    return re.findall(r'<meta\s+name="description"\s+content="([^"]*)"', text, flags=re.I)


def pick_description(existing: list[str], fallback: str) -> str:
    specific = [d for d in existing if d and not d.startswith(GENERIC_PREFIX)]
    if specific:
        return specific[-1]
    if existing:
        return existing[-1]
    return fallback


def set_or_insert_meta(text: str, title: str | None, desc: str | None, canonical: str, og_image: str | None = None) -> str:
    if title:
        if re.search(r"<title>[^<]*</title>", text, flags=re.I):
            text = re.sub(r"<title>[^<]*</title>", f"<title>{title}</title>", text, count=1, flags=re.I)
        else:
            text = text.replace("</head>", f"  <title>{title}</title>\n</head>", 1)

    found = descriptions(text)
    chosen = desc or pick_description(found, title or "Chiasson De Francesco")
    # remove all description tags then insert one after viewport or title
    text = re.sub(r'\s*<meta\s+name="description"\s+content="[^"]*"\s*/?>', "", text, flags=re.I)
    desc_tag = f'\n  <meta name="description" content="{chosen}">'
    if re.search(r'<meta name="viewport"[^>]*>', text, flags=re.I):
        text = re.sub(r'(<meta name="viewport"[^>]*>)', r"\1" + desc_tag, text, count=1, flags=re.I)
    elif "</title>" in text.lower():
        text = re.sub(r"(</title>)", r"\1" + desc_tag, text, count=1, flags=re.I)

    if title:
        text = re.sub(r'<meta property="og:title" content="[^"]*"\s*/?>', f'<meta property="og:title" content="{title}">', text, count=1)
        text = re.sub(r'<meta name="twitter:title" content="[^"]*"\s*/?>', f'<meta name="twitter:title" content="{title}">', text, count=1)
    text = re.sub(
        r'<meta property="og:description" content="[^"]*"\s*/?>',
        f'<meta property="og:description" content="{chosen}">',
        text,
        count=1,
    )
    if og_image:
        if re.search(r'<meta property="og:image"', text):
            text = re.sub(r'<meta property="og:image" content="[^"]*"\s*/?>', f'<meta property="og:image" content="{og_image}">', text, count=1)
        else:
            text = text.replace("</head>", f'  <meta property="og:image" content="{og_image}">\n</head>', 1)
    return text


def strip_json_ld(text: str) -> str:
    return re.sub(r'\s*<script type="application/ld\+json">[\s\S]*?</script>', "", text)


def inject_json_ld(text: str, payload: dict | list) -> str:
    block = json.dumps(payload, ensure_ascii=False, indent=2)
    script = f'\n<script type="application/ld+json">\n{block}\n</script>\n'
    if "</head>" in text:
        return text.replace("</head>", script + "</head>", 1)
    return text + script


def listing_json_ld(listing: dict, offer: dict, desc: str) -> dict:
    canonical = f"{BASE}/{listing['country']}/{listing['province']}/{listing['city']}/{listing['sector']}/{listing['street']}/"
    city = listing["city"].replace("-", " ").title()
    street = listing["title"].split("—")[0].strip()
    offer_node = {
        "@type": "Offer",
        "price": offer["price"],
        "priceCurrency": "CAD",
        "availability": offer["availability"],
        "url": canonical,
    }
    if offer.get("unitCode"):
        offer_node["priceSpecification"] = {
            "@type": "UnitPriceSpecification",
            "price": offer["price"],
            "priceCurrency": "CAD",
            "unitCode": offer["unitCode"],
        }
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "RealEstateListing",
                "name": offer["name"],
                "description": desc,
                "url": canonical,
                "image": f"{BASE}/src/assets/images/proprietes/{listing['uls']}/og-share.jpg",
                "identifier": listing["uls"],
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": street,
                    "addressLocality": city,
                    "addressRegion": "QC",
                    "addressCountry": "CA",
                },
                "offers": offer_node,
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Accueil", "item": f"{BASE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Propriétés", "item": f"{BASE}/proprietes.html"},
                    {"@type": "ListItem", "position": 3, "name": offer["name"], "item": canonical},
                ],
            },
        ],
    }


def person_json_ld(rel: str, broker: dict) -> dict:
    node = {
        "@context": "https://schema.org",
        "@type": ["Person", "RealEstateAgent"],
        "name": broker["name"],
        "jobTitle": broker["job"],
        "url": f"{BASE}/{rel}",
        "image": broker["image"],
        "telephone": broker["tel"],
        "worksFor": {
            "@type": "RealEstateAgent",
            "name": "Équipe Chiasson de Francesco",
            "url": f"{BASE}/",
        },
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "157 boul. Jacques-Cartier Sud",
            "addressLocality": "Sherbrooke",
            "addressRegion": "QC",
            "postalCode": "J1J 2Z4",
            "addressCountry": "CA",
        },
    }
    if broker.get("email"):
        node["email"] = broker["email"]
    return node


def article_json_ld(rel: str, title: str, desc: str, published: str, author: str, author_page: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": desc,
        "inLanguage": "fr-CA",
        "datePublished": published,
        "dateModified": published,
        "author": {"@type": "Person", "name": author, "url": f"{BASE}/{author_page}"},
        "publisher": {
            "@type": "Organization",
            "name": "Équipe Chiasson de Francesco",
            "url": BASE + "/",
            "logo": {"@type": "ImageObject", "url": f"{BASE}/src/assets/logo.png"},
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"{BASE}/{rel}"},
        "image": f"{BASE}/src/assets/pierre-olivier-chiasson.webp",
    }


def fix_root_asset_paths(path: Path, text: str) -> str:
    rel = rel_posix(path)
    depth = rel.count("/")
    if depth != 0:
        return text
    # Root HTML files must not use ../src
    text = text.replace('src="../src/', 'src="/src/')
    text = text.replace('href="../src/', 'href="/src/')
    text = text.replace('src="./src/', 'src="/src/')
    text = text.replace('href="./src/', 'href="/src/')
    return text


def process_file(path: Path, listings_by_uls: dict[str, dict]) -> None:
    rel = rel_posix(path)
    if rel.startswith("prop-") or rel in SOLD_PATHS:
        return
    text = path.read_text(encoding="utf-8")
    original = text
    if is_redirect_stub(text):
        return

    text = replace_gtag(text)
    text = fix_root_asset_paths(path, text)

    title = desc = None
    og_image = None
    if rel in PAGE_META and PAGE_META[rel]:
        title, desc = PAGE_META[rel]
    elif rel.startswith("regions/") and rel.endswith(".html"):
        slug = Path(rel).stem
        if slug in REGION_META:
            title, desc = REGION_META[slug]

    if rel == "marco.html":
        og_image = BROKERS["marco.html"]["image"]
    elif rel == "jade.html":
        og_image = BROKERS["jade.html"]["image"]
    elif rel == "pierre-olivier.html":
        og_image = BROKERS["pierre-olivier.html"]["image"]

    if rel != "index.html":
        text = set_or_insert_meta(text, title, desc, page_url(path), og_image)

    # JSON-LD (skip homepage and rewritten region FAQ pages)
    keep_ld = rel == "index.html" or "FAQPage" in text
    if not keep_ld:
        text = strip_json_ld(text)
        chosen_desc = desc or pick_description(descriptions(text), title or "")
        chosen_title = title or ""
        tm = re.search(r"<title>([^<]+)</title>", text, flags=re.I)
        if tm and not chosen_title:
            chosen_title = tm.group(1).strip()

        payload = None
        if rel in BROKERS:
            payload = person_json_ld(rel, BROKERS[rel])
        elif rel in ARTICLES:
            published, author, author_page = ARTICLES[rel]
            payload = article_json_ld(rel, chosen_title, chosen_desc, published, author, author_page)
        else:
            for listing in listings_by_uls.values():
                expected = (
                    f"{listing['country']}/{listing['province']}/{listing['city']}/"
                    f"{listing['sector']}/{listing['street']}/index.html"
                )
                if rel == expected:
                    offer = LISTING_OFFERS.get(listing["uls"])
                    if offer:
                        payload = listing_json_ld(listing, offer, chosen_desc)
                        # listing titles: intent first, not ULS
                        text = set_or_insert_meta(
                            text,
                            f"{offer['name']} | Chiasson De Francesco",
                            chosen_desc,
                            page_url(path),
                        )
                    break
        if payload:
            text = inject_json_ld(text, payload)

    if rel == "merci.html":
        text = re.sub(r'<meta name="robots" content="index, follow[^"]*"\s*/?>', "", text, flags=re.I)
        if 'name="robots"' not in text:
            text = text.replace("</head>", '  <meta name="robots" content="noindex, nofollow">\n</head>', 1)
        if "cdfTrackLead" not in text:
            text = text.replace("</body>", '<script>window.cdfTrackLead && window.cdfTrackLead("ghl_form");</script>\n</body>', 1)

    if text != original:
        path.write_text(text, encoding="utf-8")
        print(f"updated {rel}")


def write_sitemap(listings: list[dict]) -> None:
    urls = [
        (f"{BASE}/", "1.0"),
        (f"{BASE}/proprietes.html", "0.8"),
        (f"{BASE}/evaluation.html", "0.8"),
        (f"{BASE}/regions-desservies.html", "0.8"),
        (f"{BASE}/blog.html", "0.7"),
        (f"{BASE}/pierre-olivier.html", "0.7"),
        (f"{BASE}/marco.html", "0.7"),
        (f"{BASE}/jade.html", "0.7"),
        (f"{BASE}/confidentialite.html", "0.3"),
    ]
    for slug in REGION_META:
        urls.append((f"{BASE}/regions/{slug}.html", "0.8" if slug in {"sherbrooke", "magog", "bromont", "orford", "north-hatley"} else "0.6"))
    for name in ARTICLES:
        urls.append((f"{BASE}/{name}", "0.6"))
    for listing in listings:
        path = f"{BASE}/{listing['country']}/{listing['province']}/{listing['city']}/{listing['sector']}/{listing['street']}/"
        urls.append((path, "0.8"))
    urls.sort(key=lambda x: x[0])
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for loc, priority in urls:
        lines.append(f"  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><priority>{priority}</priority></url>")
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("wrote sitemap.xml")


def write_vercel_redirects(listings: list[dict]) -> None:
    vercel_path = ROOT / "vercel.json"
    data = json.loads(vercel_path.read_text(encoding="utf-8")) if vercel_path.exists() else {}
    redirects = []
    for listing in listings:
        dest = f"/{listing['country']}/{listing['province']}/{listing['city']}/{listing['sector']}/{listing['street']}/"
        redirects.append({"source": f"/{listing['legacyFile']}", "destination": dest, "permanent": True})
    sold_legacy = [
        "/prop-16-rue-lisee-cookshire-eaton-16447016.html",
        "/prop-251-rue-main-o-coaticook-10326178.html",
        "/prop-31-rue-king-o-app-305-sherbrooke-10701075.html",
        "/ca/qc/cookshire-eaton/sawyerville/16-rue-lisee",
        "/ca/qc/cookshire-eaton/sawyerville/16-rue-lisee/",
        "/ca/qc/coaticook/centre/251-rue-main-o",
        "/ca/qc/coaticook/centre/251-rue-main-o/",
        "/ca/qc/sherbrooke/les-nations/31-rue-king-o-app-305",
        "/ca/qc/sherbrooke/les-nations/31-rue-king-o-app-305/",
    ]
    for source in sold_legacy:
        redirects.append({"source": source, "destination": "/proprietes.html", "permanent": True})
    data["redirects"] = redirects
    vercel_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("wrote vercel.json redirects")


def main() -> None:
    registry = json.loads((ROOT / "data" / "properties.json").read_text(encoding="utf-8"))
    listings = registry["listings"]
    by_uls = {item["uls"]: item for item in listings}
    for path in html_files():
        process_file(path, by_uls)
    write_sitemap(listings)
    write_vercel_redirects(listings)


if __name__ == "__main__":
    main()
