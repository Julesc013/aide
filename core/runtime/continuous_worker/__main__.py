"""Opt-in CLI. No scheduled service or live activation is installed implicitly."""
import argparse
import json
from pathlib import Path

from .coordinator import Coordinator
from .contract import read_activation
from .state import Refused, State


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("preflight", "run"):
        p = sub.add_parser(name)
        p.add_argument("--activation", type=Path, required=True)
        p.add_argument("--approval-sha256", required=True)
    for name in ("status", "pause-dispatch", "drain", "resume", "emergency-stop", "cancel-task"):
        p = sub.add_parser(name)
        p.add_argument("--state-root", type=Path, required=True)
        if name == "cancel-task":
            p.add_argument("--task", required=True)
    args = parser.parse_args()
    try:
        if args.command == "preflight":
            read_activation(args.activation, args.approval_sha256)
            result = {"configuration": "valid", "dispatch": False,
                      "qualification": "external host and integration evidence still authoritative"}
        elif args.command == "run":
            runner = Coordinator(args.activation, args.approval_sha256)
            try:
                result = runner.run()
            finally:
                runner.state.close()
        else:
            if not (args.state_root / "coordinator.sqlite3").is_file():
                raise Refused("unknown state root; operator commands never initialize state")
            state = State(args.state_root)
            try:
                if args.command != "status":
                    state.control(args.command, getattr(args, "task", None))
                result = state.status()
            finally:
                state.close()
        print(json.dumps(result, indent=2))
        return 0
    except (Refused, OSError, ValueError, KeyError) as exc:
        print(json.dumps({"result": "refused", "reason": str(exc)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

