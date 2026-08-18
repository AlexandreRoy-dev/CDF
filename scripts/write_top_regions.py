#!/usr/bin/env python3
"""Write the five highest-intent Estrie region pages (unique GEO copy + FAQ schema)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://chiassondefrancesco.ca"

PAGES = [
    {
        "slug": "sherbrooke",
        "name": "Sherbrooke",
        "title": "Courtier immobilier à Sherbrooke | Chiasson De Francesco",
        "description": "Acheter ou vendre à Sherbrooke : Les Nations, Fleurimont, Lennoxville, Mont-Bellevue. Équipe Chiasson de Francesco, RE/MAX.",
        "h1": "Acheter ou vendre une propriété à Sherbrooke",
        "lead": "L'équipe Chiasson de Francesco, courtiers immobiliers RE/MAX D'ABORD à Sherbrooke, accompagne acheteurs et vendeurs dans Les Nations, Fleurimont, Lennoxville, Mont-Bellevue, Brompton et Rock Forest.",
        "intro": "Sherbrooke est le pôle urbain de l'Estrie : universités, hôpitaux, centre-ville et quartiers familiaux. Un courtier local sert autant à lire le prix réel d'une rue qu'à éviter une offre trop haute ou trop basse.",
        "sections": [
            (
                "Quartiers et types de biens",
                "Les Nations et le centre-ville concentrent condos et plex. Mont-Bellevue et Fleurimont accueillent beaucoup de unifamiliales. Lennoxville attire les ménages qui veulent le village universitaire. Rock Forest et Brompton offrent plus de terrain. Côté commercial, des artères comme Wellington et Tessier restent actives pour locaux et bâtisses.",
            ),
            (
                "Acheter à Sherbrooke",
                "Un achat ici se joue souvent sur l'inspection, le zonage (surtout en mixte résidentiel-commercial) et la comparaison avec des ventes récentes du même secteur — pas seulement le prix demandé. Nous filtrons les inscriptions Centris, visitons avec vous et négocions les conditions, pas seulement le montant.",
            ),
            (
                "Vendre une propriété à Sherbrooke",
                "Vendre à Sherbrooke, c'est d'abord une évaluation marchande honnête, puis une mise en marché (photos, description, réseau) adaptée au type de bien : condo, maison, plex ou local. L'équipe prépare les visites et gère les offres jusqu'à l'acte.",
            ),
        ],
        "related": [
            ("Propriétés à vendre", "../proprietes.html"),
            ("Vendre maintenant ou attendre ?", "../evaluation.html"),
            ("Magog et le lac Memphrémagog", "magog.html"),
            ("Pierre-Olivier Chiasson", "../pierre-olivier.html"),
        ],
        "faqs": [
            (
                "Faut-il un courtier pour vendre une maison à Sherbrooke ?",
                "Ce n'est pas obligatoire, mais un courtier local connaît les prix par quartier, prépare le dossier (évaluation, photos, description) et négocie les conditions. L'équipe Chiasson de Francesco travaille à Sherbrooke avec RE/MAX D'ABORD.",
            ),
            (
                "Quels quartiers de Sherbrooke sont les plus demandés ?",
                "La demande varie selon le type de bien. Les Nations et le centre attirent condos et plex ; Fleurimont, Mont-Bellevue et Lennoxville restent recherchés pour les unifamiliales. Un courtier compare les ventes récentes plutôt que les moyennes de toute la ville.",
            ),
            (
                "Combien de temps faut-il pour vendre à Sherbrooke ?",
                "Le délai dépend du prix, de l'état du bien et du secteur. Une propriété bien positionnée peut recevoir des offres en quelques semaines ; un bien trop cher ou atypique prend plus longtemps. Une évaluation marchande en amont réduit ce risque.",
            ),
            (
                "Offrez-vous une évaluation gratuite à Sherbrooke ?",
                "Oui. L'équipe propose une évaluation marchande et un questionnaire de timing de mise en marché pour les propriétaires en Estrie, sans obligation de signer un contrat le jour même.",
            ),
            (
                "Travaillez-vous aussi le commercial à Sherbrooke ?",
                "Oui. Pierre-Olivier Chiasson et Marco De Francesco inscrivent des locaux, fonds de commerce et bâtisses à Sherbrooke, en plus du résidentiel.",
            ),
        ],
    },
    {
        "slug": "magog",
        "name": "Magog",
        "title": "Courtier immobilier à Magog | lac Memphrémagog",
        "description": "Acheter ou vendre à Magog, porte d'entrée du lac Memphrémagog. Maisons, condos et chalets avec Chiasson de Francesco.",
        "h1": "Acheter ou vendre une propriété à Magog",
        "lead": "L'équipe Chiasson de Francesco, courtiers RE/MAX à Sherbrooke, accompagne l'achat et la vente à Magog : centre-ville, bord du lac Memphrémagog, condos et résidences de villégiature.",
        "intro": "Magog combine un vrai centre-ville, l'accès au lac et la proximité d'Orford. Les prix et les délais n'ont rien à voir entre un condo en ville, une maison de rang et un bord de lac — d'où l'intérêt d'un courtier qui travaille l'Estrie au quotidien.",
        "sections": [
            (
                "Centre-ville, lac et villégiature",
                "Le noyau urbain convient aux acheteurs qui veulent marcher vers les commerces. Le corridor du lac (et les rues qui y mènent) se négocie selon la vue, l'accès à l'eau et les contraintes de bande riveraine. Les secteurs plus résidentiels hors lac restent plus accessibles pour une résidence principale.",
            ),
            (
                "Acheter à Magog",
                "Sur le Memphrémagog, vérifiez titres, servitudes, champ d'épuration ou égouts, et la réglementation municipale avant d'offrir. Nous comparons des ventes comparables au même type de bien — pas un chalet avec un bungalow de rangée.",
            ),
            (
                "Vendre à Magog",
                "Une mise en marché au lac se joue sur les photos, la saison et un prix ancré dans les ventes récentes, pas dans l'espoir d'un « prix Magog » unique. Nous préparons le dossier et ciblons acheteurs locaux et hors région.",
            ),
        ],
        "related": [
            ("Propriétés à vendre", "../proprietes.html"),
            ("Évaluation de timing de vente", "../evaluation.html"),
            ("Orford et le mont Orford", "orford.html"),
            ("Lac Memphrémagog", "lac-memphremagog.html"),
        ],
        "faqs": [
            (
                "Quelle est la différence de prix entre Magog centre et le bord du lac ?",
                "Le bord du lac Memphrémagog se vend en général plus cher, surtout avec accès à l'eau ou une vue dégagée. Le centre-ville et les rues sans lac restent plus abordables. Seules des ventes comparables du même type de bien donnent un vrai intervalle.",
            ),
            (
                "Peut-on acheter un chalet à Magog comme résidence principale ?",
                "Oui, plusieurs propriétés de villégiature sont habitables à l'année, à condition de vérifier isolation, services (eau, égouts ou fosse) et zonage. Un courtier fait cette lecture avant l'offre.",
            ),
            (
                "Travaillez-vous Magog depuis Sherbrooke ?",
                "Oui. L'équipe Chiasson de Francesco est basée à Sherbrooke et dessert Magog, Orford et le reste de l'Estrie. Les visites et les évaluations se font sur place.",
            ),
            (
                "Quand est-il préférable de mettre en vente à Magog ?",
                "Le printemps et le début d'été attirent souvent plus d'acheteurs villégiature, mais un bien bien préparé se vend aussi hors saison. Le questionnaire de timing de l'équipe aide à trancher selon votre situation, pas seulement le calendrier touristique.",
            ),
        ],
    },
    {
        "slug": "bromont",
        "name": "Bromont",
        "title": "Courtier immobilier à Bromont | Chiasson De Francesco",
        "description": "Acheter ou vendre à Bromont : ski, vélo et maisons de village. L'équipe Chiasson de Francesco vous accompagne en Estrie.",
        "h1": "Acheter ou vendre une propriété à Bromont",
        "lead": "L'équipe Chiasson de Francesco accompagne l'achat et la vente à Bromont : village, versant ski, condos et maisons pour résidence principale ou villégiature, avec un ancrage RE/MAX en Estrie.",
        "intro": "Bromont n'est pas un quartier de Sherbrooke : le marché y mélange skieurs, navetteurs vers la Rive-Sud et familles qui veulent le village. Les condos près de la montagne et les unifamiliales en lotissement ne se comparent pas.",
        "sections": [
            (
                "Village, montagne et lotissements",
                "Le village reste le point de repère pour commerces et services. Les secteurs liés au ski et au vélo de montagne attirent la villégiature et la location courte durée — sous réserve des règlements municipaux. Les développements résidentiels hors pente conviennent davantage à une résidence à l'année.",
            ),
            (
                "Acheter à Bromont",
                "Avant d'offrir, on vérifie les frais de copropriété, les règles de location, l'accès hivernal et, pour certains secteurs, les contraintes de pente et de drainage. Nous croisons les inscriptions avec des ventes récentes du même produit (condo ski vs maison de village).",
            ),
            (
                "Vendre à Bromont",
                "Le bon acheteur n'est pas toujours local : beaucoup viennent de Montréal ou de la Montérégie. Une mise en marché claire (usage réel du bien, charges, saisonnalité) évite les visites stériles et les rabais tardifs.",
            ),
        ],
        "related": [
            ("Propriétés à vendre", "../proprietes.html"),
            ("Évaluation de timing de vente", "../evaluation.html"),
            ("Sutton", "sutton.html"),
            ("Lac-Brome (Knowlton)", "lac-brome.html"),
        ],
        "faqs": [
            (
                "Bromont est-il plus cher que Sherbrooke ?",
                "Souvent oui pour un produit comparable, surtout près de la montagne ou dans les projets récents. L'écart n'est pas automatique : un condo chargé en frais peut se rapprocher d'une unifamiliale sherbrookoise. On compare des ventes, pas des impressions.",
            ),
            (
                "Peut-on louer à court terme un condo à Bromont ?",
                "Cela dépend du règlement de copropriété et des règles municipales. Plusieurs immeubles l'interdisent ou le limitent. Il faut le vérifier avant l'achat si la location fait partie du projet.",
            ),
            (
                "L'équipe Chiasson de Francesco se déplace-t-elle à Bromont ?",
                "Oui. Les courtiers sont basés à Sherbrooke et desservent Bromont, Sutton et le reste de l'Estrie pour les visites, évaluations et inscriptions.",
            ),
            (
                "Maison de village ou condo ski : que choisir ?",
                "Une maison de village convient mieux à une résidence principale à l'année. Un condo près des pentes vise souvent la villégiature. Le bon choix dépend de l'usage, des charges et de votre horizon de détention — pas seulement de la vue.",
            ),
        ],
    },
    {
        "slug": "orford",
        "name": "Orford",
        "title": "Courtier immobilier à Orford | mont Orford",
        "description": "Maisons et chalets à Orford, au pied du mont et du parc national. Équipe Chiasson de Francesco en Estrie.",
        "h1": "Acheter ou vendre une propriété à Orford",
        "lead": "L'équipe Chiasson de Francesco accompagne l'achat et la vente à Orford : chalets, maisons au pied du mont Orford et propriétés près du parc national, en lien avec Magog et Eastman.",
        "intro": "Orford se vit autour du mont, du parc et des lacs tout proches. Le marché mélange résidences principales, villégiature et quelques immeubles de plus petite densité. Un prix « vue montagne » n'est pas un prix « rang ».",
        "sections": [
            (
                "Mont Orford, parc et lacs",
                "Les rues proches du ski et du parc national se distinguent des secteurs plus champêtres vers Eastman. L'accès au lac Memphrémagog se fait surtout via Magog ; à Orford, on achète davantage le paysage, les sentiers et la saisonnalité.",
            ),
            (
                "Acheter à Orford",
                "Vérifiez isolation, chauffage, puits ou égouts, et les contraintes du milieu naturel (bandes riveraines, pentes). Pour un chalet, confirmez s'il est vraiment quatre-saisons avant d'en faire une résidence principale.",
            ),
            (
                "Vendre à Orford",
                "Les acheteurs hors région cherchent des photos de saison et une description honnête (distance de Magog, d'autoroute, des pentes). Nous ancrons le prix sur des ventes d'Orford et d'Eastman comparables, pas sur Magog centre.",
            ),
        ],
        "related": [
            ("Magog", "magog.html"),
            ("Eastman", "eastman.html"),
            ("Propriétés à vendre", "../proprietes.html"),
            ("Évaluation de timing de vente", "../evaluation.html"),
        ],
        "faqs": [
            (
                "Orford et Magog, est-ce le même marché ?",
                "Non. Magog a un centre-ville et davantage de condos ; Orford est plus montagne et villégiature. Les prix au pied du mont ne se calquent pas sur une rue de Magog sans lac.",
            ),
            (
                "Peut-on habiter à l'année un chalet à Orford ?",
                "Seulement si le bâtiment, le chauffage et les services le permettent. Beaucoup de chalets restent saisonniers. L'inspection et le certificat de localisation évitent de le découvrir après l'offre.",
            ),
            (
                "Faut-il un courtier local pour Orford ?",
                "Un courtier qui travaille Magog–Orford–Eastman lit mieux les comparables que quelqu'un qui ne vient qu'en fin de semaine. L'équipe Chiasson de Francesco dessert ce corridor depuis Sherbrooke.",
            ),
            (
                "Quand vendre un chalet à Orford ?",
                "La fin d'hiver et le printemps attirent souvent les acheteurs ski et été, mais un bien bien préparé se vend hors pic. Le timing dépend aussi de votre prochain logement — d'où le questionnaire d'évaluation de l'équipe.",
            ),
        ],
    },
    {
        "slug": "north-hatley",
        "name": "North Hatley",
        "title": "Courtier immobilier à North Hatley | CDF",
        "description": "Acheter ou vendre à North Hatley et au lac Massawippi. L'équipe Chiasson de Francesco, courtiers RE/MAX en Estrie.",
        "h1": "Acheter ou vendre une propriété à North Hatley",
        "lead": "L'équipe Chiasson de Francesco accompagne l'achat et la vente à North Hatley : village au bord du lac Massawippi, maisons de caractère et propriétés de villégiature en Estrie.",
        "intro": "North Hatley est un petit marché : peu d'inscriptions, beaucoup d'acheteurs sensibles au village, à la vue lac et au cachet patrimonial. Une erreur de prix se paie longtemps, à la hausse comme à la baisse.",
        "sections": [
            (
                "Village et lac Massawippi",
                "Le village marche vers les commerces et l'eau. Les rues en hauteur ou en retrait du lac n'ont pas le même bassin d'acheteurs. Autour du Massawippi, Sainte-Catherine-de-Hatley et d'autres rives se comparent parfois mieux qu'une maison de Sherbrooke.",
            ),
            (
                "Acheter à North Hatley",
                "Sur un marché mince, les « prix demandés » trompent. On s'appuie sur les ventes closes, l'état réel du bâtiment (souvent plus ancien) et les contraintes riveraines. Une inspection rigoureuse n'est pas optionnelle.",
            ),
            (
                "Vendre à North Hatley",
                "Le dossier photo et l'histoire du lieu comptent autant que le nombre de chambres. Nous ciblons acheteurs régionaux et hors Estrie sans gonfler le prix au-delà de ce que le lac a réellement payé récemment.",
            ),
        ],
        "related": [
            ("Lac Massawippi", "lac-massawippi.html"),
            ("Sherbrooke", "sherbrooke.html"),
            ("Propriétés à vendre", "../proprietes.html"),
            ("Évaluation de timing de vente", "../evaluation.html"),
        ],
        "faqs": [
            (
                "Pourquoi les maisons à North Hatley semblent-elles chères ?",
                "L'offre est faible et le lac Massawippi attire une clientèle de villégiature et de résidence secondaire. Le prix se justifie (ou non) par des ventes comparables du village ou des rives, pas par le prix médian de Sherbrooke.",
            ),
            (
                "Faut-il parler anglais pour acheter à North Hatley ?",
                "Le village est historiquement bilingue. L'équipe Chiasson de Francesco travaille en français et en anglais (Marco De Francesco est bilingue), ce qui aide avec les notaires, inspecteurs et acheteurs hors Québec.",
            ),
            (
                "North Hatley convient-il comme résidence principale ?",
                "Oui pour qui accepte un village plus petit, des déplacements vers Sherbrooke pour certains services, et parfois un bâtiment plus ancien. Ce n'est pas le même quotidien qu'un quartier de Fleurimont.",
            ),
            (
                "Comment vendre sans brader au lac Massawippi ?",
                "En collant le prix aux ventes récentes du même type (bord de lac vs village), en préparant l'état du bâtiment, et en laissant le temps au bon acheteur. Une surcote « parce que c'est North Hatley » allonge souvent la mise en marché.",
            ),
        ],
    },
]


def json_ld(page: dict) -> str:
    canonical = f"{BASE}/regions/{page['slug']}.html"
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Place",
                "name": page["name"],
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": page["name"],
                    "addressRegion": "QC",
                    "addressCountry": "CA",
                },
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Accueil", "item": f"{BASE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Régions desservies", "item": f"{BASE}/regions-desservies.html"},
                    {"@type": "ListItem", "position": 3, "name": page["name"], "item": canonical},
                ],
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a},
                    }
                    for q, a in page["faqs"]
                ],
            },
        ],
    }
    return json.dumps(graph, ensure_ascii=False, indent=2)


def render(page: dict) -> str:
    sections = "\n".join(
        f"""      <h2 class="font-heading text-2xl font-bold text-brand-navy mt-10 mb-3">{h}</h2>
      <p class="text-gray-600 leading-relaxed mb-6">{p}</p>"""
        for h, p in page["sections"]
    )
    faqs_html = "\n".join(
        f"""        <div class="border border-gray-200 rounded-xl p-5 bg-white">
          <h3 class="font-semibold text-brand-navy mb-2">{q}</h3>
          <p class="text-gray-600 leading-relaxed">{a}</p>
        </div>"""
        for q, a in page["faqs"]
    )
    related = "\n".join(
        f'          <li><a href="{href}" class="text-brand-navy font-medium hover:text-brand-red">{label}</a></li>'
        for label, href in page["related"]
    )
    ld = json_ld(page)
    return f"""<!DOCTYPE html>
