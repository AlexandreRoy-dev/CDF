#!/usr/bin/env python3
"""Fill missing on-page SEO tags without rewriting body copy.

Idempotent. Homepage links to index.html become /. Listing titles that
dropped the civic address are made unique. Social tags are copied from
the title and description already on the page.
"""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from apply_seo_geo import ROOT, BASE, html_files, is_redirect_stub, rel_posix, write_sitemap  # noqa: E402

TEAM_IMAGE = f"{BASE}/src/assets/images/chiassondefrancescoteam.jpg"
HREF_RE = re.compile(
    r'(?P<attr>\bhref\s*=\s*)(?P<q>["\'])(?P<url>[^"\']+)(?P=q)',
    re.IGNORECASE,
)
SKIP_PARTS = {".git", "node_modules", "emails", ".agents", ".cursor", "public"}


def homepage_href(url: str) -> str | None:
    raw = url.strip()
    path, hashpart, query = raw, "", ""
    if "#" in path:
        path, hashpart = path.split("#", 1)
        hashpart = "#" + hashpart
    if "?" in path:
        path, query = path.split("?", 1)
        query = "?" + query
    while path.startswith("./"):
        path = path[2:]
    if path in ("index.html", "/index.html"):
        if hashpart == "#about":
            hashpart = "#courtiers"
        return "/" + query + hashpart
    return None


def rewrite_home_hrefs(text: str) -> str:
    def repl(match: re.Match) -> str:
        new = homepage_href(match.group("url"))
        if new is None:
            return match.group(0)
        return f'{match.group("attr")}{match.group("q")}{new}{match.group("q")}'

    return HREF_RE.sub(repl, text)


