# Run the ordinary Bash verifier with project-local Windows prerequisites.
# Use -Bootstrap to download/extract the pinned official tools the first time.
[CmdletBinding()]
param(
    [switch]$Bootstrap,
    [string]$Python = 'python',
    [string]$Bash = (Join-Path $env:ProgramFiles 'Git/bin/bash.exe')
)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$toolRoot = Join-Path $projectRoot 'build/toolchain/windows-x64'
$manifest = Get-Content -LiteralPath (Join-Path $projectRoot 'tools/windows-toolchain.json') -Raw | ConvertFrom-Json

if (-not [Environment]::Is64BitProcess -or $env:OS -ne 'Windows_NT') {
    throw 'This runner requires 64-bit Windows PowerShell or PowerShell on Windows.'
}
if (-not (Test-Path -LiteralPath $Bash -PathType Leaf)) {
    throw 'Git Bash was not found. Supply its bash.exe path with -Bash.'
}
$pythonExe = (Get-Command $Python -CommandType Application -ErrorAction Stop).Source
& $pythonExe -c 'import sys; assert sys.version_info >= (3, 10), "Python 3.10+ required"'
if ($LASTEXITCODE -ne 0) { throw 'Supply a working Python 3.10+ executable with -Python.' }

foreach ($tool in $manifest.tools) {
    $archive = Join-Path $toolRoot ('downloads/' + $tool.file)
    $executable = Join-Path $toolRoot $tool.executable
    if ($Bootstrap) {
        New-Item -ItemType Directory -Path (Split-Path $archive -Parent) -Force | Out-Null
        if (-not (Test-Path -LiteralPath $archive -PathType Leaf)) {
            Write-Host "Downloading $($tool.name) $($tool.version)"
            Invoke-WebRequest -Uri $tool.url -OutFile $archive -UseBasicParsing
        }
        $actualHash = (Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash
        if ($actualHash -ne $tool.sha256) {
            throw "Checksum mismatch for $archive. No archive contents were executed."
        }
        $destination = Join-Path $toolRoot $tool.destination
        New-Item -ItemType Directory -Path $destination -Force | Out-Null
        if ($tool.file.EndsWith('.exe')) {
            Copy-Item -LiteralPath $archive -Destination $executable -Force
        } else {
            $entries = @(& tar.exe -tf $archive)
            if ($LASTEXITCODE -ne 0 -or $entries.Count -eq 0) { throw "Cannot inspect $archive" }
            foreach ($entry in $entries) {
                if ($entry -match '(^[/\\])|(^[A-Za-z]:)|((^|[/\\])\.\.([/\\]|$))') {
                    throw "Unsafe archive member in $archive"
                }
            }
            & tar.exe -xf $archive -C $destination
            if ($LASTEXITCODE -ne 0) { throw "Cannot extract $archive" }
        }
        # Mark the verified archive used for this installation, outside Git.
        Set-Content -LiteralPath (Join-Path $destination '.archive-sha256') -Value $tool.sha256 -Encoding ASCII
    }
    $stamp = Join-Path (Join-Path $toolRoot $tool.destination) '.archive-sha256'
    if (-not (Test-Path -LiteralPath $executable -PathType Leaf) -or
        -not (Test-Path -LiteralPath $stamp -PathType Leaf) -or
        (Get-Content -LiteralPath $stamp -Raw).Trim() -ne $tool.sha256) {
        throw "Pinned $($tool.name) $($tool.version) is not ready. Run scripts/verify.ps1 -Bootstrap."
    }
}

$toolBins = @($manifest.tools | ForEach-Object {
    Split-Path (Join-Path $toolRoot $_.executable) -Parent
})
$oldEnvironment = @{}
foreach ($key in @('PATH', 'VALE_BIN', 'FLAPOL_PYTHON', 'FLAPOL_PROJECT')) {
    $oldEnvironment[$key] = [Environment]::GetEnvironmentVariable($key, 'Process')
}
try {
    $env:PATH = ($toolBins -join ';') + ';' + $env:PATH
    $env:VALE_BIN = (Join-Path $toolRoot 'vale/vale.exe').Replace('\', '/')
    $env:FLAPOL_PYTHON = $pythonExe.Replace('\', '/')
    $env:FLAPOL_PROJECT = $projectRoot.Replace('\', '/')
    $rubyTool = $manifest.tools | Where-Object { $_.name -eq 'ruby' }
    & (Join-Path $toolRoot $rubyTool.executable) --version
    & $env:VALE_BIN --version
    & (Join-Path $toolRoot 'jq/jq.exe') --version
    $bashCommand = @'
function python3() { "$FLAPOL_PYTHON" "$@"; }
function git() { command git -c safe.directory="$FLAPOL_PROJECT" "$@"; }
export -f python3 git
cd "$FLAPOL_PROJECT" || exit
bash scripts/verify.sh
'@
    & $Bash -c $bashCommand
    if ($LASTEXITCODE -ne 0) { throw "Verification failed (exit $LASTEXITCODE)." }
} finally {
    foreach ($key in $oldEnvironment.Keys) {
        [Environment]::SetEnvironmentVariable($key, $oldEnvironment[$key], 'Process')
    }
}
