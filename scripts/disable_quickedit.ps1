# Turns off QuickEdit mode for the current console window only (no registry or global change).
# With QuickEdit on, a mouse click or text selection in the window pauses every program writing to
# it; on 9 October 2026 that froze the Qwen3.5 pilot on a progress print for ten minutes.
try {
    $signature = @'
[DllImport("kernel32.dll")] public static extern IntPtr GetStdHandle(int handle);
[DllImport("kernel32.dll")] public static extern bool GetConsoleMode(IntPtr handle, out uint mode);
[DllImport("kernel32.dll")] public static extern bool SetConsoleMode(IntPtr handle, uint mode);
'@
    $kernel = Add-Type -MemberDefinition $signature -Name GbeConsoleMode -Namespace GbeWin32 -PassThru
    $input = $kernel::GetStdHandle(-10)
    $mode = [uint32]0
    if ($kernel::GetConsoleMode($input, [ref]$mode)) {
        # Clear ENABLE_QUICK_EDIT_MODE (0x40); ENABLE_EXTENDED_FLAGS (0x80) must be set for it to apply.
        [void]$kernel::SetConsoleMode($input, (($mode -band (-bnot [uint32]0x40)) -bor [uint32]0x80))
    }
} catch {
    Write-Host "QuickEdit could not be disabled: $($_.Exception.Message)"
}
