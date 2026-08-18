#!/usr/bin/env python3
"""Batch GEO/SEO pages: remaining regions, service pages, citable articles."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from write_top_regions import render as render_region

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://chiassondefrancesco.ca"

REMAINING = [
    {
        "slug": "coaticook",
        "name": "Coaticook",
        "title": "Courtier immobilier à Coaticook | Chiasson De Francesco",
        "description": "Acheter ou vendre à Coaticook : ville de services, gorge et campagne en Estrie. Équipe Chiasson de Francesco, RE/MAX.",
        "h1": "Acheter ou vendre une propriété à Coaticook",
        "lead": "L'équipe Chiasson de Francesco accompagne l'achat et la vente à Coaticook : maisons de ville, fermettes et propriétés près de la gorge, avec un ancrage RE/MAX à Sherbrooke.",
        "intro": "Coaticook est une vraie ville de services en Estrie, pas seulement un village-dortoir de Sherbrooke. Fromagerie, commerces, écoles et un cadre plus champêtre qu'en ville changent le type d'acheteurs : et les comparables.",
        "sections": [
            ("Ville de services et campagne", "Le noyau urbain convient aux ménages qui veulent tout à proximité. Autour, les rangs et les fermettes se négocient selon l'acreage, les bâtiments et l'accès à l'eau ou à un champ d'épuration. La gorge et les attraits touristiques attirent aussi une clientèle villégiature, distincte d'un bungalow de rue résidentielle."),
            ("Acheter à Coaticook", "Hors réseau d'égouts, inspection et tests d'eau/fosse valent plus qu'une clause copiée. En ville, comparez des ventes du même quartier, pas un prix « MRC de Coaticook » unique. Nous filtrons Centris et visitons sur place."),
            ("Vendre à Coaticook", "Un bien bien situé près des services se vend souvent plus vite qu'une fermette trop chère par rapport aux acres comparables. L'évaluation marchande évite de calquer Sherbrooke ou Magog sur Coaticook."),
        ],
        "related": [("Cookshire-Eaton", "cookshire-eaton.html"), ("Compton", "compton.html"), ("Propriétés", "../proprietes.html"), ("Évaluation", "../evaluation.html")],
        "faqs": [
            ("Coaticook est-il moins cher que Sherbrooke ?", "Souvent pour une unifamiliale comparable, oui, mais l'écart dépend de l'état, du terrain et des services. Une fermette rénovée peut dépasser un bungalow sherbrookois. On compare des ventes, pas des moyennes régionales."),
            ("Faut-il un courtier pour une fermette à Coaticook ?", "Oui surtout : acreage, bâtiments, zonage agricole et installations septiques changent le prix. Un courtier Estrie évite une surcote « ferme de rêve » sans comparables."),
            ("L'équipe se déplace-t-elle à Coaticook ?", "Oui. Les courtiers Chiasson de Francesco sont basés à Sherbrooke et desservent Coaticook, Compton et Cookshire-Eaton."),
            ("Quand vendre à Coaticook ?", "Le printemps aide souvent les biens ruraux. Un bungalow en ville se vend toute l'année s'il est au bon prix. Le questionnaire de timing de l'équipe tranche selon votre situation."),
        ],
    },
    {
        "slug": "compton",
        "name": "Compton",
        "title": "Courtier immobilier à Compton | Estrie | CDF",
        "description": "Maisons et fermettes à Compton, Estrie. L'équipe Chiasson de Francesco vous accompagne pour acheter ou vendre.",
        "h1": "Acheter ou vendre une propriété à Compton",
        "lead": "L'équipe Chiasson de Francesco accompagne l'achat et la vente à Compton : village, rangs et fermettes du comté, à une vingtaine de minutes de Sherbrooke.",
        "intro": "Compton reste rural : peu d'inscriptions, beaucoup de biens avec terre ou dépendances. Un prix demandé « parce qu'on est près de Sherbrooke » ne tient pas si le bâtiment ou le puits ne suit pas.",
        "sections": [
            ("Village et rangs", "Le village offre un ancrage communautaire. Les rangs se distinguent par la superficie, l'accès hivernal et le type d'exploitation (loisir vs agricole). Ce n'est pas le marché de Lennoxville."),
            ("Acheter à Compton", "Vérifiez titres, zonage, installations septiques et, le cas échéant, les contraintes agricoles. Une inspection de grange ou d'atelier n'est pas du luxe. Nous comparons des ventes Compton/Coaticook, pas Magog lac."),
            ("Vendre à Compton", "Photos de saison, description honnête des acres et un prix collé aux ventes closes. Trop d'attentes calquées sur Sherbrooke allongent la mise en marché."),
        ],
        "related": [("Coaticook", "coaticook.html"), ("Cookshire-Eaton", "cookshire-eaton.html"), ("Sherbrooke", "sherbrooke.html"), ("Évaluation", "../evaluation.html")],
        "faqs": [
            ("Compton convient-il comme résidence principale ?", "Oui si vous acceptez moins de services qu'en ville et parfois un déplacement vers Sherbrooke ou Coaticook. Le calme et le terrain sont le contrepartie."),
            ("Peut-on acheter une terre agricole à Compton ?", "Selon le zonage et votre statut (producteur ou non). Un courtier et, au besoin, un notaire spécialisé évitent une offre sur un lot que vous ne pourrez pas utiliser comme prévu."),
            ("Pourquoi si peu de maisons à vendre à Compton ?", "Marché mince : les propriétaires restent longtemps. Quand une inscription sort, le prix doit coller aux rares comparables, pas à un espoir de pénurie."),
            ("Travaillez-vous Compton depuis Sherbrooke ?", "Oui. L'équipe Chiasson de Francesco dessert Compton et le Haut-Saint-François."),
        ],
    },
    {
        "slug": "cookshire-eaton",
        "name": "Cookshire-Eaton",
        "title": "Courtier à Cookshire-Eaton | terrains et maisons | CDF",
        "description": "Propriétés et terrains à Cookshire-Eaton et Sawyerville. Courtiers Chiasson de Francesco pour un achat ou une vente en Estrie.",
        "h1": "Acheter ou vendre à Cookshire-Eaton",
        "lead": "L'équipe Chiasson de Francesco accompagne l'achat et la vente à Cookshire-Eaton : Cookshire, Sawyerville, terrains le long de la route 108 et maisons de village.",
        "intro": "Cookshire-Eaton mélange un noyau de services et beaucoup de lots plus grands qu'en ville. Les terrains vides et les maisons existantes ne se comparent pas : un prix à l'acre n'est pas un prix au pied carré habitable.",
        "sections": [
            ("Cookshire, Sawyerville et les rangs", "Cookshire concentre commerces et services. Sawyerville et les secteurs plus dispersés attirent qui veut du terrain. La 108 structure beaucoup de déplacements vers Sherbrooke."),
            ("Acheter terrain ou maison", "Pour un terrain : zonage, drainage, accès, coût réel d'un puits/fosse/entrée. Pour une maison : état du bâtiment d'abord, pas seulement le lot. Nous inscrivons aussi des terrains dans ce secteur."),
            ("Vendre à Cookshire-Eaton", "Un terrain trop cher par rapport aux acres vendus récemment reste en inventaire. Une maison de village bien préparée se distingue. L'évaluation sépare les deux produits."),
        ],
        "related": [("Coaticook", "coaticook.html"), ("Compton", "compton.html"), ("Propriétés", "../proprietes.html"), ("Évaluation", "../evaluation.html")],
        "faqs": [
            ("Y a-t-il des terrains à vendre à Cookshire-Eaton ?", "Oui, le secteur voit régulièrement des lots, y compris le long de la route 108. Chaque lot a ses contraintes (zonage, services). Un courtier les lit avant l'offre."),
            ("Cookshire-Eaton, c'est loin de Sherbrooke ?", "Environ une vingtaine de minutes selon le secteur. Beaucoup d'acheteurs y voient un compromis prix/espace versus la ville."),
            ("Sawyerville et Cookshire, même marché ?", "Même municipalité, produits différents. Sawyerville est plus village-rang ; Cookshire a plus de services. Les comparables doivent rester dans le bon noyau."),
            ("L'équipe inscrit-elle des terrains ?", "Oui. L'équipe Chiasson de Francesco gère maisons et terrains dans le Haut-Saint-François."),
        ],
    },
    {
        "slug": "danville",
        "name": "Danville",
        "title": "Courtier immobilier à Danville | Estrie | CDF",
        "description": "Acheter ou vendre à Danville, Estrie. Accompagnement par l'équipe Chiasson de Francesco, RE/MAX D'ABORD.",
        "h1": "Acheter ou vendre une propriété à Danville",
        "lead": "L'équipe Chiasson de Francesco accompagne l'achat et la vente à Danville : village de la MRC des Sources, maisons abordables et accès vers Val-des-Sources et Richmond.",
        "intro": "Danville est un petit marché de village : prix souvent plus accessibles que Sherbrooke, moins d'inscriptions, acheteurs locaux et de la région des Sources. Calquer un prix de Fleurimont ici ne fonctionne pas.",
        "sections": [
            ("Village des Sources", "Le centre offre l'essentiel. Autour, unifamiliales et quelques plex. La proximité de Val-des-Sources et de Richmond élargit un peu le bassin, sans en faire un marché de villégiature."),
            ("Acheter à Danville", "Vérifiez l'état réel (souvent des bâtiments plus anciens) et les services. Les comparables Danville/Val-des-Sources valent mieux qu'une moyenne estrienne."),
            ("Vendre à Danville", "Prix honnête + photos claires. Un bien trop cher attend. Nous ciblons acheteurs de la MRC et ceux qui quittent Sherbrooke pour l'espace."),
        ],
        "related": [("Val-des-Sources", "val-des-sources.html"), ("Richmond", "richmond.html"), ("Windsor", "windsor.html"), ("Évaluation", "../evaluation.html")],
        "faqs": [
            ("Danville est-il un bon coin pour une première maison ?", "Souvent oui côté budget versus Sherbrooke, si vous acceptez moins de services urbains et un marché plus lent. Inspection et fonds de réserve restent essentiels."),
            ("Peut-on investir dans un plex à Danville ?", "Possible, mais la demande locative n'est pas celle du centre-ville de Sherbrooke. Il faut les loyers réels et l'état du bâtiment, pas un rendement théorique."),
            ("Êtes-vous présents à Danville ?", "Oui. L'équipe dessert Danville, Val-des-Sources et Richmond depuis Sherbrooke."),
            ("Combien de temps pour vendre à Danville ?", "Variable. Un village mince prend parfois plus longtemps qu'un quartier sherbrookois. Le prix d'inscription est le premier levier."),
        ],
    },
    {
        "slug": "eastman",
        "name": "Eastman",
        "title": "Courtier immobilier à Eastman | près d'Orford | CDF",
        "description": "Maisons et chalets à Eastman, près d'Orford et Magog. L'équipe Chiasson de Francesco vous accompagne en Estrie.",
        "h1": "Acheter ou vendre une propriété à Eastman",
        "lead": "L'équipe Chiasson de Francesco accompagne l'achat et la vente à Eastman : village entre Magog et le mont Orford, maisons, chalets et cadre plus champêtre que Magog centre.",
        "intro": "Eastman vit dans l'orbite d'Orford et de Magog sans en être le centre-ville. Spa, village, accès montagne : les acheteurs paient le cadre, pas les mêmes rues que Magog lac.",
        "sections": [
            ("Village entre Magog et Orford", "Le village est compact. Autour, des maisons et chalets avec plus de terrain. Ce n'est ni un condo Magog ni un pied-de-pente Orford : les comparables doivent rester Eastman/Orford rural."),
            ("Acheter à Eastman", "Vérifiez quatre-saisons vs saisonnier, fosses, et distance réelle de Magog. Un « près d'Orford » marketing n'égale pas un accès ski. Inspection avant l'offre."),
            ("Vendre à Eastman", "Misez sur le cadre de vie et des photos de saison. Un prix calqué sur Magog bord de lac se brade ensuite. Nous ancrons sur les ventes Eastman et Orford comparables."),
        ],
        "related": [("Orford", "orford.html"), ("Magog", "magog.html"), ("Lac Memphrémagog", "lac-memphremagog.html"), ("Évaluation", "../evaluation.html")],
        "faqs": [
            ("Eastman ou Magog : où acheter ?", "Magog a plus de services et de condos. Eastman est plus village et nature, souvent avec plus de terrain. Le choix dépend de l'usage quotidien, pas seulement du budget."),
            ("Eastman est-il un marché de chalets ?", "Il y a de la villégiature, mais aussi des résidences principales. Il faut distinguer les deux dans le prix et l'inspection."),
            ("L'équipe connaît-elle Eastman ?", "Oui. Le corridor Magog–Orford–Eastman fait partie du territoire Chiasson de Francesco."),
            ("Quand mettre en vente à Eastman ?", "Fin d'hiver et printemps attirent souvent villégiature et montagne. Un bien au bon prix se vend aussi hors pic."),
        ],
    },
    {
        "slug": "lac-aylmer",
        "name": "Lac Aylmer",
        "title": "Propriétés au lac Aylmer | courtier Estrie | CDF",
        "description": "Acheter ou vendre en bord du lac Aylmer (Stratford, Weedon). Courtiers Chiasson de Francesco à Sherbrooke.",
        "h1": "Acheter ou vendre une propriété au lac Aylmer",
        "lead": "L'équipe Chiasson de Francesco accompagne l'achat et la vente au lac Aylmer : chalets, bord de lac et municipalités comme Stratford et Weedon, distincts du Memphrémagog.",
        "intro": "Le lac Aylmer n'est pas le Memphrémagog : autre bassin d'acheteurs, autre densité, autres prix. Un « prix lac Estrie » unique n'existe pas. Bandes riveraines et accès à l'eau dictent beaucoup de la valeur.",
        "sections": [
            ("Rives et municipalités", "Stratford, Weedon et les secteurs autour du plan d'eau mélangent villégiature et résidence. Une vue lac n'égale pas un accès à l'eau. Les rues sans lac se comparent à du rural, pas à du frontage."),
            ("Acheter au lac Aylmer", "Titres, servitudes, installation septique, inondabilité et règles municipales avant d'offrir. Un chalet trois-saisons n'est pas une résidence principale tant que le bâtiment ne le permet pas."),
            ("Vendre au lac Aylmer", "Photos d'eau et de saison, description honnête (moulure vs vrai bord de l'eau). Prix collé aux ventes Aylmer, pas Magog."),
        ],
        "related": [("Weedon", "weedon.html"), ("Lac-Mégantic", "lac-megantic.html"), ("Lac Memphrémagog", "lac-memphremagog.html"), ("Évaluation", "../evaluation.html")],
        "faqs": [
            ("Le lac Aylmer est-il moins cher que Memphrémagog ?", "En général le bassin est plus accessible, mais un vrai frontage bien situé reste un produit rare. Comparez des ventes du même lac, pas deux lacs entre eux sans nuance."),
            ("Peut-on habiter à l'année au lac Aylmer ?", "Oui si isolation, chauffage et services suivent. Beaucoup de chalets restent saisonniers. L'inspection tranche."),
            ("Desservez-vous Stratford et Weedon ?", "Oui. L'équipe Chiasson de Francesco couvre le lac Aylmer et le Haut-Saint-François."),
            ("Quoi vérifier avant d'acheter un chalet ?", "Fosse, puits, chauffage, accès hivernal, zonage et ce qui est vraiment inclus (quai, droits d'eau). Un courtier local pose ces questions avant l'offre."),
        ],
    },
    {
        "slug": "lac-brome",
        "name": "Lac-Brome",
        "title": "Courtier à Lac-Brome et Knowlton | CDF",
        "description": "Maisons et bord de lac à Lac-Brome (Knowlton). L'équipe Chiasson de Francesco vous accompagne en Estrie.",
        "h1": "Acheter ou vendre à Lac-Brome (Knowlton)",
        "lead": "L'équipe Chiasson de Francesco accompagne l'achat et la vente à Lac-Brome : Knowlton, rives du Brome Lake, village anglophone et propriétés de villégiature ou de résidence principale.",
        "intro": "Lac-Brome (Knowlton) attire une clientèle souvent bilingue, parfois montréalaise, sensible au village, aux lacs et au cachet. Ce n'est ni Sutton ski ni Sherbrooke urbain.",
        "sections": [
            ("Knowlton et le lac", "Knowlton est le cœur villageois. Le lac Brome et les rues en retrait n'ont pas le même prix. Commerces, resto et calendrier estival pèsent sur la demande villégiature."),
            ("Acheter à Lac-Brome", "Marché parfois mince, bâtiments de caractère, copropriétés de village. Vérifiez copropriété, fosses, et si le « bord de lac » est réellement un accès. Marco De Francesco travaille aussi en anglais."),
            ("Vendre à Lac-Brome", "Mise en marché bilingue utile. Prix ancré sur Knowlton/Brome, pas sur un condo de Bromont. Photos du village et du plan d'eau selon le bien."),
        ],
        "related": [("Sutton", "sutton.html"), ("Bromont", "bromont.html"), ("North Hatley", "north-hatley.html"), ("Marco De Francesco", "../marco.html")],
        "faqs": [
            ("Knowlton et Lac-Brome, c'est la même chose ?", "Knowlton est le village au sein de la ville de Lac-Brome. Les acheteurs disent souvent Knowlton ; les comparables doivent préciser le secteur (village vs rives vs rang)."),
            ("Faut-il un courtier bilingue à Lac-Brome ?", "Souvent utile. Beaucoup d'acheteurs et de documents circulent en anglais. L'équipe Chiasson de Francesco travaille en français et en anglais."),
            ("Lac-Brome est-il plus cher que Sutton ?", "Selon le produit. Un bord de lac Knowlton n'égale pas un condo ski Sutton. On compare le même type de bien."),
            ("Vous déplacez-vous à Knowlton ?", "Oui, depuis Sherbrooke, pour visites, évaluations et inscriptions à Lac-Brome."),
        ],
    },
    {
        "slug": "lac-massawippi",
        "name": "Lac Massawippi",
        "title": "Propriétés au lac Massawippi | North Hatley | CDF",
        "description": "Acheter ou vendre autour du lac Massawippi et North Hatley. Équipe Chiasson de Francesco, courtiers RE/MAX.",
        "h1": "Acheter ou vendre au lac Massawippi",
        "lead": "L'équipe Chiasson de Francesco accompagne l'achat et la vente au lac Massawippi : North Hatley, Ayer's Cliff, rives et villages, un marché plus serré que Sherbrooke.",
        "intro": "Le Massawippi est un petit lac avec une forte identité (North Hatley, Ayer's Cliff). Peu d'inscriptions, beaucoup d'attachement au lieu. Une erreur de prix se paie en mois d'affichage.",
        "sections": [
            ("North Hatley, Ayer's Cliff et les rives", "North Hatley concentre le prestige village. Ayer's Cliff et d'autres rives ont d'autres budgets. Une maison sans lac dans le secteur n'est pas un « prix Massawippi »."),
            ("Acheter au Massawippi", "Bandes riveraines, fosses, bâtiments souvent anciens, marché mince. Inspection et comparables du même versant du lac. Offre trop agressive sans comparables se paie cher."),
            ("Vendre au Massawippi", "Ne pas surcoter « parce que c'est le lac ». Photos, état du bâtiment, et patience pour le bon acheteur : souvent hors région ou bilingue."),
        ],
        "related": [("North Hatley", "north-hatley.html"), ("Sherbrooke", "sherbrooke.html"), ("Magog", "magog.html"), ("Évaluation", "../evaluation.html")],
        "faqs": [
            ("Massawippi ou Memphrémagog ?", "Deux lacs, deux clientèles. Memphrémagog (Magog) a plus de volume et de services urbains. Massawippi est plus petit, plus « village lac ». Les prix ne se recopient pas."),
            ("Ayer's Cliff fait-il partie du même marché que North Hatley ?", "Même lac, produits et budgets souvent différents. On compare rive par rive et village par village."),
            ("Faut-il parler anglais ?", "Utile. Le secteur est historiquement bilingue. L'équipe travaille en français et en anglais."),
            ("Desservez-vous tout le lac ?", "Oui. North Hatley, Ayer's Cliff et les rives du Massawippi sont dans le territoire de l'équipe."),
        ],
    },
    {
        "slug": "lac-megantic",
        "name": "Lac-Mégantic",
        "title": "Courtier immobilier au lac Mégantic | CDF",
        "description": "Acheter ou vendre une propriété à Lac-Mégantic et au lac. Équipe Chiasson de Francesco, Estrie.",
        "h1": "Acheter ou vendre à Lac-Mégantic",
        "lead": "L'équipe Chiasson de Francesco accompagne l'achat et la vente à Lac-Mégantic : ville, reconstruction du centre, rives du lac et secteur de la MRC du Granit.",
        "intro": "Lac-Mégantic a un marché local distinct de Sherbrooke : services de ville moyenne, lac, et une histoire urbaine particulière au centre. Les comparables doivent rester Granit, pas Estrie-ouest.",
        "sections": [
            ("Ville et lac", "Le centre et les quartiers résidentiels ne se vendent pas comme un chalet sur le lac. Le plan d'eau attire villégiature ; la ville attire résidence et commerce de proximité."),
            ("Acheter à Lac-Mégantic", "Distinguez résidence urbaine, commercial de rue et bord de lac. Inspection et, en centre-ville, lecture du tissu urbain actuel. Nous travaillons aussi le commercial."),
            ("Vendre à Lac-Mégantic", "Bassin d'acheteurs plus local qu'à Magog. Prix honnête et visibilité régionale (Sherbrooke inclus) aident sans gonfler au tarif Memphrémagog."),
        ],
        "related": [("Lac Aylmer", "lac-aylmer.html"), ("Weedon", "weedon.html"), ("Propriétés", "../proprietes.html"), ("Courtier commercial", "../courtier-commercial.html")],
        "faqs": [
            ("Lac-Mégantic est-il loin pour votre équipe ?", "C'est plus à l'est, mais l'équipe inscrit et accompagne dans le Granit lorsque le mandat le justifie. Discutez-en au téléphone avant une visite inutile."),
            ("Chalet au lac ou maison en ville ?", "Deux produits. Le lac se négocie sur l'accès à l'eau et la saisonnalité ; la ville sur l'état, le quartier et les services."),
            ("Y a-t-il du commercial à Lac-Mégantic ?", "Oui, à l'échelle locale. Pierre-Olivier et Marco traitent aussi le commercial, distinct du résidentiel."),
            ("Comment fixer le prix ?", "Ventes récentes Lac-Mégantic/Granit du même type. Pas un multiple de Sherbrooke."),
        ],
    },
    {
        "slug": "lac-memphremagog",
        "name": "Lac Memphrémagog",
        "title": "Propriétés au lac Memphrémagog | Magog, Orford | CDF",
        "description": "Bord de lac à Magog, Orford et Newport. L'équipe Chiasson de Francesco vous accompagne sur le Memphrémagog.",
        "h1": "Acheter ou vendre au lac Memphrémagog",
        "lead": "L'équipe Chiasson de Francesco accompagne l'achat et la vente au lac Memphrémagog : Magog, Georgeville, rives d'Orford et propriétés dont la valeur tient à l'eau, à la vue ou au village.",
        "intro": "Memphrémagog est le grand lac de l'Estrie ouest. Magog apporte les services ; les rives et villages lacustres apportent la rareté. Un condo en ville n'est pas un frontage. Les règles riveraines sont non négociables dans l'offre.",
        "sections": [
            ("Magog, rives et villages", "Magog : services + éventuellement vue ou accès. Georgeville et d'autres hameaux : plus rare, souvent plus cher au pied. Orford : montagne plus que marina. Newport (côté américain) n'est pas le même droit ni le même courtier."),
            ("Acheter au Memphrémagog", "Droit à l'eau, quai, zonage, fosses, inondabilité, copropriété si quai partagé. Un « vue lac » sans accès se paie autrement qu'un vrai bord de l'eau. Inspection + notaire avertis."),
            ("Vendre au Memphrémagog", "Ne pas coller un prix Magog centre sur un rang sans lac. Photos d'eau, saison, et comparables du même type de rive. Acheteurs locaux et hors région."),
        ],
        "related": [("Magog", "magog.html"), ("Orford", "orford.html"), ("Stanstead", "stanstead.html"), ("Évaluation", "../evaluation.html")],
        "faqs": [
            ("Vue lac ou accès à l'eau : quelle différence de prix ?", "L'accès réel (et légal) à l'eau se paie généralement plus cher qu'une vue sans droits. Chaque rive a ses ventes. Un courtier les sépare avant l'affichage."),
            ("Peut-on louer à court terme au Memphrémagog ?", "Selon le règlement municipal et, le cas échéant, la copropriété. Magog et les villages n'ont pas les mêmes règles. Vérifiez avant d'acheter pour un projet Airbnb."),
            ("Georgeville fait-il partie de Magog ?", "C'est un hameau lacustre distinct dans l'orbite Magog. Les comparables Georgeville ne sont pas ceux du centre-ville."),
            ("Vous vendez des bords de lac ?", "Oui, lorsque nous avons le mandat. L'équipe travaille Magog, Orford et les rives du Memphrémagog."),
        ],
    },
    {
        "slug": "richmond",
        "name": "Richmond",
        "title": "Courtier immobilier à Richmond | rivière Saint-François | CDF",
        "description": "Acheter ou vendre à Richmond, sur la rivière Saint-François. Courtiers Chiasson de Francesco, RE/MAX.",
        "h1": "Acheter ou vendre une propriété à Richmond",
        "lead": "L'équipe Chiasson de Francesco accompagne l'achat et la vente à Richmond : ville sur la Saint-François, unifamiliales, plex et accès vers Windsor et Sherbrooke.",
        "intro": "Richmond est une petite ville de vallée, plus industrielle et ferroviaire dans son histoire que villégiature. Les prix et la demande suivent Windsor/Sources plus que Magog.",
        "sections": [
            ("Saint-François et le noyau urbain", "Le centre et les rues résidentielles dominent. La rivière donne du cadre à certains lots, sans en faire un marché « lac ». Windsor et Danville élargissent un peu les comparables."),
            ("Acheter à Richmond", "Bâtiments parfois plus anciens, inspection importante. Comparables Richmond/Windsor. Un plex se juge aux loyers réels, pas à un rendement sherbrookois copié."),
            ("Vendre à Richmond", "Prix du marché local. Visibilité Estrie aide ; une surcote « 20 minutes de Sherbrooke » sans comparables allonge l'affichage."),
        ],
        "related": [("Windsor", "windsor.html"), ("Danville", "danville.html"), ("Sherbrooke", "sherbrooke.html"), ("Évaluation", "../evaluation.html")],
        "faqs": [
            ("Richmond est-il un bon compromis vers Sherbrooke ?", "Pour certains budgets, oui : moins cher que plusieurs quartiers sherbrookois, avec un temps de route acceptable. Le quotidien n'est pas celui du centre-ville de Sherbrooke."),
            ("Y a-t-il des plex à Richmond ?", "Oui, à petite échelle. La demande locative est locale. Analysez les baux et l'état avant le prix au pied."),
            ("Desservez-vous Richmond ?", "Oui. L'équipe Chiasson de Francesco couvre Richmond, Windsor et la vallée de la Saint-François."),
            ("Commercial à Richmond ?", "À l'échelle de la ville. Discutez d'un mandat commercial avec Pierre-Olivier ou Marco."),
        ],
    },
    {
        "slug": "stanstead",
        "name": "Stanstead",
        "title": "Courtier immobilier à Stanstead | frontière | CDF",
        "description": "Propriétés à Stanstead, près du lac Memphrémagog et de la frontière. Équipe Chiasson de Francesco.",
        "h1": "Acheter ou vendre une propriété à Stanstead",
        "lead": "L'équipe Chiasson de Francesco accompagne l'achat et la vente à Stanstead : village frontalier, patrimoine, proximité du Memphrémagog et d'un marché bilingue.",
        "intro": "Stanstead (et Rock Island / Beebe) vit la frontière au quotidien. Patrimoine, douane, et un bassin parfois transfrontalier : ce n'est pas Magog centre, ni un rang de Compton.",
        "sections": [
            ("Village frontalier", "Rues anciennes, bâtiments de caractère, proximité de Derby Line. Le Haskell Free Library illustre le caractère unique du lieu : ça n'ajoute pas automatiquement 100 000 $ à une maison sans comparables."),
            ("Acheter à Stanstead", "Inspection de bâtiments anciens, titres, et clarté sur ce qui est au Québec. Un acheteur américain n'achète pas comme un acheteur de Sherbrooke. Marco travaille en anglais."),
            ("Vendre à Stanstead", "Mise en marché bilingue utile. Comparables Stanstead/Memphrémagog sud, pas Knowlton ou Bromont ski."),
        ],
        "related": [("Magog", "magog.html"), ("Lac Memphrémagog", "lac-memphremagog.html"), ("North Hatley", "north-hatley.html"), ("Marco De Francesco", "../marco.html")],
        "faqs": [
            ("Stanstead est-il un marché bilingue ?", "Oui, historiquement. Un courtier bilingue aide avec les acheteurs et certains documents. L'équipe travaille FR/EN."),
            ("Être à la frontière change-t-il une vente ?", "Ça change le bassin d'acheteurs et parfois les questions pratiques (déplacements, services). Le droit applicable reste le Québec pour un immeuble au Québec."),
            ("Proche du lac Memphrémagog ?", "Oui, dans l'orbite sud du lac, sans être Magog. Les bords de lac se négocient à part des maisons de village."),
            ("Vous allez à Stanstead ?", "Oui, pour visites et mandats dans le secteur Memphrémagog sud."),
        ],
    },
    {
        "slug": "sutton",
        "name": "Sutton",
        "title": "Courtier immobilier à Sutton | montagne | CDF",
        "description": "Acheter ou vendre à Sutton, village de montagne en Estrie. Ski, arts et maisons : équipe Chiasson de Francesco.",
        "h1": "Acheter ou vendre une propriété à Sutton",
        "lead": "L'équipe Chiasson de Francesco accompagne l'achat et la vente à Sutton : village, ski, condos de montagne et maisons pour résidence principale ou villégiature dans les Cantons-de-l'Est.",
        "intro": "Sutton mélange arts, ski et village : un marché plus « montagne » que Sherbrooke, plus village que Bromont station. Copropriétés de pente et maisons du village ne se comparent pas.",
        "sections": [
            ("Village et montagne", "Le village marche vers cafés et galeries. Les secteurs liés au ski visent villégiature et parfois location : selon règlements. Les rangs autour offrent plus de terrain."),
            ("Acheter à Sutton", "Frais de condo, règles de location, accès hivernal, pente et drainage. Un chalet ski n'est pas une résidence à l'année tant que le bâtiment ne l'est pas. Comparables Sutton, pas Knowlton lac."),
            ("Vendre à Sutton", "Acheteurs Montréal/Rive-Sud fréquents. Mise en marché claire sur l'usage (principal vs week-end). Prix de montagne, pas de Sherbrooke."),
        ],
        "related": [("Bromont", "bromont.html"), ("Lac-Brome", "lac-brome.html"), ("Propriétés", "../proprietes.html"), ("Évaluation", "../evaluation.html")],
        "faqs": [
            ("Sutton ou Bromont ?", "Deux stations, deux villages. Bromont a plus de volume et d'infrastructures sportives récentes. Sutton a un village plus « Cantons » et un marché souvent plus artisanal. Comparez le produit (condo vs maison), pas le nom de la montagne seulement."),
            ("Peut-on louer un condo à Sutton à court terme ?", "Selon la copropriété et la municipalité. Plusieurs immeubles encadrent ou interdisent. Vérifiez avant d'acheter pour un revenu."),
            ("Sutton est-il plus cher que Magog ?", "Pour un condo ski, parfois. Pour une unifamiliale de village, ça dépend. Pas de règle unique."),
            ("Vous travaillez Sutton ?", "Oui. Bromont, Sutton et Lac-Brome font partie du territoire ouest de l'équipe."),
        ],
    },
    {
        "slug": "val-des-sources",
        "name": "Val-des-Sources",
        "title": "Courtier à Val-des-Sources | CDF",
        "description": "Maisons à Val-des-Sources (Asbestos). Courtiers Chiasson de Francesco pour un achat ou une vente en Estrie.",
        "h1": "Acheter ou vendre à Val-des-Sources",
        "lead": "L'équipe Chiasson de Francesco accompagne l'achat et la vente à Val-des-Sources : ancienne ville minière en transition, unifamiliales abordables et marché local de la MRC des Sources.",
        "intro": "Val-des-Sources (anciennement Asbestos) a un marché distinct : prix souvent plus accessibles, identité industrielle en recomposition, acheteurs surtout régionaux. Ce n'est pas un marché de villégiature lacustre.",
        "sections": [
            ("Ville des Sources", "Quartiers résidentiels, services de petite ville, proximité de Danville. Les comparables restent Sources/Richmond, pas Magog."),
            ("Acheter à Val-des-Sources", "Inspection (bâtiments d'âge variable) et lecture honnête de la demande locative si plex. Un « deal » n'en est un que si l'état et le quartier suivent."),
            ("Vendre à Val-des-Sources", "Prix du marché local. Surcoter parce que Sherbrooke a monté n'accélère rien. Photos et affichage régional aident le bon acheteur à trouver le bien."),
        ],
        "related": [("Danville", "danville.html"), ("Richmond", "richmond.html"), ("Windsor", "windsor.html"), ("Évaluation", "../evaluation.html")],
        "faqs": [
            ("Pourquoi les maisons sont-elles plus abordables à Val-des-Sources ?", "Marché local, moins de pression villégiature que les lacs, et une économie différente de Sherbrooke. L'abordabilité n'annule pas l'inspection ni les coûts de rénovation."),
            ("Bon secteur pour un premier achat ?", "Possible si le budget et le projet de vie collent à une petite ville des Sources. Visitez à différentes heures et faites inspecter."),
            ("Plex et investissement ?", "À analyser au cas par cas : loyers réels, taxes, état. Ce n'est pas le multiplicateur universitaire de Sherbrooke."),
            ("Vous allez à Val-des-Sources ?", "Oui. L'équipe dessert la MRC des Sources depuis Sherbrooke."),
        ],
    },
    {
        "slug": "weedon",
        "name": "Weedon",
        "title": "Courtier immobilier à Weedon | Estrie | CDF",
        "description": "Acheter ou vendre à Weedon, Estrie, près du lac Aylmer. Accompagnement Chiasson de Francesco, RE/MAX.",
        "h1": "Acheter ou vendre une propriété à Weedon",
        "lead": "L'équipe Chiasson de Francesco accompagne l'achat et la vente à Weedon : village sur l'axe vers Lac-Mégantic, maisons, rangs et proximité du lac Aylmer.",
        "intro": "Weedon est un village-relais du Haut-Saint-François : route, services de base, et accès vers le lac Aylmer. Marché mince, prix à coller aux ventes locales.",
        "sections": [
            ("Village et axe routier", "Le noyau villageois vs les rangs. La 112 structure les déplacements. Un chalet Aylmer n'est pas une maison de village Weedon."),
            ("Acheter à Weedon", "Fosses, puits, état, et comparables Weedon/Aylmer selon le produit. Ne pas payer un prix lac pour un lot sans eau."),
            ("Vendre à Weedon", "Peu d'inscriptions : le premier prix compte. Photos honnêtes et affichage Estrie."),
        ],
        "related": [("Lac Aylmer", "lac-aylmer.html"), ("Lac-Mégantic", "lac-megantic.html"), ("Cookshire-Eaton", "cookshire-eaton.html"), ("Évaluation", "../evaluation.html")],
        "faqs": [
            ("Weedon est-il le lac Aylmer ?", "Weedon est la municipalité ; le lac est à proximité. Une maison au village n'a pas la valeur d'un frontage. Distinguez les deux dans l'offre."),
            ("Marché actif ?", "Plus calme que Sherbrooke. Les biens au bon prix bougent ; les autres attendent."),
            ("Desservez-vous Weedon ?", "Oui, avec le lac Aylmer et le Haut-Saint-François."),
            ("Terrain ou maison ?", "Deux analyses. Un terrain se juge au zonage et au coût de viabilisation ; une maison à l'état et aux comparables bâtis."),
        ],
    },
    {
        "slug": "windsor",
        "name": "Windsor",
        "title": "Courtier immobilier à Windsor | Estrie | CDF",
        "description": "Propriétés à Windsor, Estrie, sur la Saint-François. L'équipe Chiasson de Francesco vous accompagne.",
        "h1": "Acheter ou vendre une propriété à Windsor",
        "lead": "L'équipe Chiasson de Francesco accompagne l'achat et la vente à Windsor : petite ville papetière de la Saint-François, unifamiliales, plex et accès rapide vers Sherbrooke.",
        "intro": "Windsor est plus proche de Sherbrooke que Richmond ou Val-des-Sources, avec un caractère de ville industrielle de vallée. Des acheteurs y voient un budget plus sage qu'à Fleurimont, sans être Magog.",
        "sections": [
            ("Ville de la Saint-François", "Quartiers résidentiels, quelques plex, proximité de l'usine dans l'identité locale. Richmond et Sherbrooke (Brompton) encadrent les comparables."),
            ("Acheter à Windsor", "Inspection, et pour un plex les baux. Temps de route vers Sherbrooke à valider selon votre quotidien. Comparables Windsor d'abord."),
            ("Vendre à Windsor", "Le « 15 minutes de Sherbrooke » n'excuse pas un prix de Les Nations. Affichage clair, prix de Windsor."),
        ],
        "related": [("Richmond", "richmond.html"), ("Sherbrooke", "sherbrooke.html"), ("Danville", "danville.html"), ("Évaluation", "../evaluation.html")],
        "faqs": [
            ("Windsor est-il plus abordable que Sherbrooke ?", "Souvent pour une unifamiliale comparable, oui. L'écart dépend du quartier sherbrookois vis-à-vis et de l'état du bâtiment windsorien."),
            ("Bon pour navetter vers Sherbrooke ?", "Beaucoup le font. Mesurez votre trajet aux heures de pointe, pas seulement la distance GPS."),
            ("Plex à Windsor ?", "Oui, marché locatif plus petit. Chiffres réels des loyers avant le rêve du rendement."),
            ("Vous vendez à Windsor ?", "Oui. Vallée de la Saint-François : Windsor, Richmond, et Sherbrooke Brompton selon le mandat."),
        ],
    },
]


def nav_root() -> str:
    return """  <nav class="py-4 px-6 fixed w-full top-0 z-50 bg-brand-navy shadow-md">
    <div class="relative max-w-7xl mx-auto flex items-center justify-between">
      <a href="index.html"><img src="/src/assets/logo.png" alt="Chiasson & De Francesco" class="h-10 md:h-12 w-auto"></a>
      <div class="hidden md:flex items-center gap-10">
        <a href="index.html" class="text-white hover:text-brand-red font-medium">Accueil</a>
        <a href="index.html#about" class="text-white hover:text-brand-red font-medium">Équipe</a>
        <a href="proprietes.html" class="text-white hover:text-brand-red font-medium">Propriétés</a>
        <a href="blog.html" class="text-white hover:text-brand-red font-medium">Blogue</a>
        <a href="index.html#contact" class="text-white hover:text-brand-red font-medium">Contact</a>
      </div>
      <button id="mobile-menu-btn" class="md:hidden text-white" aria-label="Menu"><svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" /></svg></button>
    </div>
    <div id="mobile-menu" class="hidden md:hidden bg-brand-navy px-6 py-6 space-y-4 border-t border-white/10 mt-4">
      <a href="index.html" class="block text-white">Accueil</a>
      <a href="proprietes.html" class="block text-white">Propriétés</a>
      <a href="blog.html" class="block text-white">Blogue</a>
      <a href="index.html#contact" class="block text-white">Contact</a>
    </div>
  </nav>"""


def footer_root() -> str:
    return """  <footer class="bg-[#232323] text-gray-400 py-12 border-t-4 border-brand-red">
    <div class="max-w-7xl mx-auto px-6 text-sm">
      <div class="flex flex-wrap justify-center gap-4">
        <a href="index.html" class="hover:text-brand-red">Accueil</a>
        <a href="vendre.html" class="hover:text-brand-red">Vendre</a>
        <a href="acheter.html" class="hover:text-brand-red">Acheter</a>
        <a href="courtier-commercial.html" class="hover:text-brand-red">Commercial</a>
        <a href="proprietes.html" class="hover:text-brand-red">Propriétés</a>
        <a href="regions-desservies.html" class="hover:text-brand-red">Régions</a>
        <a href="blog.html" class="hover:text-brand-red">Blogue</a>
      </div>
      <p class="text-center text-xs text-gray-500 mt-6">&copy; 2026 Équipe Chiasson & De Francesco. 157 boul. Jacques-Cartier Sud, Sherbrooke.</p>
    </div>
  </footer>
  <script>var b=document.getElementById('mobile-menu-btn'),m=document.getElementById('mobile-menu');if(b&&m)b.addEventListener('click',function(){m.classList.toggle('hidden');});</script>"""


def page_shell(title: str, desc: str, canonical: str, body: str, ld: dict | None = None) -> str:
    ld_html = ""
    if ld:
        ld_html = f'<script type="application/ld+json">\n{json.dumps(ld, ensure_ascii=False, indent=2)}\n</script>'
    return f"""<!DOCTYPE html>
