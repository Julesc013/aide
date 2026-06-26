# Pre-Access Path Safety

```json
{
  "invalid_path_results": [
    {
      "accessed": [],
      "path": "/tmp/outside/aide.zip",
      "raised": null
    },
    {
      "accessed": [],
      "path": "C:/outside/aide.zip",
      "raised": null
    },
    {
      "accessed": [],
      "path": "\\\\server\\share\\aide.zip",
      "raised": null
    },
    {
      "accessed": [],
      "path": "../outside/aide.zip",
      "raised": null
    },
    {
      "accessed": [],
      "path": ".aide.local/state.sqlite",
      "raised": null
    },
    {
      "accessed": [],
      "path": ".env",
      "raised": null
    }
  ],
  "symlink_result": {
    "attempted": true,
    "reason": "distribution.component_digest_mismatch,distribution.manifest_invalid,distribution.missing_artifact_ref,distribution.missing_checksum",
    "valid": false
  }
}
```
