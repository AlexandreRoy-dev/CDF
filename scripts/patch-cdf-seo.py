#!/usr/bin/env python3
"""Patch CDF site: footer network links, basic SEO meta, sitemap."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://chiassondefrancesco.ca"

OLD_SERVICES = """        <div class="lg:col-span-3">
          <h4 class="text-white font-heading font-bold text-lg mb-6 tracking-wide">Services</h4>
          <ul class="space-y-3 text-sm font-medium">
            <li><a href="index.html#contact" class="hover:text-brand-red transition-colors">Achat résidentiel</a></li>
            <li><a href="index.html#contact" class="hover:text-brand-red transition-colors">Vente de propriété</a></li>
            <li><a href="index.html#contact" class="hover:text-brand-red transition-colors">Investissement</a></li>
            <li><a href="index.html#contact" class="hover:text-brand-red transition-colors">Évaluation marchande</a></li>
          </ul>
        </div>"""

NEW_NETWORK = """        <div class="lg:col-span-3">
          <h4 class="text-white font-heading font-bold text-lg mb-6 tracking-wide">Notre réseau</h4>
          <ul class="space-y-3 text-sm font-medium">
            <li><a href="https://immobiliermaison.com/" target="_blank" rel="noopener noreferrer" class="hover:text-brand-red transition-colors">immobiliermaison.com</a></li>
            <li><a href="https://vendremamaisonsherbrooke.com/" target="_blank" rel="noopener noreferrer" class="hover:text-brand-red transition-colors">vendremamaisonsherbrooke.com</a></li>
            <li><a href="https://vendremamaisonestrie.com/" target="_blank" rel="noopener noreferrer" class="hover:text-brand-red transition-colors">vendremamaisonestrie.com</a></li>
            <li><a href="https://vendremonplex.com/" target="_blank" rel="noopener noreferrer" class="hover:text-brand-red transition-colors">vendremonplex.com</a></li>
            <li><a href="https://realestatesherbrooke.com/" target="_blank" rel="noopener noreferrer" class="hover:text-brand-red transition-colors">realestatesherbrooke.com</a></li>
          </ul>
        </div>"""

# Relative prefix for pages in subdirs
def prefix_for(path: Path) -> str:
    depth = len(path.relative_to(ROOT).parts) - 1
    return "../" * depth if depth else ""

def patch_footer(content: str, prefix: str) -> str:
    network = NEW_NETWORK
    if prefix:
        # subpages may use different index paths - network links are absolute, OK
        pass
    if OLD_SERVICES in content:
        content = content.replace(OLD_SERVICES, network)
    # Fix footer address if still generic
    content = content.replace(
        "<span class=\"block text-white font-semibold\">RE/MAX D'ABORD</span>\n                Sherbrooke, Québec",
        "<span class=\"block text-white font-semibold\">RE/MAX D'ABORD</span>\n                <address class=\"not-italic\">157 boul. Jacques-Cartier Sud<br>Sherbrooke, QC J1J 2Z4</address>",
    )
    return content

def page_url(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return f"{BASE}/"
    return f"{BASE}/{rel}"

def patch_seo(content: str, path: Path) -> str:
    if path.name == "index.html" and path.parent == ROOT:
        return content  # already done manually
    if 'rel="canonical"' in content:
        return content

    url = page_url(path)
    title_m = re.search(r"<title>([^<]+)</title>", content, re.I)
    title = title_m.group(1).strip() if title_m else "Chiasson de Francesco"
    desc = (
        "Équipe Chiasson de Francesco, courtiers immobiliers RE/MAX à Sherbrooke et en Estrie. "
        + title.replace("—", "-").replace("|", "-")
    )[:160]

    seo_block = f"""
    <meta name="description" content="{desc}">
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
    <meta name="author" content="Équipe Chiasson de Francesco">
    <link rel="canonical" href="{url}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{url}">
    <meta property="og:site_name" content="Chiasson de Francesco">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:image" content="{BASE}/src/assets/pierre-olivier-chiasson.webp">
    <meta property="og:locale" content="fr_CA">
"""

    # lang fr-CA
    content = re.sub(r'<html lang="fr"', '<html lang="fr-CA"', content, count=1)

    # inject after viewport or charset
    if '<meta name="viewport"' in content:
        content = content.replace(
            '<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">',
            '<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">' + seo_block,
            1,
        )
    return content

def generate_sitemap(paths: list[Path]) -> str:
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in sorted(paths, key=lambda x: page_url(x)):
        url = page_url(p)
        priority = "1.0" if p.name == "index.html" and p.parent == ROOT else "0.7"
        if p.name == "merci.html":
            priority = "0.3"
        lines.append(f"  <url><loc>{url}</loc><priority>{priority}</priority></url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"

def main():
    html_files = [p for p in ROOT.rglob("*.html") if ".git" not in p.parts]
    updated = 0
    for path in html_files:
        text = path.read_text(encoding="utf-8")
        original = text
        prefix = prefix_for(path)
        text = patch_footer(text, prefix)
        text = patch_seo(text, path)
        if text != original:
            path.write_text(text, encoding="utf-8")
            updated += 1
            print(f"updated: {path.relative_to(ROOT)}")

    sitemap = generate_sitemap(html_files)
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print("wrote sitemap.xml")

    robots = "User-agent: *\nAllow: /\n\nSitemap: https://chiassondefrancesco.ca/sitemap.xml\n"
    (ROOT / "robots.txt").write_text(robots, encoding="utf-8")
    print("wrote robots.txt")
    print(f"done — {updated} files patched")

if __name__ == "__main__":
    main()
