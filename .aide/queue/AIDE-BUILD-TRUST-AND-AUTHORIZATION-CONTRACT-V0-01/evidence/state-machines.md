# State Machines

Principal states:

```text
candidate -> active -> suspended|revoked|expired
```

Admission states:

```text
candidate -> admitted|admitted_with_constraints|rejected
admitted -> suspended|revoked|expired
```

Grant states:

```text
proposed -> active -> consumed|suspended|revoked|expired
```

Evaluation results:

```text
allowed
denied
approval_required
quarantined
```

The state machines are contract/projection data only in this build.
