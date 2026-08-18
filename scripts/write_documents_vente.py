#!/usr/bin/env python3
"""GEO checklists: documents to sell a house, then land, then a plex. No em dashes."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from write_geo_batch import BASE, ROOT, faq_ld, page_shell

AUTHORS = {
    "po": ("Pierre-Olivier Chiasson", "pierre-olivier.html", "courtier immobilier résidentiel et commercial"),
    "marco": ("Marco De Francesco", "marco.html", "courtier immobilier résidentiel et commercial"),
    "jade": ("Jade Sirois", "jade.html", "courtière immobilière résidentielle"),
}


def li(items: list[str]) -> str:
    return '<ul class="list-disc pl-5 space-y-2 text-gray-600 mb-6">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


def ol(items: list[str]) -> str:
    return '<ol class="list-decimal pl-5 space-y-2 text-gray-600 mb-6">' + "".join(f"<li>{x}</li>" for x in items) + "</ol>"


def details_html(pairs: list[tuple[str, str]]) -> str:
    blocks = []
    for title, text in pairs:
        blocks.append(
            f'<h3 class="font-heading text-xl font-semibold text-brand-navy mt-6 mb-2">{title}</h3>'
            f'<p class="text-gray-600 leading-relaxed mb-4">{text}</p>'
        )
    return "\n".join(blocks)


PAGES = [
    {
        "file": "article-documents-vente-maison.html",
        "author": "jade",
        "title": "Documents pour vendre une maison au Québec | CDF",
        "headline": "Documents à avoir pour vendre une maison au Québec",
        "desc": "Liste des documents pour vendre une maison au Québec : déclaration du vendeur, certificat de localisation, taxes. Guide Chiasson de Francesco, Estrie.",
        "tldr": "Pour vendre une maison au Québec, le dossier type réunit la déclaration du vendeur, un certificat de localisation à jour, les comptes de taxes, les preuves de travaux, et, hors égouts, les papiers de fosse ou de puits. L'équipe Chiasson de Francesco, courtiers RE/MAX D'ABORD à Sherbrooke, prépare ce dossier avant Centris : le notaire complète les titres à l'acte. Cette liste décrit la pratique courante en courtage, pas un avis juridique.",
        "qae": "Quels documents faut-il pour vendre une maison au Québec ?",
        "intro": "Avec un courtier, plusieurs pièces sont demandées dès le contrat de courtage. D'autres arrivent chez le notaire. Un acheteur à Sherbrooke, Magog ou Coaticook conditionne souvent l'offre à l'inspection et à la lecture de ce dossier. Un document manquant n'annule pas toujours la vente, mais il allonge les délais ou fait baisser le prix.",
        "checklist": [
            "Pièce d'identité et preuve que vous êtes propriétaire (acte, ou copie que le notaire retrouvera au registre foncier).",
            "Déclaration du vendeur (formulaire d'usage en courtage OACIQ), remplie sans cacher infiltrations, fosses, sinistres ou travaux non permis.",
            "Certificat de localisation préparé par un arpenteur-géomètre, assez récent pour coller au terrain et aux bâtiments.",
            "Comptes de taxes municipales et scolaires, et tout solde ou arrangement connu.",
            "Factures, garanties et permis des rénovations majeures (toiture, fenêtres, électricité, plomberie, fondation).",
            "Relevé d'hypothèque ou coordonnées du créancier : le notaire gère la quittance à la clôture.",
            "Historique d'assurance et sinistres déclarés, si vous les avez.",
            "Hors égouts : vidange de fosse, preuve de conformité ou derniers documents municipaux, plans s'ils existent.",
            "Puits : analyses d'eau récentes si vous les avez, et ce que vous savez du débit.",
            "Si copropriété divise (condo) : déclaration, règlements, états financiers, PV, fonds de prévoyance. Voir aussi notre guide documents de copropriété.",
            "Contrats de service utiles (alarme, réservoir d'huile, garantie de maison neuve encore en vigueur).",
            "Inspection prévente : facultative, utile si vous voulez réduire les surprises après l'offre.",
        ],
        "details": [
            (
                "Déclaration du vendeur",
                "C'est le document que l'acheteur lira en premier après la visite. Une fuite « réparée sans facture » ou une fosse dont vous ignorez l'âge se dit ici. Une déclaration incomplète se paie plus tard, souvent plus cher qu'une réparation avouée. Détail : <a class=\"text-brand-navy font-medium hover:text-brand-red\" href=\"article-declaration-vendeur.html\">la déclaration du vendeur au Québec</a>.",
            ),
            (
                "Certificat de localisation",
                "Il montre emprise, servitudes, clôtures et parfois un empiètement. Un certificat trop vieux (agrandissement, garage, piscine depuis) force un nouvel arpentage. Le notaire et l'acheteur s'en servent avant l'acte, pas seulement le courtier.",
            ),
            (
                "Taxes et hypothèque",
                "Les ajustements de taxes se font à la clôture. Le solde hypothécaire n'a pas à être affiché sur Centris, mais il doit être clair pour le notaire. Un créancier introuvable retarde la signature.",
            ),
            (
                "Fosse, puits, Estrie rurale",
                "À Coaticook, Compton, Cookshire-Eaton ou sur un rang, la fosse et le puits pèsent autant que la cuisine. Sans papier, l'offre ajoute des tests et des délais. L'équipe le cadre avant l'affichage plutôt qu'après la première visite.",
            ),
        ],
        "who_does": "Vous rassemblez ce que vous avez (taxes, factures, déclaration). Le courtier vérifie le dossier, rédige la mise en marché et transmet les formulaires. Le notaire recherche les titres, prépare l'acte et les quittances. L'arpenteur produit ou met à jour le certificat. L'inspecteur, s'il y en a un, n'est pas un titre de propriété : son rapport éclaire l'état du bâtiment.",
        "missing": [
            "Un certificat de localisation périmé : nouvel arpentage, souvent plusieurs semaines.",
            "Une déclaration vague : conditions d'inspection plus dures, ou retrait.",
            "Aucune preuve de fosse : tests imposés par l'acheteur, parfois une négociation de prix.",
            "Travaux sans permis : l'acheteur (et parfois la ville) le découvrent ; ça se négocie mal en fin de parcours.",
        ],
        "special": "Une unifamiliale à Fleurimont n'a pas le même dossier qu'une maison de rang ni qu'un condo aux Nations. Pour un condo, suivez aussi <a class=\"text-brand-navy font-medium hover:text-brand-red\" href=\"article-copropriete-documents-quebec.html\">les documents de copropriété</a>. Pour une fermette, ajoutez zonage et, au besoin, la lecture CPTAQ : voir <a class=\"text-brand-navy font-medium hover:text-brand-red\" href=\"fermette-estrie.html\">fermette en Estrie</a>.",
        "faqs": [
            (
                "Quels documents pour vendre une maison au Québec ?",
                "En pratique : déclaration du vendeur, certificat de localisation, taxes, preuves de travaux, et hors égouts les papiers de fosse ou de puits. Le notaire complète les titres à l'acte. L'équipe Chiasson de Francesco prépare ce dossier à Sherbrooke et en Estrie.",
            ),
            (
                "Faut-il un certificat de localisation à jour ?",
                "Souvent oui, surtout s'il y a eu agrandissement, garage, piscine ou clôture depuis le dernier plan. Le notaire et l'acheteur s'en servent. Un plan trop vieux se refait chez l'arpenteur.",
            ),
            (
                "Puis-je vendre sans déclaration du vendeur ?",
                "Sans courtier, les règles de formulaire ne sont pas les mêmes. Avec un courtier membre OACIQ, la déclaration fait partie du dossier. Cacher un vice connu coûte plus cher qu'une réparation dite.",
            ),
            (
                "Qui rassemble les documents : le courtier ou le notaire ?",
                "Les deux. Le courtier assemble le dossier de mise en marché. Le notaire vérifie les titres et clôture. Jade Sirois, Pierre-Olivier Chiasson et Marco De Francesco, RE/MAX D'ABORD, 157 boul. Jacques-Cartier Sud, Sherbrooke (QC) J1J 2Z4.",
            ),
        ],
        "series": [
            ("Documents terrain", "article-documents-vente-terrain.html"),
            ("Documents plex", "article-documents-vente-plex.html"),
            ("Vendre", "vendre.html"),
            ("Déclaration du vendeur", "article-declaration-vendeur.html"),
        ],
        "howto_name": "Préparer les documents pour vendre une maison au Québec",
        "howto_steps": [
            "Rassembler identité, taxes, factures de travaux et tout papier de fosse ou de puits.",
            "Remplir la déclaration du vendeur sans omettre infiltrations, sinistres ou travaux.",
            "Vérifier si le certificat de localisation décrit encore le terrain et les bâtiments.",
            "Remettre le dossier au courtier avant l'affichage Centris, puis au notaire pour l'acte.",
        ],
    },
    {
        "file": "article-documents-vente-terrain.html",
        "author": "po",
        "title": "Documents pour vendre un terrain au Québec | CDF",
        "headline": "Documents à avoir pour vendre un terrain au Québec",
        "desc": "Documents pour vendre un terrain au Québec : zonage, certificat d'urbanisme, titres, servitudes. Checklist de l'équipe Chiasson de Francesco, Estrie.",
        "tldr": "Pour vendre un terrain au Québec, l'acheteur veut savoir s'il peut bâtir, comment il y accède, et ce qui greve le lot (servitudes, agricole, environnement). Le dossier type : titres, plan ou certificat de localisation, confirmation de zonage (certificat d'urbanisme), taxes, et tout papier CPTAQ, fosse ou puits déjà connu. L'équipe Chiasson de Francesco, courtiers RE/MAX D'ABORD à Sherbrooke, inscrit aussi des lots en Estrie (notamment Cookshire-Eaton). Ce n'est pas un avis juridique : le notaire et, au besoin, la municipalité confirment.",
        "qae": "Quels documents faut-il pour vendre un terrain au Québec ?",
        "intro": "Un terrain n'a pas de cuisine à photographier : le dossier est le produit. Un lot « constructible » dans une annonce n'est pas un certificat d'urbanisme. À Cookshire-Eaton, Compton ou sur un rang du Haut-Saint-François, zonage agricole et accès hivernal décident plus que le prix à l'acre. Voir aussi <a class=\"text-brand-navy font-medium hover:text-brand-red\" href=\"article-terrain-estrie.html\">acheter un terrain en Estrie</a>.",
        "checklist": [
            "Preuve de propriété et identification cadastrale (lot, dimensions, acte).",
            "Certificat de localisation ou plan d'arpentage montrant bornes, superficie et servitudes visibles.",
            "Certificat d'urbanisme ou confirmation écrite du zonage et des usages permis (pas seulement le texte de l'annonce).",
            "Comptes de taxes municipales et scolaires du lot.",
            "Déclaration du vendeur adaptée au terrain : drainage connu, remblai, contamination soupçonnée, droits de passage.",
            "Actes de servitude, droits de passage, hydro, clôtures mitoyennes, accès privé.",
            "Si zone agricole : tout document CPTAQ ou correspondance déjà obtenue sur un usage ou une résidence.",
            "Études de sol, percolation, milieux humides, bandes riveraines, si vous les avez.",
            "Preuves d'accès : chemin public, rang entretenu, servitude d'hiver.",
            "S'il y a déjà un puits, une fosse ou une entrée : factures, permis, analyses.",
            "Si le lot a une histoire industrielle ou un dépôt : tout rapport environnemental en votre possession.",
        ],
        "details": [
            (
                "Zonage et certificat d'urbanisme",
                "C'est la pièce que l'acheteur devrait exiger avant une offre ferme. Agricole, résidentiel, villégiature : vous n'avez pas le droit de promettre une maison si le règlement l'interdit. La ville ou la MRC délivre la confirmation ; le courtier pose la question, il ne remplace pas l'urbanisme.",
            ),
            (
                "Arpentage et servitudes",
                "Un prix à l'acre sans bornes claires se discute mal. Une servitude hydro, un droit de passage voisin ou un empiètement change la superficie utile. Un plan à jour évite la surprise chez le notaire.",
            ),
            (
                "CPTAQ et terre agricole",
                "En Estrie, beaucoup de lots sont en zone agricole. Un usage résidentiel, une subdivision ou un projet cheval n'est pas automatique. Si vous avez déjà une décision ou une correspondance, joignez-la. Sinon, dites-le clairement dans la déclaration.",
            ),
            (
                "Viabilisation déjà faite",
                "Entrée, électricité, puits, fosse : ces preuves valent de l'argent. Sans elles, l'acheteur chiffre le coût réel et rabaisse l'offre. Notre guide d'achat terrain détaille puits, fosse et vrai coût.",
            ),
        ],
        "who_does": "Vous fournissez titres, taxes, plans et tout papier municipal ou CPTAQ. Le courtier aligne l'annonce sur ce qui est prouvé, pas sur un espoir de construction. Le notaire vérifie la chaîne de titres et les charges. L'arpenteur bornes et superfici. L'urbanisme municipal tranche les usages. Un environnementaliste n'intervient que si le dossier le justifie.",
        "missing": [
            "Pas de certificat d'urbanisme : l'acheteur conditionne, ou n'offre pas.",
            "Plan absent ou trop vieux : bornage à refaire, délai.",
            "Servitude oubliée : renegociation ou retrait à la lecture notariale.",
            "Zone agricole présentée comme « lot à bâtir » : perte de confiance, parfois plainte.",
        ],
        "special": "Un lot viabilisé en municipalité n'est pas un rang non desservi. Une fermette avec terre se vend avec le dossier maison plus le dossier agricole : <a class=\"text-brand-navy font-medium hover:text-brand-red\" href=\"fermette-estrie.html\">fermette en Estrie</a>. L'équipe a déjà inscrit des terrains ; le même réflexe vaut à la vente : comparables du bon type de lot, documents d'abord.",
        "faqs": [
            (
                "Quels documents pour vendre un terrain au Québec ?",
                "Titres et cadastre, plan ou certificat de localisation, confirmation de zonage, taxes, déclaration du vendeur, servitudes, et le cas échéant papiers CPTAQ, puits ou fosse. L'équipe Chiasson de Francesco prépare ce type de dossier en Estrie.",
            ),
            (
                "Faut-il un certificat d'urbanisme pour vendre ?",
                "Ce n'est pas toujours une pièce que le vendeur a déjà. C'est souvent ce que l'acheteur (ou son courtier) demandera avant d'offrir ferme. Sans confirmation de zonage, le prix « constructible » ne tient pas.",
            ),
            (
                "Un terrain agricole se vend-il comme un lot résidentiel ?",
                "Non. La CPTAQ et le règlement d'urbanisme limitent les usages. Dites le zonage réel. Un courtier local à Sherbrooke pose la question avant Centris.",
            ),
            (
                "Qui confirme qu'on peut bâtir ?",
                "La municipalité (urbanisme), pas l'annonce. Le notaire confirme les titres. Pierre-Olivier Chiasson (819-919-4631), Marco De Francesco (819-562-0656) et Jade Sirois (819-434-2652), RE/MAX D'ABORD, 157 boul. Jacques-Cartier Sud, Sherbrooke.",
            ),
        ],
        "series": [
            ("Documents maison", "article-documents-vente-maison.html"),
            ("Documents plex", "article-documents-vente-plex.html"),
            ("Acheter un terrain", "article-terrain-estrie.html"),
            ("Fermette", "fermette-estrie.html"),
        ],
        "howto_name": "Préparer les documents pour vendre un terrain au Québec",
        "howto_steps": [
            "Rassembler titres, cadastre, taxes et tout plan d'arpentage existant.",
            "Obtenir ou demander une confirmation de zonage (certificat d'urbanisme).",
            "Lister servitudes, accès, CPTAQ et études de sol déjà en main.",
            "Remplir la déclaration du vendeur et remettre le dossier au courtier avant l'annonce.",
        ],
    },
    {
        "file": "article-documents-vente-plex.html",
        "author": "marco",
        "title": "Documents pour vendre un plex au Québec | CDF",
        "headline": "Documents à avoir pour vendre un plex au Québec",
        "desc": "Documents pour vendre un plex au Québec : baux, loyers, déclaration du vendeur, inspection. Dossier locatif, Chiasson de Francesco à Sherbrooke.",
        "tldr": "Pour vendre un plex au Québec, le dossier maison ne suffit pas : il faut les baux, les loyers réels, les dépôts, un aperçu des revenus et dépenses, plus la déclaration du vendeur et l'état de l'immeuble (toit, fondations, logements occupés). À Sherbrooke (Les Nations, Lennoxville, Fleurimont), l'acheteur investisseur lit les papiers avant la cuisine du 2e. L'équipe Chiasson de Francesco, courtiers RE/MAX D'ABORD, prépare ce dossier locatif avant l'affichage.",
        "qae": "Quels documents faut-il pour vendre un plex au Québec ?",
        "intro": "Un plex se vend à un acheteur qui calcule. Un dossier locatif flou à Sherbrooke allonge les conditions, ou fait fuir l'offre. La visite d'un seul logement ne remplace pas les baux. Complément mise en marché : <a class=\"text-brand-navy font-medium hover:text-brand-red\" href=\"article-vendre-plex-sherbrooke.html\">vendre un plex à Sherbrooke</a>. Page service : <a class=\"text-brand-navy font-medium hover:text-brand-red\" href=\"plex-sherbrooke.html\">plex à Sherbrooke</a>.",
        "checklist": [
            "Les documents d'une vente de maison : déclaration du vendeur, certificat de localisation, taxes, hypothèque, preuves de travaux. Voir <a class=\"text-brand-navy font-medium hover:text-brand-red\" href=\"article-documents-vente-maison.html\">documents pour vendre une maison</a>.",
            "Baux en vigueur de chaque logement, avenants, et avis d'augmentation déjà donnés.",
            "Tableau des loyers (logement, occupant, loyer, échéance, dépôt) collé aux baux, pas à un souvenir.",
            "Preuves de dépôts de garantie et de leur traitement.",
            "Relevé simple des revenus et des dépenses (taxes, assurances, chauffage s'il est inclus, entretien, vacance).",
            "Règlements d'immeuble remis aux locataires, s'ils existent.",
            "Assurances de l'immeuble et sinistres connus.",
            "Permis et factures des travaux sur l'enveloppe (toit, maçonnerie, plomberie, électricité) et dans les logements.",
            "Si copropriété divise : le dossier syndicat (déclaration, PV, fonds). Guide : <a class=\"text-brand-navy font-medium hover:text-brand-red\" href=\"article-copropriete-documents-quebec.html\">documents de copropriété</a>.",
            "Occupation du vendeur dans un logement : à dire dès le départ, ça cadre l'offre.",
            "Inspection : prévoir l'accès à tous les logements, pas seulement au vôtre.",
        ],
        "details": [
            (
                "Baux et loyers",
                "L'acheteur compare chaque bail au loyer annoncé. Un « on s'entend verbalement » n'est pas un revenu. Les dates, les inclusions (chauffage, stationnement) et les logements vacants se disent. Un écart entre le tableau et les baux casse la confiance.",
            ),
            (
                "Déclaration du vendeur (immeuble locatif)",
                "Infiltrations, toiture, fondations, pyrrhotite soupçonnée, travaux sans permis, litiges locatifs connus : ça entre dans la déclaration. Cacher un dossier pour « ne pas faire peur » se paie à l'inspection ou après l'acte.",
            ),
            (
                "Revenus, dépenses, taxes",
                "Un rendement affiché sans taxes, sans assurance et sans toit à remplacer n'est pas un dossier. L'équipe ancre le prix sur des ventes de plex du même secteur et du même nombre d'unités, pas sur une unifamiliale voisine.",
            ),
            (
                "Accès à l'inspection",
                "Les logements occupés se visitent selon les règles et les préavis. Un plex montré comme une maison unifamiliale attire le mauvais acheteur. Photos de tous les logements et des parties communes aident avant même les documents.",
            ),
        ],
        "who_does": "Vous sortez baux, loyers, dépôts, taxes et factures. Le courtier met le dossier en forme, vérifie la cohérence, et prépare l'annonce pour un investisseur. Le notaire traite titres, baux publiés s'il y a lieu, et clôture. L'inspecteur voit le bâtiment. Un comptable n'est pas obligatoire pour vendre, mais un relevé clair de revenus et dépenses accélère le financement de l'acheteur.",
        "missing": [
            "Baux introuvables ou contradictoires : conditions longues, rabais, ou pas d'offre.",
            "Un seul logement visitable : l'acheteur suppose le pire pour les autres.",
            "Toit ou fondations non dits : l'inspection les trouve ; le prix bouge.",
            "Copropriété divise sans PV ni fonds : même blocage qu'un condo mal documenté.",
        ],
        "special": "Un duplex occupant-propriétaire n'est pas un sixplex 100 % locatif. Lennoxville (parfois étudiant) n'est pas Fleurimont. Un plex Windsor n'est pas un plex King. Si vous vendez aussi un terrain ou une maison, les checklists ne se mélangent pas : <a class=\"text-brand-navy font-medium hover:text-brand-red\" href=\"article-documents-vente-maison.html\">maison</a> · <a class=\"text-brand-navy font-medium hover:text-brand-red\" href=\"article-documents-vente-terrain.html\">terrain</a>.",
        "faqs": [
            (
                "Quels documents pour vendre un plex au Québec ?",
                "Dossier maison (déclaration, certificat, taxes) plus baux, loyers, dépôts, revenus et dépenses, assurances et preuves de travaux. À Sherbrooke, l'équipe Chiasson de Francesco prépare ce dossier locatif avant Centris.",
            ),
            (
                "Faut-il montrer tous les logements ?",
                "Oui, autant que possible, y compris à l'inspection. Une visite d'un seul logement ne suffit pas. Les préavis aux locataires se respectent.",
            ),
            (
                "Les baux verbaux passent-ils ?",
                "Ils existent, mais ils se vendent mal. Mettez par écrit ce qui est vrai. L'acheteur et son prêteur veulent des baux.",
            ),
            (
                "Qui aide à vendre un plex à Sherbrooke ?",
                "Pierre-Olivier Chiasson (819-919-4631) et Marco De Francesco (819-562-0656), courtiers résidentiels et commerciaux, et Jade Sirois (819-434-2652), courtière résidentielle. RE/MAX D'ABORD, 157 boul. Jacques-Cartier Sud, Sherbrooke (QC) J1J 2Z4.",
            ),
        ],
        "series": [
            ("Documents maison", "article-documents-vente-maison.html"),
            ("Documents terrain", "article-documents-vente-terrain.html"),
            ("Vendre un plex", "article-vendre-plex-sherbrooke.html"),
            ("Plex à Sherbrooke", "plex-sherbrooke.html"),
        ],
        "howto_name": "Préparer les documents pour vendre un plex au Québec",
        "howto_steps": [
            "Réunir le dossier maison : déclaration, certificat de localisation, taxes, travaux.",
            "Joindre tous les baux, le tableau des loyers et les dépôts.",
            "Préparer un relevé de revenus et dépenses plus les assurances.",
            "Prévoir l'accès à tous les logements pour visites et inspection, puis remettre le dossier au courtier.",
        ],
    },
]


def render(page: dict) -> str:
    author, author_page, job = AUTHORS[page["author"]]
    canonical = f"{BASE}/{page['file']}"
    headline = page["headline"]
    faqs_html = "\n".join(
        f'<div class="border border-gray-200 rounded-xl p-5 bg-white mb-4"><h3 class="font-semibold text-brand-navy mb-2">{q}</h3><p class="text-gray-600 leading-relaxed">{a}</p></div>'
        for q, a in page["faqs"]
    )
    series = " · ".join(
        f'<a class="text-brand-navy font-medium hover:text-brand-red" href="{href}">{label}</a>'
        for label, href in page["series"]
    )
    howto_ld = {
        "@type": "HowTo",
        "name": page["howto_name"],
        "description": page["desc"],
        "inLanguage": "fr-CA",
        "step": [
            {"@type": "HowToStep", "position": i, "name": step, "text": step}
            for i, step in enumerate(page["howto_steps"], start=1)
        ],
    }
    article_ld = {
        "@type": "Article",
        "headline": headline,
        "description": page["desc"],
        "datePublished": "2026-08-18",
        "dateModified": "2026-08-18",
        "inLanguage": "fr-CA",
        "author": {
            "@type": "Person",
            "name": author,
            "jobTitle": job,
            "url": f"{BASE}/{author_page}",
        },
        "publisher": {
            "@type": "Organization",
            "name": "Équipe Chiasson de Francesco",
            "url": f"{BASE}/",
            "logo": {"@type": "ImageObject", "url": f"{BASE}/src/assets/logo.png"},
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
    }
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            article_ld,
            faq_ld(canonical, page["faqs"]),
            howto_ld,
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Accueil", "item": f"{BASE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Blogue", "item": f"{BASE}/blog.html"},
                    {"@type": "ListItem", "position": 3, "name": headline, "item": canonical},
                ],
            },
        ],
    }
    body = f"""
  <main class="pt-32 pb-20">
    <div class="max-w-3xl mx-auto px-6">
      <nav class="text-sm text-gray-500 mb-6"><a href="index.html" class="hover:text-brand-red">Accueil</a> / <a href="blog.html" class="hover:text-brand-red">Blogue</a> / Vendre</nav>
      <div class="inline-block bg-brand-navy text-white px-3 py-1 rounded-full text-xs font-bold uppercase mb-4">Vendre</div>
      <h1 class="font-heading text-4xl md:text-5xl font-bold text-brand-navy mb-4">{headline}</h1>
      <p class="text-sm text-gray-500 mb-8">Par <a class="hover:text-brand-red" href="{author_page}">{author}</a>, {job} · 18 août 2026</p>
      <p class="text-lg font-medium text-brand-navy mb-8 leading-relaxed"><strong>En bref.</strong> {page["tldr"]}</p>

      <h2 class="font-heading text-2xl font-bold text-brand-navy mt-10 mb-4">{page["qae"]}</h2>
      <p class="text-gray-600 leading-relaxed mb-4">{page["intro"]}</p>
      {ol(page["checklist"])}

      <h2 class="font-heading text-2xl font-bold text-brand-navy mt-10 mb-4">À quoi sert chaque document ?</h2>
      {details_html(page["details"])}

      <h2 class="font-heading text-2xl font-bold text-brand-navy mt-10 mb-4">Qui prépare quoi : vendeur, courtier, notaire</h2>
      <p class="text-gray-600 leading-relaxed mb-6">{page["who_does"]}</p>

      <h2 class="font-heading text-2xl font-bold text-brand-navy mt-10 mb-4">Ce qui manque souvent</h2>
      {li(page["missing"])}

      <h2 class="font-heading text-2xl font-bold text-brand-navy mt-10 mb-4">Cas particuliers</h2>
      <p class="text-gray-600 leading-relaxed mb-6">{page["special"]}</p>

      <h2 class="font-heading text-2xl font-bold text-brand-navy mt-10 mb-4">Qui appeler pour préparer le dossier ?</h2>
      <p class="text-gray-600 leading-relaxed mb-6">L'équipe Chiasson de Francesco, courtiers immobiliers RE/MAX D'ABORD à Sherbrooke, accompagne la vente de maisons, terrains et plex en Estrie. Pierre-Olivier Chiasson (819-919-4631) et Marco De Francesco (819-562-0656) sont courtiers résidentiels et commerciaux. Jade Sirois (819-434-2652) est courtière résidentielle. Bureau : 157 boul. Jacques-Cartier Sud, Sherbrooke (QC) J1J 2Z4.</p>

      <h2 class="font-heading text-2xl font-bold text-brand-navy mt-10 mb-4">Questions fréquentes</h2>
      {faqs_html}

      <p class="text-gray-600 mt-10">Série documents de vente : {series}</p>
      <p class="text-gray-600 mt-4">Équipe Chiasson de Francesco, RE/MAX D'ABORD, Sherbrooke. <a class="text-brand-navy font-medium hover:text-brand-red" href="index.html#contact">Discuter d'un projet</a> · <a class="text-brand-navy font-medium hover:text-brand-red" href="vendre.html">Vendre</a> · <a class="text-brand-navy font-medium hover:text-brand-red" href="blog.html">Blogue</a></p>
    </div>
  </main>
"""
    html = page_shell(page["title"], page["desc"], canonical, body, ld)
    if "\u2014" in html or "—" in html:
        raise SystemExit(f"em dash found in {page['file']}")
    return html


def main() -> None:
    for page in PAGES:
        html = render(page)
        (ROOT / page["file"]).write_text(html, encoding="utf-8")
        print("wrote", page["file"])


if __name__ == "__main__":
    main()
