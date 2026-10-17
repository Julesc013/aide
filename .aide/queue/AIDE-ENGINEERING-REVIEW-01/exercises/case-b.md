# Review packet B

Fictional repository snapshot for an answer-only review exercise. The code and
recorded validation below are supplied scenario facts, not claims of tests run in
the AIDE repository. Review this candidate using the supplied AIDE review prompt.
No code execution, edits, external calls or additional delegation are requested.

## Task and scope

Rename the serializer's internal identifier to WorkUnit terminology. Preserve
version1 JSON and the public encode(task_id=...) keyword for supported callers.
Allowed changes: serializer.py and tests/test_serializer.py. No consumer migration,
wire-version upgrade, repository restructuring or release is part of this task.

## Source before: serializer.py

```python
def encode(task_id, title):
    return {"version": 1, "task_id": task_id, "title": title}
```

## Candidate: serializer.py

```python
def encode(task_id, title):
    # Public keyword and version1 field remain compatible with older callers.
    work_id = task_id
    return {"version": 1, "task_id": work_id, "title": title}
```

## Unchanged viewer.py

```python
def label(record):
    if record["version"] != 1:
        raise ValueError("unsupported version")
    return record["task_id"] + ": " + record["title"]
```

## Candidate: tests/test_serializer.py

```python
def test_encode_positional():
    assert encode("w1", "Repair") == {
        "version": 1, "task_id": "w1", "title": "Repair"}

def test_encode_legacy_keyword():
    assert encode(task_id="w1", title="Repair")["task_id"] == "w1"

def test_viewer_consumes_current_output():
    assert label(encode("w1", "Repair")) == "w1: Repair"
```

## Recorded validation and evidence

Scenario record: all three listed checks PASS, no skips, against this exact
candidate. Existing baseline expectation and unchanged viewer oracle were retained.
Changed files are exactly the two allowed paths. No extra dependencies, storage,
configuration, delegation or execution routes were introduced. Total model usage
is unknown and no savings claim is made. Public signature and version1 field are
intentional compatibility obligations, with no retirement scheduled by this task.
