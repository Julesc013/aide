"""Small structural readers for AIDE Harness v0.

This module intentionally does not parse full YAML. It supports only the
line-oriented checks needed by the v0 Profile/Contract records.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


class ContractReadError(Exception):
    """Raised when a required contract file cannot be read."""


def clean_scalar(value: str) -> str:
    value = value.strip()
    if " #" in value:
        value = value.split(" #", 1)[0].strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1]
    return value


@dataclass(frozen=True)
class RepoContext:
    root: Path

    def relpath(self, path: Path) -> str:
        try:
            return path.relative_to(self.root).as_posix()
        except ValueError:
            return path.as_posix()

    def path(self, relative: str | Path) -> Path:
        return self.root / relative

    def exists(self, relative: str | Path) -> bool:
        return self.path(relative).exists()

    def is_dir(self, relative: str | Path) -> bool:
        return self.path(relative).is_dir()

    def read_text(self, relative: str | Path) -> str:
        path = self.path(relative)
        try:
            return path.read_text(encoding="utf-8")
        except OSError as exc:
            raise ContractReadError(f"could not read {self.relpath(path)}: {exc}") from exc


def parse_top_level_scalars(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    pattern = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$")
    for raw_line in text.splitlines():
        if not raw_line or raw_line.startswith((" ", "\t", "#")):
            continue
        match = pattern.match(raw_line)
        if match:
            key, value = match.groups()
            values[key] = clean_scalar(value)
    return values


def list_item_ids(text: str) -> list[str]:
    ids: list[str] = []
    pattern = re.compile(r"^\s+- id:\s*(.+?)\s*$")
    for raw_line in text.splitlines():
        match = pattern.match(raw_line)
        if match:
            ids.append(clean_scalar(match.group(1)))
    return ids


def parse_queue_index(text: str) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    in_items = False
    key_value = re.compile(r"^\s+([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$")

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped == "items:":
            in_items = True
            continue
        if not in_items:
            continue
        if stripped.startswith("- id:"):
            if current is not None:
                items.append(current)
            current = {"id": clean_scalar(stripped.split(":", 1)[1])}
            continue
        if current is None:
            continue
        match = key_value.match(line)
        if match:
            key, value = match.groups()
            current[key] = clean_scalar(value)

    if current is not None:
        items.append(current)
    return items


def parse_status_file(text: str) -> dict[str, str]:
    return parse_top_level_scalars(text)
