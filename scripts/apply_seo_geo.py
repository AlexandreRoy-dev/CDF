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
        "Conseils d'achat et de vente en Estrie : courtier vs vente libre, offre d'achat, condos, bords de lac. Blogue Chiasson de Francesco.",
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
        "Politique de confidentialité de l'équipe Chiasson de Francesco, courtiers immobiliers RE/MAX D'ABORD à Sherbrooke.",
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
    "vendre.html": (
        "Vendre sa maison à Sherbrooke et en Estrie | CDF",
        "Vendre avec l'équipe Chiasson de Francesco : évaluation marchande, mise en marché Centris et négociation à Sherbrooke et en Estrie.",
    ),
    "acheter.html": (
        "Acheter une maison en Estrie | courtier Sherbrooke | CDF",
        "Acheter à Sherbrooke et en Estrie avec un courtier acheteur : recherche Centris, visites, inspection et négociation. Équipe Chiasson de Francesco.",
    ),
    "courtier-commercial.html": (
        "Courtier immobilier commercial Sherbrooke | CDF",
        "Locaux, fonds de commerce, bâtisses et terrains à Sherbrooke et au Québec. Pierre-Olivier Chiasson et Marco De Francesco, RE/MAX D'ABORD.",
    ),
    "article-courtier-ou-vente-libre.html": (
        "Vendre avec un courtier ou seul ? | Estrie | CDF",
        "Prix, clauses, temps et commission : quand un courtier immobilier à Sherbrooke paie, et quand la vente libre peut suffire.",
    ),
    "article-evaluation-marchande-estrie.html": (
        "Évaluation marchande vs municipale | Estrie | CDF",
        "L'évaluation municipale n'est pas le prix de marché à Sherbrooke. Comment une évaluation marchande de courtier s'en distingue.",
    ),
    "article-delai-vente-estrie.html": (
        "Combien de temps pour vendre en Estrie ? | CDF",
        "Prix, saison, type de bien : pourquoi une maison à Sherbrooke ne se vend pas au même rythme qu'un chalet à Orford.",
    ),
    "article-offre-achat-quebec.html": (
        "Comment faire une offre d'achat au Québec | CDF",
        "Promesse d'achat, inspection, financement : les clauses qui protègent un acheteur à Sherbrooke, et celles qui font fuir le vendeur.",
    ),
    "article-bord-de-lac-estrie.html": (
        "Acheter un bord de lac en Estrie | CDF",
        "Accès à l'eau vs vue, fosses, bandes riveraines : ce qu'un acheteur doit vérifier avant d'offrir sur un lac en Estrie.",
    ),
    "article-condo-sherbrooke.html": (
        "Acheter un condo à Sherbrooke | frais et pièges | CDF",
        "Charges, fonds de prévoyance, PV d'assemblée : ce qu'il faut lire avant d'acheter un condo aux Nations, en centre-ville ou à Fleurimont.",
    ),
    "article-premiere-maison-estrie.html": (
        "Première maison en Estrie | budget et étapes | CDF",
        "Mise de fonds, préautorisation, inspection : les étapes d'un premier achat à Sherbrooke, Magog ou en périphérie.",
    ),
    "article-zonage-commercial-sherbrooke.html": (
        "Zonage commercial à Sherbrooke | avant d'acheter | CDF",
        "H10, usages permis, décontamination : pourquoi un local ou une bâtisse à Sherbrooke se juge d'abord au zonage, pas à la vitrine.",
    ),
    "article-inspection-maison-estrie.html": (
        "Inspection préachat en Estrie | fosses et chalets | CDF",
        "Quoi faire inspecter avant d'acheter à Sherbrooke, Magog ou en rang : bâtiment, fosse, puits. Conseils de l'équipe Chiasson de Francesco.",
    ),
    "article-vendre-condo-sherbrooke.html": (
        "Vendre un condo à Sherbrooke | charges et acheteurs | CDF",
        "Copropriété à Sherbrooke : documents à préparer, frais, et comment un prix collé au marché évite un condo qui stagne sur Centris.",
    ),
    "article-navette-sherbrooke.html": (
        "Habiter autour de Sherbrooke | navette Estrie | CDF",
        "Où habiter autour de Sherbrooke selon le trajet, le budget et le mode de vie : Windsor, Richmond, Magog, Coaticook.",
    ),
    "article-terrain-estrie.html": (
        "Acheter un terrain en Estrie | zonage et viabilisation | CDF",
        "Un terrain à Cookshire-Eaton ou en rang n'est pas un prix à l'acre. Zonage, accès et viabilisation avant d'offrir.",
    ),
    "fermette-estrie.html": (
        "Vendre ou acheter une fermette en Estrie | CDF",
        "Fermettes en Estrie : acreage, zonage agricole, bâtiments. L'équipe Chiasson de Francesco accompagne Coaticook, Clifton, Compton.",
    ),
    "chalet-estrie.html": (
        "Acheter ou vendre un chalet en Estrie | CDF",
        "Chalets à Magog, Orford, lacs Estrie : quatre-saisons, fosses, accès. Courtiers Chiasson de Francesco à Sherbrooke.",
    ),
    "plex-sherbrooke.html": (
        "Acheter ou vendre un plex à Sherbrooke | CDF",
        "Duplex, triplex et multiplex à Sherbrooke : loyers, rénos, quartiers. Équipe Chiasson de Francesco, RE/MAX.",
    ),
    "courtier-acheteur-estrie.html": (
        "Courtier acheteur en Estrie | Sherbrooke | CDF",
        "Être représenté à l'achat à Sherbrooke et en Estrie : recherche, inspection, offre. Équipe Chiasson de Francesco.",
    ),
    "article-vendre-hiver-estrie.html": (
        "Vendre sa maison l'hiver en Estrie | CDF",
        "Neige, photos et prix : ce qui change vraiment quand on affiche une maison à Sherbrooke entre novembre et mars.",
    ),
    "article-notaire-immobilier-quebec.html": (
        "Notaire immobilier au Québec | rôle et délais | CDF",
        "Titres, ajustements, acte : ce que le notaire fait (et ne fait pas) quand vous achetez ou vendez à Sherbrooke.",
    ),
    "article-droits-mutation-sherbrooke.html": (
        "Droits de mutation à Sherbrooke | taxe de bienvenue | CDF",
        "La taxe de bienvenue n'est pas un détail : comment la prévoir à Sherbrooke, Magog ou ailleurs en Estrie.",
    ),
    "article-contre-offre-quebec.html": (
        "Contre-offre immobilière au Québec | CDF",
        "Comment répondre à une offre à Sherbrooke : prix, inspection, inclusions. Conseils de l'équipe Chiasson de Francesco.",
    ),
    "article-declaration-vendeur.html": (
        "Déclaration du vendeur au Québec | CDF",
        "Fuites, fosses, sinistres : pourquoi une déclaration incomplète coûte plus cher qu'une réparation avouée à Sherbrooke.",
    ),
    "article-pyrrhotite-estrie.html": (
        "Pyrrhotite et fondations en Estrie | CDF",
        "Certaines fondations au Québec ont des problèmes de granulats. En Estrie, inspection et expert, pas un diagnostic en ligne.",
    ),
    "article-schl-premier-acheteur.html": (
        "SCHL et mise de fonds au Québec | premier acheteur | CDF",
        "Moins de 20 % de mise de fonds : l'assurance prêt existe. Le principe pour un premier achat en Estrie, pas vos primes.",
    ),
    "article-magog-ou-sherbrooke.html": (
        "Magog ou Sherbrooke : où acheter ? | CDF",
        "Services, lac, budget, trajet : les vrais écarts entre acheter à Magog et à Sherbrooke, par des courtiers qui font les deux.",
    ),
    "article-bromont-ou-sutton.html": (
        "Bromont ou Sutton : où acheter ? | CDF",
        "Ski, village, condos et maisons : comment départager Bromont et Sutton sans copier un prix de station.",
    ),
    "article-vendre-plex-sherbrooke.html": (
        "Vendre un plex à Sherbrooke | dossier locatif | CDF",
        "Un plex ne se vend pas comme une unifamiliale. Dossier locatif, photos des logements, comparables.",
    ),
    "article-prix-affiche-vs-vente.html": (
        "Prix demandé vs prix de vente en Estrie | CDF",
        "À Sherbrooke, un écart trop grand entre l'affiche et les ventes closes brûle un bien. Comment ancrer le premier prix.",
    ),
    "article-copropriete-documents-quebec.html": (
        "Documents de copropriété au Québec | quoi demander | CDF",
        "Déclaration, PV, fonds, règlements : ce qu'un acheteur de condo à Sherbrooke doit obtenir avant d'offrir.",
    ),
    "article-location-courte-duree-estrie.html": (
        "Location courte durée Magog, Orford, Sutton | CDF",
        "La location courte durée dépend du règlement municipal et de la copropriété. Vérifiez avant d'acheter en Estrie.",
    ),
    "article-photos-mise-en-marche.html": (
        "Photos immobilières en Estrie | mise en marché | CDF",
        "Lumière, neige, lac, pièces vides : comment préparer les photos avant Centris en Estrie.",
    ),
    "article-documents-vente-maison.html": (
        "Documents pour vendre une maison au Québec | CDF",
        "Liste des documents pour vendre une maison au Québec : déclaration du vendeur, certificat de localisation, taxes. Guide Chiasson de Francesco, Estrie.",
    ),
    "article-documents-vente-terrain.html": (
        "Documents pour vendre un terrain au Québec | CDF",
        "Documents pour vendre un terrain au Québec : zonage, certificat d'urbanisme, titres, servitudes. Checklist de l'équipe Chiasson de Francesco, Estrie.",
    ),
    "article-documents-vente-plex.html": (
        "Documents pour vendre un plex au Québec | CDF",
        "Documents pour vendre un plex au Québec : baux, loyers, déclaration du vendeur, inspection. Dossier locatif, Chiasson de Francesco à Sherbrooke.",
    ),
    "article-vendre-acheter-sherbrooke.html": ("Vendre ou acheter à Sherbrooke : quoi savoir | CDF", "Vendre ou acheter à Sherbrooke : quartiers, prix, inspection. Guide de l'équipe Chiasson de Francesco, courtiers RE/MAX."),
    "article-vendre-acheter-magog.html": ("Vendre ou acheter à Magog : quoi savoir | CDF", "Vendre ou acheter à Magog : lac Memphrémagog, condos, chalets. Quoi savoir selon l'équipe Chiasson de Francesco."),
    "article-vendre-acheter-bromont.html": ("Vendre ou acheter à Bromont : quoi savoir | CDF", "Vendre ou acheter à Bromont : ski, village, condos. Guide local de l'équipe Chiasson de Francesco en Estrie."),
    "article-vendre-acheter-orford.html": ("Vendre ou acheter à Orford : quoi savoir | CDF", "Vendre ou acheter à Orford : mont, parc, chalets. Quoi savoir avec l'équipe Chiasson de Francesco."),
    "article-vendre-acheter-north-hatley.html": ("Vendre ou acheter à North Hatley : quoi savoir | CDF", "Vendre ou acheter à North Hatley : lac Massawippi, village. Quoi savoir, équipe Chiasson de Francesco."),
    "article-vendre-acheter-coaticook.html": ("Vendre ou acheter à Coaticook : quoi savoir | CDF", "Vendre ou acheter à Coaticook : ville de services, fermettes, gorge. Guide Chiasson de Francesco, Estrie."),
    "article-vendre-acheter-sutton.html": ("Vendre ou acheter à Sutton : quoi savoir | CDF", "Vendre ou acheter à Sutton : village, ski, condos. Quoi savoir avec Chiasson de Francesco."),
    "article-vendre-acheter-lac-brome.html": ("Vendre ou acheter à Lac-Brome : quoi savoir | CDF", "Vendre ou acheter à Lac-Brome (Knowlton) : village, lac. Guide Chiasson de Francesco, Estrie."),
    "article-vendre-acheter-lennoxville.html": ("Vendre ou acheter à Lennoxville : quoi savoir | CDF", "Vendre ou acheter à Lennoxville (Sherbrooke) : village, plex, campus. Quoi savoir, Chiasson de Francesco."),
    "article-vendre-acheter-fleurimont.html": ("Vendre ou acheter à Fleurimont : quoi savoir | CDF", "Vendre ou acheter à Fleurimont (Sherbrooke) : bungalows, familles, CHUS. Guide Chiasson de Francesco."),
    "article-vendre-acheter-les-nations.html": ("Vendre ou acheter aux Nations : quoi savoir | CDF", "Vendre ou acheter aux Nations (Sherbrooke) : condos, plex, centre. Quoi savoir, Chiasson de Francesco."),
    "article-vendre-acheter-rock-forest.html": ("Vendre ou acheter à Rock Forest : quoi savoir | CDF", "Vendre ou acheter à Rock Forest (Sherbrooke) : terrain, axe Magog. Guide Chiasson de Francesco."),
    "article-vendre-acheter-eastman.html": ("Vendre ou acheter à Eastman : quoi savoir | CDF", "Vendre ou acheter à Eastman : village, Orford, Magog. Quoi savoir, équipe Chiasson de Francesco."),
    "article-vendre-acheter-windsor.html": ("Vendre ou acheter à Windsor : quoi savoir | CDF", "Vendre ou acheter à Windsor (Estrie) : Saint-François, navette Sherbrooke. Guide Chiasson de Francesco."),
    "article-vendre-acheter-stanstead.html": ("Vendre ou acheter à Stanstead : quoi savoir | CDF", "Vendre ou acheter à Stanstead : frontière, Memphrémagog, patrimoine. Guide Chiasson de Francesco."),
    "article-vendre-acheter-cookshire-eaton.html": ("Vendre ou acheter à Cookshire-Eaton : quoi savoir | CDF", "Vendre ou acheter à Cookshire-Eaton : terrains, Sawyerville, route 108. Guide Chiasson de Francesco."),
    "article-vendre-acheter-ayers-cliff.html": ("Vendre ou acheter à Ayer's Cliff : quoi savoir | CDF", "Vendre ou acheter à Ayer's Cliff : lac Massawippi. Quoi savoir, Chiasson de Francesco."),
    "article-vendre-acheter-austin.html": ("Vendre ou acheter à Austin : quoi savoir | CDF", "Vendre ou acheter à Austin : près d'Orford et Magog. Guide Chiasson de Francesco."),
    "article-vendre-acheter-richmond.html": ("Vendre ou acheter à Richmond : quoi savoir | CDF", "Vendre ou acheter à Richmond : Saint-François, Estrie. Quoi savoir, Chiasson de Francesco."),
    "article-vendre-acheter-compton.html": ("Vendre ou acheter à Compton : quoi savoir | CDF", "Vendre ou acheter à Compton : village, rangs, fermettes. Guide Chiasson de Francesco, Estrie."),
    "article-vendre-acheter-waterville.html": ("Vendre ou acheter à Waterville : quoi savoir | CDF", "Vendre ou acheter à Waterville : entre Sherbrooke et Coaticook. Guide Chiasson de Francesco."),
    "article-vendre-acheter-hatley.html": ("Vendre ou acheter à Hatley : quoi savoir | CDF", "Vendre ou acheter à Hatley : canton, Massawippi, pas North Hatley. Guide Chiasson de Francesco."),
    "article-vendre-acheter-mont-bellevue.html": ("Vendre ou acheter à Mont-Bellevue : quoi savoir | CDF", "Vendre ou acheter à Mont-Bellevue (Sherbrooke) : unifamiliales, parc. Guide Chiasson de Francesco."),
    "article-vendre-acheter-brompton.html": ("Vendre ou acheter à Brompton : quoi savoir | CDF", "Vendre ou acheter à Brompton (Sherbrooke) : vallée, Saint-François. Guide Chiasson de Francesco."),
    "article-vendre-acheter-val-des-sources.html": ("Vendre ou acheter à Val-des-Sources : quoi savoir | CDF", "Vendre ou acheter à Val-des-Sources (Asbestos) : Estrie, MRC des Sources. Guide Chiasson de Francesco."),
    "article-vendre-acheter-lac-megantic.html": ("Vendre ou acheter à Lac-Mégantic : quoi savoir | CDF", "Vendre ou acheter à Lac-Mégantic : ville, lac, Granit. Guide Chiasson de Francesco."),
}

