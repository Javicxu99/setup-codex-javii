param(
    [switch]$NoCodeGraph
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
$bootstrapScript = Join-Path $repoRoot ".codex\skills\setup-codex-javii\scripts\setup_codex_javii.py"

if (-not (Test-Path -LiteralPath $bootstrapScript)) {
    throw "Bootstrap script not found: $bootstrapScript"
}

Write-Host "setup-codex-javii: starting default bootstrap..."
$python = Resolve-Python
& $python.Command @($python.Args + @($bootstrapScript, "--profile", "default"))
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

if ($NoCodeGraph) {
    Write-Host "CodeGraph step skipped because -NoCodeGraph was provided."
    exit 0
}

Write-Host ""
Write-Host "Optional CodeGraph setup:"
Write-Host "  installer: npx @colbymchenry/codegraph"
Write-Host "  project init: codegraph init -i"

if (-not (Test-Command "codegraph")) {
    if (Test-Command "npx") {
        if (Ask-YesNo "Run the official CodeGraph installer now?" $false) {
            & npx @colbymchenry/codegraph
            if ($LASTEXITCODE -ne 0) {
                exit $LASTEXITCODE
            }
        }
    }
    else {
        Write-Host "npx is not available. Install Node.js/npm first if you want CodeGraph."
    }
}

if (Test-Command "codegraph") {
    if (Ask-YesNo "Initialize CodeGraph in this project now?" $false) {
        & codegraph init -i
        exit $LASTEXITCODE
    }
}
else {
    Write-Host "CodeGraph is not on PATH yet. After installing it, run: codegraph init -i"
}

exit 0
