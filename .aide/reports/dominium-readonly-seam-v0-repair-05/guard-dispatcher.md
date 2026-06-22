# Guard Dispatcher

`GuardRequest` values are routed through `dispatch_guarded_request`. Forbidden families reach a guard, capture before/after state digests, refuse before calling the injected executor, and return typed decisions.
