#!/usr/bin/env python3
"""Sync Centris listings: full photo galleries + 1200x630 social share images."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import time
import urllib.parse
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://chiassondefrancesco.ca"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0 Safari/537.36"
)
OG_WIDTH = 1200
OG_HEIGHT = 630
DEFAULT_SEARCH = (
    "https://www.centris.ca/fr/propriete~a-vendre?q=H4sIAAAAAAAACk2MsQ6CMBRF_6UzAxIToyuDMSYOYlgIw5PeQmOhpAVNQ_h3X6MD27vn3vMW0RsvTiIViXg6-4LLrQSDXbY_ZEemVind4IrAkOPscYZtHY1dKDoawXaaCB_PUuPDsao5g1zT3aiPv1hT2kxw_1JpGOlLMnO0q-UHLpKnOU1orQusvGPP6A6vJYZJkxFrsh0XMEYP7SOM2OwLMhBrvX4Bb6jOs9sAAAA&sortSeed=1077964681&sort=None&pageSize=20"
)
REMAX_BASE_URL = "https://www.remax-quebec.com"
REMAX_API_URL = "https://api.remax-quebec.com/api/"
DEFAULT_REMAX_BROKER_SLUG = "p-o.chiasson"
DEFAULT_REMAX_AGENT_URL = (
    f"{REMAX_BASE_URL}/fr/courtiers-immobiliers/{DEFAULT_REMAX_BROKER_SLUG}"
)
# Public frontend key (also embedded in remax-quebec.com JS bundles).
DEFAULT_REMAX_API_KEY = "c4dWcBkE#RL78Y@zg4Y06M$qrOJAeh7Fwv!Z9T4Q1f@zZ"


def load_properties_registry() -> dict:
    path = ROOT / "data" / "properties.json"
    if not path.exists():
        return {"listings": []}
    return json.loads(path.read_text(encoding="utf-8"))


def listing_public_path(listing: dict) -> str:
    return (
        f"/{listing['country']}/{listing['province']}/{listing['city']}/"
        f"{listing['sector']}/{listing['street']}/"
    )


def http_get(url: str, session: requests.Session) -> requests.Response:
    resp = session.get(url, timeout=60)
    resp.raise_for_status()
    return resp


def extract_listing_id(url: str) -> str | None:
    match = re.search(r"/(\d{5,10})(?:[/?#]|$)", url)
    return match.group(1) if match else None


def extract_listing_links(html: str) -> list[str]:
    pattern = re.compile(r'href="(?P<path>/fr/propriete~a-vendre[^"]+?/(?P<id>\d{5,10}))"')
    seen: set[str] = set()
    links: list[str] = []
    for match in pattern.finditer(html):
        listing_id = match.group("id")
        if listing_id in seen:
            continue
        seen.add(listing_id)
        links.append("https://www.centris.ca" + match.group("path"))
    return links


def upgrade_photo_url(url: str, width: int = 1260, height: int = 1024) -> str:
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    try:
        current_w = int(query.get("w", ["0"])[0])
    except ValueError:
        current_w = 0
    if current_w >= width:
        width = current_w
        height = int(query.get("h", [str(height)])[0])
    query["w"] = [str(width)]
    query["h"] = [str(height)]
    if "sm" in query:
        query["sm"] = ["c"]
    new_query = urllib.parse.urlencode({k: v[0] for k, v in query.items()})
    return urllib.parse.urlunparse(parsed._replace(query=new_query))


def extract_mosaic_photo_urls(html: str) -> list[str]:
    match = re.search(r"window\.MosaicPhotoUrls\s*=\s*(\[[^\]]+\])", html)
    if match:
        raw = match.group(1).replace("\\u0026", "&")
        try:
            urls = json.loads(raw)
            if isinstance(urls, list) and urls:
                upgraded = []
                for index, url in enumerate(urls):
                    if index == 0:
                        upgraded.append(upgrade_photo_url(url, width=1260, height=1024))
                    else:
                        upgraded.append(upgrade_photo_url(url, width=640, height=480))
                return upgraded
        except json.JSONDecodeError:
            pass

    og_match = re.search(
        r'<meta\s+property="og:image"\s+content="([^"]+)"',
        html,
        re.IGNORECASE,
    )
    if og_match:
        return [upgrade_photo_url(og_match.group(1).replace("&amp;", "&"))]

    img_urls = re.findall(
        r'https://mspublic\.centris\.ca/media\.ashx\?[^"\']+',
        html,
    )
    deduped: list[str] = []
    seen: set[str] = set()
    for url in img_urls:
        if "t=pi" not in url:
            continue
        clean = upgrade_photo_url(url.replace("&amp;", "&"))
        if clean not in seen:
            seen.add(clean)
            deduped.append(clean)
    return deduped


def extract_meta(html: str, property_url: str) -> dict:
    og_title = None
    og_image = None
    price = None

    title_match = re.search(
        r'<meta\s+property="og:title"\s+content="([^"]+)"',
        html,
        re.IGNORECASE,
    )
    if title_match:
        og_title = title_match.group(1)

    og_image_match = re.search(
        r'<meta\s+property="og:image"\s+content="([^"]+)"',
        html,
        re.IGNORECASE,
    )
    if og_image_match:
        og_image = og_image_match.group(1).replace("&amp;", "&")

    for block in re.findall(
        r'<script[^>]*type="application/ld\+json"[^>]*>([\s\S]*?)</script>',
        html,
        re.IGNORECASE,
    ):
        price_match = re.search(r'"price"\s*:\s*([0-9]+(?:\.[0-9]+)?)', block)
        if price_match:
            price = price_match.group(1)
            break

    return {
        "id": extract_listing_id(property_url),
        "propertyUrl": property_url,
        "ogTitle": og_title,
        "ogImage": og_image,
        "price": price,
    }


def download_bytes(url: str, session: requests.Session) -> bytes:
    resp = session.get(url, timeout=120)
    resp.raise_for_status()
    return resp.content


def save_og_share_image(image_bytes: bytes, destination: Path) -> None:
    with Image.open(BytesIO(image_bytes)) as img:
        img = img.convert("RGB")
        src_w, src_h = img.size
        target_ratio = OG_WIDTH / OG_HEIGHT
        src_ratio = src_w / src_h

        if src_ratio > target_ratio:
            new_w = int(src_h * target_ratio)
            left = (src_w - new_w) // 2
            box = (left, 0, left + new_w, src_h)
        else:
            new_h = int(src_w / target_ratio)
            top = (src_h - new_h) // 2
            box = (0, top, src_w, top + new_h)

        cropped = img.crop(box).resize((OG_WIDTH, OG_HEIGHT), Image.Resampling.LANCZOS)
        destination.parent.mkdir(parents=True, exist_ok=True)
        cropped.save(destination, format="JPEG", quality=88, optimize=True)


def remax_api_headers(api_key: str) -> dict[str, str]:
    return {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Content-Language": "fr",
        "X-Header-Api": api_key,
    }


def remax_view_all_url(broker_idagent: int | str, include_sold: bool = False) -> str:
    params = {"BrokerId": broker_idagent, "Sold": "1" if include_sold else "0"}
    return f"{REMAX_BASE_URL}/fr/resultats?{urllib.parse.urlencode(params)}"


def fetch_remax_broker(slug: str, session: requests.Session) -> dict:
    url = f"{REMAX_API_URL}brokers/{slug}"
    resp = session.get(url, timeout=60)
    resp.raise_for_status()
    broker = resp.json()
    if not broker.get("idagent"):
        raise RuntimeError(f"RE/MAX broker profile missing idagent for slug {slug!r}")
    return broker


def discover_remax_listings(
    broker_idagent: int,
    session: requests.Session,
    *,
    include_sold: bool = False,
    page_size: int = 100,
) -> list[dict]:
    """Discover active listings from RE/MAX (agent page -> view all properties)."""
    listings: list[dict] = []
    page = 1
    params_base = {
        "BrokerId": broker_idagent,
        "PageSize": page_size,
        "Sold": "1" if include_sold else "0",
    }

    while True:
        params = {**params_base, "Page": page}
        resp = session.get(
            f"{REMAX_API_URL}inscriptions/search",
            params=params,
            timeout=60,
        )
        resp.raise_for_status()
        payload = resp.json()
        batch = payload.get("data") or []
        listings.extend(batch)

        meta = payload.get("meta") or {}
        last_page = meta.get("last_page") or page
        if page >= last_page or not batch:
            break
        page += 1

    return listings


def centris_url_for_remax_listing(uls: str, listing: dict) -> str:
    if listing.get("is_rental") and not listing.get("is_for_sale"):
        return f"https://www.centris.ca/fr/propriete~a-louer/{uls}"
    return f"https://www.centris.ca/fr/propriete~a-vendre/{uls}"


def centris_urls_for_id(listing_id: str) -> list[str]:
    return [
        f"https://www.centris.ca/fr/propriete~a-vendre/{listing_id}",
        f"https://www.centris.ca/fr/propriete~a-louer/{listing_id}",
        f"https://www.centris.ca/fr/inscription/{listing_id}",
    ]


def fetch_listing_html(listing_id: str, property_url: str, session: requests.Session) -> str:
    candidates = [property_url] + [
        url for url in centris_urls_for_id(listing_id) if url != property_url
    ]
    last_error: Exception | None = None
    for url in candidates:
        try:
            html = http_get(url, session).text
            if "MosaicPhotoUrls" in html or 'property="og:image"' in html:
                return html
        except requests.RequestException as exc:
            last_error = exc
    if last_error:
        raise last_error
    raise RuntimeError(f"Could not fetch listing HTML for {listing_id}")


def get_active_uls(registry: dict) -> set[str]:
    return {str(item["uls"]) for item in registry.get("listings", [])}


def cleanup_listing_folder(listing_dir: Path, saved_photos: list[str]) -> list[str]:
    """Remove gallery files that are no longer part of the current sync."""
    if not listing_dir.is_dir():
        return []

    allowed = set(saved_photos) | {"og-share.jpg", "manifest.json"}
    removed: list[str] = []
    for path in listing_dir.iterdir():
        if path.name in allowed:
            continue
        if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".webp", ".png"}:
            path.unlink()
            removed.append(str(path))
    return removed


def cleanup_stale_properties(
    images_root: Path,
    registry: dict,
    active_uls: set[str] | None = None,
) -> list[str]:
    """Delete image folders/files for listings no longer in data/properties.json."""
    if active_uls is None:
        active_uls = get_active_uls(registry)

    active_fallbacks = {
        item.get("fallbackImage")
        for item in registry.get("listings", [])
        if item.get("fallbackImage")
    }
    removed: list[str] = []

    for path in sorted(images_root.iterdir()):
        if path.is_dir() and path.name.isdigit() and path.name not in active_uls:
            shutil.rmtree(path)
            removed.append(str(path))
            print(f"  removed stale folder {path.name}/")

    for pattern in ("*.jpg", "*.jpeg", "*.webp"):
        for path in sorted(images_root.glob(pattern)):
            if not path.is_file():
                continue
            stem = path.stem
            name = path.name
            if stem.isdigit() and stem not in active_uls:
                path.unlink()
                removed.append(str(path))
                print(f"  removed stale hero {name}")
            elif not stem.isdigit() and name not in active_fallbacks:
                path.unlink()
                removed.append(str(path))
                print(f"  removed unreferenced hero {name}")

    return removed


def sync_listing(
    listing_id: str,
    property_url: str,
    session: requests.Session,
    images_root: Path,
    registry_by_uls: dict[str, dict],
) -> dict:
    print(f"Fetching listing {listing_id}...")
    html = fetch_listing_html(listing_id, property_url, session)
    meta = extract_meta(html, property_url)
    photo_urls = extract_mosaic_photo_urls(html)

    listing_dir = images_root / listing_id
    listing_dir.mkdir(parents=True, exist_ok=True)

    saved_photos: list[str] = []
    first_bytes: bytes | None = None

    for index, photo_url in enumerate(photo_urls, start=1):
        filename = f"{index:02d}.jpg"
        dest = listing_dir / filename
        try:
            photo_bytes = download_bytes(photo_url, session)
            if len(photo_bytes) < 1024:
                raise requests.RequestException("empty or too-small image payload")
            dest.write_bytes(photo_bytes)
            saved_photos.append(filename)
            if first_bytes is None:
                first_bytes = photo_bytes
            print(f"  downloaded {filename}")
        except requests.RequestException as exc:
            print(f"  WARN: failed {filename}: {exc}", file=sys.stderr)

    og_share = "og-share.jpg"
    if first_bytes:
        save_og_share_image(first_bytes, listing_dir / og_share)
        (images_root / f"{listing_id}.jpg").write_bytes(first_bytes)
        print(f"  wrote {og_share} ({OG_WIDTH}x{OG_HEIGHT})")

    registry_entry = registry_by_uls.get(listing_id, {})
    public_path = listing_public_path(registry_entry) if registry_entry else None

    manifest = {
        "uls": listing_id,
        "photos": saved_photos,
        "ogShare": og_share if first_bytes else None,
        "count": len(saved_photos),
        "publicPath": public_path,
        "ogImageUrl": (
            f"{BASE_URL}/src/assets/images/proprietes/{listing_id}/{og_share}"
            if first_bytes
            else None
        ),
    }
    (listing_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    pruned = cleanup_listing_folder(listing_dir, saved_photos)
    for path in pruned:
        print(f"  removed stale gallery file {Path(path).name}")

    return {
        **meta,
        "photos": saved_photos,
        "photoCount": len(saved_photos),
        "ogShareImage": f"src/assets/images/proprietes/{listing_id}/{og_share}" if first_bytes else None,
        "publicPath": public_path,
    }


def collect_listing_jobs(
    args: argparse.Namespace,
    session: requests.Session,
    registry: dict,
    remax_meta: dict | None = None,
) -> dict[str, str]:
    by_id: dict[str, str] = {}

    if args.official_feed_url:
        feed = http_get(args.official_feed_url, session).json()
        listings = feed.get("listings", feed)
        for item in listings:
            listing_id = str(item.get("id") or item.get("uls") or "")
            property_url = item.get("propertyUrl") or item.get("url")
            if not listing_id and property_url:
                listing_id = extract_listing_id(property_url) or ""
            if listing_id and property_url:
                by_id[listing_id] = property_url
    elif args.sync_remax:
        broker = fetch_remax_broker(args.remax_broker_slug, session)
        broker_idagent = int(broker["idagent"])
        if remax_meta is not None:
            remax_meta.update(
                {
                    "brokerSlug": broker.get("slug") or args.remax_broker_slug,
                    "brokerName": broker.get("name"),
                    "brokerMemberNo": broker.get("no_membre"),
                    "brokerIdAgent": broker_idagent,
                    "agentUrl": args.remax_agent_url,
                    "viewAllUrl": remax_view_all_url(
                        broker_idagent,
                        include_sold=args.remax_include_sold,
                    ),
                }
            )
        listings = discover_remax_listings(
            broker_idagent,
            session,
            include_sold=args.remax_include_sold,
            page_size=max(args.max_listings, 100),
        )
        for item in listings:
            uls = str(item.get("no_inscription") or "")
            if uls:
                by_id[uls] = centris_url_for_remax_listing(uls, item)
    elif args.sync_registry:
        for item in registry.get("listings", []):
            uls = str(item["uls"])
            by_id[uls] = f"https://www.centris.ca/fr/propriete~a-vendre/{uls}"
    else:
        search_html = http_get(args.search_url, session).text
        for link in extract_listing_links(search_html):
            listing_id = extract_listing_id(link)
            if listing_id:
                by_id[listing_id] = link

    if not by_id:
        raise RuntimeError("No Centris listings found to sync.")

    limit = args.max_listings
    if limit and limit > 0:
        trimmed = dict(list(by_id.items())[:limit])
        return trimmed
    return by_id


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync Centris listing galleries.")
    parser.add_argument("--search-url", default=DEFAULT_SEARCH)
    parser.add_argument("--max-listings", type=int, default=30)
    parser.add_argument("--delay-seconds", type=float, default=2.0)
    parser.add_argument("--official-feed-url", default="")
    parser.add_argument(
        "--sync-registry",
        action="store_true",
        help="Sync all listings defined in data/properties.json",
    )
    parser.add_argument(
        "--sync-remax",
        action="store_true",
        help=(
            "Discover listings from RE/MAX agent profile (view all properties), "
            "then sync galleries from Centris"
        ),
    )
    parser.add_argument(
        "--remax-broker-slug",
        default=DEFAULT_REMAX_BROKER_SLUG,
        help="RE/MAX broker slug (e.g. p-o.chiasson)",
    )
    parser.add_argument(
        "--remax-agent-url",
        default=DEFAULT_REMAX_AGENT_URL,
        help="RE/MAX courtier profile URL (for logs/metadata)",
    )
    parser.add_argument(
        "--remax-include-sold",
        action="store_true",
        help="Include sold RE/MAX listings when discovering broker properties",
    )
    parser.add_argument(
        "--output-json",
        default=str(ROOT / "data" / "centris_listings.json"),
    )
    parser.add_argument(
        "--output-images-dir",
        default=str(ROOT / "src/assets/images/proprietes"),
    )
    parser.add_argument(
        "--no-cleanup-stale",
        action="store_true",
        help="Do not delete images for listings removed from data/properties.json",
    )
    args = parser.parse_args()

    import os

    if args.sync_registry and args.sync_remax:
        parser.error("Use only one of --sync-registry or --sync-remax")

    if not args.official_feed_url:
        args.official_feed_url = os.environ.get("CENTRIS_BROKER_FEED_URL", "")
    if not args.search_url or args.search_url == DEFAULT_SEARCH:
        env_search = os.environ.get("CENTRIS_SEARCH_URL", "")
        if env_search:
            args.search_url = env_search

    env_broker_slug = os.environ.get("REMAX_BROKER_SLUG", "")
    if env_broker_slug:
        args.remax_broker_slug = env_broker_slug
    env_agent_url = os.environ.get("REMAX_AGENT_URL", "")
    if env_agent_url:
        args.remax_agent_url = env_agent_url

    registry = load_properties_registry()
    registry_by_uls = {str(item["uls"]): item for item in registry.get("listings", [])}

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        }
    )

    remax_meta: dict = {}
    remax_api_key = os.environ.get("REMAX_API_KEY", DEFAULT_REMAX_API_KEY)
    if args.sync_remax:
        session.headers.update(remax_api_headers(remax_api_key))

    jobs = collect_listing_jobs(args, session, registry, remax_meta=remax_meta)
    if args.sync_remax:
        scrape_mode = "remax"
    elif args.sync_registry:
        scrape_mode = "registry"
    elif args.official_feed_url:
        scrape_mode = "feed"
    else:
        scrape_mode = "search"
    print(f"Scrape mode: {scrape_mode}")
    if args.sync_remax:
        print(f"RE/MAX agent page: {args.remax_agent_url}")
        print(f"RE/MAX view all: {remax_meta.get('viewAllUrl')}")
        print(f"Broker: {remax_meta.get('brokerName')} ({remax_meta.get('brokerMemberNo')})")
        print("Discovered listings (Centris ULS):")
        for uls, url in jobs.items():
            print(f"  - {uls}: {url}")
    elif args.sync_registry:
        print("Listing pages (per ULS in data/properties.json):")
        for uls in jobs:
            print(f"  - https://www.centris.ca/fr/propriete~a-vendre/{uls}")
            print(f"    fallback: https://www.centris.ca/fr/propriete~a-louer/{uls}")
    elif not args.official_feed_url:
        print(f"Search page: {args.search_url}")
    print(f"Syncing {len(jobs)} listing(s)...")

    images_root = Path(args.output_images_dir)
    results = []

    for listing_id, property_url in jobs.items():
        try:
            result = sync_listing(
                listing_id,
                property_url,
                session,
                images_root,
                registry_by_uls,
            )
            results.append(result)
        except requests.RequestException as exc:
            print(f"WARN: failed listing {listing_id}: {exc}", file=sys.stderr)
            results.append(
                {
                    "id": listing_id,
                    "propertyUrl": property_url,
                    "error": str(exc),
                }
            )
        time.sleep(args.delay_seconds)

    active_uls = set(jobs.keys())
    removed_stale: list[str] = []
    if not args.no_cleanup_stale and scrape_mode in {"registry", "remax"}:
        print("Cleaning up stale property images...")
        removed_stale = cleanup_stale_properties(images_root, registry, active_uls)

    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "scrapeMode": scrape_mode,
        "searchUrl": args.search_url if scrape_mode == "search" else None,
        "registryPath": "data/properties.json" if scrape_mode == "registry" else None,
        "remax": remax_meta if scrape_mode == "remax" else None,
        "discoveredUls": sorted(active_uls) if scrape_mode == "remax" else None,
        "maxListings": args.max_listings,
        "removedStale": removed_stale,
        "listings": results,
    }

    output_json = Path(args.output_json)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"Wrote {output_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
