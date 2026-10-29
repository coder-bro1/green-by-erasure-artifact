param([switch]$Worker)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
if (-not $Worker) {
    $script = $MyInvocation.MyCommand.Path
    Start-Process powershell -ArgumentList @('-NoExit', '-ExecutionPolicy', 'Bypass', '-File', ('"' + $script + '"'), '-Worker')
    return
}
Set-Location -LiteralPath $root
Start-Transcript -Path ('runs/setup/model_check_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.log')
& .\.venv\Scripts\python.exe scripts/model_check.py
if ($LASTEXITCODE -ne 0) { throw 'Model check failed; see transcript and runs/setup/model_check.json' }
Stop-Transcript
