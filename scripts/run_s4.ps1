param([string[]]$Runs = @('phase2_qwen25_code'), [switch]$Worker)
# S4 judge replay with weaker specifications (scripts/s4_judge_specs.py) in a visible window started through
# WMI, so closing the Claude app does not stop it. GPU work: start it only when no other model run is active.
# Resumable: finished judge calls are cached and skipped. Progress: runs/s4_judge_specs/<run>/progress.json.
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
if (-not $Worker) {
    $command = 'powershell.exe -NoProfile -NoExit -ExecutionPolicy Bypass -File "' + $MyInvocation.MyCommand.Path + '" -Runs ' + ($Runs -join ',') + ' -Worker'
    $result = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine = $command; CurrentDirectory = $root}
    Write-Host ("S4 window started (process {0}, return code {1})." -f $result.ProcessId, $result.ReturnValue)
    return
}
if ($Runs.Count -eq 1 -and $Runs[0] -like '*,*') { $Runs = $Runs[0].Split(',') }
Set-Location -LiteralPath $root
. (Join-Path $PSScriptRoot 'disable_quickedit.ps1')
$env:PYTHONPATH = Join-Path $root 'src'
$env:PYTHONIOENCODING = 'utf-8'
New-Item -ItemType Directory -Force -Path 'runs/s4_judge_specs' | Out-Null
Start-Transcript -Path ('runs/s4_judge_specs/s4_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.log')
try {
    foreach ($run in $Runs) {
        $Host.UI.RawUI.WindowTitle = "GBE S4 judge replay ($run)"
        & (Join-Path $root '.venv/Scripts/python.exe') scripts/s4_judge_specs.py --run $run
        if ($LASTEXITCODE -ne 0) { throw "S4 replay of $run failed with exit code $LASTEXITCODE. Restart this script to resume." }
    }
    $Host.UI.RawUI.WindowTitle = 'GBE S4 judge replay: done'
} finally {
    Stop-Transcript -ErrorAction SilentlyContinue
}
