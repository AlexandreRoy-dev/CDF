#!/usr/bin/env python3
"""Sync Centris listings: full photo galleries + 1200x630 social share images."""

from __future__ import annotations

import argparse
import json
import re
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
        "--output-json",
        default=str(ROOT / "data" / "centris_listings.json"),
    )
    parser.add_argument(
        "--output-images-dir",
        default=str(ROOT / "src/assets/images/proprietes"),
    )
    args = parser.parse_args()

    if not args.official_feed_url:
        import os

        args.official_feed_url = os.environ.get("CENTRIS_BROKER_FEED_URL", "")
    if not args.search_url or args.search_url == DEFAULT_SEARCH:
        import os

        env_search = os.environ.get("CENTRIS_SEARCH_URL", "")
        if env_search:
            args.search_url = env_search

    registry = load_properties_registry()
    registry_by_uls = {str(item["uls"]): item for item in registry.get("listings", [])}

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        }
    )

    jobs = collect_listing_jobs(args, session, registry)
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

    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "searchUrl": args.search_url,
        "maxListings": args.max_listings,
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
