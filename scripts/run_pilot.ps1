param([string]$RunId = 'phase1_pilot',
      [ValidateSet('qwen2.5-coder:7b-instruct','qwen3.5:9b','gemma4:12b')][string]$Model = 'qwen2.5-coder:7b-instruct',
      [switch]$Worker)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
if (-not $Worker) {
    $script = $MyInvocation.MyCommand.Path
    Start-Process powershell -ArgumentList @('-NoProfile', '-NoExit', '-ExecutionPolicy', 'Bypass', '-File', ('"' + $script + '"'), '-RunId', $RunId, '-Model', $Model, '-Worker')
    return
}
Set-Location -LiteralPath $root
. (Join-Path $PSScriptRoot 'disable_quickedit.ps1')
$runDirectory = Join-Path $root ('runs/' + $RunId)
New-Item -ItemType Directory -Force -Path $runDirectory | Out-Null
Start-Transcript -Path (Join-Path $runDirectory ('pilot_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.log'))
try {
    $failurePath = Join-Path $runDirectory 'worker_error.json'
    if (Test-Path -LiteralPath $failurePath) { Remove-Item -LiteralPath $failurePath }
    . .\.venv\Scripts\Activate.ps1
    if ($Model -eq 'qwen2.5-coder:7b-instruct') {
        & (Join-Path $root '.venv/Scripts/python.exe') -m gbe.runner --run-id $RunId
    } else {
        & (Join-Path $root '.venv/Scripts/python.exe') scripts/model_pilot.py --model $Model --run-id $RunId
    }
    if ($LASTEXITCODE -ne 0) { throw "Pilot stopped with exit code $LASTEXITCODE. Restart the same RunId to resume." }
} catch {
    @{error=$_.Exception.Message; updated=(Get-Date).ToUniversalTime().ToString('o')} |
        ConvertTo-Json | Set-Content -LiteralPath (Join-Path $runDirectory 'worker_error.json') -Encoding UTF8
    Write-Host ($_ | Out-String)
    throw
} finally {
    Stop-Transcript
}
