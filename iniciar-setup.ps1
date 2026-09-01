[CmdletBinding()]
param(
    [Alias("NoCodeGraph")]
    [switch]$NoCodebaseMemory,

    [switch]$Apply,

    [ValidateSet("codex", "claude", "docs", "github", "compliance", "archify", "shared")]
    [string[]]$Components = @("codex", "claude", "docs", "github", "compliance", "archify", "shared"),

    [ValidateSet("backup", "skip")]
    [string]$OnConflict = "backup"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$minimumPython = "3.11"

function Test-Command {
    param([string]$Name)
    return $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
}

function Resolve-Python {
    $candidates = @()
    $diagnostics = [System.Collections.Generic.List[string]]::new()
    $seen = [System.Collections.Generic.HashSet[string]]::new(
        [System.StringComparer]::OrdinalIgnoreCase
    )

    if ($env:SETUP_CODEX_PYTHON) {
        $candidates += [PSCustomObject]@{
            Command = $env:SETUP_CODEX_PYTHON
            Args = @()
        }
    }

    $candidates += [PSCustomObject]@{ Command = "python"; Args = @() }
    $candidates += [PSCustomObject]@{ Command = "py"; Args = @("-3") }
    $candidates += [PSCustomObject]@{ Command = "python3"; Args = @() }

    $pathPatterns = @(
        "$env:LOCALAPPDATA\Programs\Python\Python*\python.exe",
        "$env:ProgramFiles\Python*\python.exe",
        "${env:ProgramFiles(x86)}\Python*\python.exe",
        "$env:ProgramFiles\LibreOffice\program\python.exe"
    )

    foreach ($pattern in $pathPatterns) {
        Get-ChildItem -Path $pattern -ErrorAction SilentlyContinue |
            Sort-Object FullName -Descending |
            ForEach-Object {
                $candidates += [PSCustomObject]@{
                    Command = $_.FullName
                    Args = @()
                }
            }
    }

    foreach ($candidate in $candidates) {
        $command = [string]$candidate.Command
        $args = @($candidate.Args)
        $key = $command + "|" + ($args -join " ")
        if (-not $seen.Add($key)) {
            continue
        }
        if (-not ((Test-Path -LiteralPath $command) -or (Test-Command $command))) {
            continue
        }

        try {
            $versionOutput = & $command @args -c (
                "import sys; print('.'.join(map(str, sys.version_info[:3]))); " +
                "raise SystemExit(0 if sys.version_info >= (3, 11) else 3)"
            ) 2>&1
            $exitCode = $LASTEXITCODE
            $version = (@($versionOutput) -join " ").Trim()
            if ($exitCode -eq 0) {
                return [PSCustomObject]@{
                    Command = $command
                    Args = $args
                    Version = $version
                }
            }
            if ([string]::IsNullOrWhiteSpace($version)) {
                $version = "could not start"
            }
            $diagnostics.Add("$command $($args -join ' ') -> $version")
        }
        catch {
            $diagnostics.Add("$command $($args -join ' ') -> $($_.Exception.Message)")
        }
    }

    $checked = if ($diagnostics.Count -gt 0) {
        " Checked candidates: " + ($diagnostics -join "; ")
    }
    else {
        " No runnable Python candidate was found."
    }
    throw (
        "Python $minimumPython or newer is required.$checked " +
        "Install a supported Python or set SETUP_CODEX_PYTHON to its python.exe path."
    )
}

function Ask-YesNo {
    param(
        [string]$Question,
        [bool]$Default = $false
    )

    $suffix = if ($Default) { "[Y/n]" } else { "[y/N]" }
    $answer = Read-Host "$Question $suffix"
    if ([string]::IsNullOrWhiteSpace($answer)) {
        return $Default
    }
    $normalized = $answer.Trim().ToLowerInvariant()
    return $normalized.StartsWith("y") -or $normalized.StartsWith("s")
}

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$bootstrapScript = Join-Path $repoRoot "scripts\setup_codex_javii.py"
$target = (Get-Location).Path

if (-not (Test-Path -LiteralPath $bootstrapScript)) {
    throw "Bootstrap script not found: $bootstrapScript"
}

$python = Resolve-Python
Write-Host "setup-codex-javii: Python $($python.Version)"
Write-Host "setup-codex-javii: previewing changes for $target"

$commonArguments = @(
    $bootstrapScript,
    "--profile", "default",
    "--target", $target,
    "--on-conflict", $OnConflict,
    "--components"
) + $Components

& $python.Command @($python.Args + $commonArguments + "--dry-run")
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

if (-not $Apply -and -not (Ask-YesNo "Apply this plan?" $false)) {
    Write-Host "No files were changed."
    exit 0
}

& $python.Command @($python.Args + $commonArguments + "--apply")
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

if ($NoCodebaseMemory -or -not ($Components -contains "shared")) {
    Write-Host "Codebase Memory availability check skipped; generated component choices are unchanged."
    exit 0
}

Write-Host ""
Write-Host "Codebase Memory status:"
if (Test-Command "codebase-memory-mcp") {
    Write-Host "  codebase-memory-mcp is available."
    Write-Host "  Restart Codex after first-time MCP configuration, then index the project with index_repository."
}
else {
    Write-Host "  codebase-memory-mcp is not on PATH."
    Write-Host "  Install it only if wanted: https://github.com/DeusData/codebase-memory-mcp"
    Write-Host "  The generated .mcp.json already registers the optional server command."
}

exit 0
