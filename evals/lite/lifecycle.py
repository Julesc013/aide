"""Observe real delivered Lite lifecycle; collector success is not product acceptance.

Uses the original consumer's archive/install/removal oracles without changing
their assertions. Fixtures stay below an explicitly supplied temporary parent.
No provider calls, support promotion or source refresh. Delivered workflow cases
do not patch product behavior; regression fixtures inject declared failures.
"""
from __future__ import annotations

import argparse
import base64
import gzip
import time
import hashlib
import importlib.util
import json
import os
import platform
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import traceback
import unittest

ROOT = Path(__file__).resolve().parents[2]
WORKUNITS = ("AIDE-LITE-MODERN-LIFECYCLE-01", "AIDE-LITE-POSIX-LIFECYCLE-01")
HELPER = ROOT / ".aide/queue/AIDE-CURRENT-SCOPED-LITE-QUALIFICATION-01/canaries/lifecycle_helper.py"
FIXTURES = ROOT / ".aide/scripts/tests/test_aide_distribution_fixture_portability.py"
MAX_RAW = 8 * 1024 * 1024
MAX_COMPRESSED = 2 * 1024 * 1024


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def save(path, value):
    path.write_bytes((json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode())


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def emit_receipts(out):
    """Lossless bounded log transport, not an Actions artifact/cache upload."""
    files = sorted(p for p in out.iterdir() if p.is_file())
    if sum(p.stat().st_size for p in files) > MAX_RAW:
        raise ValueError("receipt raw-byte cap exceeded; retain local files")
    body = {p.name: base64.b64encode(p.read_bytes()).decode("ascii") for p in files}
    raw = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
    packed = gzip.compress(raw, mtime=0)
    if len(packed) > MAX_COMPRESSED:
        raise ValueError("receipt transport cap exceeded; retain local files")
    encoded = base64.b64encode(packed).decode("ascii")
    chunks = [encoded[i:i + 24000] for i in range(0, len(encoded), 24000)]
    digest = hashlib.sha256(packed).hexdigest()
    for index, chunk in enumerate(chunks):
        print(f"AIDE_RECEIPT_V1 {index + 1}/{len(chunks)} {digest} {chunk}", flush=True)


def characterize(work, out, pinned, *, qualify=False, continue_local=False):
    helper = load("aide_lifecycle_original_helpers", HELPER)
    commands = []

    class Recorder(helper.Recorder):
        def run(self, label, script, root, *parts, exits=(0,), offline_text=False):
            argv = [sys.executable, "-I", "-B", str(script), "--repo-root", str(root), *parts]
            row = {"label": label, "argv": argv, "state": "started", "exit_code": None}
            started = time.monotonic()
            row["started_unix_ns"] = time.time_ns()
            commands.append(row)
            record = out / (label + ".command.json")
            save(record, row)
            streams = [out / (label + suffix) for suffix in (".stdout", ".stderr")]
            try:
                with streams[0].open("xb") as stdout, streams[1].open("xb") as stderr:
                    result = subprocess.run(argv, cwd=ROOT, stdin=subprocess.DEVNULL,
                                            stdout=stdout, stderr=stderr, timeout=60)
                row.update(state="completed", exit_code=result.returncode)
            except (OSError, subprocess.SubprocessError) as error:
                row.update(state="exception", error_type=type(error).__name__, error=str(error))
                raise
            finally:
                row["elapsed_seconds"] = time.monotonic() - started
                row["streams"] = {p.name: {"bytes": p.stat().st_size, "sha256": sha(p)}
                                  for p in streams if p.exists()}
                save(record, row)
            if any(p.stat().st_size > MAX_RAW for p in streams):
                raise ValueError("command stream cap exceeded")
            stdout, stderr = (p.read_bytes().decode("utf-8", errors="replace") for p in streams)
            if result.returncode not in exits:
                raise AssertionError(f"{label} exit {result.returncode}; see raw streams")
            if offline_text and "network_calls: none" not in stdout:
                raise AssertionError(f"{label} did not declare offline execution")
            return subprocess.CompletedProcess(argv, result.returncode, stdout, stderr)

    rec = Recorder(out)
    zip_path = ROOT / ".aide/release/stable/aide-lite-v1.1.0.zip"
    tar_path = ROOT / ".aide/release/stable/aide-lite-v1.1.0.tar.gz"
    zip_members = helper.extract_zip(zip_path, work / "published-zip")
    tar_members = helper.extract_tar(tar_path, work / "published-tar")
    if zip_members != tar_members:
        raise AssertionError("published ZIP/tar member identities differ")
    stable = work / "published-zip" / helper.PACK_NAME
    development = ROOT / ".aide/export/aide-lite-pack-v0"
    dev_members = {helper.PACK_NAME + "/" + name: digest
                   for name, digest in pinned["development_members"].items()}
    helper.verify_pack(development, dev_members)
    cases = []
    subjects = (("development-export", development),) if continue_local else (("published-1.1.0", stable), ("development-export", development))
    for subject, pack in subjects:
        module = helper.load_delivered(pack)
        for shape in ("fresh", "brownfield"):
            label = subject + "-" + shape
            target = work / label
            target.mkdir()
            row = {"subject": subject, "shape": shape, "installed": False,
                   "detached": False, "preserved": False, "native_acceptance": False,
                   "cli_sha256": sha(pack / "files/.aide/scripts/aide_lite.py")}
            authored = {}
            if shape == "brownfield":
                authored.update({"unknown.txt": b"Project-owned data.\r\n",
                                 "AGENTS.md": b"# Project rules\r\nKeep these exact bytes.\r\n",
                                 "TODO.md": b"# Project TODO\n", "PLANS.md": b"# Project plan\n",
                                 "ROADMAP.md": b"# Project roadmap\n", "CHANGELOG.md": b"# History\n",
                                 ".aide/memory/project-state.md": b"Project-owned knowledge.\n",
                                 "tools/existing.py": b"print('project tool')\n"})
            for name, raw in authored.items():
                path = target / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw)
            original_agents = authored.get("AGENTS.md")
            appended_suffix = None
            try:
                helper.install(rec, label, pack, target)
                row["installed"] = True
                if shape == "fresh":
                    authored["unknown.txt"] = b"Project-owned data added after adoption.\r\n"
                    (target / "unknown.txt").write_bytes(authored["unknown.txt"])
                receipt = module.load_portable_import_receipt(target)
                managed = set(receipt["managed"])
                unknown = {name: hashlib.sha256(raw).hexdigest() for name, raw in authored.items()
                           if name != "AGENTS.md"}
                if original_agents is not None:
                    before = (target / "AGENTS.md").read_bytes()
                    if not before.startswith(original_agents):
                        raise AssertionError("adoption changed authored guidance")
                    suffix = b"\r\n# New project rule after adoption.\r\n"
                    appended_suffix = suffix
                    (target / "AGENTS.md").write_bytes(before + suffix)
                    expected_agents = module.portable_agents_section_postimage(
                        before + suffix, receipt["managed"]["AGENTS.md"]["installed_digest"])
                    if expected_agents is None or not expected_agents.startswith(original_agents) or not expected_agents.endswith(suffix):
                        raise AssertionError("authored section preservation oracle failed")
                else:
                    expected_agents = None
                rec.installed(label + "-doctor", target, "doctor")
                plan = helper.plan_removal(rec, label + "-removal-preview", target)
                if plan["status"] != "PLANNED" or set(plan["candidate_targets"]) != managed:
                    raise AssertionError("removal plan did not cover all owned targets")
                result = rec.installed(label + "-removal-apply", target, "apply-removal", "--target",
                                       str(target), "--expect-plan", plan["plan_digest"], "--json")
                applied = json.loads(result.stdout)
                row["removal_status"] = applied["status"]
                if applied["status"] != "DETACHED" or applied["receipt_retained"]:
                    raise AssertionError("removal did not fully detach")
                helper.assert_detached(target, managed, module, unknown, authored_agents=expected_agents)
                row.update(detached=True, native_acceptance=True)
            except Exception as error:
                row.update(error_type=type(error).__name__, error=str(error), traceback=traceback.format_exc())
            finally:
                # Preservation is an independent condition, including after refusal/failure.
                row["preserved"] = all((target / name).is_file() and (target / name).read_bytes() == raw
                                       for name, raw in authored.items() if name != "AGENTS.md")
                if original_agents is not None:
                    row["preserved"] &= (target / "AGENTS.md").is_file() and (target / "AGENTS.md").read_bytes().startswith(original_agents)
                    if appended_suffix is not None:
                        row["preserved"] &= (target / "AGENTS.md").is_file() and (target / "AGENTS.md").read_bytes().endswith(appended_suffix)
                row["native_acceptance"] &= row["preserved"]
                cases.append(row)
                save(out / (label + ".case.json"), row)
    if qualify:
        cases.extend(qualify_successor(work, out, rec, helper, stable, development))
    return cases, commands, len(zip_members)


