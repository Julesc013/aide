"""Protected-config CLI: observation only; production apply always refuses."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

from .common import Refused, Git, bounded_bytes, parse_json, fields, identity, canonical
from .service import Broker


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", choices=("query", "apply"))
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--config-sha256", required=True)
    args = parser.parse_args()
    broker = None
    try:
        identity(args.config_sha256)
        raw = bounded_bytes(args.config)
        if hashlib.sha256(raw).hexdigest() != args.config_sha256:
            raise Refused("broker config drift")
        config = parse_json(raw)
        fields(config, "schema state_root exchange_root repository_root git authority")
        if config["schema"] != "aide.broker.config.v1":
            raise Refused("unknown broker configuration")
        fields(config["git"], "executable sha256")
        request_bytes = sys.stdin.buffer.read(1024 * 1024 + 1)
        if len(request_bytes) > 1024 * 1024:
            raise Refused("request byte budget")
        request = parse_json(request_bytes)
        broker = Broker(config["state_root"], config["exchange_root"], config["repository_root"],
                        Git(config["git"]["executable"], config["git"]["sha256"]), config["authority"])
        print(canonical(getattr(broker, args.operation)(request)))
        return 0
    except (Refused, OSError, ValueError, KeyError, TypeError) as exc:
        print(canonical({"schema": "aide.broker.refusal.v1", "reason": str(exc)}))
        return 2
    finally:
        if broker:
            broker.close()


if __name__ == "__main__":
    raise SystemExit(main())
