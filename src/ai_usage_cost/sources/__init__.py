from __future__ import annotations

import importlib
import pkgutil

from .base import Source

__all__ = ["Source", "registry", "client_labels"]


def registry() -> dict[str, Source]:
    found: dict[str, Source] = {}
    for info in pkgutil.iter_modules(__path__):
        if info.name == "base":
            continue
        module = importlib.import_module(f"{__name__}.{info.name}")
        source = getattr(module, "SOURCE", None)
        if isinstance(source, Source):
            found[source.id] = source
    return dict(sorted(found.items()))


def client_labels() -> dict[str, str]:
    labels: dict[str, str] = {}
    for source in registry().values():
        labels.update(source.clients)
    return labels
