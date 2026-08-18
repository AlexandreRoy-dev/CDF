#!/usr/bin/env python3
"""GEO city guides: Vendre ou acheter a [ville] : quoi savoir. No em dashes."""

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
    return "<ul class=\"list-disc pl-5 space-y-2 text-gray-600 mb-6\">" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


def ol(items: list[str]) -> str:
    return "<ol class=\"list-decimal pl-5 space-y-2 text-gray-600 mb-6\">" + "".join(f"<li>{x}</li>" for x in items) + "</ol>"


CITIES = [
    {
        "slug": "sherbrooke",
        "name": "Sherbrooke",
        "prep": "à",
        "author": "po",
        "desc": "Vendre ou acheter à Sherbrooke : quartiers, prix, inspection. Guide de l'équipe Chiasson de Francesco, courtiers RE/MAX.",
        "tldr": "Pour vendre ou acheter à Sherbrooke, le quartier décide autant que le type de bien. Les Nations, Fleurimont, Lennoxville, Mont-Bellevue, Rock Forest et Brompton n'ont pas les mêmes comparables. L'équipe Chiasson de Francesco, courtiers immobiliers RE/MAX D'ABORD à Sherbrooke, ancre le prix sur des ventes closes du même secteur, pas sur une moyenne de ville.",
        "market": "Sherbrooke est le pôle urbain de l'Estrie : universités, hôpitaux, centre-ville et quartiers familiaux. Un courtier local sert à lire le prix réel d'une rue et à éviter une offre trop haute ou trop basse.",
        "facts": [
            "Les Nations concentre condos, plex et commercial de rue (King, Wellington).",
            "Fleurimont et Mont-Bellevue accueillent surtout des unifamiliales.",
            "Lennoxville reste un village universitaire bilingue, distinct de Fleurimont.",
            "Rock Forest et Brompton offrent souvent plus de terrain, avec un autre temps de trajet.",
        ],
        "sell": "À Sherbrooke, le premier levier d'une vente est le prix d'inscription collé aux ventes récentes du même quartier. Un bungalow Fleurimont trop cher par rapport à sa rue s'use sur Centris. Un condo aux Nations se juge aussi aux charges et au fonds de prévoyance.",
        "sell_steps": [
            "Faire une évaluation marchande sur des ventes closes du même type, dans le même arrondissement.",
            "Préparer photos, déclaration du vendeur et, pour un condo ou un plex, le dossier (baux, PV, charges).",
            "Ajuster après deux à trois semaines sans trafic qualifié, plutôt que d'attendre six mois.",
        ],
        "buy": "Acheter à Sherbrooke, c'est choisir un quotidien (services, trajet, écoles) avant un prix affiché. L'inspection, le zonage en mixte, et les documents de copropriété pèsent plus qu'une visite émotionnelle.",
        "buy_steps": [
            "Obtenir une préautorisation et un budget total (mutation, notaire, inspection), pas seulement le prix Centris.",
            "Visiter le secteur le soir et un samedi, pas seulement en journée.",
            "Conditionner l'offre à l'inspection et, le cas échéant, à la lecture du dossier de copropriété.",
        ],
        "mistakes": [
            "Calquer un prix Lennoxville sur Fleurimont, ou un condo King sur un bungalow Rock Forest.",
            "Ignorer les charges d'un condo parce que le prix affiché est plus bas.",
            "Signer sans lire la déclaration du vendeur ni prévoir les droits de mutation.",
        ],
        "faqs": [
            ("Faut-il un courtier pour vendre à Sherbrooke ?", "Ce n'est pas obligatoire. Un courtier local connaît les prix par quartier, prépare le dossier et négocie les conditions. L'équipe Chiasson de Francesco travaille à Sherbrooke avec RE/MAX D'ABORD."),
            ("Quel quartier de Sherbrooke choisir pour une première maison ?", "Souvent Fleurimont ou Mont-Bellevue pour une unifamiliale, selon le budget. Lennoxville convient si le cadre village compte. Visitez plutôt que de choisir sur une moyenne de ville."),
            ("Combien de temps pour vendre à Sherbrooke ?", "Cela dépend du prix, de l'état et du secteur. Un bien juste peut recevoir des offres en quelques semaines. Un bien trop cher prend plus longtemps."),
            ("Qui sont les courtiers Chiasson de Francesco ?", "Pierre-Olivier Chiasson et Marco De Francesco (résidentiel et commercial) et Jade Sirois (résidentiel). Bureau : 157 boul. Jacques-Cartier Sud, Sherbrooke (QC) J1J 2Z4."),
        ],
    },
    {
        "slug": "magog",
        "name": "Magog",
        "prep": "à",
        "author": "marco",
        "desc": "Vendre ou acheter à Magog : lac Memphrémagog, condos, chalets. Quoi savoir selon l'équipe Chiasson de Francesco.",
        "tldr": "Pour vendre ou acheter à Magog, séparez d'abord trois produits : condo ou maison en ville, résidence hors lac, et bord du lac Memphrémagog. Ils n'ont pas le même prix, les mêmes règles riveraines, ni le même acheteur. L'équipe Chiasson de Francesco, courtiers RE/MAX D'ABORD à Sherbrooke, compare des ventes du même type, pas un « prix Magog » unique.",
        "market": "Magog combine un vrai centre-ville, l'accès au lac Memphrémagog et la proximité d'Orford. Les délais et les conditions n'ont rien à voir entre un condo en ville et un frontage.",
        "facts": [
            "Le centre convient à qui veut marcher vers les commerces.",
            "Le corridor du lac se négocie selon la vue, l'accès à l'eau et la bande riveraine.",
            "Une vue lac sans droits d'eau n'est pas un bord de lac.",
            "Orford est à côté : un chalet de montagne n'est pas un condo Magog.",
        ],
        "sell": "Vendre à Magog, c'est coller le prix aux ventes du même produit (lac vs ville) et viser la bonne saison sans surcoter « parce que c'est Magog ». Photos d'eau et de saison aident un bien lacustre. Un condo en ville se vend sur l'état, les charges et l'emplacement.",
        "sell_steps": [
            "Classer le bien : ville, hors lac, ou vrai accès à l'eau.",
            "Ancrer le prix sur des ventes Magog comparables, pas sur North Hatley ni Sherbrooke.",
            "Préparer titres, fosses ou égouts, et une description honnête du quai ou des droits.",
        ],
        "buy": "Acheter à Magog exige de vérifier titres, servitudes, installation septique ou égouts, et le règlement municipal avant d'offrir. Un chalet trois-saisons n'est pas une résidence principale tant que le bâtiment ne le permet pas.",
        "buy_steps": [
            "Faire préciser l'accès à l'eau (titres, quai, association) par écrit, pas à la visite.",
            "Inspecter bâtiment, fosse et, au besoin, inondabilité.",
            "Vérifier la location courte durée (ville et copropriété) si c'est votre plan.",
        ],
        "mistakes": [
            "Comparer un condo centre-ville à un chalet Orford.",
            "Offrir sur une « vue lac » comme s'il s'agissait d'un frontage.",
            "Oublier la fosse et les bandes riveraines dans le budget de rénovation.",
        ],
        "faqs": [
            ("Magog est-il plus cher que Sherbrooke ?", "Pour un bord de lac, souvent oui. Pour une unifamiliale hors lac, l'écart dépend de l'état et de la rue. On compare des ventes, pas deux noms de ville."),
            ("Peut-on habiter un chalet à Magog à l'année ?", "Oui si isolation, chauffage et services suivent. L'annonce « quatre-saisons » se vérifie à l'inspection."),
            ("L'équipe Chiasson de Francesco travaille-t-elle Magog ?", "Oui. Les courtiers sont basés à Sherbrooke et desservent Magog, Orford et le Memphrémagog. Les visites se font sur place."),
            ("Quand mettre en vente à Magog ?", "Le printemps attire souvent plus d'acheteurs villégiature. Un bien au bon prix se vend aussi hors saison."),
        ],
    },
    {
        "slug": "bromont",
        "name": "Bromont",
        "prep": "à",
        "author": "po",
        "desc": "Vendre ou acheter à Bromont : ski, village, condos. Guide local de l'équipe Chiasson de Francesco en Estrie.",
        "tldr": "Pour vendre ou acheter à Bromont, distinguez maison de village, lotissement hors pente et condo près des infrastructures sportives. Ce n'est pas un quartier de Sherbrooke. L'équipe Chiasson de Francesco accompagne ces dossiers depuis Sherbrooke, avec des comparables Bromont, pas Magog ni Sutton.",
        "market": "Bromont mélange skieurs, navetteurs vers la Rive-Sud et familles qui veulent le village. Un condo de pente et une unifamiliale en lotissement ne se comparent pas.",
        "facts": [
            "Le village structure commerces et résidence à l'année.",
            "Les secteurs ski et vélo attirent villégiature et parfois location, selon les règlements.",
            "Les charges de copropriété décident autant que la vue sur la montagne.",
            "Sutton et Lac-Brome sont d'autres marchés, même s'ils sont proches sur la carte.",
        ],
        "sell": "Vendre à Bromont, c'est parler le bon langage d'acheteur (principal vs week-end) et coller le prix aux ventes Bromont du même produit. Une surcote « station » sans comparables allonge l'affichage.",
        "sell_steps": [
            "Clarifier l'usage réel du bien (année, week-end, location).",
            "Rassembler le dossier de copropriété s'il y a lieu (règlements, location courte durée).",
            "Photographier village ou montagne selon ce qui vend vraiment le bien.",
        ],
        "buy": "Acheter à Bromont, c'est lire les frais de condo, les règles de location, l'accès hivernal et le drainage. Un chalet ski n'est pas une résidence à l'année tant que le bâtiment ne l'est pas.",
        "buy_steps": [
            "Lire copropriété et règlement municipal avant d'offrir pour un revenu locatif.",
            "Inspecter toiture, pente, drainage et chauffage.",
            "Comparer des ventes Bromont du même type, pas un prix Sutton ou Knowlton.",
        ],
        "mistakes": [
            "Acheter un condo « pour Airbnb » sans lire le syndicat.",
            "Coller un prix de pied-de-pente sur une maison de village.",
            "Sous-estimer les charges et le stationnement.",
        ],
        "faqs": [
            ("Bromont ou Sutton ?", "Deux stations, deux villages. Bromont a souvent plus de volume. Sutton a un village plus « Cantons ». Comparez le produit (condo vs maison), pas seulement le nom de la montagne."),
            ("Bromont convient-il comme résidence principale ?", "Oui pour une maison de village ou un lotissement hors pente, si le quotidien (trajet, services) vous convient. Un condo ski est un autre usage."),
            ("L'équipe se déplace-t-elle à Bromont ?", "Oui. Bromont, Sutton et Lac-Brome font partie du territoire ouest de l'équipe Chiasson de Francesco."),
            ("La location courte durée est-elle permise ?", "Selon l'immeuble et la ville. Plusieurs copropriétés l'encadrent ou l'interdisent. Vérifiez avant l'offre."),
        ],
    },
    {
        "slug": "orford",
        "name": "Orford",
        "prep": "à",
        "author": "marco",
        "desc": "Vendre ou acheter à Orford : mont, parc, chalets. Quoi savoir avec l'équipe Chiasson de Francesco.",
        "tldr": "Pour vendre ou acheter à Orford, le produit type est souvent chalet, maison près du mont ou du parc, rarement un condo de centre-ville. Magog est tout près, mais les comparables Orford ne sont pas ceux du Memphrémagog urbain. L'équipe Chiasson de Francesco, RE/MAX D'ABORD, traite Orford comme un marché montagne et nature.",
        "market": "Orford vit au pied du mont et du parc national. Villégiature, quatre-saisons et accès hivernal structurent la demande plus que les artères de Sherbrooke.",
        "facts": [
            "Un pied-de-pente n'est pas une maison de rang Eastman ou Austin.",
            "Fosses, puits et isolation décident si le bien est vraiment quatre-saisons.",
            "Le printemps aide souvent la villégiature, sans justifier n'importe quel prix.",
            "Eastman et Austin encadrent une partie des comparables ruraux.",
        ],
        "sell": "Vendre à Orford, c'est dire vraiment si le bâtiment est trois-saisons ou principal, et coller le prix aux ventes Orford, pas à un condo Magog.",
        "sell_steps": [
            "Décrire honnêtement chauffage, accès hivernal et services (fosse, puits).",
            "Photographier montagne et saison, sans promettre un lac qui n'existe pas.",
            "Ancrer le prix sur des ventes Orford du même type de bien.",
        ],
        "buy": "Acheter à Orford, c'est inspecter isolation, chauffage, fosse et chemin d'hiver avant d'offrir le « prix montagne ».",
        "buy_steps": [
            "Confirmer l'habitabilité à l'année à l'inspection, pas dans le titre d'annonce.",
            "Vérifier zonage et, le cas échéant, règles de location.",
            "Mesurer le trajet vers Magog ou Sherbrooke aux heures de pointe.",
        ],
        "mistakes": [
            "Payer un prix Magog lac pour un rang sans eau.",
            "Transformer un trois-saisons « avec un peu d'isolant » sans budget réel.",
            "Ignorer l'accès en février.",
        ],
        "faqs": [
            ("Orford ou Magog ?", "Magog a plus de services urbains et le lac. Orford est montagne et parc. Le choix dépend de l'usage quotidien, pas seulement du budget."),
            ("Peut-on habiter à Orford à l'année ?", "Oui si le bâtiment et l'accès le permettent. Beaucoup de chalets restent saisonniers."),
            ("L'équipe connaît-elle Orford ?", "Oui. Le corridor Magog-Orford-Eastman fait partie du territoire Chiasson de Francesco."),
            ("Quand vendre un chalet à Orford ?", "Fin d'hiver et printemps attirent souvent la villégiature. Un bien juste se vend aussi hors pic."),
        ],
    },
    {
        "slug": "north-hatley",
        "name": "North Hatley",
        "prep": "à",
        "author": "marco",
        "desc": "Vendre ou acheter à North Hatley : lac Massawippi, village. Quoi savoir, équipe Chiasson de Francesco.",
        "tldr": "Pour vendre ou acheter à North Hatley, l'offre est mince et le lac Massawippi attire villégiature et résidence secondaire. Le prix se justifie par des ventes du village ou des rives, pas par le prix médian de Sherbrooke. L'équipe Chiasson de Francesco travaille en français et en anglais (Marco De Francesco est bilingue).",
        "market": "North Hatley est un petit village lacustre, historiquement bilingue. Une maison sans lac dans le secteur n'est pas un « prix Massawippi ».",
        "facts": [
            "Le village n'est pas Hatley canton, ni Ayer's Cliff.",
            "Les rives et le noyau villageois n'ont pas le même budget.",
            "Les bâtiments sont souvent plus anciens : l'inspection pèse lourd.",
            "Sherbrooke est proche pour les services, pas pour les comparables.",
        ],
        "sell": "Vendre à North Hatley sans brader, c'est coller le prix aux ventes récentes du même type (bord de lac vs village) et laisser le temps au bon acheteur, souvent hors région.",
        "sell_steps": [
            "Séparer village et rive dans l'affichage et le prix.",
            "Préparer l'état du bâtiment (toiture, fosse, humidité).",
            "Prévoir une mise en marché bilingue si le bassin d'acheteurs l'exige.",
        ],
        "buy": "Acheter à North Hatley, c'est accepter un village plus petit, des déplacements vers Sherbrooke pour certains services, et parfois un bâtiment ancien. Bandes riveraines et fosses avant l'offre.",
        "buy_steps": [
            "Vérifier titres, droits d'eau et installation septique.",
            "Inspecter un bâtiment de caractère comme un chantier potentiel, pas comme une carte postale.",
            "Comparer rive par rive, pas avec Magog ou Knowlton.",
        ],
        "mistakes": [
            "Surcoter « parce que c'est North Hatley » sans ventes comparables.",
            "Confondre Hatley et North Hatley dans le prix.",
            "Négliger la fosse et la bande riveraine.",
        ],
        "faqs": [
            ("Pourquoi les maisons semblent-elles chères à North Hatley ?", "L'offre est faible et le lac attire une clientèle de villégiature. Le prix se justifie, ou non, par des ventes comparables du village ou des rives."),
            ("Faut-il parler anglais ?", "Utile. Le village est historiquement bilingue. L'équipe Chiasson de Francesco travaille en français et en anglais."),
            ("North Hatley convient-il comme résidence principale ?", "Oui si vous acceptez un village plus petit et des déplacements vers Sherbrooke. Ce n'est pas le quotidien d'un quartier de Fleurimont."),
            ("Ayer's Cliff, c'est le même marché ?", "Même lac, produits et budgets souvent différents. On compare village par village."),
        ],
    },
    {
        "slug": "coaticook",
        "name": "Coaticook",
        "prep": "à",
        "author": "jade",
        "desc": "Vendre ou acheter à Coaticook : ville de services, fermettes, gorge. Guide Chiasson de Francesco, Estrie.",
        "tldr": "Pour vendre ou acheter à Coaticook, distinguez maison en ville, fermette et bien près de la gorge. Coaticook est une ville de services en Estrie, pas un quartier de Sherbrooke. L'équipe Chiasson de Francesco compare des ventes Coaticook, pas Magog lac.",
        "market": "Coaticook a commerces, écoles et un cadre plus champêtre qu'en ville. Les fermettes se négocient selon l'acreage, les bâtiments et les installations septiques.",
        "facts": [
            "Le noyau urbain convient aux ménages qui veulent tout à proximité.",
            "Hors égouts, fosse et puits valent plus qu'une clause copiée.",
            "Une fermette rénovée peut dépasser un bungalow sherbrookois.",
            "Compton et Cookshire-Eaton encadrent une partie des comparables ruraux.",
        ],
        "sell": "Vendre à Coaticook, c'est éviter de calquer Sherbrooke ou Magog. Un bien près des services se vend souvent plus vite qu'une fermette trop chère par rapport aux acres comparables.",
        "sell_steps": [
            "Séparer ville et rural dans le prix et les photos.",
            "Décrire acreage et bâtiments sans marketing de « ferme de rêve ».",
            "Ancrer sur des ventes Coaticook et MRC, pas sur Fleurimont.",
        ],
        "buy": "Acheter à Coaticook, c'est inspecter, tester l'eau et la fosse hors réseau, et lire le zonage agricole si vous visez une terre.",
        "buy_steps": [
            "Filtrer Centris par vrai secteur (ville vs rang).",
            "Prévoir inspection de grange ou d'atelier s'il y a des dépendances.",
            "Vérifier zonage avant d'offrir sur une fermette.",
        ],
        "mistakes": [
            "Payer un prix Sherbrooke pour une maison Coaticook, ou l'inverse sans comparables.",
            "Oublier la fosse dans une offre rurale.",
            "Ignorer le type d'exploitation (loisir vs agricole).",
        ],
        "faqs": [
            ("Coaticook est-il moins cher que Sherbrooke ?", "Souvent pour une unifamiliale comparable, oui. L'écart dépend de l'état, du terrain et des services."),
            ("Faut-il un courtier pour une fermette ?", "Oui surtout : acreage, zonage et septique changent le prix. Un courtier Estrie évite une surcote sans comparables."),
            ("L'équipe se déplace-t-elle à Coaticook ?", "Oui. Les courtiers Chiasson de Francesco desservent Coaticook, Compton et Cookshire-Eaton."),
            ("Quand vendre à Coaticook ?", "Le printemps aide souvent les biens ruraux. Un bungalow en ville se vend toute l'année s'il est au bon prix."),
        ],
    },
    {
        "slug": "sutton",
        "name": "Sutton",
        "prep": "à",
        "author": "po",
        "desc": "Vendre ou acheter à Sutton : village, ski, condos. Quoi savoir avec Chiasson de Francesco.",
        "tldr": "Pour vendre ou acheter à Sutton, séparez village marchable, condo de montagne et maison de rang. Sutton n'est pas Bromont. L'équipe Chiasson de Francesco compare des ventes Sutton, pas Knowlton lac ni Sherbrooke.",
        "market": "Sutton mélange arts, ski et village des Cantons-de-l'Est. Les copropriétés de pente ont souvent des règles de location strictes.",
        "facts": [
            "Le village vise cafés, galeries et résidence ou week-end.",
            "Les secteurs ski visent villégiature : lisez le syndicat.",
            "Les rangs offrent plus de terrain et un autre type d'inspection.",
            "Acheteurs Montréal et Rive-Sud sont fréquents, sans garantir n'importe quel prix.",
        ],
        "sell": "Vendre à Sutton, c'est clarifier l'usage (principal vs week-end) et afficher un prix de montagne, pas de Sherbrooke.",
        "sell_steps": [
            "Joindre le dossier de copropriété (location, charges, travaux).",
            "Photographier village ou pentes selon le vrai produit.",
            "Ancrer sur des ventes Sutton du même type.",
        ],
        "buy": "Acheter à Sutton, c'est lire frais de condo, accès hivernal, pente et drainage. Un chalet ski n'est pas une résidence à l'année par défaut.",
        "buy_steps": [
            "Vérifier location courte durée dans la déclaration et à la municipalité.",
            "Inspecter toiture, chauffage et accès en hiver.",
            "Ne pas copier un prix Bromont ou Lac-Brome.",
        ],
        "mistakes": [
            "Acheter pour un revenu locatif interdit par l'immeuble.",
            "Comparer un condo ski à une maison de village Knowlton.",
            "Sous-estimer les charges.",
        ],
        "faqs": [
            ("Sutton ou Bromont ?", "Deux marchés. Bromont a souvent plus de volume. Sutton a un village plus artisanal. Comparez le produit, pas seulement la montagne."),
            ("Peut-on louer un condo à Sutton à court terme ?", "Selon la copropriété et la municipalité. Vérifiez avant d'acheter pour un revenu."),
            ("Sutton est-il plus cher que Magog ?", "Pour un condo ski, parfois. Pour une unifamiliale de village, cela dépend. Pas de règle unique."),
            ("Vous travaillez Sutton ?", "Oui. Bromont, Sutton et Lac-Brome font partie du territoire ouest de l'équipe."),
        ],
    },
    {
        "slug": "lac-brome",
        "name": "Lac-Brome",
        "prep": "à",
        "author": "marco",
        "desc": "Vendre ou acheter à Lac-Brome (Knowlton) : village, lac. Guide Chiasson de Francesco, Estrie.",
        "tldr": "Pour vendre ou acheter à Lac-Brome, Knowlton est le village, le lac Brome et les rangs sont d'autres produits. Le secteur est souvent bilingue. L'équipe Chiasson de Francesco (Marco De Francesco est bilingue) ancre le prix sur Knowlton et Brome, pas sur un condo de Bromont.",
        "market": "Lac-Brome attire une clientèle souvent bilingue, parfois montréalaise, sensible au village, aux lacs et au cachet. Ce n'est ni Sutton ski ni Sherbrooke urbain.",
        "facts": [
            "Knowlton est le cœur villageois de la ville de Lac-Brome.",
            "Le lac et les rues en retrait n'ont pas le même prix.",
            "Une mise en marché bilingue est souvent utile.",
            "Sutton et Bromont sont proches sur la carte, pas dans les comparables lacustres.",
        ],
        "sell": "Vendre à Lac-Brome, c'est viser Knowlton, rives ou rang avec le bon prix et, souvent, des documents et une annonce en deux langues.",
        "sell_steps": [
            "Préciser le secteur (village, rives, rang) dès l'affiche.",
            "Préparer photos du village ou du plan d'eau selon le bien.",
            "Ancrer sur des ventes Lac-Brome, pas Bromont ski.",
        ],
        "buy": "Acheter à Lac-Brome, c'est vérifier copropriété de village, fosses, et si le « bord de lac » est un vrai accès.",
        "buy_steps": [
            "Faire relire titres et droits d'eau.",
            "Inspecter les bâtiments de caractère.",
            "Comparer Knowlton à Knowlton, pas à Magog.",
        ],
        "mistakes": [
            "Dire Knowlton pour un rang sans préciser le secteur.",
            "Coller un prix Bromont condo sur une maison de village.",
            "Négliger la fosse hors réseau.",
        ],
        "faqs": [
            ("Knowlton et Lac-Brome, c'est la même chose ?", "Knowlton est le village au sein de la ville de Lac-Brome. Les comparables doivent préciser village, rives ou rang."),
            ("Faut-il un courtier bilingue ?", "Souvent utile. L'équipe Chiasson de Francesco travaille en français et en anglais."),
            ("Lac-Brome est-il plus cher que Sutton ?", "Selon le produit. Un bord de lac Knowlton n'égale pas un condo ski Sutton."),
            ("Vous déplacez-vous à Knowlton ?", "Oui, depuis Sherbrooke, pour visites, évaluations et inscriptions."),
        ],
    },
    {
        "slug": "lennoxville",
        "name": "Lennoxville",
        "prep": "à",
        "author": "jade",
        "desc": "Vendre ou acheter à Lennoxville (Sherbrooke) : village, plex, campus. Quoi savoir, Chiasson de Francesco.",
        "tldr": "Pour vendre ou acheter à Lennoxville, vous êtes dans un arrondissement de Sherbrooke qui se comporte encore comme un village universitaire. Les plex près du campus et les unifamiliales de rues calmes ne se comparent pas. L'équipe Chiasson de Francesco, basée à Sherbrooke, travaille aussi en anglais.",
        "market": "Lennoxville n'est pas Fleurimont. Bishop's, un centre marchable et un marché bilingue changent le type d'acheteurs et de locataires.",
        "facts": [
            "Le noyau (Queen, College, rues du campus) attire étudiants, profs et ménages qui veulent marcher.",
            "Les plex se jugent aux loyers réels et à l'état, pas à un rendement « universitaire » copié.",
            "Les bâtiments sont souvent plus anciens.",
            "Les Nations et Fleurimont sont d'autres grilles de prix.",
        ],
        "sell": "Vendre à Lennoxville, c'est miser sur le village et, pour un plex, un dossier locatif clair. Un prix « Sherbrooke moyen » ne tient pas.",
        "sell_steps": [
            "Préparer baux et photos des logements s'il s'agit d'un plex.",
            "Photographier le cadre village, pas seulement l'intérieur.",
            "Comparer des ventes Lennoxville, pas Mont-Bellevue.",
        ],
        "buy": "Acheter à Lennoxville, c'est inspecter du vieux bâti, vérifier le stationnement et le zonage mixte, et lire les baux d'un plex avant l'émotion.",
        "buy_steps": [
            "Visiter hors période étudiante et en session, si le locatif compte.",
            "Inspecter toiture, fondations, électricité.",
            "Ne pas appliquer un rendement théorique de centre-ville.",
        ],
        "mistakes": [
            "Payer un plex comme une maison unifamiliale voisine.",
            "Ignorer le stationnement et le bruit de rue près du campus.",
            "Comparer à Fleurimont sans ajuster le produit.",
        ],
        "faqs": [
            ("Lennoxville fait-il partie de Sherbrooke ?", "Oui, c'est un arrondissement. Le quotidien reste celui d'un village : commerces de proximité et campus."),
            ("Bon secteur pour un plex ?", "Près du campus, la demande locative étudiante existe. Les immeubles sont souvent plus vieux. Loyers et rénos d'abord."),
            ("Faut-il parler anglais ?", "Utile. Lennoxville est historiquement bilingue. L'équipe travaille en français et en anglais."),
            ("Moins cher que le centre-ville ?", "Parfois pour une unifamiliale, pas toujours pour un plex rénové."),
        ],
    },
    {
        "slug": "fleurimont",
        "name": "Fleurimont",
        "prep": "à",
        "author": "jade",
        "desc": "Vendre ou acheter à Fleurimont (Sherbrooke) : bungalows, familles, CHUS. Guide Chiasson de Francesco.",
        "tldr": "Pour vendre ou acheter à Fleurimont, le stock dominant est l'unifamiliale : bungalows, rues calmes, proximité du CHUS. Ce n'est pas Lennoxville ni Les Nations condos. L'équipe Chiasson de Francesco ancre le prix sur la même poche de rues, pas sur toute la ville de Sherbrooke.",
        "market": "Fleurimont est souvent le réflexe des familles qui veulent une unifamiliale à Sherbrooke sans payer un village lacustre.",
        "facts": [
            "Beaucoup de rues de bungalows et de cottages, écoles de proximité, accès 410.",
            "L'hôpital (CHUS Fleurimont) intéresse certains acheteurs, sans bonus automatique de prix.",
            "Les micro-secteurs n'ont pas tous le même âge de bâtiment.",
            "Rock Forest est plus à l'ouest, souvent avec plus de terrain.",
        ],
        "sell": "Vendre à Fleurimont, c'est coller le prix aux ventes récentes du même type de bungalow. Le volume est plus élevé qu'à North Hatley : un prix trop haut se voit tout de suite.",
        "sell_steps": [
            "Comparer la même poche de rues, pas « Fleurimont » trop large.",
            "Préparer photos, déclaration et un état honnête (toiture, fondations années 60-80).",
            "Ajuster vite s'il n'y a pas de visites qualifiées.",
        ],
        "buy": "Acheter à Fleurimont, c'est inspecter (toitures, fondations) et visiter le soir. Un premier achat y est fréquent, sans sauter l'inspection.",
        "buy_steps": [
            "Préautorisation et budget de clôture (mutation, notaire).",
            "Visiter à l'heure de pointe si vous navettez.",
            "Conditionner à l'inspection.",
        ],
        "mistakes": [
            "Afficher un prix de rue voisine plus chère sans ventes closes.",
            "Négliger l'inspection sur un « bungalow correct ».",
            "Choisir Fleurimont ou Rock Forest seulement sur le prix au pied carré.",
        ],
        "faqs": [
            ("Fleurimont est-il bon pour une première maison ?", "Souvent oui : plus d'unifamiliales et de services. Visitez le soir et un samedi. L'inspection reste non négociable."),
            ("Proche de l'hôpital, ça change le prix ?", "Cela intéresse certains acheteurs. Ce n'est pas un bonus automatique. Les ventes de la rue tranchent."),
            ("Fleurimont ou Rock Forest ?", "Fleurimont est plus ville et services. Rock Forest a souvent plus de terrain. Le trajet quotidien décide autant que le prix."),
            ("Vous vendez à Fleurimont ?", "Oui. C'est le quotidien de l'équipe Chiasson de Francesco, basée à Sherbrooke."),
        ],
    },
    {
        "slug": "les-nations",
        "name": "Les Nations",
        "prep": "aux",
        "author": "po",
        "desc": "Vendre ou acheter aux Nations (Sherbrooke) : condos, plex, centre. Quoi savoir, Chiasson de Francesco.",
        "tldr": "Pour vendre ou acheter aux Nations, à Sherbrooke, vous êtes dans le cœur dense : condos, plex, King, Wellington. Les charges et le fonds de prévoyance décident autant que la vue sur la rivière. L'équipe Chiasson de Francesco y inscrit aussi du commercial (locaux, bâtisses).",
        "market": "Les Nations, ce n'est pas Fleurimont. Un penthouse n'est pas un 4½ des années 70. Stationnement, bruit de rue et règlements de copropriété se lisent avant l'offre.",
        "facts": [
            "Plus de condos et de plex qu'à Mont-Bellevue.",
            "Le dossier de copropriété (PV, fonds, charges) est non négociable à l'achat.",
            "Un plex se juge aux baux et à l'état, pas au prix au pied d'une unifamiliale.",
            "Pierre-Olivier Chiasson et Marco De Francesco traitent aussi le commercial sur ces artères.",
        ],
        "sell": "Vendre aux Nations, c'est préparer le dossier (charges, fonds, stationnement) avant l'affiche. Un prix calqué sur « le centre a monté » sans ventes comparables allonge l'affichage.",
        "sell_steps": [
            "Rassembler déclaration, états financiers, PV et règlement.",
            "Photographier stationnement, rangement et parties communes s'ils aident.",
            "Comparer le même type d'immeuble, pas tout le centre.",
        ],
        "buy": "Acheter aux Nations, c'est lire le fonds de prévoyance avant la cuisine. Une cotisation spéciale à venir n'est pas une aubaine.",
        "buy_steps": [
            "Exiger le dossier complet dans les conditions de l'offre.",
            "Inspecter l'unité et poser des questions sur l'immeuble (toiture, stationnement).",
            "Pour un plex : baux, loyers réels, tous les logements.",
        ],
        "mistakes": [
            "Ignorer les charges parce que le prix est 20 000 $ plus bas.",
            "Comparer un condo neuf à un plex non rénové.",
            "Planifier de la location courte durée sans lire le règlement.",
        ],
        "faqs": [
            ("Les Nations, c'est le centre-ville ?", "C'est l'arrondissement qui englobe le centre et plusieurs quartiers denses. « Centre-ville » dans une annonce peut vouloir dire trois rues différentes."),
            ("Bon pour un premier condo ?", "Oui si vous lisez charges et fonds. Un prix bas avec des cotisations qui s'en viennent n'est pas une aubaine."),
            ("Vous avez des inscriptions aux Nations ?", "Selon le moment, oui, dont des adresses King et Wellington. Voyez la page propriétés."),
            ("Plex ou condo ?", "Le plex, vous gérez l'immeuble. Le condo, vous payez des charges et un syndicat. L'équipe fait les deux lectures."),
        ],
    },
    {
        "slug": "rock-forest",
        "name": "Rock Forest",
        "prep": "à",
        "author": "marco",
        "desc": "Vendre ou acheter à Rock Forest (Sherbrooke) : terrain, axe Magog. Guide Chiasson de Francesco.",
        "tldr": "Pour vendre ou acheter à Rock Forest, vous êtes dans l'ouest de Sherbrooke : souvent plus de terrain qu'aux Nations, un pied vers Magog, et des services qui varient (égouts vs fosse selon le secteur). L'équipe Chiasson de Francesco compare des micro-secteurs, pas un prix « Rock Forest » unique.",
        "market": "Rock Forest–Saint-Élie–Deauville est un arrondissement. Saint-Élie n'est pas la même poche que les rues près de la 112. Deauville, côté Magog, se discute à part.",
        "facts": [
            "Beaucoup d'acheteurs y voient un compromis ville et espace.",
            "Le type de lot et le drainage changent d'une rue à l'autre.",
            "Le trajet vers Magog ou le centre de Sherbrooke se mesure en heure de pointe.",
            "Fleurimont reste plus « services urbains ».",
        ],
        "sell": "Vendre à Rock Forest, c'est montrer le terrain et coller le prix au micro-secteur, ni Magog lac ni condo Les Nations.",
        "sell_steps": [
            "Préciser services (égouts, fosse) dans la description.",
            "Photographier le lot en saison.",
            "Ancrer sur des ventes de la même poche.",
        ],
        "buy": "Acheter à Rock Forest, c'est vérifier lot, drainage, fosse le cas échéant, et le temps réel vers le travail.",
        "buy_steps": [
            "Inspecter les bâtiments des années 70-90 avec attention (toiture, fondations).",
            "Rouler le trajet aux heures de pointe.",
            "Ne pas payer un prix Magog pour un lot sherbrookois hors lac.",
        ],
        "mistakes": [
            "Mélanger Saint-Élie, Rock Forest et Deauville dans un seul comparable.",
            "Oublier la fosse hors réseau.",
            "Choisir seulement parce que « c'est plus proche de Magog » sans visiter l'hiver.",
        ],
        "faqs": [
            ("Rock Forest, c'est encore Sherbrooke ?", "Oui, arrondissement de Sherbrooke. Le quotidien est plus dispersé que le centre-ville : l'auto est presque indispensable."),
            ("Moins cher que Fleurimont ?", "Parfois, surtout avec plus de terrain. Un cottage rénové peut dépasser un bungalow fleurimontois."),
            ("Proche de Magog ?", "Oui, c'est souvent le point. Mesurez le trajet aux heures de pointe."),
            ("Desservez-vous Saint-Élie ?", "Oui. L'arrondissement entier fait partie du territoire de l'équipe."),
        ],
    },
    {
        "slug": "eastman",
        "name": "Eastman",
        "prep": "à",
        "author": "marco",
        "desc": "Vendre ou acheter à Eastman : village, Orford, Magog. Quoi savoir, équipe Chiasson de Francesco.",
        "tldr": "Pour vendre ou acheter à Eastman, vous êtes entre Magog et le mont Orford : plus village et terrain qu'un condo Magog, moins « pied-de-pente » qu'Orford station. L'équipe Chiasson de Francesco compare Eastman et Orford rural, pas Magog lac.",
        "market": "Eastman vit dans l'orbite d'Orford et de Magog sans en être le centre-ville. Spa, village, accès montagne : les acheteurs paient le cadre.",
        "facts": [
            "Le village est compact ; autour, plus de terrain.",
            "Quatre-saisons vs saisonnier se vérifie au bâtiment, pas au marketing.",
            "Austin et Orford encadrent une partie des comparables.",
            "Ce n'est ni un condo Magog ni un ski-in Sutton.",
        ],
        "sell": "Vendre à Eastman, c'est miser sur le cadre de vie et des photos de saison. Un prix calqué sur Magog bord de lac se brade ensuite.",
        "sell_steps": [
            "Décrire honnêtement fosse, accès et saisonnalité.",
            "Photographier village et nature, pas un lac inexistant.",
            "Ancrer sur des ventes Eastman et Orford comparables.",
        ],
        "buy": "Acheter à Eastman, c'est vérifier quatre-saisons, fosses, et la distance réelle de Magog. Un « près d'Orford » n'égale pas un accès ski.",
        "buy_steps": [
            "Inspecter avant l'offre.",
            "Mesurer le trajet Magog et Sherbrooke.",
            "Lire le zonage si vous visez un projet ou de la location.",
        ],
        "mistakes": [
            "Payer Magog lac pour Eastman village.",
            "Croire qu'Eastman et Magog sont le même marché de services.",
            "Oublier l'accès hivernal.",
        ],
        "faqs": [
            ("Eastman ou Magog : où acheter ?", "Magog a plus de services et de condos. Eastman est plus village et nature, souvent avec plus de terrain."),
            ("Eastman est-il un marché de chalets ?", "Il y a de la villégiature, mais aussi des résidences principales. Distinguez les deux dans le prix."),
            ("L'équipe connaît-elle Eastman ?", "Oui. Le corridor Magog-Orford-Eastman fait partie du territoire Chiasson de Francesco."),
            ("Quand mettre en vente ?", "Fin d'hiver et printemps attirent souvent villégiature et montagne. Un bien au bon prix se vend aussi hors pic."),
        ],
    },
    {
        "slug": "windsor",
        "name": "Windsor",
        "prep": "à",
        "author": "jade",
        "desc": "Vendre ou acheter à Windsor (Estrie) : Saint-François, navette Sherbrooke. Guide Chiasson de Francesco.",
        "tldr": "Pour vendre ou acheter à Windsor, vous êtes dans une petite ville de la Saint-François, plus proche de Sherbrooke que Richmond. Le « 15 minutes de Sherbrooke » n'excuse pas un prix des Nations. L'équipe Chiasson de Francesco ancre le prix sur Windsor.",
        "market": "Windsor a un caractère de ville industrielle de vallée. Des acheteurs y voient un budget plus sage qu'à Fleurimont, sans être Magog.",
        "facts": [
            "Quartiers résidentiels, quelques plex, identité papetière.",
            "Richmond et Sherbrooke (Brompton) encadrent les comparables.",
            "Un plex se juge aux loyers locaux, pas à un rendement sherbrookois copié.",
            "Le trajet vers Sherbrooke se mesure aux heures de pointe.",
        ],
        "sell": "Vendre à Windsor, c'est un prix de Windsor et un affichage clair. La proximité de Sherbrooke aide le bassin, pas la surcote.",
        "sell_steps": [
            "Comparer des ventes Windsor d'abord.",
            "Préparer photos et déclaration.",
            "Pour un plex : dossier locatif réel.",
        ],
        "buy": "Acheter à Windsor, c'est inspecter (bâtiments souvent plus anciens) et valider le navettage. Un « deal » n'en est un que si l'état suit.",
        "buy_steps": [
            "Rouler le trajet vers Sherbrooke aux heures de pointe.",
            "Inspecter toiture, fondations, électricité.",
            "Pour un plex, lire les baux avant le prix au pied.",
        ],
        "mistakes": [
            "Afficher un prix Fleurimont parce que « c'est presque Sherbrooke ».",
            "Sous-estimer l'état d'un bâtiment plus ancien.",
            "Copier un rendement de plex des Nations.",
        ],
        "faqs": [
            ("Windsor est-il plus abordable que Sherbrooke ?", "Souvent pour une unifamiliale comparable, oui. L'écart dépend du quartier sherbrookois vis-à-vis et de l'état du bâtiment."),
            ("Bon pour navetter vers Sherbrooke ?", "Beaucoup le font. Mesurez votre trajet aux heures de pointe, pas seulement la distance GPS."),
            ("Plex à Windsor ?", "Oui, marché locatif plus petit. Chiffres réels des loyers avant le rêve du rendement."),
            ("Vous vendez à Windsor ?", "Oui. Vallée de la Saint-François : Windsor, Richmond, et Sherbrooke Brompton selon le mandat."),
        ],
    },
    {
        "slug": "stanstead",
        "name": "Stanstead",
        "prep": "à",
        "author": "marco",
        "desc": "Vendre ou acheter à Stanstead : frontière, Memphrémagog, patrimoine. Guide Chiasson de Francesco.",
        "tldr": "Pour vendre ou acheter à Stanstead, le caractère frontalier (Rock Island, Beebe) et le patrimoine changent le bassin d'acheteurs, souvent bilingue. Ce n'est pas Magog centre. L'équipe Chiasson de Francesco (Marco De Francesco est bilingue) compare Stanstead et le Memphrémagog sud.",
        "market": "Stanstead vit la frontière au quotidien. Une maison de village n'a pas la valeur d'un bord de lac. Le droit applicable reste le Québec pour un immeuble au Québec.",
        "facts": [
            "Rues anciennes, bâtiments de caractère.",
            "Proximité de Derby Line ; le Haskell Free Library illustre le lieu, sans ajouter automatiquement 100 000 $ à une maison.",
            "Mise en marché bilingue souvent utile.",
            "Orbite sud du lac Memphrémagog, distincte de Magog.",
        ],
        "sell": "Vendre à Stanstead, c'est une annonce claire (village vs lac) et des comparables locaux, pas Knowlton ou Bromont ski.",
        "sell_steps": [
            "Préparer une mise en marché bilingue si le bassin l'exige.",
            "Photographier le cachet sans cacher l'état du bâtiment.",
            "Ancrer sur Stanstead et Memphrémagog sud.",
        ],
        "buy": "Acheter à Stanstead, c'est inspecter du bâti ancien et clarifier que l'immeuble est au Québec. Un acheteur américain n'achète pas comme un acheteur de Sherbrooke.",
        "buy_steps": [
            "Inspection de bâtiments anciens (fondations, toiture, électricité).",
            "Titres clairs, côté Québec.",
            "Ne pas payer un prix Magog centre pour un village frontalier.",
        ],
        "mistakes": [
            "Croire que la frontière augmente automatiquement le prix.",
            "Comparer à Knowlton ou Bromont.",
            "Négliger l'inspection du patrimoine bâti.",
        ],
        "faqs": [
            ("Stanstead est-il un marché bilingue ?", "Oui, historiquement. Un courtier bilingue aide. L'équipe travaille FR/EN."),
            ("Être à la frontière change-t-il une vente ?", "Cela change le bassin d'acheteurs. Le droit applicable reste le Québec pour un immeuble au Québec."),
            ("Proche du lac Memphrémagog ?", "Oui, orbite sud du lac, sans être Magog. Les bords de lac se négocient à part des maisons de village."),
            ("Vous allez à Stanstead ?", "Oui, pour visites et mandats dans le secteur Memphrémagog sud."),
        ],
    },
    {
        "slug": "cookshire-eaton",
        "name": "Cookshire-Eaton",
        "prep": "à",
        "author": "po",
        "desc": "Vendre ou acheter à Cookshire-Eaton : terrains, Sawyerville, route 108. Guide Chiasson de Francesco.",
        "tldr": "Pour vendre ou acheter à Cookshire-Eaton, séparez terrain et maison. Un prix à l'acre n'est pas un prix au pied carré habitable. L'équipe Chiasson de Francesco inscrit aussi des terrains dans ce secteur, notamment le long de la route 108.",
        "market": "Cookshire concentre commerces et services. Sawyerville et les rangs attirent qui veut du terrain. La 108 structure beaucoup de déplacements vers Sherbrooke.",
        "facts": [
            "Cookshire et Sawyerville sont la même municipalité, pas le même produit.",
            "Un terrain se juge au zonage, au drainage et au coût de viabilisation.",
            "Une maison de village se juge à l'état du bâtiment d'abord.",
            "Environ une vingtaine de minutes de Sherbrooke selon le secteur.",
        ],
        "sell": "Vendre à Cookshire-Eaton, c'est ne pas vendre un terrain au prix d'une maison, ni l'inverse. Un lot trop cher par rapport aux acres vendus reste en inventaire.",
        "sell_steps": [
            "Classer le mandat : lot ou bâti.",
            "Documenter zonage et accès.",
            "Ancrer sur des ventes du bon noyau (Cookshire vs Sawyerville vs rang).",
        ],
        "buy": "Acheter un terrain ici, c'est chiffrer puits, fosse, entrée et électricité avant l'offre. Acheter une maison, c'est l'état d'abord, pas seulement le lot.",
        "buy_steps": [
            "Demander le zonage et un certificat d'urbanisme avant une offre ferme sur un lot.",
            "Chiffrer la viabilisation avec des entrepreneurs, pas avec un espoir.",
            "Inspecter toute maison existante comme en ville.",
        ],
        "mistakes": [
            "Payer un prix à l'acre copié sur le voisin sans contraintes identiques.",
            "Mélanger Sawyerville et Cookshire dans les comparables.",
            "Oublier le coût réel d'un chemin et d'une fosse.",
        ],
        "faqs": [
            ("Y a-t-il des terrains à vendre à Cookshire-Eaton ?", "Oui, le secteur voit régulièrement des lots, y compris le long de la route 108. Chaque lot a ses contraintes. Un courtier les lit avant l'offre."),
            ("Cookshire-Eaton, c'est loin de Sherbrooke ?", "Environ une vingtaine de minutes selon le secteur. Beaucoup d'acheteurs y voient un compromis prix et espace versus la ville."),
            ("Sawyerville et Cookshire, même marché ?", "Même municipalité, produits différents. Les comparables doivent rester dans le bon noyau."),
            ("L'équipe inscrit-elle des terrains ?", "Oui. L'équipe Chiasson de Francesco gère maisons et terrains dans le Haut-Saint-François."),
        ],
    },
    {
        "slug": "ayers-cliff",
        "name": "Ayer's Cliff",
        "prep": "à",
        "author": "marco",
        "desc": "Vendre ou acheter à Ayer's Cliff : lac Massawippi. Quoi savoir, Chiasson de Francesco.",
        "tldr": "Pour vendre ou acheter à Ayer's Cliff, vous partagez le lac Massawippi avec North Hatley sans le même cachet village ni les mêmes prix. Calquer un prix Hatley ici, ou l'inverse, est une erreur fréquente. L'équipe Chiasson de Francesco compare rive par rive.",
        "market": "Ayer's Cliff est un village compact, souvent plus villégiature, bilingue. Une maison sans lac n'est pas un prix de rive.",
        "facts": [
            "Le village et les rives n'ont pas le même budget.",
            "Fosses, bandes riveraines et saisonnalité avant l'offre.",
            "North Hatley, Hatley canton et Ayer's Cliff sont trois grilles.",
            "Marco De Francesco travaille en anglais, utile ici.",
        ],
        "sell": "Vendre à Ayer's Cliff, c'est des photos d'eau et de saison, et des comparables Ayer's Cliff, pas Knowlton ni Memphrémagog Magog.",
        "sell_steps": [
            "Préciser village vs rive vs rang.",
            "Décrire honnêtement quatre-saisons vs chalet.",
            "Ancrer sur le Massawippi sud.",
        ],
        "buy": "Acheter à Ayer's Cliff, c'est titres, bandes riveraines, fosse, et une inspection qui tranche la saisonnalité.",
        "buy_steps": [
            "Vérifier l'accès à l'eau par les titres.",
            "Inspecter isolation et chauffage si vous visez l'année.",
            "Ne pas copier un prix North Hatley village.",
        ],
        "mistakes": [
            "Mélanger Ayer's Cliff et North Hatley dans un seul prix.",
            "Offrir sur une vue comme sur un frontage.",
            "Oublier la fosse.",
        ],
        "faqs": [
            ("Ayer's Cliff est-il moins cher que North Hatley ?", "Souvent pour un bien comparable, le village Hatley se paie plus cher. Une vraie rive bien située à Ayer's Cliff reste un produit rare."),
            ("Résidence principale ou chalet ?", "Les deux existent. Isolation, chauffage et accès hivernal tranchent."),
            ("Secteur bilingue ?", "Oui. L'équipe travaille en français et en anglais."),
            ("Vous allez à Ayer's Cliff ?", "Oui, avec North Hatley et le Massawippi."),
        ],
    },
    {
        "slug": "austin",
        "name": "Austin",
        "prep": "à",
        "author": "marco",
        "desc": "Vendre ou acheter à Austin : près d'Orford et Magog. Guide Chiasson de Francesco.",
        "tldr": "Pour vendre ou acheter à Austin, vous êtes entre Magog, Eastman et Orford : plus champêtre que Magog centre, moins de volume. Un prix Magog condo ne s'applique pas. L'équipe Chiasson de Francesco compare Austin et Orford rural.",
        "market": "Austin a peu d'inscriptions, beaucoup de villégiature et de résidences avec terrain. L'accès au lac n'est pas automatique parce que « Austin » est dans l'annonce.",
        "facts": [
            "Rangs, chalets, quelques maisons de village.",
            "Eastman a un village plus « destination » ; Austin est souvent plus dispersé.",
            "Fosses, puits, accès hivernal, zonage.",
            "Un condo Orford et une maison Austin ne se comparent pas.",
        ],
        "sell": "Vendre à Austin, c'est des photos de saison et de l'honnêteté sur l'eau et les services. Prix Austin, pas Georgeville frontage.",
        "sell_steps": [
            "Décrire services et saisonnalité.",
            "Ne pas vendre un accès lac inexistant.",
            "Ancrer sur Austin et Orford rural.",
        ],
        "buy": "Acheter à Austin, c'est inspecter un trois-saisons avant d'en faire une résidence principale, et vérifier zonage et fosse.",
        "buy_steps": [
            "Inspection avant l'offre.",
            "Confirmer l'accès hivernal.",
            "Mesurer Magog et le ski : orbite, pas pied des pistes.",
        ],
        "mistakes": [
            "Payer Magog lac pour Austin rang.",
            "Croire qu'Austin égale Eastman village.",
            "Oublier puits et fosse au budget.",
        ],
        "faqs": [
            ("Austin ou Eastman ?", "Deux municipalités proches, deux stocks. Visitez plutôt que de choisir sur le nom."),
            ("Peut-on habiter à l'année ?", "Oui si le bâtiment et l'accès le permettent. Beaucoup de chalets restent saisonniers."),
            ("Proche du ski Orford ?", "Dans l'orbite, pas au pied des pistes."),
            ("Desservez-vous Austin ?", "Oui. Corridor Magog-Orford-Eastman-Austin."),
        ],
    },
    {
        "slug": "richmond",
        "name": "Richmond",
        "prep": "à",
        "author": "jade",
        "desc": "Vendre ou acheter à Richmond : Saint-François, Estrie. Quoi savoir, Chiasson de Francesco.",
        "tldr": "Pour vendre ou acheter à Richmond, vous êtes dans une petite ville de vallée, plus industrielle que villégiature. Les prix suivent Windsor et les Sources plus que Magog. L'équipe Chiasson de Francesco n'affiche pas un prix « 20 minutes de Sherbrooke » sans comparables Richmond.",
        "market": "Le centre et les rues résidentielles dominent. La rivière donne du cadre à certains lots, sans en faire un marché lac.",
        "facts": [
            "Bâtiments parfois plus anciens : l'inspection est importante.",
            "Un plex se juge aux loyers réels de Richmond.",
            "Windsor, Danville et Val-des-Sources élargissent un peu les comparables.",
            "Ce n'est pas Fleurimont ni Magog.",
        ],
        "sell": "Vendre à Richmond, c'est le prix du marché local. La visibilité Estrie aide ; une surcote sherbrookoise allonge l'affichage.",
        "sell_steps": [
            "Ancrer sur des ventes Richmond et Windsor.",
            "Photos claires, déclaration complète.",
            "Pour un plex : baux et état.",
        ],
        "buy": "Acheter à Richmond, c'est un possible compromis de budget vers Sherbrooke, si vous acceptez une petite ville de vallée. Inspectez.",
        "buy_steps": [
            "Visiter à différentes heures.",
            "Inspection (bâti ancien).",
            "Mesurer le trajet Sherbrooke aux heures de pointe.",
        ],
        "mistakes": [
            "Calquer Fleurimont sur Richmond.",
            "Rêver un rendement de plex universitaire.",
            "Ignorer l'état pour le prix affiché.",
        ],
        "faqs": [
            ("Richmond est-il un bon compromis vers Sherbrooke ?", "Pour certains budgets, oui. Le quotidien n'est pas celui du centre-ville de Sherbrooke."),
            ("Y a-t-il des plex à Richmond ?", "Oui, à petite échelle. La demande locative est locale."),
            ("Desservez-vous Richmond ?", "Oui. L'équipe couvre Richmond, Windsor et la vallée de la Saint-François."),
            ("Commercial à Richmond ?", "À l'échelle de la ville. Discutez d'un mandat avec Pierre-Olivier ou Marco."),
        ],
    },
    {
        "slug": "compton",
        "name": "Compton",
        "prep": "à",
        "author": "po",
        "desc": "Vendre ou acheter à Compton : village, rangs, fermettes. Guide Chiasson de Francesco, Estrie.",
        "tldr": "Pour vendre ou acheter à Compton, le marché est rural : peu d'inscriptions, beaucoup de terre ou de dépendances. Un prix « parce qu'on est près de Sherbrooke » ne tient pas si le bâtiment ou le puits ne suit pas. L'équipe Chiasson de Francesco compare Compton et Coaticook, pas Magog lac.",
        "market": "Le village offre un ancrage communautaire. Les rangs se distinguent par la superficie, l'accès hivernal et le type d'exploitation.",
        "facts": [
            "Ce n'est pas le marché de Lennoxville.",
            "Zonage, septique et, le cas échéant, contraintes agricoles.",
            "Inspection de grange ou d'atelier n'est pas du luxe.",
            "Waterville et Coaticook encadrent une partie des comparables.",
        ],
        "sell": "Vendre à Compton, c'est photos de saison, acreage honnête, prix collé aux ventes closes. Trop d'attentes calquées sur Sherbrooke allongent la mise en marché.",
        "sell_steps": [
            "Décrire acres et bâtiments sans enjoliver.",
            "Ancrer sur Compton et Coaticook rural.",
            "Afficher régionalement pour trouver le bon acheteur.",
        ],
        "buy": "Acheter à Compton, c'est titres, zonage, fosse, puits, et une lecture agricole si la terre l'exige.",
        "buy_steps": [
            "Vérifier ce que le zonage permet vraiment.",
            "Inspecter maison et dépendances.",
            "Ne pas payer un prix Magog pour un rang.",
        ],
        "mistakes": [
            "Surcoter la proximité de Sherbrooke sans comparables.",
            "Oublier la fosse et le puits.",
            "Ignorer le statut agricole.",
        ],
        "faqs": [
            ("Compton convient-il comme résidence principale ?", "Oui si vous acceptez moins de services qu'en ville et parfois un déplacement vers Sherbrooke ou Coaticook."),
            ("Peut-on acheter une terre agricole ?", "Selon le zonage et votre statut. Un courtier et un notaire évitent une offre sur un lot que vous ne pourrez pas utiliser comme prévu."),
            ("Pourquoi si peu de maisons à vendre ?", "Marché mince. Quand une inscription sort, le prix doit coller aux rares comparables."),
            ("Travaillez-vous Compton depuis Sherbrooke ?", "Oui. L'équipe dessert Compton et le Haut-Saint-François."),
        ],
    },
    {
        "slug": "waterville",
        "name": "Waterville",
        "prep": "à",
        "author": "jade",
        "desc": "Vendre ou acheter à Waterville : entre Sherbrooke et Coaticook. Guide Chiasson de Francesco.",
        "tldr": "Pour vendre ou acheter à Waterville, vous êtes dans un petit marché de village entre Sherbrooke, Compton et Coaticook. Un prix « 15 minutes de Sherbrooke » sans comparables Waterville ne tient pas. L'équipe Chiasson de Francesco ancre sur Waterville et Compton village.",
        "market": "Moins d'inscriptions que Sherbrooke, plus de services que Compton rang. L'axe vers Coaticook et Lennoxville structure les déplacements.",
        "facts": [
            "Noyau villageois et rues résidentielles.",
            "Fosses hors réseau selon l'adresse.",
            "Ce n'est ni le campus Lennoxville ni Fleurimont.",
            "Marché mince : le premier prix compte.",
        ],
        "sell": "Vendre à Waterville, c'est un prix d'entrée juste dès le jour 1. Photos honnêtes, affichage Estrie.",
        "sell_steps": [
            "Comparer Waterville et Compton village.",
            "Décrire services (égouts vs fosse).",
            "Ne pas calquer Fleurimont.",
        ],
        "buy": "Acheter à Waterville, c'est inspecter, vérifier la fosse le cas échéant, et valider le trajet vers Sherbrooke aux heures de pointe.",
        "buy_steps": [
            "Inspection et tests hors réseau si besoin.",
            "Rouler le trajet aux heures de pointe.",
            "Visiter comme un village, pas comme un quartier sherbrookois.",
        ],
        "mistakes": [
            "Payer un prix Lennoxville pour Waterville.",
            "Oublier la fosse.",
            "Choisir seulement sur le GPS.",
        ],
        "faqs": [
            ("Waterville est-il moins cher que Sherbrooke ?", "Souvent pour une unifamiliale, avec moins de services urbains. L'écart dépend de l'état et du lot."),
            ("Bon compromis vers Coaticook ?", "Oui pour qui a des attaches vers le Haut-Saint-François, tout en restant plus près de Sherbrooke que Coaticook centre."),
            ("Beaucoup de maisons à vendre ?", "Peu. Une inscription doit être au bon prix dès le jour 1."),
            ("Vous allez à Waterville ?", "Oui, avec Compton, Coaticook et Lennoxville."),
        ],
    },
    {
        "slug": "hatley",
        "name": "Hatley",
        "prep": "à",
        "author": "marco",
        "desc": "Vendre ou acheter à Hatley : canton, Massawippi, pas North Hatley. Guide Chiasson de Francesco.",
        "tldr": "Pour vendre ou acheter à Hatley, ne confondez pas avec North Hatley. Hatley est plus rural : plus de terrain, moins de vitrine touristique. L'équipe Chiasson de Francesco ne mélange pas les comparables village lacustre et canton.",
        "market": "Hatley (le canton) n'est pas le village de North Hatley. Confondre les deux dans un prix d'affichage est une erreur classique.",
        "facts": [
            "North Hatley = village lacustre serré. Hatley = plus rural.",
            "Zonage, fosses, acreage, accès hivernal.",
            "Un lot « vue lac » sans droits d'eau se paie autrement.",
            "Secteur historiquement bilingue.",
        ],
        "sell": "Vendre à Hatley, c'est ne pas afficher un prix North Hatley village. Photos de saison et acreage honnête.",
        "sell_steps": [
            "Préciser canton vs village dans toute communication.",
            "Décrire acres et bâtiments.",
            "Ancrer sur Hatley rural et Massawippi hors Hatley village.",
        ],
        "buy": "Acheter à Hatley, c'est zonage, fosse, acreage et inspection des bâtiments de campagne ou de ferme.",
        "buy_steps": [
            "Vérifier les droits d'eau s'il y a une vue lac.",
            "Inspecter comme du rural, pas comme un condo Magog.",
            "Lire le zonage avant un projet (chevaux, location, subdivision).",
        ],
        "mistakes": [
            "Payer North Hatley pour Hatley canton.",
            "Ignorer le zonage agricole.",
            "Oublier l'accès hivernal.",
        ],
        "faqs": [
            ("Hatley et North Hatley, c'est la même chose ?", "Non. North Hatley est le village. Hatley est une municipalité distincte, plus rurale."),
            ("Moins cher que North Hatley ?", "En général pour une maison sans lac, oui. Un vrai frontage reste un autre produit."),
            ("Secteur bilingue ?", "Oui, comme beaucoup du Massawippi. L'équipe travaille FR/EN."),
            ("Desservez-vous Hatley ?", "Oui, avec tout le corridor Massawippi."),
        ],
    },
    {
        "slug": "mont-bellevue",
        "name": "Mont-Bellevue",
        "prep": "à",
        "author": "jade",
        "desc": "Vendre ou acheter à Mont-Bellevue (Sherbrooke) : unifamiliales, parc. Guide Chiasson de Francesco.",
        "tldr": "Pour vendre ou acheter à Mont-Bellevue, le stock dominant est la maison, pas le condo King. Le parc du mont structure une partie du cadre. L'équipe Chiasson de Francesco compare Mont-Bellevue à Mont-Bellevue, pas à un condo des Nations.",
        "market": "Arrondissement de Sherbrooke, rues familiales, accès au parc du mont. L'université est proche sans que tout le quartier soit « étudiant » comme Lennoxville.",
        "facts": [
            "Moins de condos qu'aux Nations.",
            "Les poches de rues n'ont pas le même âge ni le même terrain.",
            "Fleurimont est l'autre grand bassin d'unifamiliales.",
            "Pente et stationnement selon le secteur.",
        ],
        "sell": "Vendre à Mont-Bellevue, c'est un prix de maison de quartier, photos du cadre, pas une comparaison avec Magog lac.",
        "sell_steps": [
            "Comparer le même type de rue.",
            "Préparer inspection pré-vente si l'état le justifie.",
            "Afficher un prix de Mont-Bellevue.",
        ],
        "buy": "Acheter à Mont-Bellevue, c'est inspecter cottages et bungalows, et visiter Fleurimont en parallèle si le budget est le critère.",
        "buy_steps": [
            "Visiter le soir.",
            "Inspection (toiture, fondations, drainage de pente).",
            "Ne pas comparer à un condo King.",
        ],
        "mistakes": [
            "Mélanger un condo isolé avec les bungalows du quartier.",
            "Ignorer la pente et le stationnement en hiver.",
            "Choisir seulement « proche de l'université » sans voir le bruit locatif de certaines rues.",
        ],
        "faqs": [
            ("Mont-Bellevue ou Fleurimont ?", "Deux arrondissements familiaux, deux grilles. Mont-Bellevue a le parc du mont ; Fleurimont a l'hôpital. Visitez les deux."),
            ("Beaucoup de condos ?", "Moins qu'aux Nations. Le stock dominant, c'est l'unifamiliale."),
            ("Proche de l'université ?", "Le campus influence certaines rues, pas tout l'arrondissement."),
            ("Vous vendez à Mont-Bellevue ?", "Oui. L'équipe est basée à Sherbrooke et y travaille au quotidien."),
        ],
    },
    {
        "slug": "brompton",
        "name": "Brompton",
        "prep": "à",
        "author": "jade",
        "desc": "Vendre ou acheter à Brompton (Sherbrooke) : vallée, Saint-François. Guide Chiasson de Francesco.",
        "tldr": "Pour vendre ou acheter à Brompton, vous êtes dans un arrondissement nord de Sherbrooke qui a gardé une identité de petite ville de vallée. Ce n'est pas Fleurimont, ni Windsor. L'équipe Chiasson de Francesco compare Brompton à Brompton.",
        "market": "Noyau, rues résidentielles, proximité de la Saint-François. Moins de condos que Les Nations. Beaucoup d'acheteurs y voient un budget plus accessible, avec un temps de route vers le centre.",
        "facts": [
            "Brompton (Bromptonville) est fusionné à Sherbrooke.",
            "Windsor est une autre ville : taxes et comparables changent.",
            "Un plex se juge aux loyers du secteur, plus petits qu'au centre-ville.",
            "Le trajet vers le centre se mesure en heure de pointe.",
        ],
        "sell": "Vendre à Brompton, c'est un prix de Brompton. Le « 10 minutes de Sherbrooke » n'excuse pas un prix des Nations.",
        "sell_steps": [
            "Ancrer sur des ventes Brompton.",
            "Photos du quartier et de l'état réel.",
            "Pour un plex : loyers locaux.",
        ],
        "buy": "Acheter à Brompton, c'est inspecter et valider le navettage vers le centre ou vers Windsor selon votre quotidien.",
        "buy_steps": [
            "Rouler le trajet aux heures de pointe.",
            "Inspection.",
            "Ne pas copier un prix Fleurimont sans comparables.",
        ],
        "mistakes": [
            "Confondre Brompton et Windsor dans les taxes et les comparables.",
            "Surcoter la fusion à Sherbrooke.",
            "Ignorer l'état d'un bâti plus ancien.",
        ],
        "faqs": [
            ("Brompton ou Windsor ?", "Brompton est un arrondissement de Sherbrooke. Windsor est une autre ville. Le trajet vers le centre de Sherbrooke est souvent plus court depuis Brompton."),
            ("Moins cher que Fleurimont ?", "Souvent pour une unifamiliale comparable, avec moins de densité. L'état du bâtiment pèse plus que le nom de l'arrondissement."),
            ("Bon pour navetter ?", "Oui pour plusieurs. Mesurez l'heure de pointe, pas le dimanche."),
            ("Vous travaillez Brompton ?", "Oui. Vallée de la Saint-François : Brompton, Windsor, Richmond."),
        ],
    },
    {
        "slug": "val-des-sources",
        "name": "Val-des-Sources",
        "prep": "à",
        "author": "po",
        "desc": "Vendre ou acheter à Val-des-Sources (Asbestos) : Estrie, MRC des Sources. Guide Chiasson de Francesco.",
        "tldr": "Pour vendre ou acheter à Val-des-Sources, le marché est local, souvent plus accessible que Sherbrooke, sans pression villégiature de lac. L'abordabilité n'annule pas l'inspection. L'équipe Chiasson de Francesco dessert la MRC des Sources depuis Sherbrooke.",
        "market": "Ancienne ville minière en transition (anciennement Asbestos). Acheteurs surtout régionaux. Ce n'est pas un marché de villégiature lacustre.",
        "facts": [
            "Quartiers résidentiels, services de petite ville, proximité de Danville.",
            "Les comparables restent Sources et Richmond, pas Magog.",
            "Un plex se juge aux loyers réels, pas au multiplicateur universitaire de Sherbrooke.",
            "Danville et Richmond encadrent une partie du bassin.",
        ],
        "sell": "Vendre à Val-des-Sources, c'est le prix du marché local. Surcoter parce que Sherbrooke a monté n'accélère rien.",
        "sell_steps": [
            "Ancrer sur des ventes Sources.",
            "Photos et affichage régional.",
            "Décrire l'état sans fard.",
        ],
        "buy": "Acheter à Val-des-Sources, c'est possible pour un premier achat serré si le projet de vie colle à une petite ville des Sources. Inspectez et visitez à différentes heures.",
        "buy_steps": [
            "Visiter le soir.",
            "Inspection (bâtiments d'âge variable).",
            "Pour un plex : loyers, taxes, état.",
        ],
        "mistakes": [
            "Copier un prix Sherbrooke.",
            "Sauter l'inspection parce que c'est « abordable ».",
            "Rêver un rendement de plex du centre-ville.",
        ],
        "faqs": [
            ("Pourquoi les maisons sont-elles plus abordables ?", "Marché local, moins de pression villégiature que les lacs, économie différente de Sherbrooke. L'abordabilité n'annule pas les coûts de rénovation."),
            ("Bon secteur pour un premier achat ?", "Possible si budget et projet de vie collent à une petite ville des Sources."),
            ("Plex et investissement ?", "Au cas par cas : loyers réels, taxes, état."),
            ("Vous allez à Val-des-Sources ?", "Oui. L'équipe dessert la MRC des Sources depuis Sherbrooke."),
        ],
    },
    {
        "slug": "lac-megantic",
        "name": "Lac-Mégantic",
        "prep": "à",
        "author": "po",
        "desc": "Vendre ou acheter à Lac-Mégantic : ville, lac, Granit. Guide Chiasson de Francesco.",
        "tldr": "Pour vendre ou acheter à Lac-Mégantic, le marché est distinct de Sherbrooke : ville moyenne, lac, MRC du Granit. Les comparables doivent rester Granit, pas Estrie-ouest. L'équipe Chiasson de Francesco s'y déplace lorsque le mandat le justifie, et traite aussi le commercial à l'échelle locale.",
        "market": "Le centre et les quartiers résidentiels ne se vendent pas comme un chalet sur le lac. Le plan d'eau attire villégiature ; la ville attire résidence et commerce de proximité.",
        "facts": [
            "Deux produits : urbain et lac.",
            "Bassin d'acheteurs plus local qu'à Magog.",
            "Milan et le Granit encadrent une partie des comparables.",
            "Pierre-Olivier et Marco traitent aussi le commercial local.",
        ],
        "sell": "Vendre à Lac-Mégantic, c'est un prix honnête et une visibilité régionale (Sherbrooke inclus) sans gonfler au tarif Memphrémagog.",
        "sell_steps": [
            "Classer ville vs lac.",
            "Ancrer sur des ventes Lac-Mégantic et Granit du même type.",
            "Photos d'eau seulement s'il y a réellement un rapport à l'eau.",
        ],
        "buy": "Acheter à Lac-Mégantic, c'est distinguer résidence urbaine, commercial de rue et bord de lac. Inspection et lecture du tissu urbain actuel en centre-ville.",
        "buy_steps": [
            "Choisir le produit (ville, lac, commercial) avant le prix.",
            "Inspecter.",
            "Ne pas copier un multiple de Sherbrooke.",
        ],
        "mistakes": [
            "Coller Magog lac sur Lac-Mégantic ville.",
            "Ignorer l'état pour le prix affiché.",
            "Mélanger chalet et maison de quartier.",
        ],
        "faqs": [
            ("Lac-Mégantic est-il loin pour votre équipe ?", "C'est plus à l'est. L'équipe inscrit et accompagne dans le Granit lorsque le mandat le justifie. Discutez-en au téléphone avant une visite inutile."),
            ("Chalet au lac ou maison en ville ?", "Deux produits. Le lac se négocie sur l'accès à l'eau et la saisonnalité ; la ville sur l'état, le quartier et les services."),
            ("Y a-t-il du commercial ?", "Oui, à l'échelle locale."),
            ("Comment fixer le prix ?", "Ventes récentes Lac-Mégantic et Granit du même type. Pas un multiple de Sherbrooke."),
        ],
    },
]


