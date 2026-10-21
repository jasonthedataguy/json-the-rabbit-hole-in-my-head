param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$StudioArguments
)

$ErrorActionPreference = 'Stop'
$taskWorkspace = $PSScriptRoot
$taskPython = $env:JSON_STUDIO_PYTHON
if (-not $taskPython) {
    $taskBundledPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
    if (Test-Path -LiteralPath $taskBundledPython) {
        $taskPython = $taskBundledPython
    } else {
        $taskCommand = Get-Command python.exe -ErrorAction SilentlyContinue
        if ($taskCommand -and $taskCommand.Source -notlike '*\WindowsApps\*') {
            $taskPython = $taskCommand.Source
        }
    }
}
if (-not $taskPython -or -not (Test-Path -LiteralPath $taskPython)) {
    throw 'Set JSON_STUDIO_PYTHON to a Python 3.11+ executable. No runtime will be installed automatically.'
}
if (-not $StudioArguments -or $StudioArguments.Count -eq 0) {
    $StudioArguments = @('status')
}
& $taskPython -X utf8 (Join-Path $taskWorkspace 'scripts\studio.py') @StudioArguments
exit $LASTEXITCODE
