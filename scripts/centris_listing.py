"""Parse a public Centris listing page into the detail shape used by refresh_po_listings.

RE/MAX Québec's inscriptions API does not list every team mandate. Listings that
are live on Centris but absent from that API are described here from the page
itself: price, address, remarks, characteristics, and the courtiers inscripteurs.
Nothing is invented when a field is missing.
"""

from __future__ import annotations

import json
import re
from html import unescape
from pathlib import Path

import requests

from team_brokers import TEAM_BY_MEMBER

ROOT = Path(__file__).resolve().parent.parent
PINNED_PATH = ROOT / "data" / "centris_pinned.json"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0 Safari/537.36"
)
HTML_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "fr-CA,fr;q=0.9,en;q=0.8",
}


def load_pinned_records() -> list[dict]:
    if not PINNED_PATH.exists():
        return []
    payload = json.loads(PINNED_PATH.read_text(encoding="utf-8"))
    records = []
    for item in payload.get("listings") or []:
        uls = str(item.get("uls") or "").strip()
        url = (item.get("centrisUrl") or "").strip()
        if uls and url:
            records.append({"uls": uls, "centrisUrl": url})
    return records


def _plain(fragment: str) -> str:
    text = re.sub(r"<[^>]+>", " ", fragment or "")
    text = unescape(text).replace("\xa0", " ")
    return re.sub(r"\s+", " ", text).strip()


def centris_page_state(html: str, final_url: str) -> str:
    """Return active, gone, or unknown for a fetched Centris listing page."""
    if not html:
        return "unknown"
    if "listingnotfound=" in (final_url or ""):
        return "gone"
    lowered = html.lower()
    if "inscription introuvable" in lowered or "cette inscription n'est plus disponible" in lowered:
        return "gone"
    has_price = 'itemprop="price"' in html or 'id="RawPrice"' in html
    has_body = "remarks-text" in html or "MosaicPhotoUrls" in html
    if has_price and has_body:
        return "active"
    if has_price or has_body:
        return "unknown"
    return "gone"


def fetch_centris_html(session: requests.Session, url: str) -> tuple[str, str, str]:
    try:
        resp = session.get(url, headers=HTML_HEADERS, timeout=60, allow_redirects=True)
    except requests.RequestException:
        return "", url, "unknown"
    if resp.status_code == 404:
        return resp.text or "", resp.url, "gone"
    if resp.status_code != 200:
        return resp.text or "", resp.url, "unknown"
    state = centris_page_state(resp.text or "", resp.url)
    return resp.text or "", resp.url, state


def protected_jobs(session: requests.Session) -> tuple[dict[str, str], bool]:
    """Centris URLs to keep in the active set.

    A pin is dropped only when Centris says the listing is gone.
    A failed check stays protected and is reported as incomplete.
    """
    jobs: dict[str, str] = {}
    complete = True
    for record in load_pinned_records():
        _html, _final, state = fetch_centris_html(session, record["centrisUrl"])
        if state == "gone":
            print(
                f"pinned ULS {record['uls']} is no longer on Centris; "
                "it will follow the sold-listing path."
            )
            continue
        if state != "active":
            complete = False
            print(
                f"WARN: could not confirm pinned ULS {record['uls']} on Centris; keeping it."
            )
        jobs[record["uls"]] = record["centrisUrl"]
    return jobs, complete


def _caracs(html: str) -> dict[str, str]:
    pairs = re.findall(
        r'class="carac-title">([^<]+)</div>\s*<div class="carac-value">([\s\S]*?)</div>',
        html,
    )
    found: dict[str, str] = {}
    for label, value_html in pairs:
        key = _plain(label)
        value = _plain(value_html)
        if key and value and key not in found:
            found[key] = value
    return found


def _count_near(html: str, css_class: str) -> int | None:
    match = re.search(rf'class="col-sm-6 {css_class}">\s*(\d+)', html)
    if not match:
        return None
    return int(match.group(1))


def _brokers(html: str) -> list[dict]:
    brokers: list[dict] = []
    seen: set[str] = set()
    for part in html.split('class="broker-info ')[1:]:
        head = part[:4000]
        id_match = re.search(r'data-broker-id="(\d+)"', head)
        name_match = re.search(r'itemprop="name">([^<]+)', head)
        if not id_match or not name_match:
            continue
        member = id_match.group(1)
        if member in seen:
            continue
        seen.add(member)
        job_match = re.search(r'itemprop="jobTitle">([^<]*)', head)
        known = TEAM_BY_MEMBER.get(member) or {}
        job = _plain(job_match.group(1)) if job_match else ""
        brokers.append(
            {
                "member": member,
                "name": _plain(name_match.group(1)),
                "job": job or known.get("job") or "",
                "phone": known.get("phone") or "",
                "profile": known.get("profile") or "",
            }
        )
    return brokers


