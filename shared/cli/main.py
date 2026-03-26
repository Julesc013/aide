"""Host-agnostic CLI bridge for the shared-core bootstrap runtime."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from shared.core.dispatcher import dispatch_json_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the AIDE shared-core boot-slice runtime.")
    parser.add_argument(
        "--request",
        type=Path,
        help="Path to a JSON request fixture. If omitted, the CLI reads JSON from stdin.",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print the JSON response for human inspection.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        request_text = _read_request_text(args.request)
    except OSError as exc:
        parser.exit(status=2, message=f"Unable to read request input: {exc}\n")

    response = dispatch_json_text(request_text)
    dump_kwargs: dict[str, object] = {"sort_keys": True}
    if args.pretty:
        dump_kwargs["indent"] = 2
    sys.stdout.write(json.dumps(response, **dump_kwargs))
    sys.stdout.write("\n")
    return 0 if response.get("status") != "failed" else 1


def _read_request_text(request_path: Path | None) -> str:
    if request_path is not None:
        return request_path.read_text(encoding="utf-8")
    return sys.stdin.read()
