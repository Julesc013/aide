"""Structural and adversarial checks for this advisory planning candidate."""
from __future__ import annotations

import copy
import json
from pathlib import Path


RELATIONSHIPS = (
    "implementation_prerequisites", "activation_gates", "qualification_gates",
    "preferred_sequence",
)
PHASES = {"start", "work", "verify", "interrupt", "resume", "conserve", "consume", "explain"}


def validate(plan):
    errors = []
    if plan.get("authority") != "advisory_navigation_not_queue_admission":
        errors.append("planning cannot grant admission")
    milestones = [m["id"] for m in plan["milestones"]]
    if set(milestones) != {f"P{i}" for i in range(12)} or len(milestones) != 12:
        errors.append("P0-P11 identities must be preserved")
    capabilities = {c["id"]: c for c in plan["capabilities"]}
    if len(capabilities) != len(plan["capabilities"]):
        errors.append("duplicate capability identity")
    for identity, capability in capabilities.items():
        if capability["milestone"] not in milestones or not capability["existing_owner"]:
            errors.append(f"missing existing owner or milestone: {identity}")
        for relationship in RELATIONSHIPS:
            refs = capability.get(relationship)
            if not isinstance(refs, list):
                errors.append(f"missing typed relationship: {identity}/{relationship}")
                continue
            for ref in refs:
                if ref not in capabilities or ref == identity:
                    errors.append(f"unknown or self relationship: {identity}/{ref}")
    def visit(identity, visiting, visited):
        if identity in visiting:
            errors.append(f"hard prerequisite cycle: {identity}")
            return
        if identity in visited or identity not in capabilities:
            return
        visiting.add(identity)
        for kind in RELATIONSHIPS[:2]:
            for ref in capabilities[identity].get(kind, []):
                visit(ref, visiting, visited)
        visiting.remove(identity)
        visited.add(identity)
    visited = set()
    for identity in capabilities:
        visit(identity, set(), visited)
    early = {
        "P6.reuse": {"P2", "P3"},
        "P8.readonly_view": {"P3", "P6", "P7"},
        "P8.relay": {"P7", "P8"},
        "P5.observation": {"P1", "P2", "P7"},
        "P10.lesson_correction": {"P10"},
        "P7.role_fixture": {"P11"},
    }
    for identity, unrelated in early.items():
        for kind in RELATIONSHIPS[:2]:
            for ref in capabilities[identity][kind]:
                if ref.split(".")[0] in unrelated:
                    errors.append(f"unnecessarily broad early gate: {identity}/{ref}")
    phases = plan["daily_use"]["phases"]
    if {p["id"] for p in phases} != PHASES or len(phases) != 8:
        errors.append("eight daily-use phases required")
    for phase in phases:
        if any(not phase.get(k) for k in ("positive", "refusal", "recovery", "evidence_required")):
            errors.append(f"missing positive/refusal/recovery evidence: {phase['id']}")
    if plan["cross_cutting"].get("unknown_usage") != "preserve_unknown":
        errors.append("unknown usage must stay unknown")
    if plan["release"].get("advanced_profiles_required_for_lite") is not False:
        errors.append("advanced profiles cannot become blanket Lite requirements")
    return errors


def main():
    root = Path(__file__).resolve().parents[4]
    plan = json.loads((root / "docs/roadmap/development-workflows.json").read_text(encoding="utf-8"))
    errors = validate(plan)
    if errors:
        raise SystemExit("FAIL: " + "; ".join(errors))
    mutations = [
        ("unknown reference", lambda p: p["capabilities"][0]["implementation_prerequisites"].append("missing.capability")),
        ("old broad P6 gate", lambda p: next(c for c in p["capabilities"] if c["id"] == "P6.reuse")["implementation_prerequisites"].append("P3.continuation")),
        ("old broad Workbench gate", lambda p: next(c for c in p["capabilities"] if c["id"] == "P8.readonly_view")["activation_gates"].append("P7.bindings")),
        ("missing recovery", lambda p: p["daily_use"]["phases"][0].pop("recovery")),
        ("invented accounting", lambda p: p["cross_cutting"].update(unknown_usage="zero")),
        ("implicit admission", lambda p: p.update(authority="operational_authority")),
    ]
    for name, mutate in mutations:
        changed = copy.deepcopy(plan)
        mutate(changed)
        if not validate(changed):
            raise SystemExit(f"FAIL: failed to reject {name}")
    print(f"PASS: {len(plan['milestones'])} milestones, {len(plan['capabilities'])} capabilities, 8 acceptance phases; 6 invalid plans refused")


if __name__ == "__main__":
    main()
