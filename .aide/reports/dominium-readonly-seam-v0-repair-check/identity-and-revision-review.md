# Identity And Revision Review

```json
{
  "identity_matrix": {
    "result": "PASS",
    "results": [
      {
        "expected_accept": true,
        "observed_accept": true,
        "remote": "https://github.com/Julesc013/dominium.git",
        "result": "PASS"
      },
      {
        "expected_accept": true,
        "observed_accept": true,
        "remote": "https://github.com/Julesc013/dominium",
        "result": "PASS"
      },
      {
        "expected_accept": true,
        "observed_accept": true,
        "remote": "git@github.com:Julesc013/dominium.git",
        "result": "PASS"
      },
      {
        "expected_accept": true,
        "observed_accept": true,
        "remote": "ssh://git@github.com/Julesc013/dominium.git",
        "result": "PASS"
      },
      {
        "expected_accept": false,
        "observed_accept": false,
        "remote": "https://github.com/Julesc013/dominium-evil.git",
        "result": "PASS"
      },
      {
        "expected_accept": false,
        "observed_accept": false,
        "remote": "https://github.com/Julesc013/dominium.git.evil.example",
        "result": "PASS"
      },
      {
        "expected_accept": false,
        "observed_accept": false,
        "remote": "https://github.com/attacker/Julesc013/dominium.git",
        "result": "PASS"
      },
      {
        "expected_accept": false,
        "observed_accept": false,
        "remote": "https://example.com/Julesc013/dominium.git",
        "result": "PASS"
      },
      {
        "expected_accept": false,
        "observed_accept": false,
        "remote": "file:///tmp/Julesc013/dominium",
        "result": "PASS"
      },
      {
        "expected_accept": false,
        "observed_accept": false,
        "remote": "C:/tmp/Julesc013/dominium",
        "result": "PASS"
      },
      {
        "expected_accept": false,
        "observed_accept": false,
        "remote": "https://user:secret@github.com/Julesc013/dominium.git",
        "result": "PASS"
      },
      {
        "expected_accept": false,
        "observed_accept": false,
        "remote": "https://github.com/Julesc013/dominium.git?redirect=evil",
        "result": "PASS"
      },
      {
        "expected_accept": false,
        "observed_accept": false,
        "remote": "https://github.com/Julesc013/dominium.git#other",
        "result": "PASS"
      }
    ]
  },
  "revision_errors": []
}
```
