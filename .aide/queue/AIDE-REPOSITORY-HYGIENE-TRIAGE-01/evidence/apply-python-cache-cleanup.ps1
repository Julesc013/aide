[CmdletBinding()]
param(
    [switch]$Apply
)

$ErrorActionPreference = 'Stop'

$ExpectedDirectories = @(
    '.aide/scripts/__pycache__',
    '.aide/scripts/tests/__pycache__',
    'core/apply/__pycache__',
    'core/compat/__pycache__',
    'core/compat/tests/__pycache__',
    'core/gateway/__pycache__',
    'core/gateway/tests/__pycache__',
    'core/harness/__pycache__',
    'core/harness/tests/__pycache__',
    'core/protocol/__pycache__',
    'core/providers/__pycache__',
    'core/providers/tests/__pycache__',
    'scripts/__pycache__',
    'shared/__pycache__',
    'shared/cli/__pycache__',
    'shared/config/__pycache__',
    'shared/core/__pycache__',
    'shared/diagnostics/__pycache__',
    'shared/protocol/__pycache__',
    'shared/tests/__pycache__'
) | Sort-Object
$ExpectedFiles = 69
$ExpectedBytes = 1351417L

$repo = [System.IO.Path]::GetFullPath((git rev-parse --show-toplevel).Trim())
$prefix = $repo + [System.IO.Path]::DirectorySeparatorChar
$actualDirectories = @(
    Get-ChildItem -LiteralPath $repo -Directory -Force -Recurse |
        Where-Object { $_.Name -eq '__pycache__' } |
        ForEach-Object {
            [System.IO.Path]::GetRelativePath($repo, $_.FullName) -replace '\\', '/'
        } |
        Sort-Object
)

$pathDifference = @(Compare-Object $ExpectedDirectories $actualDirectories)
if ($pathDifference.Count -ne 0) {
    throw "Python cache path set changed: $($pathDifference | Out-String)"
}

$files = 0
$bytes = 0L
foreach ($relative in $ExpectedDirectories) {
    $full = [System.IO.Path]::GetFullPath((Join-Path $repo $relative))
    if (-not $full.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Cache path escapes repository: $relative"
    }

    $directory = Get-Item -LiteralPath $full -Force
    if (-not $directory.PSIsContainer -or $directory.Name -ne '__pycache__' -or
        (($directory.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0)) {
        throw "Unsafe cache directory: $relative"
    }

    $tracked = @(git ls-files -- $relative)
    if ($tracked.Count -ne 0) {
        throw "Cache directory contains tracked paths: $relative"
    }

    foreach ($item in Get-ChildItem -LiteralPath $full -Force -Recurse) {
        if (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
            throw "Cache contains a reparse point: $($item.FullName)"
        }
        if (-not $item.PSIsContainer) {
            $itemRelative = [System.IO.Path]::GetRelativePath($repo, $item.FullName) -replace '\\', '/'
            git check-ignore -q -- $itemRelative
            if ($LASTEXITCODE -ne 0) {
                throw "Cache file is not ignored: $itemRelative"
            }
            $files++
            $bytes += [int64]$item.Length
        }
    }
}

if ($files -ne $ExpectedFiles -or $bytes -ne $ExpectedBytes) {
    throw "Python cache totals changed: files=$files bytes=$bytes"
}

$removedDirectories = 0
if ($Apply) {
    foreach ($relative in $ExpectedDirectories) {
        $full = [System.IO.Path]::GetFullPath((Join-Path $repo $relative))
        if (-not $full.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
            throw "Pre-remove containment failure: $relative"
        }
        $directory = Get-Item -LiteralPath $full -Force
        if (-not $directory.PSIsContainer -or $directory.Name -ne '__pycache__' -or
            (($directory.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0)) {
            throw "Pre-remove directory drift: $relative"
        }
        [System.IO.Directory]::Delete($full, $true)
        if ([System.IO.Directory]::Exists($full)) {
            throw "Cache removal failed: $relative"
        }
        $removedDirectories++
    }
}

[pscustomobject]@{
    result = 'PASS'
    mode = if ($Apply) { 'apply' } else { 'verify_only' }
    verified_directories = $ExpectedDirectories.Count
    verified_files = $files
    verified_bytes = $bytes
    removed_directories = $removedDirectories
} | ConvertTo-Json
