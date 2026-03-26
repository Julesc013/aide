"""Shared-core request dispatch for the AIDE bootstrap runtime."""

from .dispatcher import dispatch_json_text, dispatch_request_payload

__all__ = ["dispatch_json_text", "dispatch_request_payload"]
