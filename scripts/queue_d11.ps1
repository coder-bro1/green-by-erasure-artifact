param([string]$Variant = 'open', [switch]$Plan, [switch]$Worker)
# D11 Codex queue (docs/PHASE2_SPEC.md section 8.6). Started without -Worker, it relaunches itself through
# WMI as a visible window that is not a child of the calling app, so closing Claude does not stop it.
# The worker runs `scripts/d11.py queue`: tasks one at a time, sleeping through usage-limit resets.
# Restarting resumes; finished tasks are skipped. Progress: runs/d11/progress.json.
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
if (-not $Worker) {
    $command = 'powershell.exe -NoProfile -NoExit -ExecutionPolicy Bypass -File "' + $MyInvocation.MyCommand.Path + '" -Variant ' + $Variant + $(if ($Plan) { ' -Plan' } else { '' }) + ' -Worker'
    $result = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine = $command; CurrentDirectory = $root}
    Write-Host ("D11 Codex queue window started (process {0}, return code {1})." -f $result.ProcessId, $result.ReturnValue)
    return
}
Set-Location -LiteralPath $root
. (Join-Path $PSScriptRoot 'disable_quickedit.ps1')
$Host.UI.RawUI.WindowTitle = $(if ($Plan) { 'GBE D11 Codex plan' } else { "GBE D11 Codex queue ($Variant)" })
$env:PYTHONPATH = Join-Path $root 'src'
Start-Transcript -Path ('runs/d11/queue_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.log')
try {
    if ($Plan) { & (Join-Path $root '.venv/Scripts/python.exe') scripts/d11.py plan }
    else { & (Join-Path $root '.venv/Scripts/python.exe') scripts/d11.py queue --variant $Variant }
    if ($LASTEXITCODE -ne 0) { throw "D11 queue stopped with exit code $LASTEXITCODE. Restart this script to resume." }
} finally {
    Stop-Transcript -ErrorAction SilentlyContinue
}
