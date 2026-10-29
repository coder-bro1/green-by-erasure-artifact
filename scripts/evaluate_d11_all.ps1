param([switch]$Worker)
# Evaluate every D11 arm in a visible window that is independent of the Claude app (started through WMI).
# CPU only, below-normal priority (set by d11_evaluate.py). An arm whose evaluation.json is newer than both
# the evaluator script and its newest session result is skipped, so restarting resumes at the next arm.
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
if (-not $Worker) {
    $command = 'powershell.exe -NoProfile -NoExit -ExecutionPolicy Bypass -File "' + $MyInvocation.MyCommand.Path + '" -Worker'
    $result = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine = $command; CurrentDirectory = $root}
    Write-Host ("D11 evaluation window started (process {0}, return code {1})." -f $result.ProcessId, $result.ReturnValue)
    return
}
Set-Location -LiteralPath $root
. (Join-Path $PSScriptRoot 'disable_quickedit.ps1')
$env:PYTHONPATH = Join-Path $root 'src'
$env:PYTHONIOENCODING = 'utf-8'
$arms = @('gpt-6.1-sol_medium', 'gpt-6.1-sol_medium_frozen', 'gpt-6.1-sol_medium_report', 'gpt-6.1-sol_medium_frozen_disguised',
          'gpt-6-luna_high', 'gpt-6-luna_high_frozen', 'gpt-6-luna_high_report',
          'gpt-6.1-sol_medium_frozen_quixbugs', 'gpt-6.1-sol_medium_report_quixbugs',
          'claude-opus-5-5_medium_frozen', 'claude-opus-5-5_medium_report',
          'claude-opus-5-5_medium_frozen_disguised', 'claude-opus-5-5_medium_frozen_quixbugs')
# An arm is evaluated only when every task of its manifest has a finished (or time-limited) session.
$complete = @'
import json, sys
from pathlib import Path
arm = Path('runs/d11') / sys.argv[1]
name = sys.argv[1]
variant = 'open' if name.count('_') < 2 else name.split('_')[2]
taskset = name.split('_')[3] if name.count('_') >= 3 else 'humanevalfix'
manifest = Path('runs/d11') / ('manifest.json' if variant == 'open' and taskset == 'humanevalfix' else
                               f'manifest_{variant}.json' if taskset == 'humanevalfix' else f'manifest_{variant}_{taskset}.json')
tasks = json.loads(manifest.read_text(encoding='utf-8'))['tasks']
done = 0
for t in tasks:
    d = arm / f"{t['order']:02d}_{t['folder']}"
    statuses = [json.loads(p.read_text(encoding='utf-8'))['status'] for p in d.glob('attempt*/result.json')] if d.exists() else []
    done += any(s in ('FINISHED', 'TIME_LIMIT') for s in statuses)
sys.exit(0 if done == len(tasks) else 1)
'@
$evaluator = Get-Item (Join-Path $root 'scripts/d11_evaluate.py')
Start-Transcript -Path ('runs/d11/evaluate_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.log')
try {
    $i = 0
    foreach ($arm in $arms) {
        $i++
        $Host.UI.RawUI.WindowTitle = "GBE D11 evaluation: arm $i of $($arms.Count) ($arm)"
        $dir = Join-Path $root ('runs/d11/' + $arm)
        if (-not (Test-Path $dir)) { Write-Host "[$arm] no sessions yet; skipped."; continue }
        $complete | & (Join-Path $root '.venv/Scripts/python.exe') - $arm
        if ($LASTEXITCODE -ne 0) { Write-Host "[$arm] Codex sessions not complete yet; skipped."; continue }
        $out = Join-Path $dir 'evaluation.json'
        $newest = Get-ChildItem $dir -Recurse -Filter result.json | Sort-Object LastWriteTime | Select-Object -Last 1
        if ((Test-Path $out) -and (Get-Item $out).LastWriteTime -gt $evaluator.LastWriteTime -and (Get-Item $out).LastWriteTime -gt $newest.LastWriteTime) {
            Write-Host "[$arm] already evaluated with the current evaluator; skipped."
            continue
        }
        Write-Host "[$arm] evaluating (each line is one task; about 12 s per task)..."
        & (Join-Path $root '.venv/Scripts/python.exe') scripts/d11_evaluate.py --setting $arm
        if ($LASTEXITCODE -ne 0) { throw "Evaluation of $arm failed with exit code $LASTEXITCODE. Restart this script to resume." }
    }
    $Host.UI.RawUI.WindowTitle = 'GBE D11 evaluation: done'
    Write-Host 'All D11 arms evaluated.'
} finally {
    Stop-Transcript -ErrorAction SilentlyContinue
}
