"""Schema surface audit for the Dominium read-only seam."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from . import models


EXTENSION_CONTAINER_SUFFIXES = (
    "/$defs/ExtensionMap",
    "/$defs/ExtensionValue/oneOf/5",
)


def _is_object_schema(node: dict[str, Any]) -> bool:
    return (
        node.get("type") == "object"
        or "properties" in node
        or "additionalProperties" in node
        or "patternProperties" in node
        or "propertyNames" in node
    )


def _pointer(parent: str, key: str) -> str:
    escaped = key.replace("~", "~0").replace("/", "~1")
    return f"{parent}/{escaped}" if parent else f"/{escaped}"


def _value_schema_summary(node: dict[str, Any]) -> str:
    if "patternProperties" in node:
        return "patternProperties"
    additional = node.get("additionalProperties", "__omitted__")
    if additional is False:
        return "closed"
    if additional == "__omitted__":
        return "omitted"
    if additional is True:
        return "opaque"
    if isinstance(additional, dict):
        if "$ref" in additional:
            return str(additional["$ref"])
        if additional:
            return "typed_schema"
        return "empty_schema"
    return type(additional).__name__


def _classify_object(path: str, node: dict[str, Any]) -> tuple[str, str]:
    additional = node.get("additionalProperties", "__omitted__")
    has_typed_map = isinstance(additional, dict) and bool(additional) and additional is not True
    has_pattern_map = bool(node.get("patternProperties"))
    if path.endswith(EXTENSION_CONTAINER_SUFFIXES):
        return ("explicit ExtensionMap", "documented extension container")
    if additional is False:
        return ("closed canonical object", "additionalProperties is false")
    if has_typed_map or has_pattern_map:
        return ("typed dynamic map", "dynamic keys have constrained values")
    return ("unclassified", "object is open or lacks a constrained value schema")


def schema_surface_audit(schema: dict[str, Any]) -> dict[str, Any]:
    records: list[dict[str, Any]] = []

    def walk(node: Any, path: str) -> None:
        if isinstance(node, dict):
            if _is_object_schema(node):
                classification, reason = _classify_object(path or "/", node)
                additional = node.get("additionalProperties", "__omitted__")
                records.append(
                    {
                        "json_pointer": path or "/",
                        "classification": classification,
                        "additionalProperties": additional if isinstance(additional, (bool, str)) else _value_schema_summary(node),
                        "property_count": len(node.get("properties", {}) if isinstance(node.get("properties"), dict) else {}),
                        "patternProperties": sorted((node.get("patternProperties") or {}).keys()),
                        "value_schema": _value_schema_summary(node),
                        "reason": reason,
                    }
                )
            for key, value in node.items():
                walk(value, _pointer(path, str(key)))
        elif isinstance(node, list):
            for index, value in enumerate(node):
                walk(value, f"{path}/{index}" if path else f"/{index}")

    walk(schema, "")
    unclassified = [item for item in records if item["classification"] == "unclassified"]
    unintentionally_open = [
        item
        for item in records
        if item["classification"] == "unclassified"
        or (item["classification"] != "explicit ExtensionMap" and item["value_schema"] in {"opaque", "empty_schema", "omitted"})
    ]
    return {
        "schema_version": "aide.dominium-readonly-seam.schema-surface-audit.v0",
        "task_id": models.REPAIR_TASK_ID,
        "object_count": len(records),
        "unclassified_object_count": len(unclassified),
        "unintentionally_open_object_count": len(unintentionally_open),
        "objects": records,
        "unclassified_objects": unclassified,
        "unintentionally_open_objects": unintentionally_open,
    }


def audit_schema_file(path: str | Path) -> dict[str, Any]:
    return schema_surface_audit(models.read_json(Path(path)))
