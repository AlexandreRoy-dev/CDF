#!/usr/bin/env python3
"""Footer-only patch. SEO/GEO meta and sitemap live in apply_seo_geo.py."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent

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


def prefix_for(path: Path) -> str:
    depth = len(path.relative_to(ROOT).parts) - 1
    return "../" * depth if depth else ""


def patch_footer(content: str, prefix: str) -> str:
    if OLD_SERVICES in content:
        content = content.replace(OLD_SERVICES, NEW_NETWORK)
    content = content.replace(
        "<span class=\"block text-white font-semibold\">RE/MAX D'ABORD</span>\n                Sherbrooke, Québec",
        "<span class=\"block text-white font-semibold\">RE/MAX D'ABORD</span>\n                <address class=\"not-italic\">157 boul. Jacques-Cartier Sud<br>Sherbrooke, QC J1J 2Z4</address>",
    )
    return content


def main():
    html_files = [
        p for p in ROOT.rglob("*.html")
        if ".git" not in p.parts
        and "emails" not in p.parts
        and not (p.name.startswith("google") and p.suffix == ".html")
    ]
    updated = 0
    for path in html_files:
        text = path.read_text(encoding="utf-8")
        original = text
        text = patch_footer(text, prefix_for(path))
        if text != original:
            path.write_text(text, encoding="utf-8")
            updated += 1
            print(f"updated footer: {path.relative_to(ROOT)}")

    sys.path.insert(0, str(Path(__file__).parent))
    from apply_seo_geo import main as seo_main
    seo_main()
    print(f"done : {updated} footers patched; SEO/GEO applied via apply_seo_geo.py")


if __name__ == "__main__":
    main()