REGION_META = {
    "bromont": ("Courtier immobilier à Bromont | Chiasson De Francesco", "Acheter ou vendre à Bromont : ski, vélo et maisons de village. L'équipe Chiasson de Francesco vous accompagne en Estrie."),
    "coaticook": ("Courtier immobilier à Coaticook | Chiasson De Francesco", "Acheter ou vendre à Coaticook : ville de services, gorge et campagne en Estrie. Équipe Chiasson de Francesco, RE/MAX."),
    "compton": ("Courtier immobilier à Compton | CDF", "Maisons et fermettes à Compton, en Estrie. L'équipe Chiasson de Francesco vous accompagne pour acheter ou vendre."),
    "cookshire-eaton": ("Courtier à Cookshire-Eaton | terrains et maisons | CDF", "Propriétés et terrains à Cookshire-Eaton et Sawyerville. Courtiers Chiasson de Francesco pour un achat ou une vente en Estrie."),
    "danville": ("Courtier immobilier à Danville | CDF", "Acheter ou vendre à Danville, Estrie. Accompagnement par l'équipe Chiasson de Francesco, RE/MAX D'ABORD."),
    "eastman": ("Courtier immobilier à Eastman | près d'Orford | CDF", "Maisons et chalets à Eastman, près d'Orford et Magog. L'équipe Chiasson de Francesco vous accompagne en Estrie."),
    "lac-aylmer": ("Propriétés au lac Aylmer | courtier Estrie | CDF", "Acheter ou vendre en bord du lac Aylmer (Stratford, Weedon). Courtiers Chiasson de Francesco à Sherbrooke."),
    "lac-brome": ("Courtier à Lac-Brome et Knowlton | CDF", "Maisons et bord de lac à Lac-Brome (Knowlton). L'équipe Chiasson de Francesco vous accompagne."),
    "lac-massawippi": ("Propriétés au lac Massawippi | North Hatley | CDF", "Acheter ou vendre autour du lac Massawippi et North Hatley. Équipe Chiasson de Francesco, courtiers RE/MAX."),
    "lac-megantic": ("Courtier immobilier au lac Mégantic | CDF", "Acheter ou vendre une propriété à Lac-Mégantic et au lac. Équipe Chiasson de Francesco, Estrie."),
    "lac-memphremagog": ("Propriétés au lac Memphrémagog | Magog, Orford | CDF", "Bord de lac à Magog, Orford et Newport. L'équipe Chiasson de Francesco vous accompagne sur le Memphrémagog."),
    "magog": ("Courtier immobilier à Magog | lac Memphrémagog", "Acheter ou vendre à Magog, porte d'entrée du lac Memphrémagog. Maisons, condos et chalets avec Chiasson de Francesco."),
    "north-hatley": ("Courtier immobilier à North Hatley | CDF", "Acheter ou vendre à North Hatley et au lac Massawippi. L'équipe Chiasson de Francesco, courtiers RE/MAX en Estrie."),
    "orford": ("Courtier immobilier à Orford | mont Orford", "Maisons et chalets à Orford, au pied du mont et du parc national. Équipe Chiasson de Francesco en Estrie."),
    "richmond": ("Courtier immobilier à Richmond | rivière Saint-François | CDF", "Acheter ou vendre à Richmond, sur la rivière Saint-François. Courtiers Chiasson de Francesco, RE/MAX."),
    "sherbrooke": ("Courtier immobilier à Sherbrooke | Chiasson De Francesco", "Acheter ou vendre à Sherbrooke : Les Nations, Fleurimont, Lennoxville, Mont-Bellevue. Équipe Chiasson de Francesco, RE/MAX."),
    "stanstead": ("Courtier immobilier à Stanstead | frontière | CDF", "Propriétés à Stanstead, près du lac Memphrémagog et de la frontière. Équipe Chiasson de Francesco."),
    "sutton": ("Courtier immobilier à Sutton | montagne | CDF", "Acheter ou vendre à Sutton, village de montagne en Estrie. Ski, arts et maisons : équipe Chiasson de Francesco."),
    "val-des-sources": ("Courtier à Val-des-Sources | CDF", "Maisons à Val-des-Sources (Asbestos). Courtiers Chiasson de Francesco pour un achat ou une vente en Estrie."),
    "weedon": ("Courtier immobilier à Weedon | Estrie | CDF", "Acheter ou vendre à Weedon, Estrie, près du lac Aylmer. Accompagnement Chiasson de Francesco, RE/MAX."),
    "windsor": ("Courtier immobilier à Windsor | Estrie | CDF", "Propriétés à Windsor, Estrie, sur la Saint-François. L'équipe Chiasson de Francesco vous accompagne."),
    "lennoxville": ("Courtier immobilier à Lennoxville | CDF", "Acheter ou vendre à Lennoxville (Sherbrooke) : village universitaire, unifamiliales et multiplex. Équipe Chiasson de Francesco."),
    "fleurimont": ("Courtier immobilier à Fleurimont | Sherbrooke | CDF", "Maisons à Fleurimont, Sherbrooke : quartiers familiaux, bungalows et accès hôpital. Courtiers Chiasson de Francesco."),
    "rock-forest": ("Courtier à Rock Forest–Saint-Élie–Deauville | CDF", "Acheter ou vendre à Rock Forest, Sherbrooke : maisons, terrains plus grands, accès Magog. Équipe Chiasson de Francesco."),
    "les-nations": ("Courtier Les Nations Sherbrooke | condos et centre | CDF", "Condos, plex et centre-ville aux Nations, Sherbrooke. Acheter ou vendre avec l'équipe Chiasson de Francesco, RE/MAX."),
    "brompton": ("Courtier immobilier à Brompton | Sherbrooke | CDF", "Maisons à Brompton (Sherbrooke), vallée de la Saint-François. Acheter ou vendre avec Chiasson de Francesco."),
    "mont-bellevue": ("Courtier Mont-Bellevue Sherbrooke | CDF", "Unifamiliales et rues résidentielles à Mont-Bellevue, Sherbrooke. Équipe Chiasson de Francesco, RE/MAX D'ABORD."),
    "ayers-cliff": ("Courtier immobilier à Ayer's Cliff | lac Massawippi | CDF", "Maisons et bord de lac à Ayer's Cliff, Estrie. L'équipe Chiasson de Francesco vous accompagne au Massawippi."),
    "austin": ("Courtier immobilier à Austin | près d'Orford | CDF", "Maisons et chalets à Austin, Estrie, entre Magog et le mont Orford. Équipe Chiasson de Francesco."),
    "waterville": ("Courtier immobilier à Waterville | Estrie | CDF", "Acheter ou vendre à Waterville, entre Sherbrooke et Coaticook. Courtiers Chiasson de Francesco."),
    "hatley": ("Courtier immobilier à Hatley | Cantons-de-l'Est | CDF", "Propriétés à Hatley, près de North Hatley et du Massawippi. Équipe Chiasson de Francesco, Estrie."),
    "milan": ("Courtier immobilier à Milan | Estrie | CDF", "Acheter ou vendre à Milan, Estrie (MRC du Granit). L'équipe Chiasson de Francesco y inscrit aussi des propriétés."),
    "saint-isidore-de-clifton": ("Courtier à Saint-Isidore-de-Clifton | fermettes | CDF", "Fermettes et rangs à Saint-Isidore-de-Clifton, Estrie. L'équipe Chiasson de Francesco y accompagne achat et vente."),
}

