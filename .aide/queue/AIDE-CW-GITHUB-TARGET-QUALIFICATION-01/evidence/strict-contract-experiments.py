"""Real Git graph experiments for a conditional server contract, not GitHub tests."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

GIT = shutil.which("git")
assert GIT, "local Git required"


def run(root, *args, data=None, accepted=(0,)):
    env = {k: v for k, v in os.environ.items() if k.upper() in
           {"SYSTEMROOT", "WINDIR", "PATH", "TEMP", "TMP", "USERPROFILE"}}
    env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
               GIT_TERMINAL_PROMPT="0", GIT_AUTHOR_DATE="2000-01-01T00:00:00Z",
               GIT_COMMITTER_DATE="2000-01-01T00:00:00Z")
    command = [GIT, "--no-replace-objects", "-c", "core.hooksPath=" + os.devnull,
               "-c", "core.autocrlf=false", "-c", "commit.gpgsign=false",
               "-c", "user.name=Local contract fixture", "-c", "user.email=fixture@aide.invalid",
               "-c", "protocol.allow=never", "-C", str(root), *args]
    result = subprocess.run(command, input=data, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, env=env, timeout=10)
    assert result.returncode in accepted, (args, result.stderr.decode(errors="replace"))
    return result


def fixture(root):
    run(root, "init", "--quiet")
    def commit(label, files, parents):
        entries = []
        for name, content in sorted(files.items()):
            blob = run(root, "hash-object", "-w", "--stdin", data=content).stdout.decode().strip()
            entries.append("100644 blob " + blob + "\t" + name + "\n")
        tree = run(root, "mktree", data="".join(entries).encode()).stdout.decode().strip()
        args = ["commit-tree", tree]
        for parent in parents:
            args += ["-p", parent]
        return run(root, *args, data=(label + "\n").encode()).stdout.decode().strip()
    base_files = {"base.txt": b"admitted base\n"}
    candidate_files = dict(base_files, **{"change.bin": b"\x00candidate\xff"})
    a = commit("A", {}, [])
    b = commit("B", base_files, [a])
    c = commit("C", candidate_files, [b])
    d = commit("D", dict(base_files, **{"other.txt": b"other actor\n"}), [b])
    same_tree = commit("metadata advance", base_files, [b])
    descendant = commit("E", dict(candidate_files, **{"other.txt": b"later\n"}), [c])
    changed_head = commit("C2", dict(candidate_files, **{"extra.txt": b"unreviewed\n"}), [c])
    multi = commit("multi", dict(candidate_files, **{"other.txt": b"other actor\n"}), [c, d])
    return {"a": a, "b": b, "c": c, "d": d, "same_tree": same_tree,
            "descendant": descendant, "changed_head": changed_head, "multi": multi}


def experiment(name, *, target="b", head="c", strict=True, bypass=False,
               expected_head=True, ref="dev", deny_non_dev=True, candidate="c"):
    with tempfile.TemporaryDirectory(prefix="aide-strict-contract-") as temporary:
        root = Path(temporary)
        graph = fixture(root)
        base, admitted = graph["b"], graph[candidate]
        run(root, "update-ref", "refs/heads/dev", base)
        run(root, "update-ref", "refs/heads/main", base)
        observed = {"target_ref": "dev", "target": base, "head": admitted}
        # Deterministic adversarial barrier: change server state only after the
        # client's final observation, before the modeled server predicates.
        actual_target = graph[target]
        actual_head = graph[head] if candidate == "c" else admitted
        run(root, "update-ref", "refs/heads/" + ref, actual_target)
        run(root, "symbolic-ref", "HEAD", "refs/heads/" + ref)
        run(root, "read-tree", "--reset", "-u", actual_target)
        reason = None
        if deny_non_dev and ref != "dev":
            reason = "non_dev_update_denied"
        elif expected_head and actual_head != admitted:
            reason = "expected_head_mismatch"
        elif strict and not bypass and run(root, "merge-base", "--is-ancestor",
                                           actual_target, actual_head, accepted=(0, 1)).returncode:
            reason = "strict_base_not_up_to_date"
        if reason is None:
            run(root, "merge", "--no-ff", "--no-edit", actual_head)
        after = run(root, "rev-parse", "HEAD").stdout.decode().strip()
        parents = run(root, "show", "-s", "--format=%P", after).stdout.decode().split()
        tree = run(root, "show", "-s", "--format=%T", after).stdout.decode().strip()
        candidate_tree = run(root, "show", "-s", "--format=%T", admitted).stdout.decode().strip()
        changed = after != actual_target
        admitted_effect = changed and ref == "dev" and parents == [base, admitted] and tree == candidate_tree
        return {"name": name, "observed": observed, "graph": graph,
                "dispatch_ref": ref, "dispatch_base": actual_target, "dispatch_head": actual_head,
                "strict": strict, "bypass": bypass, "expected_head": expected_head,
                "deny_non_dev": deny_non_dev, "refusal": reason, "result_commit": after,
                "result_parents": parents, "result_tree": tree, "ref_changed": changed,
                "admitted_effect": admitted_effect}


CASES = [
    ("unchanged_base", {}, "admitted"),
    ("competing_base_after_read", {"target": "d"}, "refused"),
    ("same_tree_base_advance", {"target": "same_tree"}, "refused"),
    ("loose_policy_counterexample", {"target": "d", "strict": False}, "unadmitted"),
    ("bypass_counterexample", {"target": "d", "bypass": True}, "unadmitted"),
    ("rollback_counterexample", {"target": "a"}, "unadmitted"),
    ("head_changed_after_read", {"head": "changed_head"}, "refused"),
    ("missing_expected_head_counterexample", {"head": "changed_head", "expected_head": False}, "unadmitted"),
    ("same_oid_retarget_counterexample", {"ref": "main", "deny_non_dev": False}, "unadmitted"),
    ("same_oid_retarget_denied", {"ref": "main"}, "refused"),
    ("already_exact_candidate", {"target": "c"}, "unchanged"),
    ("candidate_already_in_target", {"target": "descendant"}, "refused"),
    ("multiple_parent_counterexample", {"target": "d", "candidate": "multi"}, "unadmitted"),
]


def main():
    records = []
    for name, args, expected in CASES:
        result = experiment(name, **args)
        if expected == "admitted":
            assert result["admitted_effect"], result
        elif expected == "unadmitted":
            assert result["ref_changed"] and not result["admitted_effect"], result
        elif expected == "refused":
            assert result["refusal"] and not result["ref_changed"], result
        else:
            assert not result["refusal"] and not result["ref_changed"], result
        result["expected"] = expected
        records.append(result)
        print("PASS", name, expected, flush=True)
    source = Path(__file__)
    record = {"schema": "aide.local.conditional-contract-experiments.v1",
              "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
              "git_executable_sha256": hashlib.sha256(Path(GIT).read_bytes()).hexdigest(),
              "experiments": records, "count": len(records), "result": "PASS",
              "hosted_github_qualification": False,
              "scope": "Real local Git objects and deterministic modeled server predicates; no provider calls."}
    source.with_suffix(".json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
