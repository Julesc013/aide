# Implementation Evidence

The existing portable `import-pack` owner now provides the first supported
ownership-aware update path for disposable consumers.

Implemented behavior:

- exact target-local receipt for managed files and the portable `AGENTS.md`
  section;
- previous/current/incoming byte comparison before update;
- separately checksummed predecessor-pack proof for installations that predate
  receipts;
- conflict-first refusal before any payload write;
- deterministic plan digest and optional `--expect-plan` binding;
- atomic same-directory file replacement;
- durable intent with exact preimages and postimages;
- completed, no-effect, partial, and unknown recovery classification;
- idempotent no-op rerun;
- symlink/junction and root-overlap target refusal;
- extracted CLI support through `--from-pack` and `--expect-plan`.

The accepted DistributionApplyEngine remains fixture-only. This task does not
change its capability label or claim non-disposable target qualification.
