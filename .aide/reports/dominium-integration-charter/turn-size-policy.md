# Task Turn Policy

```text
one authoritative queue task per normal turn

BUILD:
  implementation and local tests
  no independent check

CHECK:
  independent review
  no production repair

ACCEPT:
  acceptance only
  may recommend next build

REPAIR:
  bounded repair only

MEGA TURN:
  one accepted gate
  plus one directly dependent planning-only task
  maximum two commits
```

Future prompts must not soft-execute blocked downstream tasks merely to record that they are blocked. The scheduler should check dependencies before dispatch.
