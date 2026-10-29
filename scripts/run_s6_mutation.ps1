param([switch]$Worker)
# S6 mutation step (analysis/mutation_extra.py) in a visible window started through WMI. It waits until both S6
# runs have finished all 408 units (manifest "units", written only at the end of a full run), so the machine is
# idle apart from this step, then scores the new P2M tests of each run against the recorded mutants. Resumable.
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
if (-not $Worker) {
    $command = 'powershell.exe -NoProfile -NoExit -ExecutionPolicy Bypass -File "' + $MyInvocation.MyCommand.Path + '" -Worker'
    $result = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine = $command; CurrentDirectory = $root}
    Write-Host ("S6 mutation window started (process {0}, return code {1})." -f $result.ProcessId, $result.ReturnValue)
    return
}
Set-Location -LiteralPath $root
. (Join-Path $PSScriptRoot 'disable_quickedit.ps1')
$env:PYTHONPATH = Join-Path $root 'src'
$env:PYTHONIOENCODING = 'utf-8'
New-Item -ItemType Directory -Force -Path 'runs/s6_logs' | Out-Null
Start-Transcript -Path ('runs/s6_logs/s6_mutation_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.log')
try {
    $runs = @('s6_model_only_gemma4', 's6_model_only_qwen25')
    $Host.UI.RawUI.WindowTitle = 'GBE S6 mutation: waiting for both S6 runs'
    while ($true) {
        $finished = @($runs | Where-Object {
            $m = "runs/$_/manifest.json"
            (Test-Path $m) -and ((Get-Content $m -Raw | ConvertFrom-Json).units -eq 408)
        })
        if ($finished.Count -eq $runs.Count) { break }
        Write-Host ("{0} waiting: {1} of {2} S6 runs finished" -f (Get-Date -Format 'HH:mm'), $finished.Count, $runs.Count)
        Start-Sleep -Seconds 300
    }
    foreach ($run in $runs) {
        $Host.UI.RawUI.WindowTitle = "GBE S6 mutation: $run (see runs/$run/mutation/progress.json)"
        & (Join-Path $root '.venv/Scripts/python.exe') analysis/mutation_extra.py --run $run --workers 6
        if ($LASTEXITCODE -ne 0) { throw "Mutation step failed on $run with exit code $LASTEXITCODE; restart to resume." }
    }
    $Host.UI.RawUI.WindowTitle = 'GBE S6 mutation: done'
} finally {
    Stop-Transcript -ErrorAction SilentlyContinue
}
