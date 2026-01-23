$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$ApiBase = if ($env:PULSO_API_BASE) { $env:PULSO_API_BASE } else { "http://localhost:8000" }
$HealthUrl = "$ApiBase/api/health"
$MessageUrl = "$ApiBase/api/message"

# Ler PULSO_API_KEY do .env (se existir)
$ApiKey = ""
$EnvPath = Join-Path $Root ".env"
if (Test-Path $EnvPath) {
  $line = (Get-Content $EnvPath | Where-Object { $_ -match '^PULSO_API_KEY=' } | Select-Object -First 1)
  if ($line) { $ApiKey = $line.Substring("PULSO_API_KEY=".Length).Trim() }
}

Write-Host "[verify] Using API_BASE=$ApiBase"
if ($ApiKey -ne "") {
  Write-Host "[verify] PULSO_API_KEY is set (protected mode)"
} else {
  Write-Host "[verify] PULSO_API_KEY is empty (dev mode)"
}

Write-Host "[verify] Starting docker compose (detached)..."
docker compose up -d --build | Out-Null

Write-Host "[verify] Waiting for health: $HealthUrl"
$ok = $false
for ($i=0; $i -lt 40; $i++) {
  try {
    $resp = Invoke-WebRequest -UseBasicParsing -Uri $HealthUrl -Method GET -TimeoutSec 3
    if ($resp.StatusCode -eq 200) { $ok = $true; break }
  } catch {}
  Start-Sleep -Seconds 1
}
if (-not $ok) { throw "[verify] ERROR: health did not become ready" }

Write-Host "[verify] Checking /api/health response shape..."
$health = Invoke-RestMethod -Uri $HealthUrl -Method GET -TimeoutSec 5
if (-not $health.status) { throw "[verify] ERROR: health missing status" }
if (-not $health.service) { throw "[verify] ERROR: health missing service" }
if (-not $health.version) { throw "[verify] ERROR: health missing version" }
Write-Host ("[verify] health: " + ($health | ConvertTo-Json -Compress))

Write-Host "[verify] Checking X-Request-Id header on /api/message..."
$headers = @{ "Content-Type" = "application/json" }
if ($ApiKey -ne "") { $headers["X-API-Key"] = $ApiKey }

$resp2 = Invoke-WebRequest -UseBasicParsing -Uri $MessageUrl -Method POST -Headers $headers -Body '{"message":"verify"}' -TimeoutSec 10
if (-not $resp2.Headers["X-Request-Id"]) { throw "[verify] ERROR: missing X-Request-Id header" }

if ($ApiKey -ne "") {
  Write-Host "[verify] Expect 401 without key..."
  try {
    Invoke-WebRequest -UseBasicParsing -Uri $MessageUrl -Method POST -Headers @{ "Content-Type"="application/json" } -Body '{"message":"no-key"}' -TimeoutSec 10 | Out-Null
    throw "[verify] ERROR: expected 401 without key, got 200"
  } catch {
    if ($_.Exception.Response -and $_.Exception.Response.StatusCode.value__ -ne 401) {
      throw "[verify] ERROR: expected 401 without key, got $($_.Exception.Response.StatusCode.value__)"
    }
  }

  Write-Host "[verify] Expect 200 with key..."
  $resp3 = Invoke-WebRequest -UseBasicParsing -Uri $MessageUrl -Method POST -Headers $headers -Body '{"message":"with-key"}' -TimeoutSec 10
  if ($resp3.StatusCode -ne 200) { throw "[verify] ERROR: expected 200 with key" }
} else {
  Write-Host "[verify] Dev mode: expect 200 without key..."
  $respDev = Invoke-WebRequest -UseBasicParsing -Uri $MessageUrl -Method POST -Headers @{ "Content-Type"="application/json" } -Body '{"message":"dev"}' -TimeoutSec 10
  if ($respDev.StatusCode -ne 200) { throw "[verify] ERROR: expected 200 in dev mode" }
}

Write-Host "[verify] OK — smoke checks passed."
