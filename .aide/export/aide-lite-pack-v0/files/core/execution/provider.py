"""Generic execution provider protocol."""

from __future__ import annotations

from typing import Protocol

from core.protocol.execution_receipt import CapabilityOutcome, ProcessExecutionReceipt
from core.protocol.process_invocation import CapabilityBinding, CapabilityInvocation


class ExecutionProvider(Protocol):
    def execute(
        self,
        invocation: CapabilityInvocation,
        binding: CapabilityBinding,
    ) -> tuple[ProcessExecutionReceipt, CapabilityOutcome]:
        """Execute one bound capability invocation and return a neutral receipt."""
