# Centris periodic sync

Downloads **full photo galleries** from Centris for each listing in `data/properties.json`, generates a **1200×630** social share image (`og-share.jpg`) per property, and writes sync metadata to `data/centris_listings.json`.

## Files generated

- `data/centris_listings.json`
- `src/assets/images/proprietes/<uls-id>/01.jpg`, `02.jpg`, …
- `src/assets/images/proprietes/<uls-id>/og-share.jpg` (Open Graph / Twitter card)
- `src/assets/images/proprietes/<uls-id>/manifest.json`
- `src/assets/images/proprietes/<uls-id>.jpg` (hero copy for listing cards)

## Property page URLs (SEO)

Listings live at:

```text
/ca/qc/{city}/{sector}/{street}/
```

Example:

```text
https://chiassondefrancesco.ca/ca/qc/sherbrooke/les-nations/31-rue-king-o-app-305/
```

Legacy `prop-*.html` URLs redirect to the new paths.

## Run manually (Python)

From the project root:

```bash
pip install -r scripts/requirements.txt
python scripts/centris_sync.py --sync-registry --max-listings 12
```

Search-page mode (without registry):

```bash
python scripts/centris_sync.py --max-listings 8
```

Official broker feed:

```bash
export CENTRIS_BROKER_FEED_URL="https://..."
python scripts/centris_sync.py --official-feed-url "$CENTRIS_BROKER_FEED_URL"
```

## GitHub Actions (recommended)

The workflow `.github/workflows/centris-sync.yml` runs daily and can also be triggered manually from the **Actions** tab.

It will:

1. Sync all listings in `data/properties.json`
2. Download full galleries + 1200×630 share images
3. Commit and push changes back to `main`

### Optional repository configuration

| Name | Type | Purpose |
|------|------|---------|
| `CENTRIS_BROKER_FEED_URL` | Secret | Official Centris broker JSON feed |
| `CENTRIS_SEARCH_URL` | Variable | Custom Centris search URL (search-page mode only) |

### Manual run

GitHub → **Actions** → **Sync Centris listing images** → **Run workflow**

## Migrate / rebuild property pages

After editing `data/properties.json`:

```bash
python scripts/migrate_property_pages.py
```

This injects the gallery + share UI and updates SEO paths/canonicals.

## Scheduling (Windows Task Scheduler)

```powershell
python scripts/centris_sync.py --sync-registry --max-listings 12
```

## Notes / limitations

- Centris HTML can change. Gallery extraction uses `window.MosaicPhotoUrls`.
- Image URLs above 1260px wide may return empty payloads; the script caps sizes safely.
- The PowerShell script `centris_sync.ps1` remains for local Windows use but GitHub Actions uses `centris_sync.py`.