def qualify_successor(work, out, rec, helper, old, new, *, subject="development-export"):
    """Actual published predecessor, project edits, recovery and safe exit."""
    module = helper.load_delivered(new)
    changed = ".aide/scripts/aide_lite.py"
    optional = ".aide.local.example/README.md"
    old_bytes = (old / "files" / changed).read_bytes()
    new_bytes = (new / "files" / changed).read_bytes()
    if old_bytes == new_bytes:
        raise AssertionError("predecessor conflict needs real changed upstream bytes")
    cases = []
    for shape in ("fresh", "brownfield"):
        label = "published-upgrade-" + shape
        target = work / label
        target.mkdir()
        row = {"subject": subject, "shape": label,
               "native_acceptance": False, "preserved": False, "checks": []}
        authored = b"# Existing project rules\r\nPreserve outside the owned block.\r\n"
        project = {"project.txt": b"Preserve project content.\r\n",
                   "tools/project.py": b"print('project tool')\n"}
        (target / "AGENTS.md").write_bytes(authored)
        for relative, data in project.items():
            path = target / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        try:
            helper.install(rec, label + "-old-install", old, target)
            if shape == "brownfield":
                controls = {"schema_version": "aide.project-customizations.v2", "entries": {},
                            "disabled_features": [{"feature_id": "local_state_examples",
                                "rationale": "Project maintains these examples."}]}
                project[module.PROJECT_CUSTOMIZATIONS_PATH] = (json.dumps(controls, indent=2) + "\n").encode()
                project[optional] = b"Project-maintained optional example.\r\n"
                for relative in (module.PROJECT_CUSTOMIZATIONS_PATH, optional):
                    (target / relative).write_bytes(project[relative])
                local_note = b"\n# Project-specific explanation retained across update.\n"
                (target / changed).write_bytes(old_bytes + local_note)
                selected = work / "resolved-cli.py"
                selected.write_bytes(new_bytes + local_note)
                resolutions = {changed: selected}
            else:
                resolutions = {}

            def update(suffix, *extra, exits=(0,)):
                return rec.pack(label + suffix, new, "import-pack", "--pack", str(new),
                    "--from-pack", str(old), "--target", str(target), "--mode", "safe", *extra,
                    exits=exits, offline_text=True)

            if resolutions:
                before = helper.tree_hashes(target)
                preview = update("-conflict-preview", "--dry-run", exits=(2,))
                assert helper.field(preview.stdout, "status") == "PLANNED_CONFLICT"
                refused = update("-conflict-refusal", "--expect-plan", helper.field(preview.stdout, "plan_digest"), exits=(2,))
                assert helper.field(refused.stdout, "status") == "CONFLICT"
                assert helper.tree_hashes(target) == before
                row["checks"].append("real_upstream_conflict_refuses_without_writes")
            extra = ("--resolve", changed, str(selected)) if resolutions else ()
            preview = update("-update-preview", *extra, "--dry-run")
            assert helper.field(preview.stdout, "status") == "PLANNED"
            partial = module.apply_import_pack(new, target, predecessor_pack=old, resolutions=resolutions,
                expected_plan_digest=helper.field(preview.stdout, "plan_digest"), fail_after_writes=1)
            save(out / (label + "-interrupted.json"), partial)
            assert partial["status"] == "INTERRUPTED" and partial["recovery"]["classification"] == "partial"
            before = helper.tree_hashes(target)
            refused = update("-ordinary-resume-refusal", *extra, exits=(3,))
            assert helper.field(refused.stdout, "status") == "RECOVERY_REQUIRED"
            refused = update("-wrong-plan-refusal", *extra, "--recover-partial", "--expect-plan", "0" * 64, exits=(3,))
            assert helper.field(refused.stdout, "status") == "RECOVERY_REQUIRED"
            assert helper.tree_hashes(target) == before
            if resolutions:
                selected.write_bytes(new_bytes + local_note + b"# Changed after interruption.\n")
                refused = update("-changed-resolution-refusal", *extra, "--recover-partial", "--expect-plan", partial["plan_digest"], exits=(3,))
                assert helper.field(refused.stdout, "status") == "RECOVERY_REQUIRED"
                assert helper.tree_hashes(target) == before
                selected.write_bytes(new_bytes + local_note)
            recovered = update("-exact-recovery", *extra, "--recover-partial", "--expect-plan", partial["plan_digest"])
            assert helper.field(recovered.stdout, "status") == "RECOVERED"
            assert not (target / module.PORTABLE_IMPORT_INTENT_PATH).exists()
            receipt = module.load_portable_import_receipt(target)
            assert receipt["pack"] == module.import_pack_identity(new)
            assert (target / changed).read_bytes() == (new_bytes + local_note if resolutions else new_bytes)
            row["checks"].append("exact_interrupted_upgrade_recovery")
            if resolutions:
                assert receipt["disabled_features"] == ["local_state_examples"]
                assert optional not in receipt["managed"]
                assert receipt["managed"][changed]["local_overlay"]
                before = helper.tree_hashes(target)
                plan = helper.plan_removal(rec, label + "-overlay-removal-preview", target)
                operation = next(item for item in plan["operations"] if item["target"] == changed)
                assert operation["action"] == "preserve_project_overlay" and not operation["removal_candidate"]
                assert helper.tree_hashes(target) == before
                row["checks"].append("customization_disabled_examples_and_overlay_remain_project_owned")
            else:
                repair_rel = ".aide/prompts/compact-task.md"
                expected = (target / repair_rel).read_bytes()
                (target / repair_rel).unlink()  # controlled missing owned-file fixture
                preview = module.apply_portable_owned_repair(new, target, repair_rel, dry_run=True)
                interrupted = module.apply_portable_owned_repair(new, target, repair_rel,
                    expected_plan_digest=preview["plan_digest"], fail_after_write=True)
                save(out / (label + "-repair-interrupted.json"), interrupted)
                assert interrupted["status"] == "INTERRUPTED"
                result = rec.installed(label + "-repair-recovery", target, "repair-owned-file", "--pack", str(new),
                    "--target", str(target), "--path", repair_rel, "--expect-plan", preview["plan_digest"])
                assert helper.field(result.stdout, "status") == "RECOVERED"
                assert (target / repair_rel).read_bytes() == expected
                assert not (target / module.PORTABLE_REPAIR_INTENT_PATH).exists()
                row["checks"].append("installed_owned_repair_interruption_and_recovery")
                # New payload paths cannot be silently erased by an old receipt.
                before = helper.tree_hashes(target)
                result = rec.installed(label + "-rollback-path-refusal", target, "rollback-pack", "--current-pack", str(new),
                    "--previous-pack", str(old), "--target", str(target), "--dry-run", "--json", exits=(1,))
                assert "rollback payload paths differ" in result.stderr
                assert helper.tree_hashes(target) == before
                row["checks"].append("cross_version_path_change_rollback_refuses_without_writes")
                agents = (target / "AGENTS.md").read_bytes()
                begin = agents.index(b"<!-- AIDE-PORTABLE:BEGIN section=aide-lite-pack-v0")
                marker = b"<!-- AIDE-PORTABLE:END section=aide-lite-pack-v0 -->"
                end = agents.index(marker, begin) + len(marker)
                outside = agents[:begin] + agents[end:]
                plan = helper.plan_removal(rec, label + "-detach-preview", target)
                result = rec.installed(label + "-detach", target, "apply-removal", "--target", str(target),
                    "--expect-plan", plan["plan_digest"], "--json")
                assert json.loads(result.stdout)["status"] == "DETACHED"
                helper.assert_detached(target, set(receipt["managed"]), module,
                    {relative: hashlib.sha256(raw).hexdigest() for relative, raw in project.items()}, authored_agents=outside)
                helper.install(rec, label + "-published-reinstall", old, target)
                assert module.load_portable_import_receipt(target)["pack"] == module.import_pack_identity(old)
                assert (target / changed).read_bytes() == old_bytes
                row["checks"].append("detach_and_published_predecessor_reinstall")
            row["native_acceptance"] = True
        except Exception as error:
            row.update(error_type=type(error).__name__, error=str(error), traceback=traceback.format_exc())
        finally:
            row["preserved"] = all((target / name).is_file() and (target / name).read_bytes() == raw
                                   for name, raw in project.items())
            row["preserved"] &= (target / "AGENTS.md").is_file() and (target / "AGENTS.md").read_bytes().startswith(authored)
            row["native_acceptance"] &= row["preserved"]
            save(out / (label + ".case.json"), row)
            cases.append(row)
    return cases


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scratch-parent", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--emit-log", action="store_true")
    parser.add_argument("--workunit", choices=WORKUNITS, default=WORKUNITS[0])
    parser.add_argument("--input-manifest", type=Path)
    parser.add_argument("--continue-local", action="store_true")
    args = parser.parse_args()
    task = ROOT / ".aide/queue" / args.workunit
    qualify = args.workunit == WORKUNITS[1]
    if args.continue_local and (not qualify or not os.environ.get("AIDE_JOB_TMP") or not os.environ.get("AIDE_JOB_OUTPUT")):
        raise ValueError("continuation requires the exact admitted local qualification mode")
    scratch = args.scratch_parent.resolve(strict=True)
    out = args.output.resolve()
    owned = os.environ.get("AIDE_JOB_TMP") or os.environ.get("RUNNER_TEMP")
    if owned is None or scratch != Path(owned).resolve(strict=True):
        raise ValueError("scratch must equal the managed job or hosted runner temporary parent")
    output_parent = Path(os.environ["AIDE_JOB_OUTPUT"]).resolve(strict=True) if os.environ.get("AIDE_JOB_OUTPUT") else scratch
    input_manifest = task / "evidence/package-inputs.json"
    if args.input_manifest is not None:
        if not os.environ.get("AIDE_JOB_OUTPUT") or args.input_manifest.resolve() != output_parent / "package-inputs.json":
            raise ValueError("alternate input manifest is restricted to the managed job's exact output file")
        input_manifest = args.input_manifest.resolve(strict=True)
    manifest_info = input_manifest.lstat()
    if not stat.S_ISREG(manifest_info.st_mode) or manifest_info.st_nlink != 1 or manifest_info.st_size > 1024 * 1024:
        raise ValueError("input manifest must be an ordinary bounded file")
    if out.exists() or not out.is_relative_to(output_parent) or out == output_parent:
        raise ValueError("output must be a new child of the managed output or hosted temporary parent")
    out.mkdir(parents=True)
    receipt = {"observation_complete": False, "native_lifecycle_pass": False,
               "support_claimed": False, "models_requested": 0, "whole_model_usage": "unknown",
               "host": {"system": platform.system(), "release": platform.release(),
                        "version": platform.version(), "machine": platform.machine(),
                        "python": sys.version, "executable_sha256": sha(Path(sys.executable)),
                        "image_os": os.environ.get("ImageOS"), "image_version": os.environ.get("ImageVersion")},
               "source_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
               "limitations": ["initial characterization, not full Lite 1.2 qualification",
                               "fixture tests do not qualify lifecycle apply or hostile-writer isolation",
                               "no update, conflict, rollback or interruption claim from these cases",
                               "CLI offline declaration is not an OS network isolation measurement"]}
    if qualify:
        receipt["limitations"] = [
            "development export qualification is not a versioned Lite 1.2 release/archive claim",
            "published 1.1 POSIX removal refusals remain historical-profile observations",
            "POSIX mutation ownership is cooperative, without hostile-writer or outer-client containment",
            "a terminated rename gap with outstanding backups requires explicit reconciliation",
            "actual predecessor path-change rollback refuses; same-path rollback is separately tested",
            "CLI offline declaration is not an OS network isolation measurement",
        ]
    try:
        pinned = json.loads(input_manifest.read_bytes())
        actual = {name: sha(ROOT / name) for name in pinned["files"]}
        if actual != pinned["files"]:
            raise ValueError("pinned package/helper/fixture input changed")
        receipt["input_sha256"] = sha(input_manifest)
        receipt["workunit"] = args.workunit
        receipt["inputs"] = actual
        with tempfile.TemporaryDirectory(prefix="aide-modern-", dir=scratch) as directory:
            work = Path(directory)
            # Standard tempfile users, including the unchanged fixture suite, inherit this parent.
            tempfile.tempdir = str(work)
            os.environ.update(TMP=str(work), TEMP=str(work), TMPDIR=str(work))
            def test_ids(node):
                if isinstance(node, unittest.TestSuite):
                    return [name for child in node for name in test_ids(child)]
                return [node.id()]
            if args.continue_local:
                conserved = pinned.get("conserved_evidence")
                if not isinstance(conserved, dict) or not conserved.get("review_required") or conserved.get("source_commit") != "ba5c318e32c1c18e25454986d858822929c03c1c":
                    raise ValueError("exact conserved evidence is missing")
                if not conserved.get("files") or any(sha(ROOT / name) != digest for name, digest in conserved["files"].items()):
                    raise ValueError("conserved observation changed")
                receipt["conserved_evidence"] = conserved
                receipt["fixtures"] = {"tests_run": 0, "passed": True, "executed": False,
                    "reuse": "126 original fixture tests: 117 passes, 9 skips; unchanged fixture/core inputs", "source_commit": conserved["source_commit"]}
            else:
                tests_module = load("aide_modern_original_fixtures", FIXTURES)
                tests = unittest.defaultTestLoader.loadTestsFromModule(tests_module)
                ids = test_ids(tests)
                if len(ids) != len(set(ids)) or len(ids) != 126:
                    raise AssertionError("original fixture suite must contain exactly 126 unique tests")
                with (out / "fixture-tests.log").open("x", encoding="utf-8", newline="\n") as stream:
                    tests_result = unittest.TextTestRunner(stream=stream, verbosity=2).run(tests)
                receipt["fixtures"] = {"tests_run": tests_result.testsRun, "test_ids": ids,
                                       "failures": [(t.id(), detail) for t, detail in tests_result.failures],
                                       "errors": [(t.id(), detail) for t, detail in tests_result.errors],
                                       "skips": [(t.id(), why) for t, why in tests_result.skipped],
                                       "passed": tests_result.wasSuccessful()}
                save(out / "fixture-result.json", receipt["fixtures"])
            additional_passed = True
            if qualify:
                additional = {}
                modules = ("test_posix_lifecycle",) if args.continue_local else ("test_posix_filesystem", "test_posix_lifecycle")
                for name in modules:
                    loaded = load("aide_binding_" + name, ROOT / ".aide/scripts/tests" / (name + ".py"))
                    if name == "test_posix_lifecycle":
                        lifecycle_oracles = loaded.original
                    if args.continue_local:
                        affected = ("test_removal_detaches_brownfield_agents_section_preserving_authored_bytes",
                            "test_removal_interruption_keeps_intent_and_reconciles_exact_bytes",
                            "test_removal_recovers_after_receipt_retirement_before_intent_cleanup",
                            "test_source_checkout_lifecycle_fixture_is_not_exported")
                        suite = unittest.TestSuite(loaded.PortableLifecycleBindingTests(method) for method in affected)
                    else:
                        suite = unittest.defaultTestLoader.loadTestsFromModule(loaded)
                    ids = test_ids(suite)
                    if not ids or len(ids) != len(set(ids)):
                        raise AssertionError("binding regressions require unique test identities")
                    with (out / (name + ".log")).open("x", encoding="utf-8", newline="\n") as stream:
                        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
                    additional[name] = {"tests_run": result.testsRun, "test_ids": ids,
                        "failures": [(t.id(), detail) for t, detail in result.failures],
                        "errors": [(t.id(), detail) for t, detail in result.errors],
                        "skips": [(t.id(), why) for t, why in result.skipped], "passed": result.wasSuccessful()}
                    save(out / (name + ".result.json"), additional[name])
                    additional_passed &= result.wasSuccessful()
                receipt["binding_regressions"] = additional
                if os.name == "nt":
                    # Retain the original adversarial Windows tests unchanged.
                    names = (
                        "test_partial_recovery_blocks_controls_change_during_publication_and_retirement",
                        "test_disabled_controls_swap_at_receipt_effect_keeps_intent_for_reconciliation",
                        "test_removal_rename_gap_legacy_intent_without_file_identity_refuses",
                        "test_removal_leaf_change_before_handle_open_is_preserved",
                        "test_removal_rejects_parent_junction_swapped_at_handle_open",
                        "test_removal_handle_refuses_a_competing_writer_or_hard_link",
                        "test_owned_repair_stage_denies_second_process_writer",
                        "test_owned_repair_stage_setup_failure_cleans_owned_link",
                        "test_owned_repair_prepublication_failure_retries_from_missing",
                        "test_owned_repair_blocks_parent_substitution_at_publish",
                        "test_owned_repair_cleanup_rejects_junction_swap_on_success_and_recovery",
                        "test_fresh_import_serializes_second_import_and_repair_without_lock_file",
                    )
                    if args.continue_local:
                        names = ("test_removal_leaf_change_before_handle_open_is_preserved",)
                    suite = unittest.TestSuite(lifecycle_oracles.ExportImportTests(name) for name in names)
                    ids = test_ids(suite)
                    with (out / "windows-native-regressions.log").open("x", encoding="utf-8", newline="\n") as stream:
                        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
                    receipt["windows_regressions"] = {"tests_run": result.testsRun, "test_ids": ids,
                        "failures": [(t.id(), detail) for t, detail in result.failures],
                        "errors": [(t.id(), detail) for t, detail in result.errors],
                        "skips": [(t.id(), why) for t, why in result.skipped], "passed": result.wasSuccessful()}
                    save(out / "windows-regressions.result.json", receipt["windows_regressions"])
                    additional_passed &= result.wasSuccessful()
            cases, commands, members = characterize(work, out, pinned, qualify=qualify, continue_local=args.continue_local)
            accepted_cases = [c for c in cases if c["subject"] == "development-export"] if qualify else cases
            receipt.update(cases=cases, commands=commands, published_members=members,
                           observation_complete=True,
                            native_lifecycle_pass=receipt["fixtures"]["passed"] and additional_passed and all(c["native_acceptance"] for c in accepted_cases))
    except Exception as error:
        receipt.update(error_type=type(error).__name__, error=str(error), traceback=traceback.format_exc())
    finally:
        save(out / "result.json", receipt)
        save(out / "receipt-index.json", {p.name: {"bytes": p.stat().st_size, "sha256": sha(p)}
                                          for p in sorted(out.iterdir()) if p.is_file()})
        if args.emit_log:
            emit_receipts(out)
    print(json.dumps({k: receipt[k] for k in ("observation_complete", "native_lifecycle_pass", "support_claimed")}))
    return 0 if receipt["observation_complete"] else 1


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
