# Bounded WorkUnit: installed Lite repair health

Implement a side-effect-free `repair-health` CLI/API for a delivered Lite pack
and installed target. Observe exact receipt ownership, pack, managed bytes and
pending lifecycle intents. Classify missing owned files as candidates for the
existing exact-plan `repair-owned-file` path; preserve changed, unknown,
invalid, disabled and overlaid state. Prove the behavior from extracted pack
bytes in disposable fresh and authored targets. Keep repair apply and release
claims behind their separate gates.
