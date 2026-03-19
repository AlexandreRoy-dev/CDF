# Centris periodic sync (PowerShell)

This script pulls the Centris public search page HTML, extracts listing URLs, then fetches each listing page to grab:

- `og:image` (main image)
- `og:title` (best-effort title)
- `price` (best-effort, from JSON-LD if present)

It downloads images locally and writes `data/centris_listings.json`.

## Files generated

- `data/centris_listings.json`
- `src/assets/images/proprietes/centris/<id>.<ext>`

## Run manually

From the project root:

```powershell
pwsh -ExecutionPolicy Bypass -File .\scripts\centris_sync.ps1 -MaxListings 8
```

If you want to use the default search URL already embedded in the script, you can omit `-SearchUrl`.

### Optional: official broker feed

If you have an official Centris broker feed URL (JSON), you can pass it with:

```powershell
pwsh -ExecutionPolicy Bypass -File .\scripts\centris_sync.ps1 -OfficialBrokerFeedUrl "https://..." -MaxListings 8
```

Or set an environment variable:

- `CENTRIS_BROKER_FEED_URL`

## Scheduling (Windows Task Scheduler)

1. Open **Task Scheduler**
2. Create **Task**
3. **General**: set a user account that has permission to write to the project folder
4. **Triggers**: set frequency (ex: once per day)
5. **Actions**: Start a program
   - Program/script: `powershell.exe`
   - Add arguments:
     - `-ExecutionPolicy Bypass -File "C:\Users\Alex\OneDrive - Codesk\01. Roy Marketing\Clients\Chiasson De Francesco\CDF\scripts\centris_sync.ps1" -MaxListings 8`

## Notes / limitations

- Centris HTML can change. If no listing links are found, the regex may need adjustment.
- Image URLs are downloaded from each listing’s `og:image`.
- This script only downloads images + outputs JSON; it does not automatically rewrite `proprietes.html`.
