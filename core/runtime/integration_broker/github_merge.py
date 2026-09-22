"""Fixed GitHub merge contract; no credential or network dispatcher is installed."""
from .common import Refused, OID, canonical, fields, identity
from .github_api import ORIGIN, VERSION, Response, safe_json, text_value
from .pr_observation import decision

MAX_RESPONSE = 65536


def merge_request(plan, observation):
    """Build the only admitted merge request from an exact current observation.

    GitHub applies ``sha`` as an expected-head predicate. The endpoint has no
    corresponding expected-base argument, so the prior observation and policy
    checks remain prerequisites rather than claims of endpoint atomicity.
    """
    if decision(plan, observation) != "merge":
        raise Refused("GitHub merge request lacks an exact qualified observation")
    number = observation["pull"]["number"]
    body = canonical({"merge_method": "merge", "sha": plan["candidate_commit"]}).encode("utf-8")
    return {
        "method": "PUT",
        "url": f"{ORIGIN}/repos/{plan['repository']}/pulls/{number}/merge",
        "headers": {
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": VERSION,
        },
        "body": body,
    }


def classify_response(plan, observation, response):
    """Classify one synchronous response without claiming integration.

    Missing responses are intentionally not representable here. The durable
    bridge owns uncertain outcomes and prohibits replay; a later authenticated
    observation is the only route to ``integrated``.
    """
    request = merge_request(plan, observation)
    if (not isinstance(response, Response) or response.url != request["url"] or
            type(response.status) is not int or type(response.body) is not bytes or
            len(response.body) > MAX_RESPONSE):
        raise Refused("GitHub merge response identity or byte budget refused")
    content_type = None
    seen = set()
    for key, value in response.headers:
        if (not isinstance(key, str) or not isinstance(value, str) or
                key.casefold() in seen):
            raise Refused("GitHub merge response headers refused")
        seen.add(key.casefold())
        if key.casefold() == "content-type":
            content_type = value.casefold()
    if content_type is None or not content_type.startswith("application/json"):
        raise Refused("GitHub merge response is not JSON")
    value = safe_json(response.body)
    if not isinstance(value, dict):
        raise Refused("GitHub merge response object required")
    if response.status == 200:
        fields(value, "sha merged message")
        identity(value["sha"], OID)
        text_value(value["message"], 1000)
        if value["merged"] is not True:
            return {"status": "refused", "http_status": 200}
        return {"status": "submitted", "response_sha": value["sha"]}
    if response.status in (405, 409, 422):
        text_value(value.get("message"), 1000)
        return {"status": "refused", "http_status": response.status}
    raise Refused("unexpected GitHub merge response status")
