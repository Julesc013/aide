"""One finite source/export/installed checklist qualification; no publication."""
import sys
sys.dont_write_bytecode = True
import hashlib, importlib.util, json, os, subprocess, tempfile, unittest
from pathlib import Path
ROOT = Path.cwd()
TASK = ROOT / ".aide/queue/AIDE-RELEASE-CHECKLIST-PROJECTION-01"
EVIDENCE = TASK / "evidence"
OUTPUT = Path(os.environ["AIDE_JOB_OUTPUT"])
BASE = "c4357fc0fa150db5fc715a5365c52140a920d36b"
REPORTS = set(json.loads((EVIDENCE / "report-preimages.json").read_bytes()))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(name, data):
    (OUTPUT / name).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

def invoke(label, command, expected=0):
    out, err = OUTPUT / (label + ".stdout"), OUTPUT / (label + ".stderr")
    receipt = {"command":command, "state":"started", "exit_code":None}
    def record():
        save(label + ".invocation.json", receipt)
    record()
    try:
        with out.open("xb") as stdout, err.open("xb") as stderr:
            result = subprocess.run(command, cwd=ROOT, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr, timeout=120)
        receipt.update(state="completed", exit_code=result.returncode)
    except (OSError, subprocess.SubprocessError) as error:
        receipt.update(state="exception", error_type=type(error).__name__, error=str(error))
        raise
    finally:
        receipt["streams"] = {p.name:{"bytes":p.stat().st_size,"sha256":sha(p)} for p in (out,err) if p.exists()}
        record()
    assert result.returncode == expected, label
    return out.read_bytes()

def suite(subject, label):
    path = subject / ".aide/scripts/tests/test_q48_github_release_draft.py"
    module = load(label + "_q48", path)
    assert Path(module.aide_lite.__file__).resolve() == subject / ".aide/scripts/aide_lite.py"
    tests = unittest.defaultTestLoader.loadTestsFromModule(module)
    def ids(node):
        if isinstance(node, unittest.TestSuite):
            for child in node:
                yield from ids(child)
        else:
            yield node.id()
    names = list(ids(tests))
    assert len(names) == len(set(names)) == 21
    with (OUTPUT / (label + "-tests.log")).open("x", encoding="utf-8") as stream:
        result = unittest.TextTestRunner(stream=stream,verbosity=2).run(tests)
    save(label + "-tests.json", {"subject":str(subject), "test_ids":names, "tests_run":result.testsRun,
        "failures":len(result.failures), "errors":len(result.errors), "skips":[(t.id(),why) for t,why in result.skipped],
        "cli_sha256":sha(subject / ".aide/scripts/aide_lite.py"), "test_sha256":sha(path)})
    assert result.testsRun == 21 and result.wasSuccessful() and not result.skipped
    print(json.dumps({"stage":label,"tests":21,"result":"PASS"}),flush=True)

assert not subprocess.check_output(["git","status","--porcelain"]).strip()
preview = load("checklist_preview", ROOT / ".aide/queue/AIDE-DEPENDENCY-MCP-01/run_preview.py")
preview.BASE = BASE
sys.argv = [__file__,"generate"]
preview.main()

release_before = json.loads((EVIDENCE / "release-preimages.json").read_bytes())
assert all(sha(ROOT / path) == value for path,value in release_before.items())
old = load("checklist_prior_delivered",ROOT / ".aide/export/aide-lite-pack-v0/files/.aide/scripts/aide_lite.py")
lite = load("checklist_current_source",ROOT / ".aide/scripts/aide_lite.py")
before = old.github_release_checklist_data(ROOT,[],[])
after = lite.github_release_checklist_data(ROOT,[],[])
assert len(before["manual_review_required"]) == 7 and len(after["manual_review_required"]) == 10
assert all(before[key] == after[key] for key in before if key != "manual_review_required")
save("baseline-mismatch.json", {"prior_items":before["manual_review_required"],"current_items":after["manual_review_required"],
    "prior_cli_sha256":sha(Path(old.__file__)), "policy_sha256":sha(ROOT / lite.RELEASE_CHECKLIST_POLICY_PATH),
    "other_fields_equal":True, "prior_qualification_repeated":False})
