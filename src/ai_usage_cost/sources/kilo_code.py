"""Kilo Code v7 -- an OpenCode fork storing ``kilo.db``; same parser, different roots.

Legacy Kilo v5 task-dir logs belong to the Cline-family parser. v7 imports those legacy
tasks into ``kilo.db``, so a machine that has both may count imported work twice.
"""

from __future__ import annotations

from .opencode import make_source

SOURCE = make_source(
    source_id="kilo-code",
    label="Kilo Code",
    app="kilo",
    db_env="KILO_DB",
    display_path="$XDG_DATA_HOME/kilo/kilo.db (or ~/.local/share/kilo, %APPDATA%\\kilo)",
)
