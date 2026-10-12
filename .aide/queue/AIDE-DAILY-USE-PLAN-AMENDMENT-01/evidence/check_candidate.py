"""Check this task's exact diff scope, added links and preserved release paths."""
from __future__ import annotations

import fnmatch
import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / ".aide/queue/AIDE-DAILY-USE-PLAN-AMENDMENT-01/task.yaml"


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True,
                          encoding="utf-8").stdout


def main():
    text = TASK.read_text(encoding="utf-8")
    section = text.split("  allowed_paths:\n", 1)[1].split("  generated_only:", 1)[0]
    allowed = re.findall(r"^    - (.+)$", section, re.MULTILINE)
    changed = sorted(set(git("diff", "--name-only", "HEAD").splitlines()
                         + git("ls-files", "--others", "--exclude-standard").splitlines()))
    errors = []
    for path in changed:
        if not any(fnmatch.fnmatchcase(path, pattern) for pattern in allowed):
            errors.append(f"out of scope: {path}")
        if path.startswith((".aide/export/", ".aide/release/", "core/", "specs/")):
            errors.append(f"operative/release source changed: {path}")
    current = ""
    links = 0
    for line in git("diff", "--unified=0", "HEAD").splitlines():
        if line.startswith("+++ b/"):
            current = line[6:]
        elif line.startswith("+") and not line.startswith("+++") and current.endswith(".md"):
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", line[1:]):
                if "://" in target or target.startswith("#"):
                    continue
                target = target.split("#", 1)[0]
                if not (ROOT / current).parent.joinpath(target).exists():
                    errors.append(f"missing added link: {current} -> {target}")
                links += 1
    release_ref = git("rev-parse", "aide-lite-v1.0.0^{}").strip()
    if release_ref != "0f293eb6a99dbd444bfa35016007b13451c49275":
        errors.append("published tag subject changed")
    manifest_path = ".aide/queue/AIDE-DAILY-USE-PLAN-AMENDMENT-01/evidence/candidate-manifest.json"
    manifest = [{"path": p, "sha256": hashlib.sha256((ROOT / p).read_bytes()).hexdigest()}
                for p in changed if p != manifest_path and (ROOT / p).is_file()]
    result = {"status": "FAIL" if errors else "PASS", "changed_files": len(changed),
              "added_links_checked": links, "release_tag_commit": release_ref,
              "errors": errors, "candidate_files": manifest,
              "note": "Manifest excludes itself. File hashes support review; this is not an independent verdict."}
    print(json.dumps(result, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
