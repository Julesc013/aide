# A2A Preview Boundary

`a2a-agent-card.preview.json` is accepted only as structurally valid preview
metadata.

It records:

- `preview_only: true`
- `endpoint_implemented: false`
- `url: null`
- disabled task delegation, worker execution, admission, trust, provider calls,
  network calls, and repository mutation.

This acceptance is not:

- A2A server;
- A2A task delegation;
- A2A authentication;
- A2A worker execution;
- external agent registration.
