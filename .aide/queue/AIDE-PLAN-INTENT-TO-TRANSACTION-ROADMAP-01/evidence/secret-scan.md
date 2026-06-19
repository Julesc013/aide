# Secret Scan

Secret-like scan over changed files passed.

Patterns checked:

- AWS access-key shape
- OpenAI-style `sk-` token shape
- GitHub personal-access-token shape
- private-key block headers
- obvious assigned password strings
- obvious assigned API key strings

Result:

```text
secret-like scan: PASS (28 changed files)
```
