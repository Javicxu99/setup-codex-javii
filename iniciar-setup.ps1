param(
    [Alias("NoCodeGraph")]
    [switch]$NoCodebaseMemory
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Test-Command {
    param([string]$Name)
    return $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
}

function Resolve-Python {
    $candidates = @()

    if ($env:SETUP_CODEX_PYTHON) {
        $candidates += @{ Command = $env:SETUP_CODEX_PYTHON; Args = @() }
    }

    $candidates += @{ Command = "python"; Args = @() }
    $candidates += @{ Command = "py"; Args = @("-3") }
    $candidates += @{ Command = "python3"; Args = @() }

    $pathPatterns = @(
        "$env:LOCALAPPDATA\Programs\Python\Python*\python.exe",
        "$env:ProgramFiles\Python*\python.exe",
        "${env:ProgramFiles(x86)}\Python*\python.exe",
        "$env:ProgramFiles\LibreOffice\program\python.exe"
    )

    foreach ($pattern in $pathPatterns) {
        Get-ChildItem -Path $pattern -ErrorAction SilentlyContinue | ForEach-Object {
            $candidates += @{ Command = $_.FullName; Args = @() }
        }
    }

    foreach ($candidate in $candidates) {
        $command = $candidate.Command
        $args = $candidate.Args
        if ((Test-Path -LiteralPath $command) -or (Test-Command $command)) {
            try {
                & $command @args -c "import sys; print(sys.version)" *> $null
                if ($LASTEXITCODE -eq 0) {
                    return $candidate
                }
            }
            catch {
                continue
            }
        }
    }

    throw "Python was not found. Install Python 3 or set SETUP_CODEX_PYTHON to a python.exe path."
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
    return $answer.Trim().ToLowerInvariant().StartsWith("y")
}

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$bootstrapScript = Join-Path $repoRoot "scripts\setup_codex_javii.py"

if (-not (Test-Path -LiteralPath $bootstrapScript)) {
    throw "Bootstrap script not found: $bootstrapScript"
}

Write-Host "setup-codex-javii: starting default bootstrap..."
$python = Resolve-Python
& $python.Command @($python.Args + @($bootstrapScript, "--profile", "default"))
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

if ($NoCodebaseMemory) {
    Write-Host "codebase-memory-mcp guidance skipped because -NoCodebaseMemory was provided."
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
    Write-Host "  Install it from: https://github.com/DeusData/codebase-memory-mcp"
    Write-Host "  The generated .mcp.json already registers the server command."
}

exit 0
