"""Deterministic patch generation from verified diagnosis evidence."""

from __future__ import annotations

from .patching import PatchOperation, StructuredPatch


class PatchGenerator:
    """Generate a narrow patch; it never edits files itself."""

    def generate_dto_test_patch(self) -> StructuredPatch:
        return StructuredPatch(
            operations=(
                PatchOperation(
                    path="tests/test_order.py",
                    old_text="{'user_id': 'u-001'}",
                    new_text="{'uid': 'u-001'}",
                ),
            ),
            allowed_paths=("tests/test_order.py",),
        )
