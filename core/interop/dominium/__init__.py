"""Offline read-only AIDE-Dominium seam helpers."""

from .bundle import (
    dominium_seam_diff,
    dominium_seam_status,
    project_dominium_seam,
    snapshot_dominium_source,
    validate_dominium_seam,
    run_dominium_seam_demo,
    unsupported_operation_refusal,
)
from .models import RECOMMENDED_NEXT_TASK, REPAIR_TASK_ID, TASK_ID
from .workunit_validation import (
    CAPABILITY_ID as WORKUNIT_VALIDATION_CAPABILITY_ID,
    CHECK_TASK_ID as WORKUNIT_VALIDATION_CHECK_TASK_ID,
    run_slice as run_dominium_workunit_validation_slice,
    status as dominium_workunit_validation_status,
    validate_slice_reports as validate_dominium_workunit_validation_slice,
)
from .registered_validation_backend import (
    CAPABILITY_ID as REGISTERED_VALIDATION_CAPABILITY_ID,
    CHECK_TASK_ID as REGISTERED_VALIDATION_CHECK_TASK_ID,
    run_backend as run_dominium_registered_validation_backend,
    status as dominium_registered_validation_status,
    validate_reports as validate_dominium_registered_validation_backend,
)

__all__ = [
    "dominium_seam_diff",
    "dominium_seam_status",
    "project_dominium_seam",
    "snapshot_dominium_source",
    "validate_dominium_seam",
    "run_dominium_seam_demo",
    "unsupported_operation_refusal",
    "dominium_workunit_validation_status",
    "run_dominium_workunit_validation_slice",
    "validate_dominium_workunit_validation_slice",
    "dominium_registered_validation_status",
    "run_dominium_registered_validation_backend",
    "validate_dominium_registered_validation_backend",
    "WORKUNIT_VALIDATION_CAPABILITY_ID",
    "WORKUNIT_VALIDATION_CHECK_TASK_ID",
    "REGISTERED_VALIDATION_CAPABILITY_ID",
    "REGISTERED_VALIDATION_CHECK_TASK_ID",
    "RECOMMENDED_NEXT_TASK",
    "REPAIR_TASK_ID",
    "TASK_ID",
]