<html lang="fr-CA" class="scroll-smooth">
<head>
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-VBQPR5ZNV0"></script>
  <script src="/src/assets/js/ga.js"></script>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{BASE}/src/assets/images/chiassondefrancescoteam.jpg">
  <meta property="og:locale" content="fr_CA">
  <link rel="icon" type="image/svg+xml" href="/src/assets/favicon.svg">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Inter:400,500,600,700,800,900|Playfair+Display:400,500,600,700,800,900&amp;subset=latin">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>tailwind.config={{theme:{{extend:{{fontFamily:{{heading:['"Playfair Display"','serif'],body:['"Inter"','sans-serif']}},colors:{{brand:{{red:'#AA1120',navy:'#0c2749'}}}}}}}}}};</script>
  {ld_html}
</head>
<body class="antialiased bg-gray-50 text-gray-900 font-body min-h-screen flex flex-col">
{nav_root()}
{body}
{footer_root()}
</body>
</html>
"""


SERVICES = [
    {
        "file": "vendre.html",
        "title": "Vendre sa maison à Sherbrooke et en Estrie | CDF",
        "desc": "Vendre avec l'équipe Chiasson de Francesco : évaluation marchande, mise en marché Centris et négociation à Sherbrooke et en Estrie.",
        "h1": "Vendre une propriété à Sherbrooke et en Estrie",
        "lead": "L'équipe Chiasson de Francesco, courtiers RE/MAX D'ABORD à Sherbrooke, prépare le prix, le dossier et la négociation pour vendre une maison, un condo, un plex ou un immeuble en Estrie.",
        "sections": [
            ("Une évaluation avant l'affichage", "Le premier levier d'une vente, c'est le prix d'inscription. Trop haut, le bien s'use sur Centris. Trop bas, vous laissez de l'argent. Nous ancrons le prix sur des ventes récentes du même secteur : Les Nations n'est pas Magog, Coaticook n'est pas Bromont."),
            ("Mise en marché", "Photos, description honnête, réseau RE/MAX et diffusion. Home staging léger quand ça paie. Visites accompagnées, comptes rendus, et ajustement si le marché ne répond pas : pas d'attente passive de six mois."),
            ("Négociation et conditions", "Le prix n'est pas le seul enjeu : inspection, délais, inclusions, financement. L'équipe gère les offres jusqu'à l'acte chez le notaire."),
            ("Vendre sans urgence : ou avec", "Si vous hésitez encore entre vendre maintenant ou attendre, commencez par le questionnaire de timing. Il ne remplace pas une évaluation sur place, mais il cadre la décision."),
        ],
        "faqs": [
            ("Combien coûte un courtier pour vendre à Sherbrooke ?", "La rémunération est prévue au contrat de courtage (généralement un pourcentage du prix de vente, à confirmer par écrit). Il n'y a pas de « tarif unique Estrie » affiché ici : on le discute avant de signer."),
            ("Puis-je vendre sans courtier ?", "Oui. Le risque, c'est le prix, les clauses et le temps. Un courtier local réduit les erreurs coûteuses. Lisez aussi notre article courtier vs vente libre."),
            ("Combien de temps pour vendre ?", "Ça dépend du prix, de l'état et du secteur. Un bien juste n'a pas le même délai qu'un bien 15 % au-dessus des comparables."),
            ("Intervenez-vous hors Sherbrooke ?", "Oui : Magog, Bromont, Orford, North Hatley, Coaticook et le reste de l'Estrie, selon le mandat."),
        ],
        "links": [("Évaluer le timing", "evaluation.html"), ("Documents maison", "article-documents-vente-maison.html"), ("Documents terrain", "article-documents-vente-terrain.html"), ("Documents plex", "article-documents-vente-plex.html"), ("Fermette", "fermette-estrie.html"), ("Chalet", "chalet-estrie.html"), ("Plex", "plex-sherbrooke.html"), ("Régions desservies", "regions-desservies.html")],
    },
    {
        "file": "acheter.html",
        "title": "Acheter une maison en Estrie | courtier Sherbrooke | CDF",
        "desc": "Acheter à Sherbrooke et en Estrie avec un courtier acheteur : recherche Centris, visites, inspection et négociation. Équipe Chiasson de Francesco.",
        "h1": "Acheter une propriété à Sherbrooke et en Estrie",
        "lead": "L'équipe Chiasson de Francesco représente les acheteurs à Sherbrooke et en Estrie : recherche ciblée, lecture des comparables, visites et négociation des conditions : pas seulement du prix.",
        "sections": [
            ("Courtier acheteur, à quoi ça sert", "Le vendeur a souvent déjà un courtier. Le vôtre lit les défauts, le zonage, et ce que le marché a vraiment payé dans la rue : pas l'annonce. Au Québec, les règles d'agence s'expliquent avant de visiter sérieusement."),
            ("Recherche et filtres", "Centris, hors-marché parfois, et le territoire réel : Fleurimont n'est pas Lennoxville, un chalet Orford n'est pas un condo Magog. Nous évitons les visites hors critères."),
            ("Offre, inspection, notaire", "Une offre trop émotive se paie. Inspection, tests (fosse, pyrite selon le cas), et notaire. Les frais de clôture (mutation, notaire, ajustements) se prévoient : voir notre guide des frais cachés."),
            ("Premier achat", "Préautorisation, mise de fonds, SCHL si moins de 20 %, et calendrier réaliste. Jade, Pierre-Olivier et Marco accompagnent aussi les premiers acheteurs."),
        ],
        "faqs": [
            ("Le courtier acheteur est-il gratuit ?", "Au Québec, la rémunération est prévue aux contrats. Souvent, une part de la commission du listage rémunère le courtier collaborateur. On vous l'explique clairement avant de commencer."),
            ("Puis-je visiter sans courtier ?", "Oui. Un courtier structure les visites, relit les déclarations du vendeur et prépare l'offre. C'est là que l'erreur coûte."),
            ("Achetez-vous hors Estrie ?", "Le cœur du mandat est Sherbrooke et l'Estrie. Des inscriptions de l'équipe existent aussi ailleurs au Québec ; on en discute au cas par cas."),
            ("Par où commencer ?", "Préautorisation hypothécaire, critères (secteur, budget, type), puis recherche. Contactez l'équipe ou commencez par une région (Sherbrooke, Magog, Bromont…)."),
        ],
        "links": [("Frais cachés à l'achat", "article-frais-caches.html"), ("Pièges du premier acheteur", "article-eviter-les-pieges.html"), ("Sherbrooke", "regions/sherbrooke.html")],
    },
    {
        "file": "courtier-commercial.html",
        "title": "Courtier immobilier commercial Sherbrooke | CDF",
        "desc": "Locaux, fonds de commerce, bâtisses et terrains à Sherbrooke et au Québec. Pierre-Olivier Chiasson et Marco De Francesco, RE/MAX D'ABORD.",
        "h1": "Courtage immobilier commercial à Sherbrooke",
        "lead": "Pierre-Olivier Chiasson et Marco De Francesco, courtiers résidentiels et commerciaux RE/MAX D'ABORD, accompagnent locaux, fonds de commerce, bâtisses et projets à Sherbrooke, en Estrie et sur des mandats ailleurs au Québec.",
        "sections": [
            ("Ce que « commercial » veut dire ici", "Local au pied, fonds de commerce (achalandage, équipements), bâtisse mixte, terrain à développer. Chaque produit a ses comparables, son zonage et souvent la TPS/TVQ. Ce n'est pas une unifamiliale avec un autre panneau."),
            ("Zonage et due diligence", "Le règlement d'urbanisme, les usages permis, la décontamination, le stationnement et les baux en place pèsent plus que la vitrine. Nous travaillons avec vos fiscalistes, inspecteurs et, au besoin, urbanistes."),
            ("Exemples de mandats", "L'équipe a notamment inscrit des locaux et bâtisses à Sherbrooke (Wellington, Tessier), un condo commercial à Montréal et d'autres produits hors Estrie. Le détail est sur les fiches en ligne tant qu'elles sont actives."),
            ("Investisseur vs occupant", "Un occupant juge l'usage. Un investisseur juge le bail, le covenant et le taux. La même adresse n'a pas le même prix selon le scénario. On le sépare dès l'évaluation."),
        ],
        "faqs": [
            ("Faites-vous seulement le résidentiel ?", "Non. Pierre-Olivier et Marco sont aussi courtiers commerciaux. Jade se concentre sur le résidentiel."),
            ("Intervenez-vous à Montréal ou Québec ?", "Lorsque le mandat le justifie, oui : des fiches hors Estrie l'illustrent. Le bureau reste à Sherbrooke."),
            ("Un dépanneur ou un resto, c'est du commercial ?", "Souvent un fonds de commerce + un bail ou un immeuble. Les équipements et l'achalandage se négocient à part des murs. Voyez avec l'équipe le bon véhicule."),
            ("Par où commencer ?", "Appel ou formulaire : type de bien, occupation vs investissement, échéance. Une visite à l'aveugle sans zonage fait perdre du temps."),
        ],
        "links": [("Propriétés", "proprietes.html"), ("Pierre-Olivier", "pierre-olivier.html"), ("Marco", "marco.html")],
    },
]


ARTICLES = [
    {
        "file": "article-courtier-ou-vente-libre.html",
        "title": "Vendre avec un courtier ou seul ? | Estrie | CDF",
        "headline": "Vendre avec un courtier ou sans : ce qui change en Estrie",
        "desc": "Prix, clauses, temps et commission : quand un courtier immobilier à Sherbrooke paie, et quand la vente libre peut suffire.",
        "date": "18 août 2026",
        "published": "2026-08-18",
        "tag": "Vendre",
        "author": "Pierre-Olivier Chiasson",
        "author_page": "pierre-olivier.html",
        "kicker": "En Estrie, la vente libre n'est pas « gratuite » : vous payez en temps, en risque de clauses, et parfois en prix. Voici comment décider.",
        "sections": [
            ("Ce que le courtier facture vraiment", "La commission n'est pas un impôt : c'est un contrat. Elle couvre mise en marché, réseau, négociation et responsabilité professionnelle. Un pourcentage sur 400 000 $ n'a de sens que si le prix net et le délai s'améliorent assez pour le justifier : ce n'est pas automatique."),
            ("Où la vente libre casse", "Prix d'affichage copié sur une annonce voisine, visite d'acheteurs mal cadrée, offre avec conditions que vous ne lisez pas. À Sherbrooke comme à Magog, le marché punit vite un bien 10 % trop cher. Sans comparables de ventes closes, vous naviguez à l'estime."),
            ("Où elle peut suffire", "Bien atypique déjà promis à un acheteur identifié, copropriété avec un voisin acquéreur, ou vous avez déjà fait trois transactions et un notaire solide. Même là, une évaluation indépendante reste utile."),
            ("Le test simple", "Si vous ne pouvez pas citer trois ventes récentes du même type dans votre secteur, vous n'êtes pas en position de fixer le prix seul. L'équipe Chiasson de Francesco le fait tous les jours à Sherbrooke et en Estrie."),
        ],
    },
    {
        "file": "article-evaluation-marchande-estrie.html",
        "title": "Évaluation marchande vs municipale | Estrie | CDF",
        "headline": "Évaluation municipale et prix de vente : ne les confondez pas",
        "desc": "L'évaluation municipale n'est pas le prix de marché à Sherbrooke. Comment une évaluation marchande de courtier s'en distingue.",
        "date": "18 août 2026",
        "published": "2026-08-18",
        "tag": "Vendre",
        "author": "Marco De Francesco",
        "author_page": "marco.html",
        "kicker": "Beaucoup de propriétaires estrien·nes affichent « évaluation municipale + 20 % ». C'est l'une des façons les plus sûres de rester trop longtemps sur Centris.",
        "sections": [
            ("À quoi sert l'évaluation municipale", "Elle sert surtout à taxer. Le rôle est périodique, parfois en retard sur un quartier qui a bougé, parfois trop haut après une rénovation mal comprise. Ce n'est pas une offre d'acheteur."),
            ("L'évaluation marchande", "Un courtier compare des ventes closes, pas des demandes. Même typologie, même secteur, ajustements (état, terrain, reno). À Lennoxville, le comparables n'est pas Rock Forest."),
            ("Quand les deux divergent", "Rive de lac, commercial mixte, fermette, ou immeuble avec baux : l'écart peut être large. C'est normal. Ce qui n'est pas normal, c'est d'ignorer l'écart."),
            ("Avant de signer un contrat", "Demandez sur quelles ventes le prix proposé s'appuie. Si la réponse est vague, ce n'est pas une évaluation, c'est un espoir. L'équipe Chiasson de Francesco ancre le prix avant l'affiche."),
        ],
    },
    {
        "file": "article-delai-vente-estrie.html",
        "title": "Combien de temps pour vendre en Estrie ? | CDF",
        "headline": "Délai de vente en Estrie : ce qui allonge vraiment l'affichage",
        "desc": "Prix, saison, type de bien : pourquoi une maison à Sherbrooke ne se vend pas au même rythme qu'un chalet à Orford.",
        "date": "18 août 2026",
        "published": "2026-08-18",
        "tag": "Vendre",
        "author": "Jade Sirois",
        "author_page": "jade.html",
        "kicker": "Il n'existe pas de « délai moyen Estrie » utile. Un condo au centre-ville de Sherbrooke et une fermette à Compton n'ont pas le même calendrier.",
        "sections": [
            ("Le prix d'inscription", "C'est le facteur n°1. Un bien 8 à 15 % au-dessus des ventes récentes accumule des jours, puis des baisses publiques qui signalent un problème aux acheteurs."),
            ("Le type de bien", "Unifamiliale en quartier familial : plus de volume. Chalet, bord de lac, commercial, terre : moins d'acheteurs, plus de conditions. Orford au printemps n'est pas Fleurimont en novembre."),
            ("La préparation", "Photos sombres, odeurs, travaux visibles non budgétés : les visiteurs partent. Un home staging léger et une inspection pré-vente évitent les négociations-surprises."),
            ("Ce que nous faisons", "Après deux à trois semaines sans trafic qualifié, on révise le prix ou le positionnement : on n'attend pas six mois. Le questionnaire de timing aide aussi à ne pas afficher trop tôt par rapport à votre prochain logement."),
        ],
    },
    {
        "file": "article-offre-achat-quebec.html",
        "title": "Comment faire une offre d'achat au Québec | CDF",
        "headline": "Offre d'achat au Québec : prix, conditions et erreurs fréquentes",
        "desc": "Promesse d'achat, inspection, financement : les clauses qui protègent un acheteur à Sherbrooke, et celles qui font fuir le vendeur.",
        "date": "18 août 2026",
        "published": "2026-08-18",
        "tag": "Acheter",
        "author": "Pierre-Olivier Chiasson",
        "author_page": "pierre-olivier.html",
        "kicker": "Une offre n'est pas un « j'aime » sur Centris. Au Québec, c'est un document qui engage. Mal rédigée, elle vous coûte la maison : ou vous y enferme trop vite.",
        "sections": [
            ("Prix vs conditions", "Gagner 5 000 $ et perdre l'inspection, ce n'est pas gagner. En marché plus calme, on négocie délais et travaux. En marché tendu, le prix et la solidité du financement parlent plus fort."),
            ("Inspection et tests", "Prévoir le temps et le professionnel. Fosse, toiture, fondations. Une clause d'inspection « pour la forme » ne protège personne."),
            ("Financement", "Préautorisation n'est pas un certificat de fonds. La condition de financement a une date. La rater sans plan B est une erreur de premier acheteur classique."),
            ("Inclusions", "Lave-vaisselle, stores, cabanon, quai : écrivez-les. « Ce qui était là à la visite » se discute mal chez le notaire. Un courtier acheteur verrouille ça avant."),
        ],
    },
    {
        "file": "article-bord-de-lac-estrie.html",
        "title": "Acheter un bord de lac en Estrie | CDF",
        "headline": "Bord de lac en Estrie : Memphrémagog, Massawippi, Aylmer",
        "desc": "Accès à l'eau vs vue, fosses, bandes riveraines : ce qu'un acheteur doit vérifier avant d'offrir sur un lac en Estrie.",
        "date": "18 août 2026",
        "published": "2026-08-18",
        "tag": "Acheter",
        "author": "Marco De Francesco",
        "author_page": "marco.html",
        "kicker": "« Bord de lac » dans une annonce veut parfois dire une vue, un droit d'accès, ou réellement le frontage. Les trois n'ont pas le même prix : ni les mêmes règles.",
        "sections": [
            ("Trois lacs, trois marchés", "Memphrémagog (Magog, rives) : plus de services et de volume. Massawippi (North Hatley) : plus rare, plus village. Aylmer : autre bassin, souvent plus accessible. Ne copiez pas un prix d'un lac sur l'autre."),
            ("Droit à l'eau", "Titres, servitudes, quai, association de riverains. Un sentier « tout le monde passe » n'est pas un droit. Le notaire et le courtier doivent le voir avant l'offre, pas après."),
            ("Environnement et fosse", "Bandes riveraines, installation septique, parfois inondabilité. Un chalet charmant avec une fosse hors norme devient un chantier. Budgetz la mise aux normes."),
            ("Saisonnier vs quatre-saisons", "Isolation, chauffage, accès hivernal. Transformer un trois-saisons coûte plus que « un peu d'isolant ». L'inspection le dit plus clair que l'annonce."),
        ],
    },
    {
        "file": "article-condo-sherbrooke.html",
        "title": "Acheter un condo à Sherbrooke | frais et pièges | CDF",
        "headline": "Condo à Sherbrooke : frais de copropriété, fonds et inspections",
        "desc": "Charges, fonds de prévoyance, PV d'assemblée : ce qu'il faut lire avant d'acheter un condo aux Nations, en centre-ville ou à Fleurimont.",
        "date": "18 août 2026",
        "published": "2026-08-18",
        "tag": "Acheter",
        "author": "Jade Sirois",
        "author_page": "jade.html",
        "kicker": "Le prix affiché d'un condo à Sherbrooke n'est pas le coût de possession. Les frais mensuels et le fonds de prévoyance décident si l'affaire est bonne.",
        "sections": [
            ("Les frais ne sont pas un détail", "Un condo 20 000 $ moins cher avec 150 $ de plus par mois de charges peut coûter plus cher en cinq ans. Demandez l'historique des hausses et les travaux votés."),
            ("Fonds de prévoyance et études", "Toiture, stationnement, briques : si le fonds est maigre, c'est vous qui paierez la cotisation spéciale. Lisez les PV et l'étude du fonds quand elle existe."),
            ("Déclaration et règlements", "Animaux, Airbnb, rénovations. Un projet de location courte durée dans un immeuble qui l'interdit n'est pas un malentendu, c'est un non."),
            ("Secteurs", "Les Nations et le centre : plus de condos, plus de volume. Fleurimont et autres : parfois des copropriétés plus petites. Les comparables restent dans le même type d'immeuble."),
        ],
    },
    {
        "file": "article-premiere-maison-estrie.html",
        "title": "Première maison en Estrie | budget et étapes | CDF",
        "headline": "Première maison à Sherbrooke et en Estrie : le parcours réaliste",
        "desc": "Mise de fonds, préautorisation, inspection : les étapes d'un premier achat à Sherbrooke, Magog ou en périphérie, sans romantiser le « deal ».",
        "date": "18 août 2026",
        "published": "2026-08-18",
        "tag": "Acheter",
        "author": "Jade Sirois",
        "author_page": "jade.html",
        "kicker": "Le premier achat en Estrie se joue sur le budget total (pas seulement le prix Centris) et sur un secteur que vous supporterez en janvier, pas seulement en juillet.",
        "sections": [
            ("L'argent autour du prix", "Mise de fonds, SCHL, droits de mutation, notaire, inspection, déménagement. Notre guide des frais cachés liste les postes. Arrivez chez le notaire avec une réserve, pas à 200 $ près."),
            ("Préautorisation", "Elle cadre le maximum. Elle ne dit pas quelle rue acheter. Un courtier hypothécaire + un courtier immobilier, ce n'est pas un luxe, c'est deux métiers."),
            ("Où chercher", "Sherbrooke pour les services. Magog si le lac et la villégiature comptent. Windsor/Richmond si le budget est plus serré et le navettage acceptable. Visitez le soir et un samedi matin."),
            ("L'émotion", "La première maison n'a pas à être la dernière. Une inspection sévère sur un « coup de cœur » vous évite d'acheter les problèmes du vendeur."),
        ],
    },
    {
        "file": "article-zonage-commercial-sherbrooke.html",
        "title": "Zonage commercial à Sherbrooke | avant d'acheter | CDF",
        "headline": "Zonage mixte et commercial à Sherbrooke : lisez le règlement avant l'offre",
        "desc": "H10, usages permis, décontamination : pourquoi un local ou une bâtisse à Sherbrooke se juge d'abord au zonage, pas à la vitrine.",
        "date": "18 août 2026",
        "published": "2026-08-18",
        "tag": "Commercial",
        "author": "Pierre-Olivier Chiasson",
        "author_page": "pierre-olivier.html",
        "kicker": "Une vitrine sur Wellington n'autorise pas tous les usages. À Sherbrooke, le règlement d'urbanisme décide si votre projet est légal : l'annonce Centris, non.",
        "sections": [
            ("Usages permis vs « on verra »", "Restauration, dépanneur, bureaux, résidentiel dans un mixte : chaque zone a une grille. Un courtier commercial commence par ça, pas par le loyer rêvé."),
            ("Mixte et projets", "Des bâtisses attendent un projet résidentiel ou une occupation commerciale. Sol, décontamination, stationnement et hauteurs changent la faisabilité. Les études ne sont pas optionnelles."),
            ("Fonds de commerce", "Acheter les murs n'est pas acheter l'achalandage. Permis, équipements, baux. Deux négociations, parfois deux actes."),
            ("Qui appeler", "Pierre-Olivier et Marco traitent le commercial. Apportez votre usage cible et votre échéance ; on vous dira vite si le zonage tue le projet."),
        ],
    },
    {
        "file": "article-inspection-maison-estrie.html",
        "title": "Inspection préachat en Estrie | fosses et chalets | CDF",
        "headline": "Inspection préachat en Estrie : maisons, fosses et chalets",
        "desc": "Quoi faire inspecter avant d'acheter à Sherbrooke, Magog ou en rang : bâtiment, fosse, puits. Conseils de l'équipe Chiasson de Francesco.",
        "date": "18 août 2026",
        "published": "2026-08-18",
        "tag": "Acheter",
        "author": "Jade Sirois",
        "author_page": "jade.html",
        "kicker": "En Estrie, l'inspection ne s'arrête pas au toit. Fosses, puits, chalets trois-saisons et bâtiments de ferme changent la liste : et parfois l'offre.",
        "sections": [
            ("Le bâtiment d'abord", "Fondations, toiture, électricité, humidité. Un bungalow des années 1970 à Fleurimont n'a pas les mêmes points de vigilance qu'une maison de village à North Hatley. L'inspecteur en bâtiment reste le premier rendez-vous après une offre conditionnelle."),
            ("Hors égouts municipaux", "Une grande partie de l'Estrie rurale (Coaticook, Compton, rangs d'Orford, bords de lac) fonctionne à la fosse. Un test et une lecture de conformité valent plus qu'une clause copiée. Une mise aux normes se chiffre en milliers, pas en « petit ajustement »."),
            ("Chalets et villégiature", "Isolation, chauffage, accès hivernal, quai. Un trois-saisons vendu comme résidence principale est un chantier. Magog, Orford, Aylmer : même logique, différents règlements riverains."),
            ("Après le rapport", "Renégocier, se retirer, ou accepter avec réserve. Un courtier acheteur traduit le jargon et évite de tout laisser tomber pour un détail cosmétique : ou d'ignorer une fissure structurelle."),
        ],
    },
    {
        "file": "article-vendre-condo-sherbrooke.html",
        "title": "Vendre un condo à Sherbrooke | charges et acheteurs | CDF",
        "headline": "Vendre un condo à Sherbrooke : charges, fonds et mise en marché",
        "desc": "Copropriété à Sherbrooke : documents à préparer, frais, et comment un prix collé au marché évite un condo qui stagne sur Centris.",
        "date": "18 août 2026",
        "published": "2026-08-18",
        "tag": "Vendre",
        "author": "Pierre-Olivier Chiasson",
        "author_page": "pierre-olivier.html",
        "kicker": "Un condo aux Nations ne se vend pas comme une unifamiliale à Fleurimont. Les acheteurs lisent les charges et le fonds avant la vue sur la rivière.",
        "sections": [
            ("Le dossier acheteur", "Déclaration de copropriété, états financiers, PV, règlement, historique des cotisations. Un dossier incomplet fait fuir les courtiers collaborateurs et allonge les conditions."),
            ("Charges et fonds", "Des frais élevés se justifient s'ils paient un immeuble bien tenu. Un fonds maigre se paie en baisse de prix ou en condition. On l'affiche honnêtement, on ne le cache pas dans une note de bas de page."),
            ("Prix", "Comparables du même type d'immeuble, pas « le condo d'à côté 40 000 $ plus cher sans rénos ». Les Nations, le centre et Fleurimont n'ont pas le même bassin."),
            ("Mise en marché", "Photos des parties communes si elles aident, stationnement, rangement. L'équipe Chiasson de Francesco prépare le dossier avant l'affiche, pas après la première visite déçue."),
        ],
    },
    {
        "file": "article-navette-sherbrooke.html",
        "title": "Habiter Windsor, Richmond ou Magog et travailler à Sherbrooke | CDF",
        "headline": "Navetter vers Sherbrooke : Windsor, Richmond, Magog, Coaticook",
        "desc": "Où habiter autour de Sherbrooke selon le trajet, le budget et le mode de vie. Lecture de courtier, pas un palmarès de distances GPS.",
        "date": "18 août 2026",
        "published": "2026-08-18",
        "tag": "Acheter",
        "author": "Marco De Francesco",
        "author_page": "marco.html",
        "kicker": "Beaucoup d'acheteurs veulent « 20 minutes de Sherbrooke » et un prix plus bas. Le trajet réel, le quotidien d'hiver et le type de bien comptent plus que le pin Google.",
        "sections": [
            ("Windsor et Richmond", "Vallée de la Saint-François : souvent plus abordable, navette plausible. Windsor est plus proche ; Richmond un cran plus loin. Visitez à l'heure de pointe, pas un dimanche après-midi."),
            ("Magog et Orford", "Services, lac, montagne : et un prix souvent plus élevé. Le trajet Magog–Sherbrooke est courant, mais ce n'est pas le même budget qu'un bungalow de Rock Forest."),
            ("Coaticook et Cookshire-Eaton", "Plus champêtre, moins de volume. Le compromis est l'espace et le calme, pas la proximité du CHUS. Un premier acheteur pressé par le travail de quart doit mesurer le trajet, pas le rêve."),
            ("Comment on aide", "On ne vous vend pas une municipalité. On aligne budget, type de bien et quotidien. L'équipe Chiasson de Francesco connaît ces corridors pour les avoir parcourus en visites, pas seulement en carte."),
        ],
    },
    {
        "file": "article-terrain-estrie.html",
        "title": "Acheter un terrain en Estrie | zonage et viabilisation | CDF",
        "headline": "Acheter un terrain en Estrie : zonage, puits, fosse et vrai coût",
        "desc": "Un terrain à Cookshire-Eaton ou en rang n'est pas un prix à l'acre. Zonage, accès et viabilisation avant d'offrir. Courtiers Chiasson de Francesco.",
        "date": "18 août 2026",
        "published": "2026-08-18",
        "tag": "Acheter",
        "author": "Pierre-Olivier Chiasson",
        "author_page": "pierre-olivier.html",
        "kicker": "Le prix demandé d'un lot en Estrie cache souvent le coût réel : entrée, puits, fosse, drainage, et parfois l'impossibilité de bâtir ce que vous aviez en tête.",
        "sections": [
            ("Zonage d'abord", "Agricole, résidentiel, villégiature : vous n'avez pas le droit de faire n'importe quoi. Un lot « pour une maison » dans une annonce n'est pas un certificat d'urbanisme. Demandez-le avant l'offre ferme."),
            ("Viabilisation", "Puits, fosse, électricité, chemin. Un acre pas cher loin des services peut coûter plus cher qu'un lot municipal à Cookshire. Chiffrez avec des entrepreneurs, pas avec un espoir."),
            ("Accès et hiver", "Servitude, entretien de rang, pente. Un beau lot en juillet peut être un cauchemar en février. Visitez hors saison si vous comptez habiter à l'année."),
            ("L'équipe et les terrains", "Nous inscrivons aussi des terrains (notamment Cookshire-Eaton). Même lecture à l'achat : comparables au bon type de lot, pas un prix à l'acre copié sur le voisin."),
        ],
        "extra_links": [("Documents pour vendre un terrain", "article-documents-vente-terrain.html")],
    },
]


def faq_ld(canonical: str, faqs: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    }


def write_service(s: dict) -> None:
    sections = "\n".join(
        f'<h2 class="font-heading text-2xl font-bold text-brand-navy mt-10 mb-3">{h}</h2><p class="text-gray-600 leading-relaxed mb-6">{p}</p>'
        for h, p in s["sections"]
    )
    faqs = "\n".join(
        f'<div class="border border-gray-200 rounded-xl p-5 bg-white mb-4"><h3 class="font-semibold text-brand-navy mb-2">{q}</h3><p class="text-gray-600">{a}</p></div>'
        for q, a in s["faqs"]
    )
    links = " · ".join(f'<a class="text-brand-navy font-medium hover:text-brand-red" href="{h}">{t}</a>' for t, h in s["links"])
    body = f"""
  <header class="pt-32 pb-10 bg-white border-b">
    <div class="max-w-3xl mx-auto px-6">
      <p class="text-sm text-gray-500 mb-3"><a href="index.html" class="hover:text-brand-red">Accueil</a> / {s["h1"].split()[0]}</p>
      <h1 class="font-heading text-4xl md:text-5xl font-bold text-brand-navy">{s["h1"]}</h1>
      <p class="text-lg text-gray-600 mt-4">{s["lead"]}</p>
    </div>
  </header>
  <main class="flex-grow py-12"><div class="max-w-3xl mx-auto px-6">
    {sections}
    <h2 class="font-heading text-2xl font-bold text-brand-navy mt-10 mb-4">Questions fréquentes</h2>
    {faqs}
    <p class="mt-8 text-gray-600">Pour aller plus loin : {links}</p>
    <div class="flex flex-wrap gap-4 mt-8">
      <a href="index.html#contact" class="bg-brand-navy text-white font-semibold py-3 px-6 rounded-lg hover:bg-brand-red">Nous contacter</a>
      <a href="evaluation.html" class="bg-gray-200 text-brand-navy font-semibold py-3 px-6 rounded-lg">Questionnaire vendeur</a>
    </div>
  </div></main>