LISTING_OFFERS = {
    "25365838": {"price": "1300", "availability": "https://schema.org/InStock", "unitCode": "MON", "name": "Condo à louer : 31, Rue King O., app. 304, Sherbrooke"},
    "26831137": {"price": "234900", "availability": "https://schema.org/InStock", "name": "Maison à vendre : 505, Chemin de la Yard, Milan"},
    "23954624": {"price": "949900", "availability": "https://schema.org/InStock", "name": "Fermette à vendre : 251, 9e Rang, Saint-Isidore-de-Clifton"},
    "10043722": {"price": "100000", "availability": "https://schema.org/InStock", "name": "Fonds de commerce à vendre : 182, Rue Wellington N., Sherbrooke"},
    "13807137": {"price": "425000", "availability": "https://schema.org/InStock", "name": "Co-propriété à vendre : 760, Av. Honoré-Mercier, Québec"},
    "20828105": {"price": "650000", "availability": "https://schema.org/InStock", "name": "Bâtisse commerciale à vendre : 800, Rue Tessier, Sherbrooke"},
    "17958008": {"price": "1475000", "availability": "https://schema.org/InStock", "name": "Co-propriété commerciale à vendre : 1111, Rue Saint-Urbain, Montréal"},
    "27084256": {"price": "54000", "availability": "https://schema.org/InStock", "name": "Terrain à vendre : Boul. des Chasseurs, Saint-Alexis-des-Monts"},
    "11185705": {"price": "1275000", "availability": "https://schema.org/InStock", "name": "Terrain à vendre : Route 108, Cookshire-Eaton"},
}

