[CmdletBinding()]
param([switch]$Apply)
$ErrorActionPreference = 'Stop'
$estate = [IO.Path]::GetFullPath('D:\Projects\AIDE')
$primary = Join-Path $estate 'aide'
$receipts = Join-Path $estate '_recovery\resource-cleanup-20260926'
$inventory = Get-Content -Raw -LiteralPath (Join-Path $receipts 'worktree-inventory.json') | ConvertFrom-Json
$effects = [Collections.Generic.List[object]]::new()
$before = (Get-Volume -DriveLetter D).SizeRemaining
function Save-Receipt {
    @{mode=$(if ($Apply) {'apply'} else {'check'});before_free=$before;after_free=(Get-Volume -DriveLetter D).SizeRemaining;effects=@($effects)} |
        ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $receipts 'worktree-retirement.json')
}
foreach ($row in $inventory) {
    if ($row.protected -or $row.error -or -not $row.ancestor_dev) { continue }
    $root = [IO.Path]::GetFullPath($row.path)
    if (-not (Test-Path -LiteralPath $root)) { continue }
    if ([IO.Path]::GetDirectoryName($root) -ne $estate -or $root -eq $primary) { throw 'Containment failure' }
    $changes = @($row.status | Where-Object { $_ })
    if (@($changes | Where-Object { $_ -notmatch '^!! .+/__pycache__/$' }).Count) { continue }
    $effect = [ordered]@{path=$root;head=$row.head;branch=$row.branch;result='preflight';bytes=0L;files=0;cache_files=0}
    $effects.Add($effect); Save-Receipt
    $head = (& git -C $root rev-parse HEAD).Trim()
    $ref = (& git -C $primary rev-parse $row.branch).Trim()
    if ($head -ne $row.head -or $ref -ne $head) { throw 'HEAD/ref changed' }
    # No live reviewer remains on these integrated branches. Check observed commands
    # for an exact checkout reference, excluding this script's own PowerShell host.
    $writers = @(Get-CimInstance Win32_Process | Where-Object {
        $_.ProcessId -ne $PID -and $_.CommandLine -and
        ($_.CommandLine.Contains($root) -or $_.CommandLine.Contains($root.Replace('\','/')))
    })
    if ($writers.Count) { $effect.result='active_command_preserved'; Save-Receipt; continue }
    # Stream filesystem metadata; do not follow links, hash source, or hold a
    # whole checkout listing in memory. Refuse nested repositories and aliases.
    $pending = [Collections.Generic.Stack[string]]::new(); $pending.Push($root)
    while ($pending.Count) {
        $directory = $pending.Pop()
        $info = Get-Item -LiteralPath $directory -Force
        if ($info.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Reparse point: $directory" }
        foreach ($item in Get-ChildItem -LiteralPath $directory -Force) {
            if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Reparse point: $($item.FullName)" }
            if ($item.Name -eq '.git' -and $directory -ne $root) { throw "Nested repository: $($item.FullName)" }
            if ($item.PSIsContainer) { $pending.Push($item.FullName) }
            else { $effect.bytes += $item.Length; $effect.files++ }
        }
    }
    foreach ($entry in $changes) {
        $relative = $entry.Substring(3).TrimEnd('/')
        $cache = [IO.Path]::GetFullPath((Join-Path $root $relative))
        if (-not $cache.StartsWith($root+'\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Cache escape' }
        $tracked = @(& git -C $root ls-files -- $relative)
        if ($tracked.Count) { throw 'Tracked cache preserved' }
        foreach ($item in Get-ChildItem -LiteralPath $cache -Force) {
            if ($item.PSIsContainer -or $item.Extension -ne '.pyc' -or $item.Length -lt 16) { throw 'Unknown cache content preserved' }
            $stream = [IO.File]::OpenRead($item.FullName)
            try { $magic = [byte[]]::new(4); if ($stream.Read($magic,0,4) -ne 4 -or $magic[2] -ne 13 -or $magic[3] -ne 10) { throw 'Invalid Python bytecode' } }
            finally { $stream.Dispose() }
            $effect.cache_files++
        }
    }
    $fresh = @(& git -C $root status --porcelain=v1 --untracked-files=all --ignored=matching)
    if ($LASTEXITCODE -ne 0 -or @($fresh | Where-Object { $_ -notmatch '^!! .+/__pycache__/$' }).Count) { throw 'Local state changed; preserved' }
    if ($Apply) {
        foreach ($entry in $changes) {
            $cache = [IO.Path]::GetFullPath((Join-Path $root $entry.Substring(3).TrimEnd('/')))
            if (-not $cache.StartsWith($root+'\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Cache pre-remove escape' }
            Remove-Item -LiteralPath $cache -Recurse
        }
        $effect.result='pending_git_remove'; Save-Receipt
        & git -C $primary worktree remove -- $root
        if ($LASTEXITCODE -ne 0) { $effect.result='remove_failed_reconcile_required'; Save-Receipt; throw 'Git removal failed' }
        $effect.ref_after = (& git -C $primary rev-parse $row.branch).Trim()
        $effect.path_absent = -not (Test-Path -LiteralPath $root)
        if (-not $effect.path_absent -or $effect.ref_after -ne $head) { throw 'Retirement result mismatch' }
        $effect.result='removed_refs_retained'
    } else { $effect.result='verified_disposable' }
    Save-Receipt
}
Get-Content -Raw -LiteralPath (Join-Path $receipts 'worktree-retirement.json')