"""
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            faq_ld(f"{BASE}/{s['file']}", s["faqs"]),
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Accueil", "item": f"{BASE}/"},
                    {"@type": "ListItem", "position": 2, "name": s["h1"], "item": f"{BASE}/{s['file']}"},
                ],
            },
        ],
    }
    (ROOT / s["file"]).write_text(page_shell(s["title"], s["desc"], f"{BASE}/{s['file']}", body, graph), encoding="utf-8")
    print("wrote", s["file"])


def write_article(a: dict) -> None:
    sections = "\n".join(
        f'<h2 class="font-heading text-2xl font-bold text-brand-navy mt-10 mb-4">{h}</h2><p class="text-gray-600 leading-relaxed mb-6">{p}</p>'
        for h, p in a["sections"]
    )
    faqs_html = ""
    if a.get("faqs"):
        items = "\n".join(
            f'<div class="border border-gray-200 rounded-xl p-5 bg-white mb-4"><h3 class="font-semibold text-brand-navy mb-2">{q}</h3><p class="text-gray-600">{ans}</p></div>'
            for q, ans in a["faqs"]
        )
        faqs_html = f'<h2 class="font-heading text-2xl font-bold text-brand-navy mt-10 mb-4">Questions fréquentes</h2>\n{items}'
    extra = ""
    if a.get("region_href"):
        extra = f' · <a class="text-brand-navy font-medium hover:text-brand-red" href="{a["region_href"]}">{a.get("region_label", "Page région")}</a>'
    if a.get("extra_links"):
        extra += "".join(
            f' · <a class="text-brand-navy font-medium hover:text-brand-red" href="{href}">{label}</a>'
            for label, href in a["extra_links"]
        )
    body = f"""
  <main class="pt-32 pb-20">
    <div class="max-w-3xl mx-auto px-6">
      <nav class="text-sm text-gray-500 mb-6"><a href="index.html" class="hover:text-brand-red">Accueil</a> / <a href="blog.html" class="hover:text-brand-red">Blogue</a> / {a["tag"]}</nav>
      <div class="inline-block bg-brand-navy text-white px-3 py-1 rounded-full text-xs font-bold uppercase mb-4">{a["tag"]}</div>
      <h1 class="font-heading text-4xl md:text-5xl font-bold text-brand-navy mb-4">{a["headline"]}</h1>
      <p class="text-sm text-gray-500 mb-8">Par <a class="hover:text-brand-red" href="{a["author_page"]}">{a["author"]}</a> · {a["date"]}</p>
      <p class="text-xl font-medium text-brand-navy mb-8">{a["kicker"]}</p>
      {sections}
      {faqs_html}
      <p class="text-gray-600 mt-10">Équipe Chiasson de Francesco, RE/MAX D'ABORD, Sherbrooke. <a class="text-brand-navy font-medium hover:text-brand-red" href="index.html#contact">Discuter d'un projet</a> · <a class="text-brand-navy font-medium hover:text-brand-red" href="blog.html">Retour au blogue</a>{extra}</p>
    </div>
  </main>
