param([string[]]$Models = @('qwen3.5:9b', 'gemma4:12b'),
      [switch]$Worker)
# Visible queue for the supplemental pilots. For each model in order it waits until the model is
# registered in Ollama, runs its model check, opens the pilot in its own window, and waits for that
# pilot to finish before starting the next model. Finished runs are skipped, so it is safe to restart.
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
if (-not $Worker) {
    $script = $MyInvocation.MyCommand.Path
    $modelList = $Models -join ','
    Start-Process powershell -ArgumentList @('-NoProfile', '-NoExit', '-ExecutionPolicy', 'Bypass', '-File', ('"' + $script + '"'), '-Models', $modelList, '-Worker')
    return
}
if ($Models.Count -eq 1 -and $Models[0] -like '*,*') { $Models = $Models[0].Split(',') }
Set-Location -LiteralPath $root
. (Join-Path $PSScriptRoot 'disable_quickedit.ps1')
$Host.UI.RawUI.WindowTitle = 'GBE model queue (Qwen3.5, then Gemma 4)'
$guard = [System.IO.File]::Open((Join-Path $root 'runs/setup/model_queue.lock'), [System.IO.FileMode]::OpenOrCreate, [System.IO.FileAccess]::ReadWrite, [System.IO.FileShare]::None)
$statePath = Join-Path $root 'runs/setup/model_queue.json'
# phase1_qwen35_pilot stopped at 21 of 80 units on an Ollama repeat-limit abort; it could not resume
# after the abort handling changed the harness, so it continues as _r2 with its response cache copied.
$runIds = @{ 'qwen3.5:9b' = 'phase1_qwen35_pilot_r2'; 'gemma4:12b' = 'phase1_gemma4_pilot' }

function Save-State([string]$Model, [string]$Status, [string]$Detail) {
    @{model=$Model; status=$Status; detail=$Detail; queue=$Models; updated=(Get-Date).ToUniversalTime().ToString('o')} |
        ConvertTo-Json | Set-Content -LiteralPath $statePath -Encoding UTF8
    Write-Host ("[{0}] {1} {2} : {3}" -f (Get-Date -Format 'HH:mm:ss'), $Model, $Status, $Detail)
}
function Run-Finished([string]$Id) {
    $directory = Join-Path $root ('runs/' + $Id)
    $progressPath = Join-Path $directory 'progress.json'
    $manifestPath = Join-Path $directory 'manifest.json'
    if (-not (Test-Path -LiteralPath $progressPath) -or -not (Test-Path -LiteralPath $manifestPath)) { return $false }
    $progress = Get-Content -LiteralPath $progressPath -Raw | ConvertFrom-Json
    $manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
    return ($progress.percent -ge 100 -and $manifest.end_time -and (Test-Path -LiteralPath (Join-Path $directory 'tests.csv')))
}

try {
    Start-Transcript -Path ('runs/setup/model_queue_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.log')
    foreach ($model in $Models) {
        $runId = $runIds[$model]
        if (-not $runId) { throw "No run ID defined for $model" }
        if (Run-Finished $runId) { Save-State $model 'DONE' "$runId already finished; skipped."; continue }
        while ($true) {
            $tags = (Invoke-RestMethod http://localhost:11434/api/tags).models.name
            if ($model -in $tags) { break }
            Save-State $model 'WAITING_FOR_IMPORT' 'Model not registered in Ollama yet; the installer window must finish first.'
            Start-Sleep -Seconds 30
        }
        $failurePath = Join-Path $root ('runs/' + $runId + '/worker_error.json')
        $active = Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'python.exe' -and $_.CommandLine -match [regex]::Escape($runId) }
        if ($active) {
            Save-State $model 'RUNNING' "A worker for $runId is already running; watching it instead of starting another."
        } else {
            Save-State $model 'CHECKING' 'Running the model check (thinking off, 8192 context, GPU residency).'
            & .\.venv\Scripts\python.exe scripts/model_check.py --model $model
            if ($LASTEXITCODE -ne 0) { throw "Model check failed for $model" }
            $checks = Get-Content -LiteralPath runs/setup/model_check.json -Raw | ConvertFrom-Json
            $row = $checks.models.$model
            if (-not $row.fully_on_gpu) { Save-State $model 'WARNING' 'Model did not load fully onto the GPU; continuing and recording residency.' }
            if ($row.thinking_returned) { Save-State $model 'WARNING' 'Model returned reasoning text despite think:false; continuing, the harness strips and counts it.' }
            Copy-Item -LiteralPath runs/setup/model_check.json -Destination configs/models.json
            # A failure file from an earlier stopped attempt would otherwise be read before the new
            # window has a chance to remove it.
            if (Test-Path -LiteralPath $failurePath) { Remove-Item -LiteralPath $failurePath }
            Save-State $model 'STARTING' "Opening the pilot window for $runId."
            & .\scripts\run_pilot.ps1 -RunId $runId -Model $model
            Start-Sleep -Seconds 20
        }
        while (-not (Run-Finished $runId)) {
            if (Test-Path -LiteralPath $failurePath) {
                throw ("$runId stopped: " + (Get-Content -LiteralPath $failurePath -Raw) + " Restart this queue to resume.")
            }
            $progressPath = Join-Path $root ('runs/' + $runId + '/progress.json')
            $detail = 'Pilot window opened; waiting for first progress.'
            if (Test-Path -LiteralPath $progressPath) {
                $p = Get-Content -LiteralPath $progressPath -Raw | ConvertFrom-Json
                $detail = "{0} of {1} units ({2}%), ETA {3} min" -f $p.done, $p.total, [math]::Round($p.percent,1), [math]::Round($p.eta_seconds/60,0)
            }
            Save-State $model 'RUNNING' $detail
            Start-Sleep -Seconds 60
        }
        Save-State $model 'DONE' "$runId finished."
    }
    Save-State 'all' 'DONE' 'All queued supplemental pilots finished. Verification and the Phase 1 report remain pending.'
} catch {
    Save-State 'queue' 'FAILED' $_.Exception.Message
    throw
} finally {
    Stop-Transcript -ErrorAction SilentlyContinue
    $guard.Dispose()
}
