"""Task-local read-only inventory; observations do not establish portability."""
from __future__ import annotations

import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
OUTPUT = Path(__file__).parent / "evidence" / "source-inventory.json"
EXTENSIONS = {".py", ".c", ".cpp", ".h", ".cs", ".swift", ".ts", ".ps1", ".sh", ".cmd", ".bat"}
PLATFORM_IMPORTS = {"winreg", "msvcrt", "fcntl", "pwd", "grp", "resource", "ctypes.wintypes"}
HINTS = ("WinDLL", "kernel32", "CreateProcess", "powershell.exe", "pwsh", "Get-CimInstance", "Get-Volume")


def main() -> None:
    tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode("utf-8").split("\0")
    files, historical = [], []
    syntax_errors = []
    for name in sorted(filter(None, tracked)):
        path = ROOT / name
        if path.suffix not in EXTENSIONS or name.startswith(".aide/export/"):
            continue
        if name.startswith(".aide/queue/"):
            if path.suffix == ".ps1":
                historical.append({"path": name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
            continue
        raw = path.read_bytes()
        text = raw.decode("utf-8-sig")
        row = {"path": name, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
               "text_hints": [hint for hint in HINTS if hint in text]}
        if path.suffix == ".py":
            try:
                tree = ast.parse(text, filename=name)
                imports = set()
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        imports.update(alias.name for alias in node.names)
                    elif isinstance(node, ast.ImportFrom) and node.module:
                        imports.add(node.module)
                        imports.update(node.module + "." + alias.name for alias in node.names)
                row["platform_import_observations"] = sorted(imports & PLATFORM_IMPORTS)
            except SyntaxError as error:
                syntax_errors.append({"path": name, "line": error.lineno, "message": error.msg})
        files.append(row)
    result = {
        "schema": "aide.task-source-inventory.v1",
        "source_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "scope": "Git-tracked selected code extensions outside queue history and duplicate export payloads; extensionless launchers are observed separately.",
        "limitations": "AST parsing uses this interpreter only; imports and text hints are incomplete investigation candidates, not a semantic audit or OS support verdict. PATH absence does not establish machine-wide absence.",
        "counts": dict(sorted(Counter(Path(row["path"]).suffix for row in files).items())),
        "parser_runtime": {"implementation": sys.implementation.name, "version": list(sys.version_info[:3])},
        "files": files, "syntax_errors": syntax_errors, "historical_powershell": historical,
        "extensionless_launchers": [name for name in ("scripts/aide", "scripts/aide-queue-status", "scripts/aide-queue-next", "scripts/aide-queue-run") if name in tracked],
        "tools_on_path": {name: bool(shutil.which(name)) for name in ("python", "py", "pwsh", "wsl", "docker", "clang", "gcc", "cl", "cmake", "git")},
        "product_qualified": False,
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"counts": result["counts"], "historical_powershell": len(historical), "syntax_errors": len(syntax_errors), "product_qualified": False}))
    if syntax_errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
