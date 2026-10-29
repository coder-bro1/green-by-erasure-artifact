param([switch]$Worker)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
if (-not $Worker) {
    $script = $MyInvocation.MyCommand.Path
    Start-Process powershell -ArgumentList @('-NoExit', '-ExecutionPolicy', 'Bypass', '-File', ('"' + $script + '"'), '-Worker')
    return
}
Set-Location -LiteralPath $root
New-Item -ItemType Directory -Force runs/setup | Out-Null
Start-Transcript -Path (Join-Path 'runs/setup' ('pull_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.log'))
& .\.venv\Scripts\python.exe scripts/pull_models.py
if ($LASTEXITCODE -ne 0) { throw 'Model download failed' }
Stop-Transcript
