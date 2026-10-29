param([switch]$Worker)
# Starts the pinned Ollama 0.40.1 server in its own window without the tray app, so the app's updater cannot install
# a newer version during a run. The variables reproduce the "server config" line the app's server logged on
# 28 October 2026 (models on D:, Vulkan on, one request at a time, flash attention off); everything else is default.
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
if (-not $Worker) {
    $command = 'powershell.exe -NoProfile -NoExit -ExecutionPolicy Bypass -File "' + $MyInvocation.MyCommand.Path + '" -Worker'
    $result = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine = $command; CurrentDirectory = $root}
    Write-Host ("Ollama server window started (process {0}, return code {1})." -f $result.ProcessId, $result.ReturnValue)
    return
}
$env:OLLAMA_MODELS = '<models>'
$env:OLLAMA_VULKAN = '1'
$env:OLLAMA_NUM_PARALLEL = '1'
$env:OLLAMA_FLASH_ATTENTION = '0'
$Host.UI.RawUI.WindowTitle = 'Ollama 0.40.1 server (pinned; close to stop)'
$log = Join-Path $root ('runs/s6_logs/ollama_serve_' + (Get-Date -Format 'yyyyMMdd_HHmmss'))
# The server logs to stderr; Windows PowerShell 5.1 turns redirected native stderr into errors, so redirect through
# Start-Process instead (the variables above are inherited).
Write-Host "Ollama server running; log in $log.err.log"
Start-Process -FilePath "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" -ArgumentList 'serve' -NoNewWindow -Wait `
    -RedirectStandardOutput "$log.out.log" -RedirectStandardError "$log.err.log"
