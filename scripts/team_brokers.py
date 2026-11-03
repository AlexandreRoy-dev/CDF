"""Team brokers for Équipe Chiasson De Francesco, RE/MAX D'ABORD.

idagent values are the public RE/MAX Québec BrokerId (inscriptions/search).
no_membre values are the Centris data-broker-id attributes.
Phones and emails are the coordinates published on the site.
"""

from __future__ import annotations

# Visible agency name. Never append « Inc. ».
AGENCY_NAME = "RE/MAX D'ABORD, agence immobilière"

TEAM_BROKERS: list[dict] = [
    {
        "slug": "p-o.chiasson",
        "idagent": 24115,
        "no_membre": "124729",
        "name": "Pierre-Olivier Chiasson",
        "phone": "819-919-4631",
        "email": "p-o.chiasson@remax-quebec.com",
        "profile": "/pierre-olivier.html",
        "job": "Courtier immobilier résidentiel et commercial",
    },
    {
        "slug": "marco.defrancesco",
        "idagent": 21772,
        "no_membre": "119714",
        "name": "Marco De Francesco",
        "phone": "819-562-0656",
        "email": "marco.defrancesco@remax-quebec.com",
        "profile": "/marco.html",
        "job": "Courtier immobilier résidentiel et commercial",
    },
    {
        "slug": "jade.sirois",
        "idagent": 26057,
        "no_membre": "141323",
        "name": "Jade Sirois",
        "phone": "819-434-2652",
        "email": "jade.sirois@remax-quebec.com",
        "profile": "/jade.html",
        "job": "Courtière immobilière résidentielle",
    },
    {
        "slug": "pierreluc.giroux",
        "idagent": 25873,
        "no_membre": "140191",
        "name": "Pierre-Luc Giroux",
        "phone": "514-889-2927",
        "email": "pierreluc.giroux@remax-quebec.com",
        "profile": "/pierre-luc.html",
        "job": "Courtier immobilier résidentiel",
    },
]

TEAM_BY_MEMBER: dict[str, dict] = {broker["no_membre"]: broker for broker in TEAM_BROKERS}
