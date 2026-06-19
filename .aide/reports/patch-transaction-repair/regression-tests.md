# Regression Tests

Status: `PASS_WITH_WARNINGS`

Focused PatchTransaction tests now cover:

- `C:repo/file.txt` rejected;
- `C:repo\file.txt` rejected;
- `C:/repo/file.txt` rejected;
- `C:\repo\file.txt` rejected;
- lowercase drive prefix rejected;
- ordinary repo-relative colon-free path remains valid;
- `src//file.py` plus `src/file.py` rejected in `declared_changed_paths`;
- duplicate-normalized values rejected in `allowed_paths`;
- duplicate-normalized values rejected in `forbidden_paths`;
- diagnostics identify colliding original values and canonical path;
- existing allowed/forbidden overlap rejection still passes;
- existing traversal and absolute path tests still pass;
- valid distinct normalized paths remain accepted;
- repeated projection remains deterministic;
- source inputs remain unchanged;
- no apply or target mutation occurs.

Latest focused suite result recorded for this repair hardening:

```text
Ran 31 tests
OK
```
