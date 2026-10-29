param([string[]]$Runs = @('phase2_qwen25_code', 'phase2_qwen35_code', 'phase2_gemma4_code',
                          'phase2_qwen25_spec', 'phase2_qwen25_seed1', 'phase2_qwen25_seed2', 'phase2_qwen25_seed3'),
      [switch]$Worker)
# Phase 2 queue (docs/PHASE2_SPEC.md section 7). Started without -Worker, it launches itself through WMI
# as a separate visible window that is not a child of the calling app, so closing Claude or a terminal
# does not stop it. The worker runs each run ID in order in this window, with live progress, then runs
# scripts/verify_run.py on it; a failed run or failed check stops the queue. Restarting resumes: finished
# units and runs are skipped, cached model answers are reused.
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
if (-not $Worker) {
    $command = 'powershell.exe -NoProfile -NoExit -ExecutionPolicy Bypass -File "' + $MyInvocation.MyCommand.Path +
               '" -Runs ' + ($Runs -join ',') + ' -Worker'
    $result = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine = $command; CurrentDirectory = $root}
    Write-Host ("Phase 2 queue window started (process {0}, return code {1})." -f $result.ProcessId, $result.ReturnValue)
    return
}
if ($Runs.Count -eq 1 -and $Runs[0] -like '*,*') { $Runs = $Runs[0].Split(',') }
Set-Location -LiteralPath $root
. (Join-Path $PSScriptRoot 'disable_quickedit.ps1')
$state = Join-Path $root 'runs/phase2_queue/state.json'
New-Item -ItemType Directory -Force -Path (Split-Path $state) | Out-Null
$guard = [System.IO.File]::Open((Join-Path $root 'runs/phase2_queue/queue.lock'), [System.IO.FileMode]::OpenOrCreate,
                                [System.IO.FileAccess]::ReadWrite, [System.IO.FileShare]::None)
$python = Join-Path $root '.venv/Scripts/python.exe'
$env:PYTHONPATH = Join-Path $root 'src'

function Save-State([string]$Run, [string]$Status, [string]$Detail) {
    @{run = $Run; status = $Status; detail = $Detail; queue = $Runs; updated = (Get-Date).ToUniversalTime().ToString('o')} |
        ConvertTo-Json | Set-Content -LiteralPath $state -Encoding UTF8
    Write-Host ("[{0}] {1} {2}: {3}" -f (Get-Date -Format 'HH:mm:ss'), $Run, $Status, $Detail)
}
function Run-Finished([string]$Id) {
    $dir = Join-Path $root ('runs/' + $Id)
    if (-not (Test-Path -LiteralPath (Join-Path $dir 'tests.csv'))) { return $false }
    $manifest = Get-Content -LiteralPath (Join-Path $dir 'manifest.json') -Raw | ConvertFrom-Json
    return [bool]$manifest.end_time
}
function Verified([string]$Id) {
    $path = Join-Path $root ('runs/' + $Id + '/verification.json')
    if (-not (Test-Path -LiteralPath $path)) { return $false }
    $v = Get-Content -LiteralPath $path -Raw | ConvertFrom-Json
    return ($v.section8_all_pass -and $v.'P1-c'.pass -and $v.'P1-e'.pass -and $v.'P1-a'.pass)
}

Start-Transcript -Path ('runs/phase2_queue/queue_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.log')
try {
    foreach ($run in $Runs) {
        $Host.UI.RawUI.WindowTitle = "GBE Phase 2 queue: $run"
        if (-not (Run-Finished $run)) {
            Save-State $run 'RUNNING' 'Model runs in progress; see this window or runs/<run>/progress.json.'
            & $python -m gbe.runner --run-id $run
            if ($LASTEXITCODE -ne 0) { throw "$run stopped with exit code $LASTEXITCODE. Restart this queue to resume." }
        }
        if (-not (Verified $run)) {
            Save-State $run 'VERIFYING' 'Running scripts/verify_run.py (CPU only).'
            & $python scripts/verify_run.py --run-id $run | Out-File -Encoding utf8 (Join-Path $root ('runs/' + $run + '/verify_stdout.json'))
            & $python scripts/go_no_go.py --run-id $run | Out-Null
            if (-not (Verified $run)) { throw "$run failed verification; see runs/$run/verification.json. The queue stops here." }
        }
        Save-State $run 'DONE' 'Run finished and verified.'
    }
    Save-State 'all' 'DONE' 'All queued Phase 2 runs finished and verified. Mutation analysis and reviews remain.'
} catch {
    Save-State 'queue' 'FAILED' $_.Exception.Message
    throw
} finally {
    Stop-Transcript -ErrorAction SilentlyContinue
    $guard.Dispose()
}
