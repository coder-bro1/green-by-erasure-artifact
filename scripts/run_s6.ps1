param([switch]$Worker)
# S6 model-only overwrite (scripts/s6_model_only_overwrite.py) in a visible window started through WMI: Gemma 4
# first, then Qwen2.5. Each run resumes per unit and per model call. Needs Ollama 0.40.1 running; uses the GPU.
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
if (-not $Worker) {
    $command = 'powershell.exe -NoProfile -NoExit -ExecutionPolicy Bypass -File "' + $MyInvocation.MyCommand.Path + '" -Worker'
    $result = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine = $command; CurrentDirectory = $root}
    Write-Host ("S6 window started (process {0}, return code {1})." -f $result.ProcessId, $result.ReturnValue)
    return
}
Set-Location -LiteralPath $root
. (Join-Path $PSScriptRoot 'disable_quickedit.ps1')
$env:PYTHONPATH = Join-Path $root 'src'
$env:PYTHONIOENCODING = 'utf-8'
New-Item -ItemType Directory -Force -Path 'runs/s6_logs' | Out-Null
Start-Transcript -Path ('runs/s6_logs/s6_' + (Get-Date -Format 'yyyyMMdd_HHmmss') + '.log')
try {
    foreach ($source in @('phase2_gemma4_code', 'phase2_qwen25_code')) {
        $Host.UI.RawUI.WindowTitle = "GBE S6 model-only overwrite: $source (see runs/s6_model_only_*/progress.json)"
        & (Join-Path $root '.venv/Scripts/python.exe') scripts/s6_model_only_overwrite.py --source $source
        if ($LASTEXITCODE -ne 0) { throw "S6 failed on $source with exit code $LASTEXITCODE; restart this script to resume." }
    }
    $Host.UI.RawUI.WindowTitle = 'GBE S6 model-only overwrite: done'
} finally {
    Stop-Transcript -ErrorAction SilentlyContinue
}
