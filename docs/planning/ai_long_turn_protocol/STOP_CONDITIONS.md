# Stop Conditions

Stop and report instead of widening scope when any condition below appears.

## Authority Stops

- no queue item or intake packet exists for non-trivial work
- allowed paths are missing or insufficient
- current queue state conflicts with the prompt
- dependency status is unknown or failed
- review is required before continuation

## Safety Stops

- destructive operation is needed
- secret or credential access is needed
- branch creation, merge, promotion, push, prune, tag, or publication is needed
- target-repo mutation is needed
- provider/model, Gateway, or network behavior is needed
- external discovery is needed
- user hardware or environment details are needed

## Quality Stops

- validation failure is broad or unrelated to the task
- generated report churn cannot be classified
- manual content conflict cannot be merged clearly
- evidence is missing, stale, or not reviewable

## Reporting

When stopping, record:

- stop condition
- current files changed
- validation already run
- evidence path
- exact next action required