ARTICLES = {
    "article-previsions-2026.html": ("2026-01-05", "Pierre-Olivier Chiasson", "pierre-olivier.html"),
    "article-eviter-les-pieges.html": ("2025-11-15", "Pierre-Olivier Chiasson", "pierre-olivier.html"),
    "article-frais-caches.html": ("2025-10-30", "Pierre-Olivier Chiasson", "pierre-olivier.html"),
    "article-investir-sherbrooke.html": ("2025-11-28", "Pierre-Olivier Chiasson", "pierre-olivier.html"),
    "article-home-staging.html": ("2025-12-12", "Pierre-Olivier Chiasson", "pierre-olivier.html"),
    "article-courtier-ou-vente-libre.html": ("2026-08-18", "Pierre-Olivier Chiasson", "pierre-olivier.html"),
    "article-evaluation-marchande-estrie.html": ("2026-08-18", "Marco De Francesco", "marco.html"),
    "article-delai-vente-estrie.html": ("2026-08-18", "Jade Sirois", "jade.html"),
    "article-offre-achat-quebec.html": ("2026-08-18", "Pierre-Olivier Chiasson", "pierre-olivier.html"),
    "article-bord-de-lac-estrie.html": ("2026-08-18", "Marco De Francesco", "marco.html"),
    "article-condo-sherbrooke.html": ("2026-08-18", "Jade Sirois", "jade.html"),
    "article-premiere-maison-estrie.html": ("2026-08-18", "Jade Sirois", "jade.html"),
    "article-zonage-commercial-sherbrooke.html": ("2026-08-18", "Pierre-Olivier Chiasson", "pierre-olivier.html"),
    "article-inspection-maison-estrie.html": ("2026-08-18", "Jade Sirois", "jade.html"),
    "article-vendre-condo-sherbrooke.html": ("2026-08-18", "Pierre-Olivier Chiasson", "pierre-olivier.html"),
    "article-navette-sherbrooke.html": ("2026-08-18", "Marco De Francesco", "marco.html"),
    "article-terrain-estrie.html": ("2026-08-18", "Pierre-Olivier Chiasson", "pierre-olivier.html"),
    "article-vendre-hiver-estrie.html": ("2026-08-18", "Jade Sirois", "jade.html"),
    "article-notaire-immobilier-quebec.html": ("2026-08-18", "Pierre-Olivier Chiasson", "pierre-olivier.html"),
    "article-droits-mutation-sherbrooke.html": ("2026-08-18", "Jade Sirois", "jade.html"),
    "article-contre-offre-quebec.html": ("2026-08-18", "Marco De Francesco", "marco.html"),
    "article-declaration-vendeur.html": ("2026-08-18", "Pierre-Olivier Chiasson", "pierre-olivier.html"),
    "article-pyrrhotite-estrie.html": ("2026-08-18", "Marco De Francesco", "marco.html"),
    "article-schl-premier-acheteur.html": ("2026-08-18", "Jade Sirois", "jade.html"),
    "article-magog-ou-sherbrooke.html": ("2026-08-18", "Marco De Francesco", "marco.html"),
    "article-bromont-ou-sutton.html": ("2026-08-18", "Pierre-Olivier Chiasson", "pierre-olivier.html"),
    "article-vendre-plex-sherbrooke.html": ("2026-08-18", "Pierre-Olivier Chiasson", "pierre-olivier.html"),
    "article-prix-affiche-vs-vente.html": ("2026-08-18", "Marco De Francesco", "marco.html"),
    "article-copropriete-documents-quebec.html": ("2026-08-18", "Jade Sirois", "jade.html"),
    "article-location-courte-duree-estrie.html": ("2026-08-18", "Marco De Francesco", "marco.html"),
    "article-photos-mise-en-marche.html": ("2026-08-18", "Jade Sirois", "jade.html"),
    "article-documents-vente-maison.html": ("2026-08-18", "Jade Sirois", "jade.html"),
    "article-documents-vente-terrain.html": ("2026-08-18", "Pierre-Olivier Chiasson", "pierre-olivier.html"),
    "article-documents-vente-plex.html": ("2026-08-18", "Marco De Francesco", "marco.html"),
    "article-vendre-acheter-sherbrooke.html": ("2026-08-18", "Pierre-Olivier Chiasson", "pierre-olivier.html"),
    "article-vendre-acheter-magog.html": ("2026-08-18", "Marco De Francesco", "marco.html"),
    "article-vendre-acheter-bromont.html": ("2026-08-18", "Pierre-Olivier Chiasson", "pierre-olivier.html"),
    "article-vendre-acheter-orford.html": ("2026-08-18", "Marco De Francesco", "marco.html"),
    "article-vendre-acheter-north-hatley.html": ("2026-08-18", "Marco De Francesco", "marco.html"),
    "article-vendre-acheter-coaticook.html": ("2026-08-18", "Jade Sirois", "jade.html"),
    "article-vendre-acheter-sutton.html": ("2026-08-18", "Pierre-Olivier Chiasson", "pierre-olivier.html"),
    "article-vendre-acheter-lac-brome.html": ("2026-08-18", "Marco De Francesco", "marco.html"),
    "article-vendre-acheter-lennoxville.html": ("2026-08-18", "Jade Sirois", "jade.html"),
    "article-vendre-acheter-fleurimont.html": ("2026-08-18", "Jade Sirois", "jade.html"),
    "article-vendre-acheter-les-nations.html": ("2026-08-18", "Pierre-Olivier Chiasson", "pierre-olivier.html"),
    "article-vendre-acheter-rock-forest.html": ("2026-08-18", "Marco De Francesco", "marco.html"),
    "article-vendre-acheter-eastman.html": ("2026-08-18", "Marco De Francesco", "marco.html"),
    "article-vendre-acheter-windsor.html": ("2026-08-18", "Jade Sirois", "jade.html"),
    "article-vendre-acheter-stanstead.html": ("2026-08-18", "Marco De Francesco", "marco.html"),
    "article-vendre-acheter-cookshire-eaton.html": ("2026-08-18", "Pierre-Olivier Chiasson", "pierre-olivier.html"),
    "article-vendre-acheter-ayers-cliff.html": ("2026-08-18", "Marco De Francesco", "marco.html"),
    "article-vendre-acheter-austin.html": ("2026-08-18", "Marco De Francesco", "marco.html"),
    "article-vendre-acheter-richmond.html": ("2026-08-18", "Jade Sirois", "jade.html"),
    "article-vendre-acheter-compton.html": ("2026-08-18", "Pierre-Olivier Chiasson", "pierre-olivier.html"),
    "article-vendre-acheter-waterville.html": ("2026-08-18", "Jade Sirois", "jade.html"),
    "article-vendre-acheter-hatley.html": ("2026-08-18", "Marco De Francesco", "marco.html"),
    "article-vendre-acheter-mont-bellevue.html": ("2026-08-18", "Jade Sirois", "jade.html"),
    "article-vendre-acheter-brompton.html": ("2026-08-18", "Jade Sirois", "jade.html"),
    "article-vendre-acheter-val-des-sources.html": ("2026-08-18", "Pierre-Olivier Chiasson", "pierre-olivier.html"),
    "article-vendre-acheter-lac-megantic.html": ("2026-08-18", "Pierre-Olivier Chiasson", "pierre-olivier.html"),
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
    title = listing.get("title") or ""
    if " : " in title:
        street = title.split(" : ", 1)[0].strip()
    elif "\u2014" in title:
        street = title.split("\u2014", 1)[0].strip()
    else:
        street = title.split(",")[0].strip()
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
        (f"{BASE}/vendre.html", "0.8"),
        (f"{BASE}/acheter.html", "0.8"),
        (f"{BASE}/courtier-commercial.html", "0.8"),
        (f"{BASE}/courtier-acheteur-estrie.html", "0.8"),
        (f"{BASE}/fermette-estrie.html", "0.7"),
        (f"{BASE}/chalet-estrie.html", "0.7"),
        (f"{BASE}/plex-sherbrooke.html", "0.7"),
        (f"{BASE}/regions-desservies.html", "0.8"),
        (f"{BASE}/blog.html", "0.7"),
        (f"{BASE}/pierre-olivier.html", "0.7"),
        (f"{BASE}/marco.html", "0.7"),
        (f"{BASE}/jade.html", "0.7"),
        (f"{BASE}/confidentialite.html", "0.3"),
    ]
    for slug in REGION_META:
        urls.append((f"{BASE}/regions/{slug}.html", "0.8" if slug in {"sherbrooke", "magog", "bromont", "orford", "north-hatley", "lennoxville", "fleurimont", "les-nations"} else "0.6"))
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