class MetaGrab(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.desc = ""
        self.canon = ""
        self.og: dict[str, str] = {}
        self.tw: dict[str, str] = {}
        self.links: list[tuple[str, str]] = []
        self._in_title = False
        self._link_href = ""
        self._link_text: list[str] = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "title":
            self._in_title = True
        if tag == "meta":
            name = (d.get("name") or "").lower()
            prop = (d.get("property") or "").lower()
            content = d.get("content") or ""
            if name == "description" and not self.desc:
                self.desc = content
            if name.startswith("twitter:"):
                self.tw[name] = content
            if prop.startswith("og:"):
                self.og[prop] = content
        if tag == "link" and (d.get("rel") or "").lower() == "canonical":
            self.canon = d.get("href") or ""
        if tag == "a" and d.get("href"):
            self._link_href = d["href"]
            self._link_text = []

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._link_href:
            self._link_text.append(data)

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag == "a" and self._link_href:
            label = re.sub(r"\s+", " ", "".join(self._link_text)).strip()
            self.links.append((self._link_href, label))
            self._link_href = ""
            self._link_text = []


def esc(value: str) -> str:
    return value.replace("&", "&amp;").replace('"', "&quot;")


def ensure_social(text: str, rel: str) -> str:
    if is_redirect_stub(text) or rel.startswith("google"):
        return text
    grab = MetaGrab()
    grab.feed(text)
    title = grab.title.strip()
    desc = grab.desc.strip()
    image = grab.og.get("og:image") or grab.tw.get("twitter:image") or TEAM_IMAGE
    canon = grab.canon or (f"{BASE}/" if rel == "index.html" else f"{BASE}/{rel}")
    og_type = "article" if rel.startswith("article-") else "website"
    lines: list[str] = []
    if "og:type" not in grab.og:
        lines.append(f'  <meta property="og:type" content="{og_type}">')
    if "og:site_name" not in grab.og:
        lines.append('  <meta property="og:site_name" content="Équipe Chiasson De Francesco">')
    if "og:title" not in grab.og and title:
        lines.append(f'  <meta property="og:title" content="{esc(title)}">')
    if "og:description" not in grab.og and desc:
        lines.append(f'  <meta property="og:description" content="{esc(desc)}">')
    if "og:url" not in grab.og:
        lines.append(f'  <meta property="og:url" content="{esc(canon)}">')
    if "og:image" not in grab.og:
        lines.append(f'  <meta property="og:image" content="{esc(image)}">')
    if "og:locale" not in grab.og:
        lines.append('  <meta property="og:locale" content="fr_CA">')
    if "twitter:card" not in grab.tw:
        lines.append('  <meta name="twitter:card" content="summary_large_image">')
    if "twitter:title" not in grab.tw and title:
        lines.append(f'  <meta name="twitter:title" content="{esc(title)}">')
    if "twitter:description" not in grab.tw and desc:
        lines.append(f'  <meta name="twitter:description" content="{esc(desc)}">')
    if "twitter:image" not in grab.tw:
        lines.append(f'  <meta name="twitter:image" content="{esc(image)}">')
    if not lines:
        return text
    block = "\n" + "\n".join(lines) + "\n"
    if "</head>" in text:
        return text.replace("</head>", block + "</head>", 1)
    return text


def fill_button_alts(text: str) -> str:
    pattern = re.compile(
        r'(<button\b[^>]*>)(\s*<img\b[^>]*\balt="")([^>]*>)([^<]*)(</button>)',
        re.IGNORECASE,
    )

    def repl(match: re.Match) -> str:
        label = re.sub(r"\s+", " ", match.group(4)).strip()
        if not label:
            return match.group(0)
        img = match.group(2).replace('alt=""', f'alt="{esc(label)}"', 1)
        return match.group(1) + img + match.group(3) + match.group(4) + match.group(5)

    return pattern.sub(repl, text)


def noindex_redirects(text: str) -> str:
    if not is_redirect_stub(text) or re.search(r"noindex", text, re.I):
        return text
    tag = '  <meta name="robots" content="noindex, follow">\n'
    if "<head>" in text:
        return text.replace("<head>", "<head>\n" + tag, 1)
    return text


def replace_title_trio(text: str, old: str, new: str) -> str:
    return text.replace(old, new)


LISTING_TITLES = {
    "ca/qc/saint-isidore-de-clifton/centre/251-9e-rang/index.html": "Fermette à vendre, 251, 9e Rang | CDF",
    "ca/qc/saint-isidore-de-clifton/centre/251z-9e-rang/index.html": "Fermette à vendre, 251Z 9e Rang | CDF",
}
OLD_LISTING_TITLE = "Fermette à vendre à Saint-Isidore-de-Clifton | CDF"
DUP_NOTE = (
    "<!-- SEO: ULS 19753390 (251Z 9e Rang). Même prix affiché que l'ULS 23954624 "
    "(251, 9e Rang) et lot d'environ 56 acres, mais chambres et photos diffèrent. "
    "Les deux inscriptions Centris répondent. Titre distinct. Pas de canonical croisé "
    "tant que P-O n'a pas confirmé qu'il s'agit d'une seule propriété. -->\n"
)


def abs_url(href: str, rel: str) -> str | None:
    path = href.split("#", 1)[0].split("?", 1)[0]
    if not path or path.startswith(("mailto:", "tel:", "http://", "https://", "//")):
        return path if path.startswith("http") else None
    if path.startswith("/"):
        url = BASE + path
    else:
        parent = "" if "/" not in rel else rel.rsplit("/", 1)[0] + "/"
        url = f"{BASE}/{parent}{path}"
    if url.endswith("/index.html"):
        url = url[: -len("index.html")]
    return url


def item_list(name: str, page_url: str, links: list[tuple[str, str]]) -> dict:
    elements = []
    for i, (item_name, url) in enumerate(links, start=1):
        elements.append(
            {
                "@type": "ListItem",
                "position": i,
                "name": item_name,
                "item": url,
            }
        )
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "name": name,
                "url": page_url,
                "inLanguage": "fr-CA",
                "isPartOf": {"@id": f"{BASE}/#website"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Accueil", "item": f"{BASE}/"},
                    {"@type": "ListItem", "position": 2, "name": name, "item": page_url},
                ],
            },
            {"@type": "ItemList", "name": name, "itemListElement": elements},
        ],
    }


def webpage_ld(name: str, desc: str, url: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": name,
        "description": desc,
        "url": url,
        "inLanguage": "fr-CA",
        "isPartOf": {"@id": f"{BASE}/#website"},
    }


