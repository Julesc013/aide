# Provider Review

Material finding `A2A-CHECK-004`: `provider` is present, but `provider.url` is `null`. For the pinned AgentProvider shape, present provider objects require non-empty `organization` and `url`. The check did not fabricate a URL.
