param([string[]]$Steps = @('generate', 'filter', 'select'), [switch]$Worker)
# S2 natural-fault builder (scripts/s2_natural_faults.py) in a visible window started through WMI.
# 'generate' uses the GPU; 'filter' and 'select' are CPU only. Every step resumes where it stopped.
# Progress: runs/s2_natural/generation_progress.json.
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
if (-not $Worker) {
    $command = 'powershell.exe -NoProfile -NoExit -ExecutionPolicy Bypass -File "' + $MyInvocation.MyCommand.Path + '" -Steps ' + ($Steps -join ',') + ' -Worker'
    $result = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine = $command; CurrentDirectory = $root}
    Write-Host ("S2 window started (process {0}, return code {1})." -f $result.ProcessId, $result.ReturnValue)
    return
}
if ($Steps.Count -eq 1 -and $Steps[0] -like '*,*') { $Steps = $Steps[0].Split(',') }
Set-Location -LiteralPath $root
. (Join-Path $PSScriptRoot 'disable_quickedit.ps1')
$env:PYTHONPATH = Join-Path $root 'src'
$env:PYTHONIOENCODING = 'utf-8'
New-Item -ItemType Directory -Force -Path 'runs/s2_natural' | Out-Null
Start-Transcript -Path ('runs/s2_natural/s2_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.log')
try {
    foreach ($step in $Steps) {
        $Host.UI.RawUI.WindowTitle = "GBE S2 natural faults: $step"
        & (Join-Path $root '.venv/Scripts/python.exe') scripts/s2_natural_faults.py $step
        if ($LASTEXITCODE -ne 0) { throw "S2 step $step failed with exit code $LASTEXITCODE. Restart this script to resume." }
    }
    $Host.UI.RawUI.WindowTitle = 'GBE S2 natural faults: done'
} finally {
    Stop-Transcript -ErrorAction SilentlyContinue
}
