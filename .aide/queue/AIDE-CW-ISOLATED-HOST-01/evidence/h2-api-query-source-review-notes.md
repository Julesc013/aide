# H2 Supported API-Set Query Source Notes

The retained two-API resource effect failed on the first virtual contract with
Win32 error 2. That request remains consumed and was not replayed. Microsoft
documents API-set names as contracts rather than files and provides
`GetApiSetModuleBaseName` for dependency analyzers to obtain the implementation
module name.

The new source introduces a separate native adapter. It does not change the
constructor or dispatch behavior of the historical resource observer. The query
session requires an exact Windows build, immutable sorted contract names, a
finite expiry/duration, one durable reservation, and one exact durable intent
before each query. Any build, guard, clock, acknowledgement, HRESULT, output
length, host spelling, capacity, or serialization failure consumes the request
without partial success or automatic replay.

The 256-row ceiling is a bounded correction for the already observed 180-name
Python closure, not a wildcard or omission. Tests execute all 180 rows within a
257-call budget. Returned hosts are canonical physical DLL basenames only;
duplicate host values are allowed because many contracts can share one host.

This is author/source evidence, not independent review. No native constructor,
API query, file observation, copy, grant, profile, child, credential, network,
provider, broker, or release effect ran. A reviewer must bind these bytes before
an exact real-host query packet is prepared.
