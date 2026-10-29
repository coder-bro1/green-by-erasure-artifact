param([string]$RunId = 'c1_qwen25_code', [switch]$Worker)
# Stage C pipeline run (docs/C1_PROTOCOL.md section 6): Qwen2.5-Coder 7B, P1 to P4 on the buggy and fixed versions
# of the 30 BugsInPy bugs, in a visible window started through WMI. Resumes from runs/<run>/units; cached model
# answers are reused. Needs Ollama 0.40.1 running (GPU) and the environments in <work>.
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
if (-not $Worker) {
    $command = 'powershell.exe -NoProfile -NoExit -ExecutionPolicy Bypass -File "' + $MyInvocation.MyCommand.Path +
               '" -RunId ' + $RunId + ' -Worker'
    $result = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine = $command; CurrentDirectory = $root}
    Write-Host ("C1 pipeline window started (process {0}, return code {1})." -f $result.ProcessId, $result.ReturnValue)
    return
}
Set-Location -LiteralPath $root
. (Join-Path $PSScriptRoot 'disable_quickedit.ps1')
$env:PYTHONPATH = Join-Path $root 'src'
$env:PYTHONIOENCODING = 'utf-8'
New-Item -ItemType Directory -Force -Path ('runs/' + $RunId) | Out-Null
Start-Transcript -Path ('runs/' + $RunId + '/c1_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.log')
try {
    $Host.UI.RawUI.WindowTitle = "GBE C1 pipeline: $RunId (see runs/$RunId/progress.json)"
    & (Join-Path $root '.venv/Scripts/python.exe') -m gbe.runner --run-id $RunId
    if ($LASTEXITCODE -ne 0) { throw "$RunId stopped with exit code $LASTEXITCODE; restart this script to resume." }
    $Host.UI.RawUI.WindowTitle = "GBE C1 pipeline: $RunId done"
} finally {
    Stop-Transcript -ErrorAction SilentlyContinue
}
