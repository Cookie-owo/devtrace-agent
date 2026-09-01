"""Controlled self-repair primitives for isolated verification."""

from .generator import PatchGenerator
from .patching import IsolatedWorkspace, PatchApplyResult, PatchOperation, StructuredPatch
from .service import ControlledRepairService, RepairOutcome

__all__ = [
    "IsolatedWorkspace",
    "PatchApplyResult",
    "PatchOperation",
    "StructuredPatch",
    "PatchGenerator",
    "ControlledRepairService",
    "RepairOutcome",
]
