# External Discovery Policy

Long turns must not turn missing outside evidence into invented facts.

## External Discovery Means

- broad source or web discovery
- target-repo inspection outside the authorized workspace
- provider/model calls
- network fetches
- hardware or environment observation not available in the current repo
- public publication or deployment checks

## Rule

When external discovery is required, stop and create a handoff or evidence
request unless the WorkUnit explicitly authorizes that discovery method.

## Handoff Contents

Record:

- exact question to answer
- sources or systems to inspect
- forbidden actions
- expected artifact format
- how returned evidence will be validated
- which WorkUnit should resume after evidence returns

## Anti-Overclaim Rule

Leads, summaries, generated reports, and model output are not external evidence
unless a reviewed policy says so and validation records support the claim.