def render(city: dict) -> str:
    key = city["author"]
    author, author_page, job = AUTHORS[key]
    name = city["name"]
    prep = city["prep"]
    file_name = f"article-vendre-acheter-{city['slug']}.html"
    canonical = f"{BASE}/{file_name}"
    region_href = f"regions/{city['slug']}.html"
    headline = f"Vendre ou acheter {prep} {name} : quoi savoir"
    title = f"Vendre ou acheter {prep} {name} : quoi savoir | CDF"

    facts = li(city["facts"])
    mistakes = li(city["mistakes"])
    sell_ol = ol(city["sell_steps"])
    buy_ol = ol(city["buy_steps"])
    faqs_html = "\n".join(
        f'<div class="border border-gray-200 rounded-xl p-5 bg-white mb-4"><h3 class="font-semibold text-brand-navy mb-2">{q}</h3><p class="text-gray-600 leading-relaxed">{a}</p></div>'
        for q, a in city["faqs"]
    )
    body = f"""
  <main class="pt-32 pb-20">
    <div class="max-w-3xl mx-auto px-6">
      <nav class="text-sm text-gray-500 mb-6"><a href="index.html" class="hover:text-brand-red">Accueil</a> / <a href="blog.html" class="hover:text-brand-red">Blogue</a> / Guide local</nav>
      <div class="inline-block bg-brand-navy text-white px-3 py-1 rounded-full text-xs font-bold uppercase mb-4">Guide local</div>
      <h1 class="font-heading text-4xl md:text-5xl font-bold text-brand-navy mb-4">{headline}</h1>
      <p class="text-sm text-gray-500 mb-8">Par <a class="hover:text-brand-red" href="{author_page}">{author}</a>, {job} · 18 août 2026</p>
      <p class="text-lg font-medium text-brand-navy mb-8 leading-relaxed"><strong>En bref.</strong> {city["tldr"]}</p>

      <h2 class="font-heading text-2xl font-bold text-brand-navy mt-10 mb-4">Qu'est-ce qui distingue le marché immobilier {prep} {name} ?</h2>
      <p class="text-gray-600 leading-relaxed mb-4">{city["market"]}</p>
      {facts}

      <h2 class="font-heading text-2xl font-bold text-brand-navy mt-10 mb-4">Quoi savoir avant de vendre {prep} {name} ?</h2>
      <p class="text-gray-600 leading-relaxed mb-4">{city["sell"]}</p>
      {sell_ol}

      <h2 class="font-heading text-2xl font-bold text-brand-navy mt-10 mb-4">Quoi savoir avant d'acheter {prep} {name} ?</h2>
      <p class="text-gray-600 leading-relaxed mb-4">{city["buy"]}</p>
      {buy_ol}

      <h2 class="font-heading text-2xl font-bold text-brand-navy mt-10 mb-4">Erreurs fréquentes {prep} {name}</h2>
      {mistakes}

      <h2 class="font-heading text-2xl font-bold text-brand-navy mt-10 mb-4">Qui appeler pour vendre ou acheter {prep} {name} ?</h2>
      <p class="text-gray-600 leading-relaxed mb-6">L'équipe Chiasson de Francesco, courtiers immobiliers RE/MAX D'ABORD à Sherbrooke, accompagne l'achat et la vente {prep} {name}. Pierre-Olivier Chiasson (819-919-4631) et Marco De Francesco (819-562-0656) sont courtiers résidentiels et commerciaux. Jade Sirois (819-434-2652) est courtière résidentielle. Bureau : 157 boul. Jacques-Cartier Sud, Sherbrooke (QC) J1J 2Z4. Page région : <a class="text-brand-navy font-medium hover:text-brand-red" href="{region_href}">{name}</a>.</p>

      <h2 class="font-heading text-2xl font-bold text-brand-navy mt-10 mb-4">Questions fréquentes</h2>
      {faqs_html}

      <p class="text-gray-600 mt-10">Équipe Chiasson de Francesco, RE/MAX D'ABORD, Sherbrooke. <a class="text-brand-navy font-medium hover:text-brand-red" href="index.html#contact">Discuter d'un projet</a> · <a class="text-brand-navy font-medium hover:text-brand-red" href="vendre.html">Vendre</a> · <a class="text-brand-navy font-medium hover:text-brand-red" href="acheter.html">Acheter</a> · <a class="text-brand-navy font-medium hover:text-brand-red" href="blog.html">Blogue</a></p>
    </div>
  </main>
"""
    article_ld = {
        "@type": "Article",
        "headline": headline,
        "description": city["desc"],
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
        "about": {"@type": "Place", "name": name, "address": {"@type": "PostalAddress", "addressLocality": name, "addressRegion": "QC", "addressCountry": "CA"}},
        "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
    }
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            article_ld,
            faq_ld(canonical, city["faqs"]),
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
    return page_shell(title, city["desc"], canonical, body, ld), file_name, title, city["desc"]


def link_region(slug: str, name: str, prep: str) -> None:
    path = ROOT / "regions" / f"{slug}.html"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    href = f"../article-vendre-acheter-{slug}.html"
    if href in text:
        return
    label = f"Vendre ou acheter {prep} {name} : quoi savoir"
    item = f'          <li><a href="{href}" class="text-brand-navy font-medium hover:text-brand-red">{label}</a></li>\n'
    needle = '<ul class="list-disc pl-5 space-y-2 text-gray-600 mb-8">\n'
    if needle in text:
        path.write_text(text.replace(needle, needle + item, 1), encoding="utf-8")
        print("linked", path.name)


def main() -> None:
    for city in CITIES:
        html, file_name, title, desc = render(city)
        (ROOT / file_name).write_text(html, encoding="utf-8")
        print("wrote", file_name)
        link_region(city["slug"], city["name"], city["prep"])


if __name__ == "__main__":
    main()
