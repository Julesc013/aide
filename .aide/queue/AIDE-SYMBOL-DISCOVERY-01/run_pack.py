"""Owned pack refresh and installed fresh symbol discovery."""
import sys
sys.dont_write_bytecode = True
import hashlib, importlib.util, json, os, subprocess, tempfile
from pathlib import Path

ROOT = Path.cwd()
TASK = ROOT / '.aide/queue/AIDE-SYMBOL-DISCOVERY-01'
OUTPUT = Path(os.environ['AIDE_JOB_OUTPUT'])

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

def invoke(label, command, cwd=ROOT, expected=0):
    stdout, stderr = OUTPUT / (label + '.stdout'), OUTPUT / (label + '.stderr')
    receipt = OUTPUT / (label + '.invocation.json')
    record = {'command': command, 'cwd': str(cwd), 'state': 'started', 'exit_code': None}
    def save():
        receipt.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    save()
    try:
        with stdout.open('xb') as out, stderr.open('xb') as err:
            result = subprocess.run(command, cwd=cwd, stdin=subprocess.DEVNULL,
                                    stdout=out, stderr=err, timeout=90)
        record.update(state='completed', exit_code=result.returncode)
    except (OSError, subprocess.SubprocessError) as error:
        record.update(state='exception', error_type=type(error).__name__, error=str(error))
        raise
    finally:
        record['streams'] = {p.name: {'bytes': p.stat().st_size, 'sha256': sha(p)}
                             for p in (stdout, stderr) if p.exists()}
        save()
    assert result.returncode == expected, label + ' failed; original output retained'
    return stdout.read_bytes()

assert not subprocess.check_output(['git', 'status', '--porcelain']).strip()
release_before = json.loads((TASK / 'evidence/release-preimages.json').read_text(encoding='utf-8'))
assert all(sha(ROOT / p) == h for p, h in release_before.items())
refresh = load('symbol_refresh', ROOT / '.aide/queue/AIDE-DAILY-PACK-REFRESH-01/run_refresh.py')
inventory = TASK / 'evidence/prior-pack-inventory.json'
before = json.loads(inventory.read_text(encoding='utf-8'))
# Reuse the completed export from failed job2; do not invoke reset/export again.
sys.path.insert(0, str(ROOT))
from core.execution.managed_workspace import content_digest, load_config
e = TASK / "evidence"
retired = json.loads((e / "pack-attempt-02.json").read_text(encoding="utf-8"))
assert retired["phase"] == "retired" and retired["result"]["exit_code"] == 1
assert retired["result"]["quiescent"] and retired["scratch_absent"] and retired["reservation_released"]
_, roots, _ = load_config(ROOT / ".aide.local/execution.json")
assert not (roots["scratch"] / retired["job_id"]).exists()
for name, digest in retired["collected_manifest"].items():
    assert content_digest(Path(retired["retained"]) / name) == digest
completed = json.loads((e / "attempt-02-qualification.json").read_text(encoding="utf-8"))
assert completed == json.loads((Path(retired["retained"]) / "output/qualification.json").read_text(encoding="utf-8"))
assert completed["status"] == "PASS" and completed["after_files"] == 872
assert all(item["exit_code"] == 0 for item in completed["operations"].values())
assert completed["ownership_tests"] == {"tests_run": 6, "failures": 0, "errors": 0, "skips": 0}
pack = ROOT / refresh.PACK_REL
after = refresh.inventory_bytes(pack)
assert after == completed["after_sha256s"]
source_checks = json.loads((e / "attempt-01-source-tests.json").read_text(encoding="utf-8"))
assert source_checks["tests_run"] == 44 and not any(source_checks[k] for k in ["errors","failures","skips"])
for path, digest in source_checks["inputs"].items():
    assert sha(ROOT / path) == digest
old = {name: entry["sha256"] for name, entry in before["files"].items()}
changed = {"files/.aide/scripts/aide_lite.py", "files/docs/reference/file-quality-ledger.md",
           "files/.aide/commands/catalog.yaml"}
