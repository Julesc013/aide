"""Task-local structural proof; does not qualify runtime or adopt requirements."""
import fnmatch
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[3]
TASK = ROOT / ".aide/queue/AIDE-ARCHITECTURE-RECONCILIATION-01"
BASE = "3d186d0584bb40f18402a626c9fe099260fae3d4"


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                          text=True, encoding="utf-8", check=True).stdout


manifest = json.loads((ROOT / "specs/control-plane/amendment-manifest.json").read_text(encoding="utf-8"))
imported = json.loads((ROOT / "specs/control-plane/import-manifest.json").read_text(encoding="utf-8"))
assert manifest["baseline_commit"] == BASE and len(manifest["records"]) == 19
for record in manifest["records"]:
    current = (ROOT / record["destination"]).read_bytes().replace(b"\r\n", b"\n")
    original = git("show", BASE + ":" + record["destination"]).encode()
    assert current.startswith(original), record["destination"]
    assert hashlib.sha256(original).hexdigest() == record["baseline_git_lf_sha256"]
    assert hashlib.sha256(current).hexdigest() == record["current_git_lf_sha256"]
    assert b"proposed design, not adoption, activation or qualification" in current

requirements, cases, draft_count = [], [], 0
for record in imported["records"]:
    if record.get("disposition") != "import_as_explicit_draft":
        continue
    text = (ROOT / record["destination"]).read_text(encoding="utf-8")
    draft_count += 1
    assert "\nstatus: draft\n" in text and "\n  adoption: proposed\n" in text
    assert "behavioral_qualification: not_run" in text
    requirements.extend(re.findall(r"^### (UR-[A-Z]+-\d+)\b", text, re.M))
    cases.extend(re.findall(r"^\| `(UC-[A-Z]+-\d+)`", text, re.M))
assert draft_count == 34
assert len(requirements) == len(set(requirements)) == 244
assert len(cases) == len(set(cases)) == 244
git("diff", "--exit-code", BASE, "--", "specs/control-plane/import-manifest.json")

changed = set(git("diff", "--name-only", BASE).splitlines())
changed.update(git("ls-files", "--others", "--exclude-standard").splitlines())
packet = (TASK / "task.yaml").read_text(encoding="utf-8")
block = packet.split("  allowed_paths:\n", 1)[1].split("  generated_only:", 1)[0]
allowed = [line.strip()[2:] for line in block.splitlines() if line.strip().startswith("- ")]
assert all(any(fnmatch.fnmatchcase(path, pattern) for pattern in allowed)
           for path in changed), "Changed path outside allowed scope"

broken, link_count = [], 0
for name in sorted(changed):
    if not name.endswith(".md"):
        continue
    source = ROOT / name
    text = re.sub(r"```[\s\S]*?```", "", source.read_text(encoding="utf-8-sig"))
    for target in re.findall(r"\[[^\]\n]*\]\(([^\)\n]+)\)", text):
        target = target.strip().strip("<>")
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#") or "*" in target:
            continue
        link_count += 1
        if not (source.parent / unquote(target.split("#", 1)[0])).resolve().exists():
            broken.append({"source": name, "target": target})
assert not broken, broken
git("diff", "--check")

result = {"result": "PASS_WITH_SOURCE_CUSTODY_LIMITATION", "amended_topic_owners": 19,
          "original_text_preserved": True, "draft_chapters": draft_count,
          "original_UR_aliases": len(requirements), "original_UC_designs": len(cases),
          "historical_import_receipt_unchanged": True,
          "changed_paths_in_scope": len(changed), "relative_links_checked": link_count,
          "broken_links": broken, "source_raw_hash_known": manifest["source"]["sha256"] is not None,
          "behavioral_cases_run": 0}
(TASK / "evidence/structural-checks.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result))
