[CmdletBinding()]
param(
    [switch]$Apply
)

$ErrorActionPreference = 'Stop'

$ExpectedManifestSha256 =
    '381213944009ef69aa4860ccb4269b9a0ecd72091fe3f0cb5fa41de40dcfe47d'
$ManifestPath =
    '.aide/queue/AIDE-REPOSITORY-HYGIENE-TRIAGE-01/evidence/archive-duplicate-candidate.json'
$ExpectedFiles = 506
$ExpectedBytes = 101279517L

function Get-Sha256Hex {
    param([byte[]]$Bytes)

    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        return ([System.BitConverter]::ToString($sha.ComputeHash($Bytes))).Replace('-', '').ToLowerInvariant()
    }
    finally {
        $sha.Dispose()
    }
}

function Get-GitBlobBytes {
    param(
        [string]$Repo,
        [string]$Object
    )

    $start = [System.Diagnostics.ProcessStartInfo]::new()
    $start.FileName = (Get-Command git).Source
    $start.WorkingDirectory = $Repo
    $start.UseShellExecute = $false
    $start.RedirectStandardOutput = $true
    $start.RedirectStandardError = $true
    $start.CreateNoWindow = $true
    $null = $start.ArgumentList.Add('cat-file')
    $null = $start.ArgumentList.Add('blob')
    $null = $start.ArgumentList.Add($Object)

    $process = [System.Diagnostics.Process]::new()
    $process.StartInfo = $start
    $null = $process.Start()
    $memory = [System.IO.MemoryStream]::new()
    try {
        $process.StandardOutput.BaseStream.CopyTo($memory)
        $stderr = $process.StandardError.ReadToEnd()
        $process.WaitForExit()
        if ($process.ExitCode -ne 0) {
            throw "git cat-file failed: $stderr"
        }
        return $memory.ToArray()
    }
    finally {
        $memory.Dispose()
        $process.Dispose()
    }
}

function Resolve-ContainedFile {
    param(
        [string]$Repo,
        [string]$RelativePath
    )

    $full = [System.IO.Path]::GetFullPath((Join-Path $Repo $RelativePath))
    $prefix = $Repo + [System.IO.Path]::DirectorySeparatorChar
    if (-not $full.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Path escapes repository: $RelativePath"
    }
    $item = Get-Item -LiteralPath $full -Force
    if ($item.PSIsContainer -or
        (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0)) {
        throw "Path is not an ordinary file: $RelativePath"
    }
    return $item
}

$repo = [System.IO.Path]::GetFullPath((git rev-parse --show-toplevel).Trim())
$manifestBytes = Get-GitBlobBytes -Repo $repo -Object "HEAD:$ManifestPath"
$manifestHash = Get-Sha256Hex -Bytes $manifestBytes
if ($manifestHash -ne $ExpectedManifestSha256) {
    throw "Canonical manifest hash mismatch: $manifestHash"
}

$manifest = [System.Text.Encoding]::UTF8.GetString($manifestBytes) | ConvertFrom-Json
$records = @($manifest.records)
if ($records.Count -ne $ExpectedFiles -or
    [int64]$manifest.summary.size_bytes -ne $ExpectedBytes) {
    throw 'Canonical manifest summary does not match the approved candidate.'
}

$untracked = [System.Collections.Generic.HashSet[string]]::new(
    [System.StringComparer]::Ordinal
)
@(git ls-files --others --exclude-standard) | ForEach-Object {
    $null = $untracked.Add(($_ -replace '\\', '/'))
}
$tracked = [System.Collections.Generic.HashSet[string]]::new(
    [System.StringComparer]::Ordinal
)
@(git ls-files) | ForEach-Object {
    $null = $tracked.Add(($_ -replace '\\', '/'))
}

Add-Type -AssemblyName System.IO.Compression.FileSystem
$archives = @{}
$verifiedBytes = 0L
try {
    foreach ($record in $records) {
        $relative = ([string]$record.path) -replace '\\', '/'
        if (-not $untracked.Contains($relative)) {
            throw "Candidate is no longer visible untracked: $relative"
        }

        $item = Resolve-ContainedFile -Repo $repo -RelativePath $relative
        if ([int64]$item.Length -ne [int64]$record.size_bytes) {
            throw "Candidate size mismatch: $relative"
        }
        $looseHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $item.FullName).Hash.ToLowerInvariant()
        if ($looseHash -ne [string]$record.sha256) {
            throw "Candidate hash mismatch: $relative"
        }

        $archiveRelative = ([string]$record.archive_path) -replace '\\', '/'
        if (-not $tracked.Contains($archiveRelative)) {
            throw "Custody archive is not tracked: $archiveRelative"
        }
        if (-not $archives.ContainsKey($archiveRelative)) {
            $archiveItem = Resolve-ContainedFile -Repo $repo -RelativePath $archiveRelative
            $archives[$archiveRelative] = [System.IO.Compression.ZipFile]::OpenRead(
                $archiveItem.FullName
            )
        }

        $entry = $archives[$archiveRelative].GetEntry([string]$record.archive_member)
        if ($null -eq $entry) {
            throw "Archive member missing: $archiveRelative :: $($record.archive_member)"
        }
        $stream = $entry.Open()
        $sha = [System.Security.Cryptography.SHA256]::Create()
        try {
            $entryHash = ([System.BitConverter]::ToString($sha.ComputeHash($stream))).Replace('-', '').ToLowerInvariant()
        }
        finally {
            $sha.Dispose()
            $stream.Dispose()
        }
        if ($entryHash -ne [string]$record.sha256) {
            throw "Archive member hash mismatch: $archiveRelative :: $($record.archive_member)"
        }
        $verifiedBytes += [int64]$record.size_bytes
    }
}
finally {
    foreach ($archive in $archives.Values) {
        $archive.Dispose()
    }
}

if ($verifiedBytes -ne $ExpectedBytes) {
    throw "Verified byte total mismatch: $verifiedBytes"
}

$removed = 0
$removedBytes = 0L
if ($Apply) {
    foreach ($record in $records) {
        $relative = ([string]$record.path) -replace '\\', '/'
        $probe = @(git ls-files --others --exclude-standard -- $relative)
        if ($probe.Count -ne 1 -or (($probe[0] -replace '\\', '/') -ne $relative)) {
            throw "Pre-remove tracking drift: $relative"
        }

        $item = Resolve-ContainedFile -Repo $repo -RelativePath $relative
        $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $item.FullName).Hash.ToLowerInvariant()
        if ($hash -ne [string]$record.sha256) {
            throw "Pre-remove hash drift: $relative"
        }

        [System.IO.File]::Delete($item.FullName)
        if ([System.IO.File]::Exists($item.FullName)) {
            throw "Removal failed: $relative"
        }
        $removed++
        $removedBytes += [int64]$record.size_bytes
    }
}

[pscustomobject]@{
    result = 'PASS'
    mode = if ($Apply) { 'apply' } else { 'verify_only' }
    manifest_sha256 = $manifestHash
    verified_files = $records.Count
    verified_bytes = $verifiedBytes
    tracked_archives = $archives.Count
    removed_files = $removed
    removed_bytes = $removedBytes
} | ConvertTo-Json
