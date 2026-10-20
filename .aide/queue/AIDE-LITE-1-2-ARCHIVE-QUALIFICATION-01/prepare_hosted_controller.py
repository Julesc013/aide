"""Adapt the existing bounded hosted observer; never dispatch during preparation."""
from pathlib import Path

ROOT = Path.cwd()
TASK = Path(__file__).parent
original = ROOT / '.aide/queue/AIDE-LITE-POSIX-LIFECYCLE-01/observe_hosted.py'
source = original.read_text(encoding='utf-8')


def change(before, after, count=1):
    global source
    assert source.count(before) == count, before
    source = source.replace(before, after)


for before, after in [('source-03.json', 'hosted-source.json'), ('source-effect-03.json', 'hosted-effect.json'),
                      ('source-review-03.json', 'hosted-review.json'), ('source-execution-03.log', 'hosted-checkpoint.log'),
                      ('checkpoint_and_host.py', 'checkpoint_and_host.py')]:
    if before != after:
        change(before, after)
change('for ref in ("main", "dev", "origin/main", "origin/dev"):\n                assert git("rev-parse", ref) == plan["integration_base"]',
       'for ref in ("dev", "origin/dev"):\n                assert git("rev-parse", ref) == plan["dev_base"]\n            for ref in ("main", "origin/main"):\n                assert git("rev-parse", ref) == plan["main_base"]')
change('plan["integration_base"], "refs/heads/main": plan["integration_base"]',
       'plan["dev_base"], "refs/heads/main": plan["main_base"]')
start = source.index('            local = json.loads(')
end = source.index('            repo = api(', start)
source = source[:start] + '''            pins = json.loads((EVIDENCE / "hosted-inputs.json").read_bytes())
            assert sha(EVIDENCE / "hosted-inputs.json") == plan["package_inputs_sha256"]
            assert all(sha(ROOT / name) == value for name, value in pins["files"].items())
            build = json.loads((EVIDENCE / "revised-build-qualified.json").read_bytes())
            assert build["state"] == "PASS_REVISED_BUILD_AND_COMPLETE_DELTA_ONLY"
            assert build["scratch_absent"] and build["reservation_released"]
            assert all(workspace.content_digest(Path(build["retained"]) / name) == value
                       for name, value in build["collected_manifest"].items())
            reuse = json.loads((EVIDENCE / "revised-behavior-reuse-review.json").read_bytes())
            assert reuse["decision"] == "ACCEPT" and not reuse["required_fixes"]
            assert all(sha(ROOT / name) == value for name, value in plan["stable_assets"].items())
''' + source[end:]
change(' + " lifecycle observation"', ' + " actual archive qualification"')
change('assert 1 <= len(decoded) <= 256', 'assert 1 <= len(decoded) <= 512')
change('r"[a-z0-9][a-z0-9._-]{0,127}"', 'r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}"')
start = source.index('                data = json.loads(files["result.json"])')
end = source.index('                destination = logs / profile', start)
source = source[:start] + '''                data = json.loads(files["release-result.json"])
                assert data["source_commit"] == plan["source_commit"]
                profile = {"aide-lite-local-windows-server": "windows-2025-x64",
                           "aide-lite-local-linux": "ubuntu-24.04-x64",
                           "aide-lite-local-macos": "macos-15-arm64"}[data["profile_id"]]
                nested = json.loads(files.get("nested-receipt-map.json", b"{}"))
                for name, item in nested.items():
                    assert not name.startswith("/") and ".." not in Path(name).parts
                    assert hashlib.sha256(files[item["transport_member"]]).hexdigest() == item["sha256"]
''' + source[end:]
start = source.index('        for profile, bundle in profiles.items():')
end = source.index('    except BaseException as error:', start)
source = source[:start] + '''        for profile, bundle in profiles.items():
            data = bundle["data"]
            passed = (data["status"] == "PASS" and data["fixture_retired"]
                      and data.get("input_sha256") == plan["package_inputs_sha256"]
                      and len(data.get("forms", [])) == 49
                      and len(data.get("unqualified_cli_forms", [])) == 7)
            summary["profiles"][profile] = {"status": data["status"], "qualification_pass": passed,
                "environment": data.get("environment"), "declared_environment": data.get("declared_environment"),
                "forms": data.get("forms", []), "cases": data.get("cases", []),
                "fixture_retired": data["fixture_retired"],
                "receipt_index_sha256": bundle["receipt_index_sha256"],
                "error": data.get("error"), "error_type": data.get("error_type")}
        summary["qualification_pass"] = all(p["qualification_pass"] for p in summary["profiles"].values())
        remaining()
        summary_bytes = (json.dumps(summary, indent=2) + "\\n").encode()
        assert len(summary_bytes) <= 2 * 1024 * 1024
        (EVIDENCE / "hosted-observed.json").write_bytes(summary_bytes)
        record.update(state="observed_terminal", summary_sha256=sha(EVIDENCE / "hosted-observed.json"))
        save()
        print(json.dumps({"state": record["state"], "run_id": run_id,
                         "qualification_pass": summary["qualification_pass"],
                         "profiles": {p: b["qualification_pass"] for p, b in summary["profiles"].items()}}), flush=True)
''' + source[end:]
destination = TASK / 'observe_hosted.py'
assert not destination.exists()
destination.write_text(source, encoding='utf-8', newline='\n')
print('Prepared bounded observer from ' + original.relative_to(ROOT).as_posix() + '; no effect executed.')
