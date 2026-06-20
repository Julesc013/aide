# Capability Negotiation Review

Client capabilities observed in the initialize request:

- `roots`
- `sampling`

Server capabilities observed in the initialize result:

- `resources`
- `tools`
- `prompts`

The server does not advertise `roots`, `sampling`, or `elicitation` as server
features. Catalogue availability remains distinct from runtime serving.

No client capability is treated as implemented AIDE behavior.