suite(ROOT, "source")

original = json.loads((ROOT / lite.GITHUB_RELEASE_CHECKLIST_JSON_PATH).read_bytes())
checklist = lite.github_release_checklist_data(ROOT,original["blockers"],original["warnings"])
assert all(original[key] == checklist[key] for key in original if key != "manual_review_required")
lite.write_text_if_changed(ROOT / lite.GITHUB_RELEASE_CHECKLIST_JSON_PATH,lite.stable_json_text(checklist))
lite.write_text_if_changed(ROOT / lite.GITHUB_RELEASE_CHECKLIST_MD_PATH,lite.render_github_release_checklist_md(checklist))
validation = lite.github_release_draft_validation_data(ROOT)
assert validation["result"] == "PASS" and validation["no_publish"]
lite.write_text_if_changed(ROOT / lite.GITHUB_RELEASE_DRAFT_VALIDATION_JSON_PATH,lite.stable_json_text(validation))
lite.write_text_if_changed(ROOT / lite.GITHUB_RELEASE_DRAFT_VALIDATION_MD_PATH,lite.render_github_release_draft_validation_md(validation))
release_after = {p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT / ".aide/release").rglob("*") if p.is_file()}
assert release_before.keys() == release_after.keys()
assert {p for p in release_before if release_before[p] != release_after[p]} <= REPORTS
assert lite.run_golden_github_release_checklist(ROOT).result == "PASS"
save("report-refresh.json", {"result":"PASS","preimages":{p:release_before[p] for p in REPORTS},
    "postimages":{p:release_after[p] for p in REPORTS}, "other_release_files_unchanged":len(release_before)-len(REPORTS),
    "legacy_bundle_source_preserved":checklist["source_commit"], "policy_sha256":sha(ROOT / lite.RELEASE_CHECKLIST_POLICY_PATH),
    "source_cli_sha256":sha(Path(lite.__file__))})

refresh = load("checklist_refresh", ROOT / ".aide/queue/AIDE-DAILY-PACK-REFRESH-01/run_refresh.py")
inventory = EVIDENCE / "prior-pack-inventory.json"
prior = json.loads(inventory.read_bytes())
sys.argv = [__file__,"refresh","--inventory",str(inventory.relative_to(ROOT)),"--inventory-sha256",sha(inventory)]
refresh.main()
pack = ROOT / refresh.PACK_REL
post = refresh.inventory_bytes(pack)
previous = {name:row["sha256"] for name,row in prior["files"].items()}
payloads = {"files/.aide/scripts/aide_lite.py","files/.aide/scripts/tests/test_q48_github_release_draft.py","files/docs/reference/github-release-draft.md"}
assert set(previous) == set(post) and len(post) == 875
assert {name for name in previous if previous[name] != post[name]} - refresh.EXCLUDED == payloads
for name in payloads:
    source = ROOT / name.removeprefix("files/")
    expected = lite.portable_cli_text(source.read_text(encoding="utf-8")).encode("utf-8") if name.endswith("/aide_lite.py") else source.read_bytes()
    assert (pack / name).read_bytes() == expected
suite(pack / "files", "delivered")

