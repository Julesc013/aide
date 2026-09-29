# Current Lite pre-unlink removal recovery

- Harness source: `202fa0a880209899c76c72cf5d363ca513d2c891`, tree
  `c7dc7f6ec84566bb4fc29526a1fd795aea0b0382`.
- Delivered local ZIP SHA-256:
  `95ecee6c422f07005bf25175aae347b500f2f6343d58c702856a6e977126902f`.
- Environment: Windows 10 build 19045, Python 3.14.7, AIDE-managed D job,
  disposable brownfield consumer. No model or network effect was invoked.

| Boundary | Managed job | Receipt SHA-256 | Summary SHA-256 | Result |
| --- | --- | --- | --- | --- |
| Before first receipt-owned unlink | `1f6319a90deb47c0b43058a9f4e9d775` | `e46c47c29db2741c15697c620bab65d15fda65d2277fd587220994970ef1ab9e` | `bb613180cd288918ff3b117a5abe1894adbc585b0418671c54a41d40246c63d9` | PASS: child exit 77; zero owned unlinks; all 813 managed file hashes unchanged; intent and receipt retained; fresh delivered CLI `DETACHED`; authored and project-owned bytes preserved. |
| After first receipt-owned unlink, prior-mode regression | `51fe41e182794930951a0139ba199f39` | `db9f5ec7cd6bb3517f8f87025ff1903a9d9df45d91cf5c32c39058f8c5efcdca` | `e95291a2d73eb7cbe1f688f3df7507e4a713c0f65ac99007425f663f0cdbd7b0` | PASS: child exit 77; one owned unlink; intent and receipt retained; fresh delivered CLI `DETACHED`; authored and project-owned bytes preserved. |

Both exact receipts record exit zero, scratch absent, reservation released and
source/asset input hashes. Retained outputs are under the approved shared D
execution root, keyed by the job IDs above. The pre-unlink job peaked at
246,505,472 memory bytes and 8,673,307 scratch bytes; the regression job
peaked at 246,571,008 and 8,246,816 respectively. The bounded observer
started zero model requests; it cannot account for unrelated host requests.

Independent `/root/stable_effect_review` returned **ACCEPT** for this exact
harness source and these two local recovery observations after checking the
control flow, both receipts and summary digests, unchanged archive extraction
checks, prior mode and cleanup. This is supplemental local Windows recovery
evidence. It does not prove hostile-writer safety, downloaded-byte behavior,
whole-release acceptance, main promotion or publication. The ten historical
owner decisions remain required for the release path.
