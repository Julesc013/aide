# AIDE Lite 1.0.0

AIDE Lite is the local Windows companion for adopting AIDE in a new or
existing Git project. Download the ZIP or tar archive, verify it against
`aide-lite-v1.0.0.SHA256SUMS.txt`, extract it outside the development checkout,
and follow `install.md` in the extracted pack. The archive includes the
portable CLI, import policy, checksums and reference documentation.

The supported local flow covers safe install, project-owned customization,
three-way updates and conflict resolution, explicit partial-import recovery,
owned-file repair, rollback and owned-material removal. Preview before an
apply operation and retain the exact plan digest required by the CLI. Direct
project edits and disabled optional content are preserved according to their
recorded ownership and current-byte checks; unknown rationale stays unknown.
Feedback is created only by an explicit dry-run option and is never sent by
the CLI.

The first stable Lite release has no published predecessor. Update tests use
synthetic fixture packs and do not create a compatibility promise for another
published version. The declared support posture is T3 Limited Support on the
qualified Windows 10 19045 / Python 3.14.7 local CLI profile. The CLI can run
locally after archive acquisition; the release does not claim OS-level network
isolation. Native isolated-host automation, hosted GitHub effects, model-enabled
autonomous operation and non-Windows lifecycle apply are outside this profile.

Fresh-fixture `validate` can report two warnings before optional task and
managed adapter content is generated. Context `verify` can report classified
WARN results for optional reports, cache and fixture diff scope; inspect its
output before using it as evidence. See the included reference documentation
for customization, update, repair, rollback, removal and recovery details.
