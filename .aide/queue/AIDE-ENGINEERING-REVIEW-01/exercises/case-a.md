# Review packet A

Fictional repository snapshot for an answer-only review exercise. The code and
recorded validation below are supplied scenario facts, not claims of tests run in
the AIDE repository. Review this candidate using the supplied AIDE review prompt.
No code execution, edits, external calls or additional delegation are requested.

## Task and scope

Rename internal Task identifiers to WorkUnit identifiers in the Python serializer.
Keep the public version1 JSON interface compatible with the currently supported
offline viewer. Allowed changes: serializer.py and tests/test_serializer.py.
No wire-version upgrade, consumer migration or release is part of this task.

## Source before: serializer.py

```python
def encode(task_id, title):
    return {"version": 1, "task_id": task_id, "title": title}
```

## Candidate: serializer.py

```python
def encode(work_id, title):
    return {"version": 1, "work_id": work_id, "title": title}
```

## Candidate: tests/test_serializer.py

```python
def test_encode():
    assert encode("w1", "Repair") == {
        "version": 1, "work_id": "w1", "title": "Repair"}
```

## Unchanged viewer contract and source: viewer.py

The shipped viewer accepts version1 and reads title and task_id. Existing persisted
files use that schema. Version1 support remains part of the project's acceptance.

```python
def label(record):
    if record["version"] != 1:
        raise ValueError("unsupported version")
    return record["task_id"] + ": " + record["title"]
```

## Recorded validation and evidence

Scenario record: `python -m unittest tests.test_serializer` PASS1, no skips.
No viewer compatibility check was recorded for this candidate. Changed files are
exactly the two allowed paths. No other effects or configuration changes occurred.
Controller/review usage is unavailable. The author requests acceptance for the
internal rename; later consumer migration is outside this task.
