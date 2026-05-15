# Secret and Local-State Scan

## Command

Pattern:

`sk-[A-Za-z0-9]|sk-ant|api[_-]?key|SECRET|TOKEN|PASSWORD|BEGIN PRIVATE KEY|OPENAI_API_KEY|ANTHROPIC_API_KEY|DEEPSEEK_API_KEY`

Scopes:

`.aide .aide.local.example AGENTS.md README.md ROADMAP.md PLANS.md IMPLEMENT.md DOCUMENTATION.md docs core shared scripts tools .gitignore`

## Result

PASS_AFTER_INSPECTION.

Matches were policy, documentation, regex, example, fixture, or test references. No actual provider credential, local secret file, raw prompt body, raw response body, or `.aide.local/**` payload was found in the committed/source audit scope.

## Allowed Match Classes

- `.aide.local.example`
- policy text explaining forbidden secrets
- test fixtures containing fake/example key names
- regex patterns in provider tests or scans
- documentation references to secret handling

## Release Archive Scan

Zip and tarball scans found no forbidden paths:

- `.git/`
- `.aide.local/`
- `.env`
- `secrets/`
- raw prompt/response logs
- provider keys
