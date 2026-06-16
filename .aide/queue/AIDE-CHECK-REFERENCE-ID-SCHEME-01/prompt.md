# Prompt: AIDE-CHECK-REFERENCE-ID-SCHEME-01

Create and process a bounded, check-only queue WorkUnit that independently reviews `AIDE-BUILD-REFERENCE-ID-SCHEME-01`.

This is not an implementation task. Verify the minimal stable AIDE Reference ID Scheme, then stop at `needs_review` with evidence.

Expected result if live evidence matches the build report:

```text
PASS_WITH_WARNINGS
```

Recommended next task if the check passes or passes with warnings:

```text
AIDE-ACCEPT-REFERENCE-ID-SCHEME-01
```

Do not recommend EventRecord directly from this check. EventRecord can only follow ReferenceID acceptance.
