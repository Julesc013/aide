# Security Boundary Review

The MCP contract records security expectations only:

- user consent before future tool invocation;
- tool descriptions and annotations are not trusted authorization;
- resource URIs require validation;
- sensitive resources require access control;
- no raw credentials in projections;
- no arbitrary filesystem exposure;
- no live network behavior;
- no mutation tools in v0.

The generated contract does not expose `file://`, `http://`, or `https://`
resource roots and does not bind or declare a live endpoint.