def inject_ld(text: str, payload: dict) -> str:
    if "application/ld+json" in text:
        return text
    block = json.dumps(payload, ensure_ascii=False, indent=2)
    script = f'\n<script type="application/ld+json">\n{block}\n</script>\n'
    return text.replace("</head>", script + "</head>", 1)


HOME_LD = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": ["RealEstateAgent", "LocalBusiness"],
            "@id": f"{BASE}/#organization",
            "name": "Équipe Chiasson De Francesco",
            "url": f"{BASE}/",
            "image": f"{BASE}/src/assets/images/chiassondefrancescoteam.jpg",
            "telephone": "+1-819-919-4631",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "157 boul. Jacques-Cartier Sud",
                "addressLocality": "Sherbrooke",
                "addressRegion": "QC",
                "postalCode": "J1J 2Z4",
                "addressCountry": "CA",
            },
            "areaServed": [
                {"@type": "City", "name": "Sherbrooke"},
                {"@type": "City", "name": "Magog"},
                {"@type": "AdministrativeArea", "name": "Estrie"},
            ],
            "parentOrganization": {
                "@type": "RealEstateAgent",
                "name": "RE/MAX D'ABORD INC.",
                "telephone": "+1-819-822-2222",
            },
            "contactPoint": [
                {
                    "@type": "ContactPoint",
                    "telephone": "+1-819-919-4631",
                    "contactType": "customer service",
                    "name": "Pierre-Olivier Chiasson",
                    "email": "p-o.chiasson@remax-quebec.com",
                    "availableLanguage": ["fr-CA"],
                },
                {
                    "@type": "ContactPoint",
                    "telephone": "+1-819-562-0656",
                    "contactType": "customer service",
                    "name": "Marco De Francesco",
                    "email": "marco.defrancesco@remax-quebec.com",
                    "availableLanguage": ["fr-CA", "en-CA"],
                },
                {
                    "@type": "ContactPoint",
                    "telephone": "+1-819-434-2652",
                    "contactType": "customer service",
                    "name": "Jade Sirois",
                    "availableLanguage": ["fr-CA"],
                },
                {
                    "@type": "ContactPoint",
                    "telephone": "+1-514-889-2927",
                    "contactType": "customer service",
                    "name": "Pierre-Luc Giroux",
                    "email": "pierreluc.giroux@remax-quebec.com",
                    "availableLanguage": ["fr-CA"],
                },
            ],
        },
        {
            "@type": "WebSite",
            "@id": f"{BASE}/#website",
            "name": "Équipe Chiasson De Francesco",
            "url": f"{BASE}/",
            "inLanguage": "fr-CA",
            "publisher": {"@id": f"{BASE}/#organization"},
        },
    ],
}


def upgrade_home(text: str) -> str:
    if 'rel="alternate"' not in text:
        links = (
            f'  <link rel="alternate" hreflang="fr-CA" href="{BASE}/">\n'
            f'  <link rel="alternate" hreflang="x-default" href="{BASE}/">\n'
            '  <link rel="llms-txt" href="/llms.txt">\n'
        )
        text = text.replace(
            f'<link href="{BASE}/" rel="canonical"/>',
            f'<link href="{BASE}/" rel="canonical"/>\n{links}',
            1,
        )
    if '"@type": "WebSite"' not in text and "application/ld+json" in text:
        block = json.dumps(HOME_LD, ensure_ascii=False, indent=2)
        text = re.sub(
            r'<script type="application/ld\+json">[\s\S]*?</script>',
            f'<script type="application/ld+json">\n{block}\n</script>',
            text,
            count=1,
        )
    return text


def named_links(grab: MetaGrab, rel: str, pred) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    seen = set()
    for href, label in grab.links:
        url = abs_url(href, rel)
        if not url or url in seen or not pred(href, url):
            continue
        seen.add(url)
        name = label or Path(url.rstrip("/").split("/")[-1])
        found.append((name, url))
    return found


