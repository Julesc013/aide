"""Exact reviewed archive checkpoint, then eight serial original consumers."""
from pathlib import Path
import hashlib
import importlib.util
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from core.apply.managed_commit import create_commit
from core.execution import managed_workspace as workspace

TASK = Path(__file__).parent
EVIDENCE = TASK / "evidence"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, timeout=30).strip()


def main():
    source = EVIDENCE / "consumer-source.json"
    effect = EVIDENCE / "consumer-effect.json"
    assert len(sys.argv) == 3 and [sha(source), sha(effect)] == sys.argv[1:]
    mapped = json.loads(source.read_bytes())
    plan = json.loads(effect.read_bytes())
    assert mapped["effect_sha256"] == sha(effect)
    verdict = json.loads((EVIDENCE / "consumer-review.json").read_bytes())
    assert verdict["decision"] == "ACCEPT" and not verdict["required_fixes"]
    assert verdict["reviewer"] == "/root/review_disked_continuation"
    assert verdict["source_sha256"] == sha(source) and verdict["effect_sha256"] == sha(effect)
    assert verdict["controller_sha256"] == sha(Path(__file__))
    allowed = set(mapped["files"]) | {source.relative_to(ROOT).as_posix(),
                                     (EVIDENCE / "consumer-review.json").relative_to(ROOT).as_posix()}
    outcome_path = EVIDENCE / "consumer-execution.log"
    with outcome_path.open("x", encoding="utf-8") as stream:
        stream.write("{}\n")
    outcome = {"state": "started"}

    def save():
        outcome_path.write_bytes((json.dumps(outcome, indent=2) + "\n").encode())

    config, roots, _ = workspace.load_config(ROOT / ".aide.local/execution.json")
    assert workspace.digest(config) == plan["control_config_digest"]
    spec = importlib.util.spec_from_file_location("archive_build_commit_check", ROOT / ".aide/scripts/aide_lite.py")
    lite = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = lite
    spec.loader.exec_module(lite)
    try:
        with workspace.estate_lock(roots["control"]), workspace.estate_lock(roots["control"], "dispatch.lock"):
            assert workspace.dispatch_state(roots["control"])["mode"] == "running"
            assert not (roots["control"] / "active.json").exists()
            assert git("branch", "--show-current") == plan["task_branch"]
            assert git("rev-parse", "HEAD") == plan["base"]
            for ref in ("main", "dev", "origin/main", "origin/dev"):
                assert git("rev-parse", ref) == plan["integration_base"]
            assert not git("diff", "--cached", "--name-only")
            changed = set(git("diff", "--name-only").splitlines())
            changed |= set(git("ls-files", "--others", "--exclude-standard").splitlines())
            assert changed == allowed, sorted(changed ^ allowed)
            assert all(sha(ROOT / name) == value for name, value in mapped["files"].items())
            for flags in (("--all",), ("--push", "--all")):
                assert git("remote", "get-url", *flags, "origin") == plan["origin_url"]
            remote = dict(line.split()[::-1] for line in git("ls-remote", "--heads", "origin", "dev", "main").splitlines())
            assert remote == {"refs/heads/dev": plan["integration_base"], "refs/heads/main": plan["integration_base"]}
            helper_plan = lite.make_git_helper_plan(ROOT, "plan", dry_run=True)
            outcome["helper_plan"] = helper_plan
            save()
            assert helper_plan["status"] == "blocked"
            assert helper_plan["blockers"] == ["dirty_tree_requires_classification"], helper_plan["blockers"]
            git("diff", "--check")
            git("add", "--", *sorted(allowed))
            assert set(git("diff", "--cached", "--name-only").splitlines()) == allowed
            for name in allowed:
                assert git("hash-object", "--no-filters", "--", name) == git("rev-parse", ":" + name), name
            tree = git("write-tree")
            message = (EVIDENCE / "consumer-message.txt").read_bytes()
            commit = create_commit(ROOT, message=message, expected_message_sha256=sha(EVIDENCE / "consumer-message.txt"),
                                   expected_ref="refs/heads/" + plan["task_branch"], expected_head=plan["base"],
                                   expected_tree=tree, allowed_paths=sorted(allowed), apply=True,
                                   validator=lambda text: [c.message for c in lite.validate_commit_message_text(text) if c.severity == "FAIL"])
            outcome["commit"] = commit
            save()
            assert commit["status"] == "COMMITTED"
            assert not git("status", "--porcelain")
            subprocess.run(["py", "-3", "-B", ".aide/scripts/aide_lite.py", "commit", "check", "--latest"],
                           cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        subject_commit, subject_tree = commit['candidate_commit'], commit['expected_tree']
        assert plan['cases'] == list(range(8))
        outcome['consumer_subject'] = {'commit': subject_commit, 'tree': subject_tree,
                                       'branch': plan['task_branch']}
        outcome['consumer_results'] = []
        for index in plan['cases']:
            assert git('branch', '--show-current') == plan['task_branch']
            assert git('rev-parse', 'HEAD') == subject_commit
            assert git('rev-parse', 'HEAD^{tree}') == subject_tree
            qualification, _, _ = workspace.load_config(ROOT / plan['qualification_config'])
            assert workspace.digest(qualification) == plan['qualification_config_digest']
            job = json.loads((EVIDENCE / 'consumer-job-template.json').read_bytes())
            job.update(source_commit=subject_commit, source_tree=subject_tree)
            job['argv'].append(str(index))
            assert not git('status', '--porcelain')
            outcome.update(state='consumer_admission', current_case=index, current_job=job)
            save()
            result = workspace.run(ROOT / plan['qualification_config'], job)
            outcome['consumer_results'].append({'case': index, 'receipt': result})
            outcome.update(state='consumer_terminal')
            save()
            print(json.dumps({'case': index, 'job_id': result.get('job_id'),
                              'phase': result.get('phase'), 'result': result.get('result')}), flush=True)
            assert result.get('config_digest') == plan['qualification_config_digest']
            assert result.get('job') == job and result.get('manifest_digest') == workspace.digest(job)
            assert result['job']['source_commit'] == subject_commit and result['job']['source_tree'] == subject_tree
            assert result.get('phase') == 'retired' and result.get('scratch_absent') and result.get('reservation_released')
            assert result.get('result', {}).get('exit_code') == 0 and result['result'].get('quiescent')
            assert git('branch', '--show-current') == plan['task_branch']
            assert git('rev-parse', 'HEAD') == subject_commit and git('rev-parse', 'HEAD^{tree}') == subject_tree
            assert not git('status', '--porcelain')
        outcome.update(state='all_eight_consumers_terminal_pass')
        save()
    except BaseException as error:
        outcome.update(state="stopped", error_type=type(error).__name__, error=str(error))
        save()
        raise


if __name__ == "__main__":
    main()