<html lang="fr-CA" class="scroll-smooth">
<head>
  <link rel="icon" type="image/svg+xml" href="/src/assets/favicon.svg">
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-VBQPR5ZNV0"></script>
  <script src="/src/assets/js/ga.js"></script>
  <title>{page["title"]}</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta name="description" content="{page["description"]}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <meta name="author" content="Équipe Chiasson de Francesco">
  <link rel="canonical" href="{BASE}/regions/{page["slug"]}.html">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{BASE}/regions/{page["slug"]}.html">
  <meta property="og:site_name" content="Chiasson de Francesco">
  <meta property="og:title" content="{page["title"]}">
  <meta property="og:description" content="{page["description"]}">
  <meta property="og:image" content="{BASE}/src/assets/images/chiassondefrancescoteam.jpg">
  <meta property="og:locale" content="fr_CA">
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Inter:400,500,600,700,800,900|Playfair+Display:400,500,600,700,800,900&amp;subset=latin">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>tailwind.config = {{ theme: {{ extend: {{ fontFamily: {{ heading: ['"Playfair Display"', 'serif'], body: ['"Inter"', 'sans-serif'] }}, colors: {{ brand: {{ red: '#AA1120', navy: '#0c2749' }} }} }} }} }};</script>
<script type="application/ld+json">
{ld}
</script>
</head>
<body class="antialiased bg-gray-50 text-gray-900 font-body flex flex-col min-h-screen">
  <nav class="py-4 px-6 fixed w-full top-0 z-50 bg-brand-navy shadow-md">
    <div class="relative max-w-7xl mx-auto flex items-center justify-between">
      <a href="../index.html"><img src="/src/assets/logo.png" alt="Chiasson & De Francesco" class="h-10 md:h-12 w-auto"></a>
      <div class="hidden md:flex items-center gap-10">
        <a href="../index.html" class="text-white hover:text-brand-red transition-colors font-medium">Accueil</a>
        <a href="../index.html#about" class="text-white hover:text-brand-red font-medium">Équipe</a>
        <a href="../proprietes.html" class="text-white hover:text-brand-red font-medium">Propriétés</a>
        <a href="../blog.html" class="text-white hover:text-brand-red font-medium">Blogue</a>
        <a href="../index.html#contact" class="text-white hover:text-brand-red font-medium">Contact</a>
      </div>
      <button id="mobile-menu-btn" class="md:hidden text-white focus:outline-none" aria-label="Ouvrir le menu"><svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" /></svg></button>
    </div>
    <div id="mobile-menu" class="hidden md:hidden bg-brand-navy px-6 py-6 space-y-4 border-t border-white/10 mt-4">
      <a href="../index.html" class="block text-white hover:text-brand-red font-medium">Accueil</a>
      <a href="../index.html#about" class="block text-white hover:text-brand-red font-medium">Équipe</a>
      <a href="../proprietes.html" class="block text-white hover:text-brand-red font-medium">Propriétés</a>
      <a href="../blog.html" class="block text-white hover:text-brand-red font-medium">Blogue</a>
      <a href="../index.html#contact" class="block text-white hover:text-brand-red font-medium">Contact</a>
    </div>
  </nav>
  <header class="pt-32 pb-12 bg-white border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-6">
      <nav class="text-sm text-gray-500 mb-4" aria-label="Fil d'Ariane">
        <a href="../index.html" class="hover:text-brand-red">Accueil</a>
        <span class="mx-1">/</span>
        <a href="../regions-desservies.html" class="hover:text-brand-red">Régions desservies</a>
        <span class="mx-1">/</span>
        <span class="text-gray-700">{page["name"]}</span>
      </nav>
      <h1 class="font-heading text-4xl md:text-5xl font-bold text-brand-navy">{page["h1"]}</h1>
      <p class="text-gray-600 mt-4 max-w-3xl text-lg">{page["lead"]}</p>
    </div>
  </header>
  <main class="flex-grow py-12">
    <div class="max-w-3xl mx-auto px-6">
      <p class="text-gray-600 leading-relaxed mb-6">{page["intro"]}</p>
{sections}
      <h2 class="font-heading text-2xl font-bold text-brand-navy mt-10 mb-3">À propos de l'équipe</h2>
      <p class="text-gray-600 leading-relaxed mb-6">Équipe Chiasson de Francesco, RE/MAX D'ABORD, 157 boul. Jacques-Cartier Sud, Sherbrooke (QC) J1J 2Z4. Pierre-Olivier Chiasson : <a href="tel:8199194631" class="text-brand-navy hover:text-brand-red">819-919-4631</a> · Marco De Francesco : <a href="tel:8195620656" class="text-brand-navy hover:text-brand-red">819-562-0656</a> · Jade Sirois : <a href="tel:8194342652" class="text-brand-navy hover:text-brand-red">819-434-2652</a>.</p>
      <h2 class="font-heading text-2xl font-bold text-brand-navy mt-10 mb-4">Questions fréquentes</h2>
      <div class="space-y-4 mb-10">
{faqs_html}
      </div>
      <h2 class="font-heading text-2xl font-bold text-brand-navy mt-10 mb-3">Pour aller plus loin</h2>
      <ul class="list-disc pl-5 space-y-2 text-gray-600 mb-8">
{related}
      </ul>
      <div class="flex flex-wrap gap-4">
        <a href="../proprietes.html" class="inline-block bg-brand-navy text-white font-semibold py-3 px-6 rounded-lg hover:bg-brand-red transition-colors">Voir nos propriétés</a>
        <a href="../evaluation.html" class="inline-block bg-gray-200 text-brand-navy font-semibold py-3 px-6 rounded-lg hover:bg-gray-300 transition-colors">Évaluer le timing de vente</a>
        <a href="../index.html#contact" class="inline-block bg-gray-200 text-brand-navy font-semibold py-3 px-6 rounded-lg hover:bg-gray-300 transition-colors">Nous contacter</a>
      </div>
    </div>
  </main>
  <footer id="footer" class="bg-[#232323] text-gray-400 py-12 border-t-4 border-brand-red font-body">
    <div class="max-w-7xl mx-auto px-6">
      <div class="flex flex-col md:flex-row justify-between items-center gap-4 text-sm">
        <a href="../index.html" class="hover:text-brand-red transition-colors">Accueil</a>
        <a href="../proprietes.html" class="hover:text-brand-red transition-colors">Propriétés</a>
        <a href="../regions-desservies.html" class="hover:text-brand-red transition-colors">Régions desservies</a>
        <a href="../index.html#contact" class="hover:text-brand-red transition-colors">Contact</a>
      </div>
      <div class="flex flex-wrap justify-center gap-x-4 gap-y-2 text-xs mt-4 text-gray-500">
        <a href="https://immobiliermaison.com/" target="_blank" rel="noopener noreferrer" class="hover:text-brand-red transition-colors">immobiliermaison.com</a>
        <a href="https://vendremamaisonsherbrooke.com/" target="_blank" rel="noopener noreferrer" class="hover:text-brand-red transition-colors">vendremamaisonsherbrooke.com</a>
        <a href="https://vendremamaisonestrie.com/" target="_blank" rel="noopener noreferrer" class="hover:text-brand-red transition-colors">vendremamaisonestrie.com</a>
        <a href="https://vendremonplex.com/" target="_blank" rel="noopener noreferrer" class="hover:text-brand-red transition-colors">vendremonplex.com</a>
        <a href="https://realestatesherbrooke.com/" target="_blank" rel="noopener noreferrer" class="hover:text-brand-red transition-colors">realestatesherbrooke.com</a>
      </div>
      <p class="text-center text-xs text-gray-500 mt-6">&copy; 2026 Équipe Chiasson & De Francesco.</p>
    </div>
  </footer>
  <script>var b=document.getElementById('mobile-menu-btn'),m=document.getElementById('mobile-menu');if(b&&m)b.addEventListener('click',function(){{m.classList.toggle('hidden');}});</script>
</body>
</html>
"""


def main() -> None:
    out = ROOT / "regions"
    for page in PAGES:
        path = out / f"{page['slug']}.html"
        path.write_text(render(page), encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
