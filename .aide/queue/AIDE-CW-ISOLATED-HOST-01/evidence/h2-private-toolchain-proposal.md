# Next source slice: private tool image and held worker roots

Build a reusable bounded private-image preparer and prove a minimal pinned
Python image first. The current native PASS does not qualify Python, Git or
Codex. This is a source/test proposal, with a later exact effect manifest before
any additional profile use, grants or isolated runtime launch. It creates no
new profile and changes no shared installation or parent ACL.

## Concrete inputs and limits

The read-only h2-local-tool-input-inventory.json binds installed inputs. Python
python.exe is 106,208 bytes, python314.dll 6,785,760, and Lib excluding site-packages
and bytecode totals 15,298,202 bytes (721 Python sources). Git's mingw64/bin/git.exe
is 4,344,208 bytes. The actual Codex executable is 359,245,096 bytes, so the H1
16MiB one-write native fixture API cannot silently become its image loader.
Dependency closure and actual execution remain unproved; no binary was copied.

First implement source-only ImageSpec/prepare_image validation in a focused
core/runtime/continuous_worker/windows_image.py and direct
.aide/scripts/tests/test_continuous_worker_windows_image.py. Extend only the
owned-object helper with an explicitly separate admitted streaming-copy method;
keep existing write(bytes) 16MiB semantics unchanged. A finite ImageSpec binds
relative paths, bytes/SHA256, total/entry/per-file/chunk/time budgets, executable
and DLL dependency declarations, package/user SIDs and protected input root
identities. Default absent specification refuses. A candidate future full-image
ceiling is 512MiB per file/768MiB total, at most 2048 materialized entries and 64KiB
chunks; these explicit H2 image limits require review and do not relax any worker
candidate, output or H1 budget. The first Python effect can choose much less.

## Image preparation and launch contract

- Reserve one generation intent durably before any output object. Hold trusted
  source objects without write/delete sharing, reject reparse/case aliases/ADS,
  and verify exact bytes while copying to exclusively created private handles.
- A single-use streaming writer consumes admission before the first write,
  bounds every chunk and cumulative bytes/time, flushes, and verifies declared
  length/digest before publishing a complete file observation. Short write,
  excess/early EOF, source identity drift or failed flush retains incomplete
  objects and durable recovery evidence; no replay, grant or cleanup follows.
- Build a deterministic Python standard-library ZIP from explicitly admitted
  sources, not arbitrary site-packages. Record ZIP member digests and policy;
  never execute source import hooks, filters or package managers while building.
  Bind python314._pth to the private ZIP/private DLL root, omit import site, and
  run with isolated/no-site/no-bytecode flags. Resolve exact PE dependency closure
  against pinned private inputs plus the explicit Windows system-DLL contract;
  reject unexpected DLL/search paths, symlinks and ambient environment injection.
- Seal all image objects and verify complete image identity/content before exact
  package read/execute grants. Worker scratch/clone/output are separate low-label
  owned modify roots; controller/broker/evidence and synthetic credential canary
  remain outside. No inherited broad package grant or real credential path.
- Hold the prepared image/root observations through SecurityLaunch and expose
  an internal trusted-controller factory, never worker-selectable authority.
  Separate immediate effect-boundary checks from bounded periodic observations;
  the native probe's 252/256 lookup count is not a scalable host polling policy.

## Meaningful source and ordinary disposable tests

Use synthetic binary fixtures spanning multiple chunks, with mutation after
admission, partial/extra reads, wrong digests, failed flush and crash after intent.
Refuse stale/source-object substitution, junctions, case/ADS paths, moved protected
root, incomplete generation, wrong package grants, unlisted DLLs, escaping._pth,
site/user-path injection and oversized manifests before effects. Reopen retained
failed state and show no second writer/no uncertain-object deletion. Verify the
exact streaming bound without allocating the whole 359MB Codex executable.

After source review, propose one exact Python-only real AppContainer effect:
import standard library from the private image, read its own code, write only its
owned scratch and refuse protected synthetic canaries, DACL mutation and controller
access. Test a worker-created junction reaching a protected canary and record the
actual denial; no real secret read. Bind all image/object/token/Job/stdout facts.
AppContainer descendants/supervisor-death checks remain separate admitted cells.
No further effect is authorized by this document alone.

## Subsequent required work

Git private dependency closure and local-only clone/patch fixtures follow the
Python seam; then actual Codex image and offline CLI execution. No Git helper may
consult global credentials/config or fetch. H4 controlled model transport remains
required: zero-capability Codex cannot simply receive general internet capability
or controller tokens. A separately reviewed narrow transport/host must mediate
model requests and enforce credentials/egress, then actual broker/target contracts
and a live pilot can qualify. This proposal does not claim that closure complete.
