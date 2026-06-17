# Remaining Risks

- EventRecord remains projection-only; there is no runtime event store, event log, replay, or state reconstruction.
- Full JSON Schema Draft 2020-12 validation remains deferred.
- Event family names are reserved vocabulary only and do not implement their named future subsystems.
- The latest task packet remains stale relative to queue truth.
- OKF is not implemented by this acceptance task; it is only the recommended next queue task.