def _parse_address(address: str) -> dict:
    text = _plain(address)
    apt = ""
    apt_match = re.search(r",\s*app\.\s*([^,]+)", text, re.IGNORECASE)
    if apt_match:
        apt = apt_match.group(1).strip()
        text = (text[: apt_match.start()] + text[apt_match.end() :]).strip(" ,")
    parts = [part.strip() for part in text.split(",") if part.strip()]
    civic = parts[0] if parts else ""
    street = parts[1] if len(parts) > 2 else ""
    municipality = ", ".join(parts[2:]) if len(parts) > 2 else (parts[-1] if parts else "")
    if len(parts) == 2 and not street:
        street = ""
        municipality = parts[1]
    return {
        "noCiviqueDebut": civic,
        "nomRueComplet": street,
        "appartement": apt,
        "municipalite": municipality,
        "display": {"fr": _plain(address)},
    }


def _kind_and_type(page_title: str, caracs: dict[str, str]) -> tuple[str, str]:
    style = caracs.get("Style de bâtiment", "")
    copro = caracs.get("Type de copropriété", "")
    title = (page_title or "").lower()
    if "condo" in title or copro:
        if copro.lower().startswith("divis"):
            return "Condo", "Copropriété divise"
        if copro:
            return "Condo", copro
        return "Condo", "Copropriété"
    tokens = [token.strip() for token in style.split(",") if token.strip()]
    lowered = [token.lower() for token in tokens]
    if any("plain-pied" in token or "plain pied" in token for token in lowered):
        kind = "Maison de plain-pied"
    elif "maison" in title:
        kind = "Maison"
    else:
        kind = (page_title or "Propriété").split(" à ")[0].strip() or "Propriété"
    detached = next(
        (token for token in tokens if token.lower().startswith(("détach", "detach"))),
        "",
    )
    return kind, detached or (tokens[-1] if tokens else "")


def parse_centris_listing(html: str, uls: str) -> dict:
    """Build a RE/MAX-like detail dict from a Centris listing page."""
    state = centris_page_state(html, "")
    if state != "active":
        raise ValueError(f"Centris page for ULS {uls} is not an active listing")

    price_match = re.search(r'itemprop="price"\s+content="(\d+)"', html) or re.search(
        r'id="RawPrice">(\d+)<', html
    )
    if not price_match:
        raise ValueError(f"Centris page for ULS {uls} has no price")
    price = int(price_match.group(1))

    address_match = re.search(
        r'class="property-summary-header__address"[^>]*>\s*([^<]+)',
        html,
    )
    if not address_match:
        raise ValueError(f"Centris page for ULS {uls} has no address")
    address = _plain(address_match.group(1))

    remarks_match = re.search(r'class="remarks-text">([\s\S]*?)</div>', html)
    remarks = _plain(remarks_match.group(1)) if remarks_match else ""
    if not remarks:
        raise ValueError(f"Centris page for ULS {uls} has no description")

    title_match = re.search(r'data-id="PageTitle">([^<]+)', html)
    page_title = _plain(title_match.group(1)) if title_match else ""
    caracs = _caracs(html)
    kind, property_type = _kind_and_type(page_title, caracs)

    detail: dict = {
        "no_inscription": str(uls),
        "is_rental": False,
        "is_for_sale": True,
        "price_sale": price,
        "display_price": {"fr": f"{price:,}".replace(",", " ") + "$"},
        "property_kind": {"fr": kind},
        "address": _parse_address(address),
        "content": {"description": {"fr": remarks}},
        "listing_brokers": _brokers(html),
        "source": "centris",
    }
    if property_type:
        detail["property_type"] = {"fr": property_type}
    rooms = _count_near(html, "piece")
    beds = _count_near(html, "cac")
    baths = _count_near(html, "sdb")
    if rooms:
        detail["nb_of_rooms"] = rooms
    if beds:
        detail["nb_of_bedrooms"] = beds
    if baths:
        detail["nb_of_bathrooms"] = baths
    year = caracs.get("Année de construction")
    if year and year.isdigit():
        detail["date_construction"] = {"annee_construction": int(year)}
    lot = caracs.get("Superficie du terrain")
    if lot:
        detail["superficie_terrain"] = {"tooltip_fr": lot}
    living = caracs.get("Superficie nette") or caracs.get("Superficie habitable")
    if living:
        detail["superficie_habitable"] = living
    return detail


def detail_for_uls(session: requests.Session, uls: str) -> dict | None:
    """Return a Centris detail dict for a pinned ULS, or None if it is not pinned."""
    record = next((item for item in load_pinned_records() if item["uls"] == str(uls)), None)
    if not record:
        return None
    html, final_url, state = fetch_centris_html(session, record["centrisUrl"])
    if state != "active":
        raise requests.HTTPError(
            f"Pinned ULS {uls} is not an active Centris listing ({state}, {final_url})"
        )
    return parse_centris_listing(html, str(uls))
