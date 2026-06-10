# Protected Path Checks

## Result

`PASS`

Reviewed uninstall plans include protected roots:

- `.git`
- `.github`
- `.aide.local`
- `.env`
- `.env.*`
- `secrets`
- `credentials`

Target, release, provider, Gateway, and target-repo surfaces remain blocked or out of scope.
