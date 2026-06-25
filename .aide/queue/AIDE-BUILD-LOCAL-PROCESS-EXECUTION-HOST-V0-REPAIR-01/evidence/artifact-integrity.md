# Artifact Integrity

Worker artifacts are accepted only when declared by the event stream and verified against the disposable workspace.

Validation requires:

- contained relative path;
- regular file;
- no symlink or reparse component;
- declared byte count matches actual byte count;
- declared SHA-256 matches actual file digest;
- file size is within fixture limits;
- no unexpected extra worker files appear.

The live run persisted one content-addressed worker artifact:

`.aide/reports/local-process-execution-host/artifacts/sha256/1aa1e0a91a6ec1a45852e213d2cbcda372996806728daa320123a17d6fcaac05.json`
