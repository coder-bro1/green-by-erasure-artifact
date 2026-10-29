param(
    [string]$DownloadDirectory,
    [Parameter(Mandatory=$true)][string]$ModelDirectory,
    [ValidateSet('all','qwen3.5:9b','gemma4:12b')][string]$Model = 'all',
    [switch]$NoTranscript,
    [switch]$Worker
)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
if (-not $DownloadDirectory) { $DownloadDirectory = Join-Path $root 'downloads' }
$DownloadDirectory = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($DownloadDirectory)
$ModelDirectory = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($ModelDirectory)
if (-not $Worker) {
    $script = $MyInvocation.MyCommand.Path
    Start-Process powershell -ArgumentList @('-NoProfile', '-NoExit', '-ExecutionPolicy', 'Bypass', '-File', ('"' + $script + '"'), '-DownloadDirectory', ('"' + $DownloadDirectory + '"'), '-ModelDirectory', ('"' + $ModelDirectory + '"'), '-Model', $Model, '-Worker')
    return
}
Set-Location -LiteralPath $root
if (-not $NoTranscript) {
    Start-Transcript -Path ('runs/setup/manual_import_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.log')
}
Write-Host "Download directory: $DownloadDirectory"
Write-Host "Ollama model store: $ModelDirectory"
Write-Host 'This must be the storage directory used by the running Ollama server.'
$files = Get-Content -LiteralPath configs/model_downloads.json -Raw | ConvertFrom-Json
if ($Model -ne 'all') { $files = @($files | Where-Object { $_.model -eq $Model }) }
foreach ($file in $files) {
    $source = Join-Path $DownloadDirectory $file.download_name
    if (-not (Test-Path -LiteralPath $source -PathType Leaf)) { throw "Missing file: $source" }
    if ((Get-Item -LiteralPath $source).Length -ne $file.size) { throw "Incomplete download: $source" }
    Write-Host "Verifying $($file.download_name)..."
    if ((Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash.ToLowerInvariant() -ne $file.sha256) {
        throw "SHA-256 mismatch: $source"
    }
}
$blobRoot = Join-Path $ModelDirectory 'blobs'
New-Item -ItemType Directory -Force -Path $blobRoot | Out-Null
foreach ($file in $files) {
    $source = Join-Path $DownloadDirectory $file.download_name
    $destination = Join-Path $blobRoot $file.filename
    if (Test-Path -LiteralPath $destination) {
        if ((Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash.ToLowerInvariant() -ne $file.sha256) {
            throw "Existing cache file has a different hash: $destination"
        }
    } else {
        Write-Host "Installing $($file.download_name)..."
        Copy-Item -LiteralPath $source -Destination $destination
    }
}
foreach ($tag in @($files.model | Select-Object -Unique)) {
    & ollama pull $tag
    if ($LASTEXITCODE -ne 0) { throw "Model registration failed: $tag" }
}
& ollama list
if (-not $NoTranscript) { Stop-Transcript }
