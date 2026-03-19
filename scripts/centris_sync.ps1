param(
  [string]$SearchUrl = "https://www.centris.ca/fr/propriete~a-vendre?q=H4sIAAAAAAAACk2MsQ6CMBRF_6UzAxIToyuDMSYOYlgIw5PeQmOhpAVNQ_h3X6MD27vn3vMW0RsvTiIViXg6-4LLrQSDXbY_ZEemVind4IrAkOPscYZtHY1dKDoawXaaCB_PUuPDsao5g1zT3aiPv1hT2kxw_1JpGOlLMnO0q-UHLpKnOU1orQusvGPP6A6vJYZJkxFrsh0XMEYP7SOM2OwLMhBrvX4Bb6jOs9sAAAA&sortSeed=1077964681&sort=None&pageSize=20",
  [int]$MaxListings = 8,
  [int]$DelaySeconds = 2,
  [string]$OfficialBrokerFeedUrl = "",
  [string]$OutputJsonPath = "",
  [string]$OutputImagesDir = ""
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Resolve-Path -Path (Join-Path $PSScriptRoot "..")
if ([string]::IsNullOrWhiteSpace($ProjectRoot)) {
  throw "Could not resolve project root from $PSScriptRoot"
}

if ([string]::IsNullOrWhiteSpace($OutputJsonPath)) {
  $OutputJsonPath = (Join-Path $ProjectRoot "data/centris_listings.json")
}

if ([string]::IsNullOrWhiteSpace($OutputImagesDir)) {
  $OutputImagesDir = (Join-Path $ProjectRoot "src/assets/images/proprietes/centris")
}

function Get-IdFromCentrisUrl {
  param([Parameter(Mandatory=$true)][string]$Url)

  # Centris listing URLs end with the ULS id.
  $m = [regex]::Match($Url, "/(\d{5,10})(?:[/?#]|$)")
  if ($m.Success) { return $m.Groups[1].Value }
  return $null
}

function Get-ExtensionFromUrl {
  param([Parameter(Mandatory=$true)][string]$Url)

  $ext = [System.IO.Path]::GetExtension($Url)
  if ([string]::IsNullOrWhiteSpace($ext)) { return ".jpg" }
  if ($ext.Length -gt 5) { return ".jpg" }
  return $ext
}

function Invoke-HttpGet {
  param([Parameter(Mandatory=$true)][string]$Url)

  # Some CDNs return different content depending on headers.
  $headers = @{
    "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"
    "Accept" = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
  }

  return Invoke-WebRequest -Uri $Url -Headers $headers -UseBasicParsing -TimeoutSec 60
}

function Extract-ListingLinks {
  param([Parameter(Mandatory=$true)][string]$Html)

  # Example (from Centris): /fr/propriete~a-vendre.../12854222
  # Capture all such URLs; we'll de-dupe later by id.
  $pattern = 'href="(?<path>/fr/propriete~a-vendre[^"]+?/(?<id>\d{5,10}))"'
  $matches = [regex]::Matches($Html, $pattern)

  $out = New-Object System.Collections.Generic.List[string]
  foreach ($match in $matches) {
    $path = $match.Groups["path"].Value
    if (-not [string]::IsNullOrWhiteSpace($path)) {
      $out.Add(("https://www.centris.ca" + $path))
    }
  }
  return $out
}

function Extract-OgImageAndTitleAndPrice {
  param(
    [Parameter(Mandatory=$true)][string]$PropertyHtml,
    [Parameter(Mandatory=$true)][string]$PropertyUrl
  )

  $ogImage = $null
  $ogTitle = $null

  # OG image / title are usually reliable.
  $ogImageMatch = [regex]::Match($PropertyHtml, '<meta\s+property="og:image"\s+content="([^"]+)"', "IgnoreCase")
  if ($ogImageMatch.Success) { $ogImage = $ogImageMatch.Groups[1].Value }

  $ogTitleMatch = [regex]::Match($PropertyHtml, '<meta\s+property="og:title"\s+content="([^"]+)"', "IgnoreCase")
  if ($ogTitleMatch.Success) { $ogTitle = $ogTitleMatch.Groups[1].Value }

  # Try JSON-LD for price (best-effort).
  $price = $null
  $ldMatches = [regex]::Matches($PropertyHtml, '<script[^>]*type="application/ld\+json"[^>]*>(?<json>[\s\S]*?)</script>', "IgnoreCase")
  foreach ($lm in $ldMatches) {
    $json = $lm.Groups["json"].Value

    # Look for `"price":` in JSON-LD.
    $pMatch = [regex]::Match($json, '"price"\s*:\s*(?<price>[0-9]+(?:\.[0-9]+)?)', "IgnoreCase")
    if ($pMatch.Success) {
      $price = $pMatch.Groups["price"].Value
      break
    }
  }

  return @{
    propertyUrl = $PropertyUrl
    ogTitle = $ogTitle
    ogImage = $ogImage
    price = $price
    id = (Get-IdFromCentrisUrl -Url $PropertyUrl)
  }
}

function Download-File {
  param(
    [Parameter(Mandatory=$true)][string]$Url,
    [Parameter(Mandatory=$true)][string]$DestinationPath
  )

  $parent = Split-Path -Parent $DestinationPath
  if (-not (Test-Path $parent)) {
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
  }

  Invoke-WebRequest -Uri $Url -OutFile $DestinationPath -UseBasicParsing -TimeoutSec 120
}

Write-Host "Centris sync starting..."
Write-Host "SearchUrl: $SearchUrl"

$byId = @{}

if ([string]::IsNullOrWhiteSpace($OfficialBrokerFeedUrl)) {
  $OfficialBrokerFeedUrl = $env:CENTRIS_BROKER_FEED_URL
}

if (-not [string]::IsNullOrWhiteSpace($OfficialBrokerFeedUrl)) {
  Write-Host "Using official broker feed: $OfficialBrokerFeedUrl"
  $feedResp = Invoke-HttpGet -Url $OfficialBrokerFeedUrl
  $feedJson = $null
  try {
    $feedJson = $feedResp.Content | ConvertFrom-Json
  }
  catch {
    throw "Official broker feed URL returned non-JSON content. Please provide a JSON feed or remove OfficialBrokerFeedUrl."
  }

  $listingsArr = $null
  if ($feedJson.PSObject.Properties.Name -contains "listings") {
    $listingsArr = $feedJson.listings
  }
  else {
    $listingsArr = $feedJson
  }

  $tmpIds = New-Object System.Collections.Generic.List[string]
  foreach ($item in $listingsArr) {
    $id = $null
    $propertyUrl = $null

    if ($item.PSObject.Properties.Name -contains "id") { $id = $item.id }
    if (-not $id -and $item.PSObject.Properties.Name -contains "uls") { $id = $item.uls }
    if ($item.PSObject.Properties.Name -contains "propertyUrl") { $propertyUrl = $item.propertyUrl }
    if (-not $propertyUrl -and $item.PSObject.Properties.Name -contains "url") { $propertyUrl = $item.url }

    if (-not $id -and $propertyUrl) { $id = Get-IdFromCentrisUrl -Url $propertyUrl }
    if (-not $id) { continue }
    if (-not $propertyUrl) { continue }

    if (-not $byId.ContainsKey($id)) {
      $byId[$id] = $propertyUrl
      $tmpIds.Add($id) | Out-Null
    }
  }

  if ($tmpIds.Count -eq 0) {
    throw "No usable listings found in official feed JSON. Expected fields like id/uls and propertyUrl/url."
  }

  $ids = @($byId.Keys) | Select-Object -First $MaxListings
  Write-Host ("Found {0} unique listing ids from feed, syncing first {1}..." -f $byId.Keys.Count, $ids.Count)
}
else {
  Write-Host "Scraping public search page..."
  $searchResp = Invoke-HttpGet -Url $SearchUrl
  $searchHtml = $searchResp.Content

  $links = Extract-ListingLinks -Html $searchHtml
  if ($links.Count -eq 0) {
    throw "No Centris listing links found in search HTML. The markup may have changed."
  }

  foreach ($l in $links) {
    $id = Get-IdFromCentrisUrl -Url $l
    if (-not $id) { continue }
    if (-not $byId.ContainsKey($id)) {
      $byId[$id] = $l
    }
  }

  $ids = @($byId.Keys) | Select-Object -First $MaxListings
  Write-Host ("Found {0} unique listing ids, syncing first {1}..." -f $byId.Keys.Count, $ids.Count)
}

$results = New-Object System.Collections.Generic.List[object]

foreach ($id in $ids) {
  $propertyUrl = $byId[$id]
  Write-Host "Fetching: $id"

  Start-Sleep -Seconds $DelaySeconds
  try {
    $resp = Invoke-HttpGet -Url $propertyUrl
    $meta = Extract-OgImageAndTitleAndPrice -PropertyHtml $resp.Content -PropertyUrl $propertyUrl

    $imageFile = $null
    if ($meta.ogImage) {
      $ext = Get-ExtensionFromUrl -Url $meta.ogImage
      $imageFile = ("{0}/{1}{2}" -f $OutputImagesDir, $id, $ext)
      Write-Host ("Downloading image -> {0}" -f $imageFile)
      Download-File -Url $meta.ogImage -DestinationPath $imageFile
    }

    $results.Add([pscustomobject]@{
      id = $meta.id
      propertyUrl = $meta.propertyUrl
      ogTitle = $meta.ogTitle
      price = $meta.price
      imageFile = $imageFile
    }) | Out-Null
  }
  catch {
    Write-Host ("WARN: failed for id {0}: {1}" -f $id, $_.Exception.Message) -ForegroundColor Yellow
    $results.Add([pscustomobject]@{
      id = $id
      propertyUrl = $propertyUrl
      ogTitle = $null
      price = $null
      imageFile = $null
    }) | Out-Null
  }
}

$outObj = [pscustomobject]@{
  generatedAt = (Get-Date).ToString("o")
  searchUrl = $SearchUrl
  maxListings = $MaxListings
  listings = $results
}

if (-not (Test-Path (Split-Path -Parent $OutputJsonPath))) {
  New-Item -ItemType Directory -Path (Split-Path -Parent $OutputJsonPath) -Force | Out-Null
}

$json = $outObj | ConvertTo-Json -Depth 10
Set-Content -Path $OutputJsonPath -Value $json -Encoding UTF8

Write-Host "Centris sync completed."
Write-Host ("Wrote JSON: {0}" -f $OutputJsonPath)
