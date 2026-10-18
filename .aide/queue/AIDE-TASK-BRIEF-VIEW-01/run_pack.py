"""Owned pack refresh and installed offline brief presentation."""
import sys
sys.dont_write_bytecode = True
import hashlib, importlib.util, json, os, subprocess, tempfile
from pathlib import Path

ROOT = Path.cwd()
TASK = ROOT / '.aide/queue/AIDE-TASK-BRIEF-VIEW-01'
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
        receipt.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8', newline='\n')
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
refresh = load('brief_view_refresh', ROOT / '.aide/queue/AIDE-DAILY-PACK-REFRESH-01/run_refresh.py')
inventory = TASK / 'evidence/prior-pack-inventory.json'
before = json.loads(inventory.read_text(encoding='utf-8'))
sys.argv = [__file__, 'refresh', '--inventory', str(inventory.relative_to(ROOT)),
            '--inventory-sha256', sha(inventory)]
refresh.main()
pack = ROOT / refresh.PACK_REL
after = refresh.inventory_bytes(pack)
old = {name: entry['sha256'] for name, entry in before['files'].items()}
changed = {'files/.aide/scripts/aide_lite.py'}
added = {'files/.aide/scripts/task_brief_view.py', 'files/.aide/scripts/tests/test_task_brief_view.py'}
assert set(after) - set(old) == added and not (set(old) - set(after))
assert {name for name in old if old[name] != after[name]} - refresh.EXCLUDED == changed
source_cli = load('brief_view_source_projection', ROOT / '.aide/scripts/aide_lite.py')
for name in changed | added:
    source = ROOT / name.removeprefix('files/')
    expected = (source_cli.portable_cli_text(source.read_text(encoding='utf-8')).encode('utf-8')
                if name == 'files/.aide/scripts/aide_lite.py' else source.read_bytes())
    assert (pack / name).read_bytes() == expected
invoke('delivered-tests', [sys.executable, '-B', str(TASK / 'run_checks.py'), str(pack / 'files')])

q31 = load("brief_view_q31", ROOT / ".aide/scripts/tests/test_q31_export_pack_governance.py")
aide = load("brief_view_delivered_cli", pack / "files/.aide/scripts/aide_lite.py")
with tempfile.TemporaryDirectory(prefix="brief-view-consumer-") as directory:
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
    helper = ".aide/scripts/task_brief_view.py"
    assert receipt["managed"][helper]["installed_digest"] == sha(target / helper) == sha(ROOT / helper)
    assert receipt["managed"][helper]["ownership"] == "aide_portable_managed"
    from html.parser import HTMLParser
    class Page(HTMLParser):
        def __init__(self, raw):
            super().__init__(convert_charrefs=True)
            self.capture = False; self.parts = []; self.tags = []
            self.feed(raw.decode("ascii")); self.close()
        def handle_starttag(self, tag, attrs):
            self.tags.append((tag,dict(attrs)))
            if tag == "pre" and dict(attrs).get("id") == "observation-json": self.capture = True
        def handle_endtag(self, tag):
            if tag == "pre": self.capture = False
        def handle_data(self, value):
            if self.capture: self.parts.append(value)

    selected = ".aide/scripts/aide_lite.py"
    def write(relative, text):
        path=target/relative; path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(text,encoding="utf-8",newline="\n")
    task_id="PROJECT-VIEW-01"; selected_file="src/repair.py"
    write(f".aide/queue/{task_id}/task.yaml",f"id: {task_id}\ntitle: Preserve the project <contract>\nowner: project-team\n")
    write(f".aide/queue/{task_id}/status.yaml",f"task_id: {task_id}\nstatus: passed\nresult: FIXTURE_PASS\nnext_action: verify_adoption\nremaining_obligations:\n  - native_adoption\n")
    write(selected_file,"def repair():\n    return 1\n")
    write(aide.FILE_QUALITY_LEDGER_JSON_PATH,json.dumps({
        "schema_version":"aide.file-quality-ledger.v0","source_commit":"a"*40,
        "records":[{"path":selected_file,"owner":"project-module","kind":"source","status":"active",
        "quality_level":"documented","recommended_next_action":"inspect","docs_refs":[],"test_refs":[],
        "dependency_refs":[],"warnings":[],"exemptions":[]}]}))
    write(aide.OUTCOME_LEDGER_PATH,"")
    protected=[selected,helper,"docs/reference/task-packets.md",aide.FILE_QUALITY_LEDGER_JSON_PATH,
               aide.OUTCOME_LEDGER_PATH,".aide/queue/AIDE-VALIDATION-OUTPUT-01/task.yaml",
               ".aide/queue/AIDE-VALIDATION-OUTPUT-01/status.yaml",".aide/queue/index.yaml"]
    source_before={p:sha(ROOT/p) for p in protected}
    target_before=refresh.inventory_bytes(target)
    prefix=[sys.executable,"-I",str(target/selected)]
    observations={}
    for label,repository,identity,path in [
            ("installed",target,task_id,selected_file),
            ("real-source",ROOT,"AIDE-VALIDATION-OUTPUT-01",".aide/scripts/tests/test_validation_output.py")]:
        outputs={}
        expected_exit=0 if label=="installed" else 2
        for mode in ["json","html"]:
            outputs[mode]=invoke(label+"-"+mode,prefix+["--repo-root",str(repository),"task","brief",
                "--task-id",identity,"--path",path,"--"+mode],target,expected=expected_exit)
        data=json.loads(outputs["json"]);page=Page(outputs["html"])
        assert json.loads("".join(page.parts))==data
        assert data["continuation"]["task"]["task_id"]==identity
        assert data["continuation"]["recommendation"]=="inspect_completed_evidence"
        assert not data["execution_admitted"] and not data["acceptance_verified"]
        assert not {tag for tag,_ in page.tags}&{"script","iframe","frame","form","img","link","object","embed"}
        assert not any(key.lower().startswith("on") or key in {"href","src","action","srcdoc","style"}
                       for _,attrs in page.tags for key in attrs)
        if label=="installed":
            assert data["continuation"]["task"]["remaining_obligations"]==["native_adoption"]
            assert data["quality"]["owner"]=="project-module"
            assert b"&lt;contract&gt;" in outputs["html"]
        else:
            recorded=json.loads((TASK/"evidence/attempt-01-actual-brief.json").read_bytes())
            assert data==recorded
        canonical=json.dumps(data,sort_keys=True,ensure_ascii=True,separators=(",",":")).encode("ascii")
        observations[label]={"state":data["result"],"task_id":identity,
            "observation_sha256":hashlib.sha256(canonical).hexdigest(),"html_sha256":hashlib.sha256(outputs["html"]).hexdigest(),
            "complete_json_equal":True,"inactive_markup":True,"execution_admitted":False}
    assert refresh.inventory_bytes(target)==target_before
    assert all(sha(ROOT/p)==h for p,h in source_before.items())
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
              "source_inputs_unchanged": source_before, "browser_render": "NOT_RUN", "execution_authority": False}
    (OUTPUT / "installed-consumer.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8", newline="\n")
assert all(sha(ROOT / p) == h for p,h in release_before.items())
assert refresh.inventory_bytes(pack) == after and len(after) == 874
(OUTPUT / "delivered-result.json").write_text(json.dumps({
    "status": "PASS", "delivered_tests": 104, "safe_installed_consumer": "PASS",
    "changed_payload": sorted(changed), "added_payload": sorted(added),
    "pack_members": len(after), "pack_sha256s": after, "models_requested": 0,
}, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({"status":"PASS", "delivered_tests":104, "safe_installed_consumer":"PASS"}))
