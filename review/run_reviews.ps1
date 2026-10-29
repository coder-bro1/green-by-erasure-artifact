param([string[]]$Runs = @('phase2_qwen25_spec', 'phase2_qwen25_seed1', 'phase2_qwen25_seed2', 'phase2_qwen25_seed3',
                          'phase2_qwen25_disguised', 'phase2_qwen35_disguised', 'phase2_gemma4_disguised'), [switch]$Worker)
# Reviewer checks (review/check_run.py, review/leak_r2.py) for finished runs, at below-normal priority, in a
# visible window started through WMI. A run whose review/out/<run>/ already holds results newer than its
# tests.csv is skipped, so restarting resumes.
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
if (-not $Worker) {
    $command = 'powershell.exe -NoProfile -NoExit -ExecutionPolicy Bypass -File "' + $MyInvocation.MyCommand.Path + '" -Runs ' + ($Runs -join ',') + ' -Worker'
    $result = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine = $command; CurrentDirectory = $root}
    Write-Host ("Review window started (process {0}, return code {1})." -f $result.ProcessId, $result.ReturnValue)
    return
}
if ($Runs.Count -eq 1 -and $Runs[0] -like '*,*') { $Runs = $Runs[0].Split(',') }
Set-Location -LiteralPath $root
. (Join-Path $root 'scripts/disable_quickedit.ps1')
$env:PYTHONPATH = Join-Path $root 'src'
$env:PYTHONIOENCODING = 'utf-8'
$python = Join-Path $root '.venv/Scripts/python.exe'
New-Item -ItemType Directory -Force -Path 'review/out' | Out-Null
Start-Transcript -Path ('review/out/reviews_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.log')
try {
    $i = 0
    foreach ($run in $Runs) {
        $i++
        $Host.UI.RawUI.WindowTitle = "GBE reviews: $i of $($Runs.Count) ($run)"
        $done = Join-Path $root "review/out/$run/leak_r2_done.txt"
        if ((Test-Path $done) -and (Get-Item $done).LastWriteTime -gt (Get-Item "runs/$run/tests.csv").LastWriteTime) {
            Write-Host "[$run] already reviewed; skipped."; continue
        }
        Write-Host "[$run] check_run.py"
        & $python review/low_priority.py review/check_run.py $run
        if ($LASTEXITCODE -ne 0) { throw "check_run.py failed for $run" }
        Write-Host "[$run] leak_r2.py"
        & $python review/low_priority.py review/leak_r2.py $run
        if ($LASTEXITCODE -ne 0) { throw "leak_r2.py failed for $run" }
        Set-Content -LiteralPath $done -Value (Get-Date -Format o) -Encoding utf8
    }
    $Host.UI.RawUI.WindowTitle = 'GBE reviews: done'
    Write-Host 'All reviews finished.'
} finally {
    Stop-Transcript -ErrorAction SilentlyContinue
}
