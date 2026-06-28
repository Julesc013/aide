# Safety Scans

Safety posture:

- Refused context-binding scenarios do not emit successful UpdateReceipt fixture outputs.
- Refused context-binding scenarios do not execute operations.
- Canonical fixture preservation remains true.
- Real target repository mutation remains false.
- Source repo apply remains false.
- External repo touch remains false.
- Release publication remains false.
- Network/provider/model call remains false.

Path, credential-pattern, source-output misuse, diff, and commit-policy checks are included in final validation.