q31 = load("checklist_import_fixture", ROOT / ".aide/scripts/tests/test_q31_export_pack_governance.py")
delivered = load("checklist_delivered", pack / "files/.aide/scripts/aide_lite.py")
with tempfile.TemporaryDirectory(prefix="checklist-consumer-") as directory:
    target = Path(directory)
    q31.init_target_git(target)
    owned = {"AGENTS.md":b"Project-owned working rules.\r\n","TODO.md":b"Project-owned tasks.\n","PLANS.md":b"Project-owned plan.\n","ROADMAP.md":b"Project-owned roadmap.\n","CHANGELOG.md":b"Project-owned history.\n"}
    for name,raw in owned.items():
        (target / name).write_bytes(raw)
    plan = delivered.apply_import_pack(pack,target,dry_run=True,mode="safe")
    assert not plan["conflicts"]
    result = delivered.apply_import_pack(pack,target,mode="safe",expected_plan_digest=plan["plan_digest"])
    assert result["status"] == "APPLIED" and not result["conflicts"] and not (target / "core").exists()
    agents_after = (target / "AGENTS.md").read_bytes()
    assert agents_after.startswith(owned["AGENTS.md"])
    installed = load("checklist_installed",target / ".aide/scripts/aide_lite.py")
    assert sha(Path(installed.__file__)) == sha(pack / "files/.aide/scripts/aide_lite.py")
    data = installed.github_release_checklist_data(target,[],[])
    assert data["manual_review_required"] == after["manual_review_required"]
    path = target / installed.GITHUB_RELEASE_CHECKLIST_JSON_PATH
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(installed.stable_json_text(data),encoding="utf-8",newline="\n")
    protected = {p.relative_to(target).as_posix():sha(p) for p in target.rglob("*") if p.is_file() and ".git" not in p.parts}
    args = [sys.executable,"-B",str(Path(installed.__file__)),"--repo-root",str(target),"release","checklist"]
    assert b"manual_review_current: true" in invoke("installed-current",args)
    assert all(sha(target / name) == value for name,value in protected.items())
    policy = target / installed.RELEASE_CHECKLIST_POLICY_PATH
    raw_policy = policy.read_bytes()
    policy.write_bytes(raw_policy + b"\n")
    assert b"manual_review_current: true" in invoke("installed-repeat",args)
    policy.write_text("manual_review_items:\n  - Review project-owned ABI\n",encoding="utf-8")
    assert b"manual_review_current: false" in invoke("installed-stale",args,1)
    data = installed.github_release_checklist_data(target,[],[])
    path.write_text(installed.stable_json_text(data),encoding="utf-8",newline="\n")
    assert b"manual_review_current: true" in invoke("installed-tailored",args)
    policy.write_text("manual_review_items: []\n",encoding="utf-8")
    assert b"manual_review_current: false" in invoke("installed-empty",args,1)
    policy.write_bytes(raw_policy)
    path.unlink()
    missing_before = {p.relative_to(target).as_posix():sha(p) for p in target.rglob("*") if p.is_file() and ".git" not in p.parts}
    assert b"manual_review_current: false" in invoke("installed-missing",args,1)
    assert missing_before == {p.relative_to(target).as_posix():sha(p) for p in target.rglob("*") if p.is_file() and ".git" not in p.parts}
    assert (target / "AGENTS.md").read_bytes() == agents_after
    assert all((target/name).read_bytes() == raw for name,raw in owned.items() if name != "AGENTS.md")
    save("installed-consumer.json", {"result":"PASS","customization_preserved":sorted(owned),"agents_manual_prefix_preserved":True,"agents_complete_postimport_bytes_preserved":True,"core_absent":True,
        "fresh_process_current_repeat_stale_tailored_empty_missing":True,"current_call_read_only":True,"native_downstream_adoption":False,
        "installed_cli_sha256":sha(Path(installed.__file__)),"manual_items":after["manual_review_required"]})
assert all(sha(ROOT / path) == value for path,value in release_before.items() if path not in REPORTS)
save("qualified.json", {"result":"PASS","source_tests":21,"delivered_tests":21,"ownership_tests":6,"pack_members":875,
    "payloads_changed":sorted(payloads),"pack_sha256s":post,"fixed_preview":preview.verify(),"models_requested":0,
    "whole_outcome_usage":"unknown","new_os_support_claimed":False,"native_downstream_adoption":False})
print(json.dumps({"result":"PASS","source_tests":21,"delivered_tests":21,"installed":"PASS"}),flush=True)
