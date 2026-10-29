param([switch]$Worker)
# S5 CoverUp audit (scripts/s5_coverup.py) in a visible window started through WMI; resumes from
# runs/s5_coverup/results.jsonl. Needs Ollama 0.40.1 running; uses the GPU and some CPU.
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
if (-not $Worker) {
    $command = 'powershell.exe -NoProfile -NoExit -ExecutionPolicy Bypass -File "' + $MyInvocation.MyCommand.Path + '" -Worker'
    $result = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine = $command; CurrentDirectory = $root}
    Write-Host ("S5 window started (process {0}, return code {1})." -f $result.ProcessId, $result.ReturnValue)
    return
}
Set-Location -LiteralPath $root
. (Join-Path $PSScriptRoot 'disable_quickedit.ps1')
$env:PYTHONPATH = Join-Path $root 'src'
$env:PYTHONIOENCODING = 'utf-8'
New-Item -ItemType Directory -Force -Path 'runs/s5_coverup' | Out-Null
Start-Transcript -Path ('runs/s5_coverup/s5_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.log')
try {
    $Host.UI.RawUI.WindowTitle = 'GBE S5 CoverUp audit (see runs/s5_coverup/progress.json)'
    & (Join-Path $root '.venv/Scripts/python.exe') scripts/s5_coverup.py
    if ($LASTEXITCODE -ne 0) { throw "S5 failed with exit code $LASTEXITCODE; restart this script to resume." }
    $Host.UI.RawUI.WindowTitle = 'GBE S5 CoverUp audit: done'
} finally {
    Stop-Transcript -ErrorAction SilentlyContinue
}
