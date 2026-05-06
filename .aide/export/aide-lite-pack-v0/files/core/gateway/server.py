"""Localhost-only HTTP skeleton for Q19 Gateway status endpoints."""

from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Type

from .gateway_status import GATEWAY_VERSION, SERVICE_NAME, endpoint_payload, repo_root_from


LOCAL_HOSTS = {"127.0.0.1", "localhost", "::1"}


def make_handler(repo_root: Path) -> Type[BaseHTTPRequestHandler]:
    root = repo_root.resolve()

    class GatewayHandler(BaseHTTPRequestHandler):
        server_version = f"{SERVICE_NAME}/{GATEWAY_VERSION}"

        def do_GET(self) -> None:  # noqa: N802 - stdlib hook name
            status_code, payload = endpoint_payload(self.path, root)
            body = (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
            self.send_response(status_code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_POST(self) -> None:  # noqa: N802 - stdlib hook name
            payload = {
                "status": "method_not_allowed",
                "service": SERVICE_NAME,
                "message": "Q19 Gateway skeleton exposes GET status endpoints only.",
                "provider_calls_enabled": False,
                "model_calls_enabled": False,
            }
            body = (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
            self.send_response(405)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format: str, *args: object) -> None:
            # Keep the skeleton quiet by default; future Gateway logging needs a reviewed policy.
            return

    return GatewayHandler


def serve(repo_root: Path, host: str = "127.0.0.1", port: int = 8765) -> None:
    if host not in LOCAL_HOSTS:
        raise ValueError("Q19 Gateway skeleton may bind only to localhost/127.0.0.1/::1")
    handler = make_handler(repo_root)
    httpd = ThreadingHTTPServer((host, port), handler)
    print(f"{SERVICE_NAME} {GATEWAY_VERSION} listening on http://{host}:{port}")
    print("local skeleton only; provider/model forwarding is disabled")
    try:
        httpd.serve_forever()
    finally:
        httpd.server_close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="AIDE Gateway skeleton server.")
    parser.add_argument("--repo-root", default=str(repo_root_from()))
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args(argv)
    serve(Path(args.repo_root), host=args.host, port=args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
