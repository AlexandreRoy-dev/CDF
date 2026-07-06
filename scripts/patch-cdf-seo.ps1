# Patch CDF site: footer network links, basic SEO meta, sitemap
$Root = "c:\Users\Alex\OneDrive - Codesk\01. Roy Marketing\Clients\Chiasson De Francesco\CDF"
$Base = "https://chiassondefrancesco.ca"

$OldServices = @'
        <div class="lg:col-span-3">
          <h4 class="text-white font-heading font-bold text-lg mb-6 tracking-wide">Services</h4>
          <ul class="space-y-3 text-sm font-medium">
            <li><a href="index.html#contact" class="hover:text-brand-red transition-colors">Achat résidentiel</a></li>
            <li><a href="index.html#contact" class="hover:text-brand-red transition-colors">Vente de propriété</a></li>
            <li><a href="index.html#contact" class="hover:text-brand-red transition-colors">Investissement</a></li>
            <li><a href="index.html#contact" class="hover:text-brand-red transition-colors">Évaluation marchande</a></li>
          </ul>
        </div>
'@

$NewNetwork = @'
        <div class="lg:col-span-3">
          <h4 class="text-white font-heading font-bold text-lg mb-6 tracking-wide">Notre réseau</h4>
          <ul class="space-y-3 text-sm font-medium">
            <li><a href="https://immobiliermaison.com/" target="_blank" rel="noopener noreferrer" class="hover:text-brand-red transition-colors">immobiliermaison.com</a></li>
            <li><a href="https://vendremamaisonsherbrooke.com/" target="_blank" rel="noopener noreferrer" class="hover:text-brand-red transition-colors">vendremamaisonsherbrooke.com</a></li>
            <li><a href="https://vendremamaisonestrie.com/" target="_blank" rel="noopener noreferrer" class="hover:text-brand-red transition-colors">vendremamaisonestrie.com</a></li>
            <li><a href="https://vendremonplex.com/" target="_blank" rel="noopener noreferrer" class="hover:text-brand-red transition-colors">vendremonplex.com</a></li>
            <li><a href="https://realestatesherbrooke.com/" target="_blank" rel="noopener noreferrer" class="hover:text-brand-red transition-colors">realestatesherbrooke.com</a></li>
          </ul>
        </div>
'@

$OldAddress = @'
                <span class="block text-white font-semibold">RE/MAX D'ABORD</span>
                Sherbrooke, Québec
'@

$NewAddress = @'
                <span class="block text-white font-semibold">RE/MAX D'ABORD</span>
                <address class="not-italic">157 boul. Jacques-Cartier Sud<br>Sherbrooke, QC J1J 2Z4</address>
'@

function Get-PageUrl($filePath) {
    $rel = $filePath.Substring($Root.Length + 1).Replace('\', '/')
    if ($rel -eq 'index.html') { return "$Base/" }
    return "$Base/$rel"
}

$files = Get-ChildItem -Path $Root -Filter "*.html" -Recurse | Where-Object { $_.FullName -notmatch '\\.git\\' }
$updated = 0

foreach ($file in $files) {
    $content = [System.IO.File]::ReadAllText($file.FullName)
    $original = $content

    $content = $content.Replace($OldServices, $NewNetwork)
    $content = $content.Replace($OldAddress, $NewAddress)
    $content = $content -replace '<html lang="fr"', '<html lang="fr-CA"', 1

    if ($content -notmatch 'rel="canonical"' -and $file.Name -ne 'index.html' -or ($file.Name -eq 'index.html' -and $file.DirectoryName -ne $Root)) {
        if ($content -match '<title>([^<]+)</title>') {
            $title = $Matches[1].Trim()
            $desc = ("Équipe Chiasson de Francesco, courtiers immobiliers RE/MAX à Sherbrooke et en Estrie. " + $title).Substring(0, [Math]::Min(160, ("Équipe Chiasson de Francesco, courtiers immobiliers RE/MAX à Sherbrooke et en Estrie. " + $title).Length))
            $url = Get-PageUrl $file.FullName
            $seo = @"

    <meta name="description" content="$desc">
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
    <meta name="author" content="Équipe Chiasson de Francesco">
    <link rel="canonical" href="$url">
    <meta property="og:type" content="website">
    <meta property="og:url" content="$url">
    <meta property="og:site_name" content="Chiasson de Francesco">
    <meta property="og:title" content="$title">
    <meta property="og:description" content="$desc">
    <meta property="og:image" content="$Base/src/assets/pierre-olivier-chiasson.webp">
    <meta property="og:locale" content="fr_CA">
"@
            $content = $content.Replace('<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">', '<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">' + $seo)
        }
    }

    if ($content -ne $original) {
        [System.IO.File]::WriteAllText($file.FullName, $content)
        $updated++
        Write-Host "updated: $($file.FullName.Substring($Root.Length + 1))"
    }
}

# Sitemap
$urls = $files | ForEach-Object { Get-PageUrl $_.FullName } | Sort-Object
$sitemap = "<?xml version=`"1.0`" encoding=`"UTF-8`"?>`n<urlset xmlns=`"http://www.sitemaps.org/schemas/sitemap/0.9`">`n"
foreach ($file in ($files | Sort-Object FullName)) {
    $url = Get-PageUrl $file.FullName
    $priority = if ($file.Name -eq 'index.html' -and $file.DirectoryName -eq $Root) { '1.0' } elseif ($file.Name -eq 'merci.html') { '0.3' } else { '0.7' }
    $sitemap += "  <url><loc>$url</loc><priority>$priority</priority></url>`n"
}
$sitemap += "</urlset>`n"
[System.IO.File]::WriteAllText("$Root\sitemap.xml", $sitemap)

$robots = "User-agent: *`nAllow: /`n`nSitemap: https://chiassondefrancesco.ca/sitemap.xml`n"
[System.IO.File]::WriteAllText("$Root\robots.txt", $robots)

Write-Host "wrote sitemap.xml and robots.txt"
Write-Host "done - $updated files patched"