added = {"files/.aide/scripts/quality_symbols.py", "files/.aide/scripts/tests/test_quality_symbols.py"}
assert set(after) - set(old) == added and not (set(old) - set(after))
assert {name for name in old if old[name] != after[name]} - refresh.EXCLUDED == changed
catalog = "files/.aide/commands/catalog.yaml"
prior_catalog = (e / "catalog-preimage.yaml").read_bytes()
assert hashlib.sha256(prior_catalog).hexdigest() == old[catalog]
old_invocation = b"quality <ledger|validate|status|explain-file|docs|tests|modules|reuse>"
new_invocation = b"quality <ledger|validate|status|explain-file|inspect-symbol|docs|tests|modules|reuse>"
assert prior_catalog.count(old_invocation) == 1
assert (pack / catalog).read_bytes() == prior_catalog.replace(old_invocation, new_invocation)
source_cli = load('symbol_source_projection', ROOT / '.aide/scripts/aide_lite.py')
for name in (changed | added) - {catalog}:
    source = ROOT / name.removeprefix('files/')
    expected = (source_cli.portable_cli_text(source.read_text(encoding='utf-8')).encode('utf-8')
                if name == 'files/.aide/scripts/aide_lite.py' else source.read_bytes())
    assert (pack / name).read_bytes() == expected
invoke('delivered-tests', [sys.executable, '-B', str(TASK / 'run_checks.py'), str(pack / 'files')])

