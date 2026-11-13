$ErrorActionPreference = 'Stop'
$repo = 'ren148056842/MGAT-FinRL'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    if ((git status --porcelain).Length -gt 0) { throw 'Commit reviewed changes before publishing.' }
    if ((git branch --show-current).Trim() -ne 'main') { throw 'Expected main branch.' }
    $url = 'https://github.com/' + $repo + '.git'
    $remote = git remote get-url origin 2>$null
    if ($LASTEXITCODE -ne 0) { git remote add origin $url }
    elseif ($remote.Trim() -ne $url) { throw 'Unexpected origin; refusing to publish.' }
    git -c http.sslBackend=openssl push origin main
    if ($LASTEXITCODE -ne 0) { throw 'Push failed; check authentication and remote contents.' }
    git -c http.sslBackend=openssl push origin refs/tags/v1.0.0
    if ($LASTEXITCODE -ne 0) { throw 'Tag push failed; no forced replacement attempted.' }
    if (Get-Command gh -ErrorAction SilentlyContinue) {
        gh repo edit $repo --description 'Research companion for multi-relational graph attention Transformer forecasts and reinforcement learning portfolio strategies.' --add-topic graph-attention-networks --add-topic transformers --add-topic reinforcement-learning --add-topic portfolio-optimization --add-topic reproducible-research
        if ($LASTEXITCODE -ne 0) { throw 'Repository metadata update failed.' }
    } else {
        Write-Warning 'GitHub CLI is unavailable; description and topics still require configuration.'
    }
    Write-Host 'Published main and v1.0.0. Verify a fresh remote checkout before any source deletion.'
} finally { Pop-Location }