"""
    article_ld = {
        "@type": "Article",
        "headline": a["headline"],
        "description": a["desc"],
        "datePublished": a["published"],
        "dateModified": a["published"],
        "inLanguage": "fr-CA",
        "author": {"@type": "Person", "name": a["author"], "url": f"{BASE}/{a['author_page']}"},
        "publisher": {
            "@type": "Organization",
            "name": "Équipe Chiasson de Francesco",
            "url": f"{BASE}/",
            "logo": {"@type": "ImageObject", "url": f"{BASE}/src/assets/logo.png"},
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"{BASE}/{a['file']}"},
    }
    if a.get("faqs"):
        ld = {"@context": "https://schema.org", "@graph": [article_ld, faq_ld(f"{BASE}/{a['file']}", a["faqs"])]}
    else:
        ld = {"@context": "https://schema.org", **article_ld}
    (ROOT / a["file"]).write_text(page_shell(a["title"], a["desc"], f"{BASE}/{a['file']}", body, ld), encoding="utf-8")
    print("wrote", a["file"])


def main() -> None:
    for page in REMAINING:
        extras = [
            ("Vendre une propriété", "../vendre.html"),
            ("Acheter en Estrie", "../acheter.html"),
        ]
        skip = {h for _, h in extras}
        page["related"] = extras + [(t, h) for t, h in page["related"] if h not in skip]
        path = ROOT / "regions" / f"{page['slug']}.html"
        path.write_text(render_region(page), encoding="utf-8")
        print("wrote", path.relative_to(ROOT))
    for s in SERVICES:
        write_service(s)
    for a in ARTICLES:
        write_article(a)


if __name__ == "__main__":
    main()
