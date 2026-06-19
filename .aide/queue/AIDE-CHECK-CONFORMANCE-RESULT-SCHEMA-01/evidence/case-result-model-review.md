# Case Result Model Review

Status:

```text
PASS
```

Reviewed 10 case results against 10 accepted profile cases.

Findings:

- no duplicate case ids;
- no missing case results;
- no unknown case results;
- case refs bind to the expected profile ref;
- requirement-level snapshots match the profile cases;
- evaluator snapshots match the profile cases;
- outcomes are from the allowed outcome vocabulary;
- evidence refs exist;
- assertion results are `PASS`;
- `execution_performed`, `admission_performed`, `subject_admitted`, and
  `trusted` are false for every case result;
- `runner_ref` is null for every case result.
