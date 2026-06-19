# Drive-Prefix Repair

Status: `PASS_WITH_WARNINGS`

The validator rejects Windows drive-prefixed paths before accepting a path as a
portable repository-relative PatchTransaction locator.

Rejected examples:

- `C:repo/file.txt`
- `C:repo\file.txt`
- `C:/repo/file.txt`
- `C:\repo\file.txt`
- `z:relative.txt`

The detection is platform-independent and uses a bounded leading drive-prefix
rule equivalent to `^[A-Za-z]:`.

Preserved behavior:

- ordinary colon-free repository-relative paths remain valid;
- POSIX absolute paths remain invalid;
- Windows absolute paths remain invalid;
- traversal remains invalid;
- empty or dot-only paths remain invalid.
