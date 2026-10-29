param([switch]$Worker)
# Stage C installation and developer-test check (analysis/c1_install.py) in a visible window started through WMI;
# resumes from runs/c1/install/*.json. Needs network (GitHub, PyPI); works in <work>.
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
if (-not $Worker) {
    $command = 'powershell.exe -NoProfile -NoExit -ExecutionPolicy Bypass -File "' + $MyInvocation.MyCommand.Path + '" -Worker'
    $result = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine = $command; CurrentDirectory = $root}
    Write-Host ("C1 install window started (process {0}, return code {1})." -f $result.ProcessId, $result.ReturnValue)
    return
}
Set-Location -LiteralPath $root
. (Join-Path $PSScriptRoot 'disable_quickedit.ps1')
$env:PYTHONIOENCODING = 'utf-8'
New-Item -ItemType Directory -Force -Path 'runs/c1' | Out-Null
Start-Transcript -Path ('runs/c1/install_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.log')
try {
    $Host.UI.RawUI.WindowTitle = 'GBE C1 install (see runs/c1/install_progress.json, review/out/c1_install.md)'
    & (Join-Path $root '.venv-c2/Scripts/python.exe') analysis/c1_install.py
    if ($LASTEXITCODE -ne 0) { throw "C1 install failed with exit code $LASTEXITCODE; restart this script to resume." }
    $Host.UI.RawUI.WindowTitle = 'GBE C1 install: done'
} finally {
    Stop-Transcript -ErrorAction SilentlyContinue
}