q31 = load("symbol_q31", ROOT / ".aide/scripts/tests/test_q31_export_pack_governance.py")
aide = load("symbol_delivered_cli", pack / "files/.aide/scripts/aide_lite.py")
with tempfile.TemporaryDirectory(prefix="symbol-consumer-") as directory:
    target = Path(directory)
    q31.init_target_git(target)
    (target / "AGENTS.md").write_text("Project-owned working rules; preserve.\n", encoding="utf-8")
    (target / "notes.txt").write_bytes(b"Project customization remains.\r\n")
    manual = {name: (target / name).read_bytes() for name in ["AGENTS.md", "notes.txt"]}
    preview = aide.apply_import_pack(pack, target, dry_run=True, mode="safe")
    assert not preview["conflicts"]
    installed = aide.apply_import_pack(pack, target, mode="safe", expected_plan_digest=preview["plan_digest"])
    assert installed["status"] == "APPLIED" and not installed["conflicts"]
    assert not (target / "core").exists()
    for name, raw in manual.items():
        assert raw in (target / name).read_bytes()
    receipt = json.loads((target / aide.PORTABLE_IMPORT_RECEIPT_PATH).read_bytes())
    helper = ".aide/scripts/quality_symbols.py"
    assert receipt["managed"][helper]["installed_digest"] == sha(target / helper) == sha(ROOT / helper)
    assert receipt["managed"][helper]["ownership"] == "aide_portable_managed"
    selected = ".aide/scripts/aide_lite.py"
    protected = [selected, helper, "docs/reference/file-quality-ledger.md", aide.FILE_QUALITY_LEDGER_JSON_PATH]
    source_before = {p: sha(ROOT / p) for p in protected}
    target_before = refresh.inventory_bytes(target)
    prefix = [sys.executable, "-I", str(target / selected)]
    observations = {}
    for label, repository in [("installed", target), ("real-source", ROOT)]:
        raw = invoke(label + "-inspect", prefix + ["--repo-root", str(repository), "quality",
            "inspect-symbol", "portable_cli_text", "--path", selected, "--json"], target)
        report = json.loads(raw)
        assert report["result"] == "PASS" and report["read_only"]
        syntax = report["files"][0]["syntax"]
        assert syntax["sha256"] == sha(repository / selected) and syntax["state"] == "parsed"
        definitions = syntax["definitions"]["items"]
        assert len(definitions) == 1 and definitions[0]["qualified_name"] == "portable_cli_text"
        assert definitions[0]["kind"] == "function" and len(syntax["calls"]["items"]) >= 1
        assert all(call["resolution"] == "unresolved" for call in syntax["calls"]["items"])
        observations[label] = {"sha256": syntax["sha256"], "definition": definitions[0],
                               "call_locations": [call["line"] for call in syntax["calls"]["items"]],
                               "recorded_context_state": report["files"][0]["recorded_context"]["state"]}
    text = invoke("installed-text", prefix + ["--repo-root", str(target), "quality",
        "inspect-symbol", "portable_cli_text", "--path", selected], target).decode("ascii")
    assert "runtime binding" in text and "source_sha256:" in text
    assert refresh.inventory_bytes(target) == target_before
    assert all(sha(ROOT / p) == h for p,h in source_before.items())
    # Independent oracle: source and delivered text differ at exactly the intended
    # binding line. Do not use the implementation under test as the only oracle.
    source_lines = (ROOT / selected).read_text(encoding="utf-8").splitlines()
    delivered_lines = (target / selected).read_text(encoding="utf-8").splitlines()
    assert len(source_lines) == len(delivered_lines)
    differences = [(n + 1, a, b) for n,(a,b) in enumerate(zip(source_lines,delivered_lines)) if a != b]
    assert len(differences) == 1
    assert differences[0][1] == 'WORK_EFFORT_MODULE_PATH = "core/execution/work_effort.py"'
    assert differences[0][2] == 'WORK_EFFORT_MODULE_PATH = ".aide/scripts/aide_work_effort.py"'
    assert sha(ROOT / selected) != sha(target / selected)
    for name, raw in manual.items():
        assert raw in (target / name).read_bytes()
    record = {"result": "PASS", "observations": observations, "helper_receipt": receipt["managed"][helper],
              "independent_projection_binding_oracle": True, "one_intentional_binding_line_changed": differences[0][0],
              "customization_preserved": True, "core_absent": True, "fresh_process_read_only": True,
              "source_inputs_unchanged": source_before, "semantic_resolution_claimed": False}
    (OUTPUT / "installed-consumer.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
assert all(sha(ROOT / p) == h for p,h in release_before.items())
assert refresh.inventory_bytes(pack) == after and len(after) == 872
(OUTPUT / "delivered-result.json").write_text(json.dumps({
    "status": "PASS", "delivered_tests": 44, "safe_installed_consumer": "PASS",
    "changed_payload": sorted(changed), "added_payload": sorted(added),
    "pack_members": len(after), "pack_sha256s": after, "models_requested": 0,
}, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status":"PASS", "delivered_tests":44, "safe_installed_consumer":"PASS"}))


# Complete the final preview in this remaining allocation; the successful export
# and source tests above are reused, not repeated.
for label, args in [("final-doctor", ["doctor"]), ("final-validation", ["validate"]), ("final-pack-status", ["pack-status"])]:
    invoke(label, [sys.executable, "-B", ".aide/scripts/aide_lite.py", *args])
preview = load("symbol_final_preview", ROOT / ".aide/queue/AIDE-DEPENDENCY-MCP-01/run_preview.py")
preview.BASE = "118ab7829f300050394dc67a3af943963acfe218"
sys.argv = [str(TASK / "run_pack.py"), "generate"]
preview.main()
assert refresh.inventory_bytes(pack) == after
assert all(sha(ROOT / path) == digest for path,digest in source_checks["inputs"].items())
assert all(sha(ROOT / p) == h for p,h in release_before.items())
(OUTPUT / "qualification.json").write_text(json.dumps({
    "result": "PASS", "source_tests_reused": 44, "delivered_tests": 44,
    "installed_consumer": "PASS", "prior_failed_job_preserved": retired["job_id"],
    "completed_export_reused": True, "export_repeated": False,
    "catalogue_exact_delta": True, "preview": preview.verify(), "models_requested": 0,
    "whole_outcome_usage": "unknown",
}, indent=2) + "\n", encoding="utf-8")
