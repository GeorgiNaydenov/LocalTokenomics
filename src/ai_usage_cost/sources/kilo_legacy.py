"""Kilo Code legacy v5 task dirs: see ``cline.py`` for the format.

Kilo v7 (``kilo.db``, an OpenCode fork) is read by the OpenCode parser; v7 also imports legacy
tasks, so the same work can show up in both sources. ``tokensIn`` is assumed inclusive of cache
like Roo (Kilo v5 descends from it) [unverified].
"""

from __future__ import annotations

from pathlib import Path

from .cline import _TOKENS_IN_INCLUSIVE, Spec, make_source, task_roots

_SPEC = Spec(
    "kilo-code-legacy",
    "Kilo Code (legacy)",
    "kilocode.kilo-code",
    _TOKENS_IN_INCLUSIVE["kilo-code-legacy"],
)


def default_roots() -> list[Path]:
    return task_roots(_SPEC.ext_id)


SOURCE = make_source(
    _SPEC,
    label="Kilo Code (legacy)",
    default_roots=default_roots,
    display_path=(
        "<VS Code user data>/User/globalStorage/kilocode.kilo-code/tasks/<id>/ui_messages.json"
    ),
)
