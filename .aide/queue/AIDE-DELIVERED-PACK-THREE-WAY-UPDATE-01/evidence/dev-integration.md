# Combined update and repair-health dev integration

2026-09-25. The exact scoped `dev` integration effect passed. This is not
main promotion or stable-release acceptance.

- Source merge `99a9e54da887a3a209cfd73df345c55735819368`, tree
  `7a3838f027031522cb3862815bf15072fd8b538c`; converged candidate
  `54b9d45eeaa3f10034acf9603d710a3955efcfed`, tree
  `ffbaeceeea79725108970383ac241a3416d0ebba`. `dev` base was
  `d4b67c96ff81eb10aeecd6763b538331844619c9`; the candidate was a
  12-commit descendant and both worktrees were clean.
- After artifact projection `d137f936` and metadata convergence `54b9d45e`,
  `release bundle`, `release validate`, `release draft` and
  `release draft-validate` each exited 0 and changed zero tracked files.
  The ZIP/tar hashes stayed
  `32c1f0ad5465809eec5d8ed64c801e8d3ca31c0fe5840ca41188a376325711f9`
  and `22101aa98982cf8b88d6a4540d814e9751095207535427a4e5a5fc3f36833044`.
  The earlier full export/changelog replay changed 30 derived records and is
  preserved as failed evidence; it is not claimed as zero-change.
- Final canonical `validate`, `doctor`, `pack-status` and the 12-commit
  `dev..HEAD` message range all passed. Log SHA-256 values:
  `7b326b01165e7743abe7d770bad1646dab78f4a411352dfbd8faae83b383e789`,
  `0c1351ded532d4b7d924d989190cf25fbe57be2ac41c63da5546689087ddacf8`,
  `17eb7a713285498d636c31fd8f0e50e9b1a632f16f230bd1f2db48a19f2bb673`,
  `4eabb7e3ae6dbee3ba492fe87f981847878999d713668c226ea3e5a3c46bef91`.
  Pack provenance was `PASS_SOURCE_ANCESTOR`, zero problems.
- External exact effect manifest
  `D:/Projects/AIDE/_review_scratch/combined-update-health-54b9d45e-dev-effect-manifest.json`
  SHA-256 `f6f90d2a6a3c549090b892ca9f03275a11dc53b8cc85c2e27a15cd54224949a0`
  bound only FF local `dev` then normal push. Independent conditional **GO**
  report
  `D:/Projects/AIDE/_review_scratch/combined-update-health-54b9d45e-dev-effect-review.md`
  SHA-256 `3758f659057a21c15c18307b072c8e3fc5d32b393fc2fc03692a1a5d9c3ca568`
  checked exact source/artifact ancestry, machine gates and preview limits.
- Immediately before the effect, `BLACKGLASS-WIN1\Jules` was authenticated
  as `Julesc013`; local `dev`, `origin/dev`, `git ls-remote` and the GitHub ref
  API all reported `d4b67c96`. One worktree held `dev`; candidate and primary
  worktrees were clean. `git plan` was `ready_dry_run` with log SHA-256
  `a67e2a1c9e5e6cdcd198cdb5e8a124ba63917625b5b6c8390e79bfb4d0a9e66e`;
  its four generated primary reports were restored before the effect.
- `git merge --ff-only 54b9d45e` and normal `git push origin dev` both exited
  0. Effect log
  `D:/Projects/AIDE/_review_scratch/combined-update-health-54b9d45e-dev-effect.log`
  SHA-256 `bc27265eb962ffc8bf11408e2fc374dabe09add2ed69902c741b623acbb1ff4b`.
  After push, local HEAD, `origin/dev`, `git ls-remote` and GitHub ref API all
  reported full `54b9d45eeaa3f10034acf9603d710a3955efcfed`; local tree
  was `ffbaeceeea79725108970383ac241a3416d0ebba` and primary worktree
  was clean. No push retry or force was needed.

The accepted local previews remain no-publish. Synthetic predecessor packs,
OS-level offline trace, full lifecycle/hosted/native profile qualification,
main, tag, publication and downloaded-asset checks remain with the parent
campaign. This task's implemented three-way and disabled-feature behavior is
integrated into `dev` with the exact limitations above.
