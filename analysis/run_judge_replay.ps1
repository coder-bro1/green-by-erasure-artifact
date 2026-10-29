param([string[]]$Runs = @('phase1_pilot', 'phase1_qwen35_pilot_r2', 'phase1_gemma4_pilot'),
      [string[]]$Variants = @('v2a', 'v2b'),
      [switch]$Worker)
# Opens a separate window and replays the P4 judge with the new prompt variants on every finished
# pilot run, one after another. Resumable: finished cases are skipped. Start it only after all
# pilots have finished, so it does not compete with them for the GPU.
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
if (-not $Worker) {
    Start-Process powershell -ArgumentList @('-NoProfile', '-NoExit', '-ExecutionPolicy', 'Bypass', '-File',
        ('"' + $MyInvocation.MyCommand.Path + '"'), '-Runs', ($Runs -join ','), '-Variants', ($Variants -join ','), '-Worker')
    return
}
if ($Runs.Count -eq 1 -and $Runs[0] -like '*,*') { $Runs = $Runs[0].Split(',') }
if ($Variants.Count -eq 1 -and $Variants[0] -like '*,*') { $Variants = $Variants[0].Split(',') }
Set-Location -LiteralPath $root
. (Join-Path $root 'scripts/disable_quickedit.ps1')
$Host.UI.RawUI.WindowTitle = 'GBE judge replay'
Start-Transcript -Path ('runs/setup/judge_replay_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.log')
try {
    foreach ($variant in $Variants) {
        foreach ($run in $Runs) {
            & .\.venv\Scripts\python.exe analysis/judge_replay.py replay --run $run --variant $variant
            if ($LASTEXITCODE -ne 0) { throw "Replay failed for $run $variant; rerun this script to resume." }
        }
    }
    $scoreArgs = @('analysis/judge_replay.py', 'score') + ($Runs | ForEach-Object { @('--run', $_) })
    & .\.venv\Scripts\python.exe @scoreArgs
} finally {
    Stop-Transcript
}
