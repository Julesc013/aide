# AIDE Provider Contracts

`core/providers/` contains Q20 offline provider-adapter contract helpers.

This package does not call providers, models, local runtimes, or network
services. It loads committed metadata from `.aide/providers/`, validates the
no-call boundary, and produces compact status dictionaries for AIDE Lite and
the local Gateway skeleton.

Live provider execution remains deferred to a future reviewed queue phase.
