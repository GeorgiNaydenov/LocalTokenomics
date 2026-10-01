"""Roo Code (final release 3.53.0, archived 2026-05-15): see ``cline.py`` for the format.

Roo logs NO model id in its task files, so events carry ``model=None`` and are unpriced; the
tool's own USD ``cost`` still rides in ``reported_cost``. ``tokensIn`` is inclusive of cache
(Task.ts ``totalInputTokens``); older Roo builds may differ [unverified].
"""

from __future__ import annotations

from pathlib import Path

from .cline import _TOKENS_IN_INCLUSIVE, Spec, make_source, task_roots

_SPEC = Spec("roo-code", "Roo Code", "rooveterinaryinc.roo-cline", _TOKENS_IN_INCLUSIVE["roo-code"])


def default_roots() -> list[Path]:
    return task_roots(_SPEC.ext_id)


SOURCE = make_source(
    _SPEC,
    label="Roo Code",
    default_roots=default_roots,
    display_path=(
        "<VS Code user data>/User/globalStorage/rooveterinaryinc.roo-cline/tasks/<id>/"
        "ui_messages.json"
    ),
)