def add_missing_schema(text: str, rel: str) -> str:
    if "application/ld+json" in text or is_redirect_stub(text):
        return text
    grab = MetaGrab()
    grab.feed(text)
    title = grab.title.strip()
    desc = grab.desc.strip()
    if rel == "blog.html":
        links = named_links(
            grab,
            rel,
            lambda href, url: "article-" in href or href in {
                "vendre.html",
                "acheter.html",
                "fermette-estrie.html",
                "chalet-estrie.html",
                "plex-sherbrooke.html",
            },
        )
        return inject_ld(text, item_list(title or "Blogue", f"{BASE}/blog.html", links[:40]))
    if rel == "proprietes.html":
        links = named_links(grab, rel, lambda href, url: "/ca/qc/" in url)
        return inject_ld(text, item_list(title or "Propriétés", f"{BASE}/proprietes.html", links))
    if rel == "regions-desservies.html":
        links = named_links(grab, rel, lambda href, url: "/regions/" in url and url.endswith(".html"))
        return inject_ld(text, item_list(title or "Régions desservies", f"{BASE}/regions-desservies.html", links))
    if rel == "confidentialite.html":
        return inject_ld(
            text,
            webpage_ld(title or "Politique de confidentialité", desc, f"{BASE}/confidentialite.html"),
        )
    if rel == "evaluation.html":
        return inject_ld(text, webpage_ld(title, desc, f"{BASE}/evaluation.html"))
    return text


def fix_merci(text: str) -> str:
    old_desc = "Équipe Chiasson de Francesco, courtiers immobiliers RE/MAX à Sherbrooke et en Estrie. Merci - Chiasson & De Francesco"
    new_desc = "Votre demande a bien été reçue. L'équipe analysera votre message et vous contactera."
    text = text.replace(old_desc, new_desc)
    text = text.replace("Merci - Chiasson & De Francesco", "Merci | Équipe Chiasson De Francesco")
    return text


def fix_evaluation_h1(text: str) -> str:
    if "<h1" in text:
        return text
    h1 = (
        '<h1 class="font-heading text-4xl sm:text-5xl text-brand-navy leading-tight px-6 pt-28">'
        "Vendre maintenant, plus tard, ou pas encore ?"
        "</h1>"
    )
    return text.replace(
        '<main id="eval-app" class="eval-shell"></main>',
        f'<main id="eval-app" class="eval-shell">{h1}</main>',
        1,
    )


def process_html(path: Path) -> bool:
    rel = rel_posix(path)
    original = path.read_text(encoding="utf-8")
    text = original
    text = rewrite_home_hrefs(text)
    text = noindex_redirects(text)
    text = fill_button_alts(text)
    if rel in LISTING_TITLES:
        text = replace_title_trio(text, OLD_LISTING_TITLE, LISTING_TITLES[rel])
    if rel.endswith("251z-9e-rang/index.html") and "ULS 19753390" not in text.split("</head>", 1)[0]:
        text = text.replace(
            '<link rel="canonical" href="https://chiassondefrancesco.ca/ca/qc/saint-isidore-de-clifton/centre/251z-9e-rang/">',
            '<link rel="canonical" href="https://chiassondefrancesco.ca/ca/qc/saint-isidore-de-clifton/centre/251z-9e-rang/">\n'
            + DUP_NOTE,
            1,
        )
    if rel == "merci.html":
        text = fix_merci(text)
    if rel == "index.html":
        text = upgrade_home(text)
    if rel == "evaluation.html":
        text = fix_evaluation_h1(text)
    text = ensure_social(text, rel)
    text = add_missing_schema(text, rel)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def process_py(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    text = rewrite_home_hrefs(original)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = []
    for path in html_files():
        if process_html(path):
            changed.append(rel_posix(path))
    for path in (ROOT / "scripts").glob("*.py"):
        if process_py(path):
            changed.append(path.relative_to(ROOT).as_posix())
    registry = json.loads((ROOT / "data" / "properties.json").read_text(encoding="utf-8"))
    write_sitemap(registry["listings"])
    print(f"updated {len(changed)} files")
    for name in changed:
        print(" ", name)


if __name__ == "__main__":
    main()
