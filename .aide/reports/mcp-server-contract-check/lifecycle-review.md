# Lifecycle Review

The lifecycle fixture order is coherent:

1. `initialize-request.json`
2. `initialize-result.json`
3. `initialized-notification.json`
4. list/read/call/refusal fixtures

The initialize request declares a concrete protocol version, capabilities, and
client implementation information. The initialize result declares the server
protocol version, capabilities, and server implementation information.

No lifecycle state machine, connection, transport, shutdown behavior, server
process, or endpoint exists.
