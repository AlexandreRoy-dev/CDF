# Lancement secteurs 2026-10-10 (option 1, GitHub Pages)

## URL map (old -> new)

| Ancienne URL (en ligne) | Nouvelle page | Source aperçu | Texte unique SEO |
|---|---|---|---|
| / | / (nouvel accueil v2) | e-modele-bibeau.html | n/a |
| /regions/sherbrooke.html | /regions/sherbrooke.html | secteurs/courtier-immobilier-sherbrooke.html | oui |
| /regions/magog.html | /regions/magog.html | secteurs/courtier-immobilier-magog.html | oui |
| /regions/rock-forest.html | /regions/rock-forest.html | secteurs/courtier-immobilier-rock-forest.html | oui |
| /regions/fleurimont.html | /regions/fleurimont.html | secteurs/courtier-immobilier-fleurimont.html | oui |
| /regions/lennoxville.html | /regions/lennoxville.html | secteurs/courtier-immobilier-lennoxville.html | oui |
| /regions/les-nations.html | /regions/les-nations.html | secteurs/courtier-immobilier-les-nations.html | non |
| /regions/orford.html | /regions/orford.html | secteurs/courtier-immobilier-orford.html | oui |
| /regions/north-hatley.html | /regions/north-hatley.html | secteurs/courtier-immobilier-north-hatley.html | oui |
| /regions/mont-bellevue.html | /regions/mont-bellevue.html | secteurs/courtier-immobilier-mont-bellevue.html | non |
| /regions/brompton.html | /regions/brompton.html | secteurs/courtier-immobilier-brompton.html | non |
| (nouvelle) | /regions/jacques-cartier.html | secteurs/courtier-immobilier-jacques-cartier.html | non |
| /regions/austin.html | /regions/austin.html | secteurs/courtier-immobilier-austin.html | non |
| /regions/ayers-cliff.html | /regions/ayers-cliff.html | secteurs/courtier-immobilier-ayers-cliff.html | non |
| /regions/bromont.html | /regions/bromont.html | secteurs/courtier-immobilier-bromont.html | non |
| /regions/coaticook.html | /regions/coaticook.html | secteurs/courtier-immobilier-coaticook.html | non |
| /regions/compton.html | /regions/compton.html | secteurs/courtier-immobilier-compton.html | non |
| /regions/cookshire-eaton.html | /regions/cookshire-eaton.html | secteurs/courtier-immobilier-cookshire-eaton.html | non |
| /regions/danville.html | /regions/danville.html | secteurs/courtier-immobilier-danville.html | non |
| /regions/eastman.html | /regions/eastman.html | secteurs/courtier-immobilier-eastman.html | oui |
| /regions/hatley.html | /regions/hatley.html | secteurs/courtier-immobilier-hatley.html | non |
| /regions/lac-brome.html | /regions/lac-brome.html | secteurs/courtier-immobilier-lac-brome.html | phrase seulement |
| /regions/lac-megantic.html | /regions/lac-megantic.html | secteurs/courtier-immobilier-lac-megantic.html | non |
| /regions/milan.html | /regions/milan.html | secteurs/courtier-immobilier-milan.html | non |
| /regions/richmond.html | /regions/richmond.html | secteurs/courtier-immobilier-richmond.html | non |
| /regions/saint-isidore-de-clifton.html | /regions/saint-isidore-de-clifton.html | secteurs/courtier-immobilier-saint-isidore-de-clifton.html | non |
| /regions/stanstead.html | /regions/stanstead.html | secteurs/courtier-immobilier-stanstead.html | phrase seulement |
| /regions/sutton.html | /regions/sutton.html | secteurs/courtier-immobilier-sutton.html | non |
| /regions/val-des-sources.html | /regions/val-des-sources.html | secteurs/courtier-immobilier-val-des-sources.html | non |
| /regions/waterville.html | /regions/waterville.html | secteurs/courtier-immobilier-waterville.html | non |
| /regions/weedon.html | /regions/weedon.html | secteurs/courtier-immobilier-weedon.html | non |
| /regions/windsor.html | /regions/windsor.html | secteurs/courtier-immobilier-windsor.html | non |

Inchangées: les 3 pages lac (regions/lac-aylmer, lac-massawippi, lac-memphremagog) et toutes les autres pages en ligne.

## Changements
- index.html remplacé par le nouvel accueil (JSON-LD RealEstateAgent du live conservé).
- 30 pages regions/*.html remplacées, regions/jacques-cartier.html ajoutée.
- assets-v2/ ajouté (polices, photos, logos, images OG).
- sitemap.xml: lastmod 2026-10-10 sur les 31 pages, jacques-cartier ajoutée (125 URL). robots.txt inchangé.
- Toutes les pages lancées: index, follow; canonical sur chiassondefrancesco.ca.
- Retirés: notes d'aperçu, chips Exemple/Aperçu, blocs vides, faux avis, fausses fiches, faux billets, carte à intégrer, programmes RE/MAX non rédigés, formulaire maquette (remplacé par un bouton vers evaluation.html), matrice de liens et liens vers pages absentes.
- Liens propres remappés vers les pages en ligne (.html). Pierre-Luc Giroux: pas de page profil en ligne, lien retiré.
- Générateur: /workspace/cdf-v2/sector-gen/prod_build.py, vérif: prod_verify.py.
