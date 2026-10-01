"""Maintainer tool: compare our price table with LiteLLM's public catalogue.

`ai-usage-cost` ships a hand-maintained table (src/ai_usage_cost/rates.json) and fetches
nothing at runtime. This script is NOT part of the package: it reads rates.json as plain
JSON (v1 and v2 schema both work), downloads LiteLLM's catalogue and prints what a human
should review. It never writes rates.json.

    python scripts/rates_diff.py
    python scripts/rates_diff.py --catalog litellm.json --format json --fail-on-findings

Sections: models missing from our table (with a proposed v2 row skeleton), price drift,
preview rows, retired/stale rows, and a watchlist of models we cannot price yet.
Every skeleton is a proposal derived from a secondary source: check the vendor page.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path
from typing import Any

CATALOG_URL = (
    "https://raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json"
)
USER_AGENT = "ai-usage-cost-rates-diff/1.0 (maintainer price-table check; read-only)"
DEFAULT_RATES = Path(__file__).resolve().parent.parent / "src" / "ai_usage_cost" / "rates.json"
FETCH_TIMEOUT_S = 30

# Catalogue modes that carry per-token chat pricing. LiteLLM files many codex / pro models
# under "responses", so that mode counts too.
TEXT_MODES = frozenset({"chat", "completion", "responses"})

# Provider prefixes stripped from catalogue keys (repeatedly). Keys carrying any other
# prefix are third-party hosts (openrouter, fireworks_ai, ...) and are ignored.
PROVIDER_PREFIXES = (
    "us.anthropic.",
    "eu.anthropic.",
    "apac.anthropic.",
    "global.anthropic.",
    "anthropic.",
    "amazon.",
    "meta.",
    "openai/",
    "anthropic/",
    "gemini/",
    "vertex_ai/",
    "xai/",
    "deepseek/",
    "moonshot/",
    "meta/",
    "typesafe/",
    "mistral/",
    "minimax/",
    "bedrock/",
    "azure/",
    "azure_ai/",
    "dashscope/",
    "zai/",
)
REGIONAL_ID = re.compile(r"^(?:us|eu|apac|jp|au|ca|global|us-gov)\.")

# What may follow a row's `match` and still be "the same model" (mirrors the lookup rule).
BENIGN_TOKEN = r"(?:-\d{8}|-\d{4}-\d{2}-\d{2}|@\d{8}|\[1m\]|-v\d+(?::\d+)?|-latest)"
BENIGN_REMAINDER = re.compile(rf"^{BENIGN_TOKEN}+$")
BENIGN_TAIL = re.compile(rf"{BENIGN_TOKEN}+$")

WATCHLIST_LITERAL = ("gemini-4", "codex-auto-review")
VARIANT_SUFFIXES = {
    "priority": "priority",
    "flex": "flex",
    "batches": "batch",
    "ultrafast": "ultrafast",
}
BAND_FIELD = re.compile(r"_above_(\d+)k_tokens(?:_(priority|flex|batches|ultrafast))?$")

# First-party providers whose bare/prefixed catalogue keys we trust over cloud re-sellers.
FIRST_PARTY_PREFIXES = ("openai/", "anthropic/", "gemini/", "xai/", "deepseek/", "moonshot/")
ID_PROVIDERS = (
    ("claude", "anthropic"),
    ("gpt-", "openai"),
    ("codex", "openai"),
    ("chatgpt", "openai"),
    ("gemini", "google"),
    ("gemma", "google"),
    ("grok", "xai"),
    ("deepseek", "deepseek"),
    ("kimi", "moonshot"),
    ("mistral", "mistral"),
    ("codestral", "mistral"),
    ("devstral", "mistral"),
    ("ministral", "mistral"),
    ("magistral", "mistral"),
    ("muse", "meta"),
    ("llama", "meta"),
    ("qwen", "alibaba"),
    ("glm", "zhipu"),
    ("minimax", "minimax"),
    ("nova", "amazon"),
)
LITELLM_PROVIDERS = {
    "openai": "openai",
    "text-completion-openai": "openai",
    "anthropic": "anthropic",
    "gemini": "google",
    "vertex_ai-language-models": "google",
    "xai": "xai",
    "deepseek": "deepseek",
    "moonshot": "moonshot",
    "mistral": "mistral",
    "meta_llama": "meta",
    "minimax": "minimax",
    "dashscope": "alibaba",
    "zai": "zhipu",
}

Row = dict[str, Any]
Entry = dict[str, Any]


class CatalogError(RuntimeError):
    """Catalogue could not be fetched or parsed."""


def normalise_key(key: str) -> str | None:
    """Catalogue key -> lowercase model id, or None when the key is not ours to compare.

    None for third-party hosts, `bedrock/us-east-1/...` style paths and fine-tunes.
    Known provider prefixes are stripped repeatedly.
    """
    name = key.strip().lower()
    stripped = True
    while stripped:
        stripped = False
        for prefix in PROVIDER_PREFIXES:
            if name.startswith(prefix):
                name = name[len(prefix) :]
                stripped = True
    if not name or "/" in name or name.startswith("ft:") or REGIONAL_ID.match(name):
        return None
    return name


def classify(model_id: str, matches: list[str]) -> tuple[str, str | None]:
    """Reproduce our lookup: longest startswith `match`; remainder decides the kind.

    Returns (kind, match) with kind in exact | suffix | estimated | none.
    """
    best: str | None = None
    for match in matches:
        if model_id.startswith(match) and (best is None or len(match) > len(best)):
            best = match
    if best is None:
        return "none", None
    rest = model_id[len(best) :]
    if not rest:
        return "exact", best
    if BENIGN_REMAINDER.match(rest):
        return "suffix", best
    return "estimated", best


def per_million(value: Any) -> float | None:
    """Per-token cost -> USD per 1M tokens, rounded to 6 decimals; None when absent."""
    if isinstance(value, bool) or not isinstance(value, int | float):
        return None
    return round(float(value) * 1e6, 6)


def _fields(entry: Entry, suffix: str) -> dict[str, float]:
    """PriceSet for one catalogue field family; `suffix` like `_above_272k_tokens_priority`."""
    out: dict[str, float] = {}
    names = (
        ("input", f"input_cost_per_token{suffix}"),
        ("output", f"output_cost_per_token{suffix}"),
        ("cache_read", f"cache_read_input_token_cost{suffix}"),
        ("cache_write_5m", f"cache_creation_input_token_cost{suffix}"),
    )
    for name, field in names:
        price = per_million(entry.get(field))
        if price is not None:
            out[name] = price
    # LiteLLM spells the 1h write rate `..._above_1hr` + any band/tier suffix.
    hour = per_million(entry.get(f"cache_creation_input_token_cost_above_1hr{suffix}"))
    if hour is not None:
        out["cache_write_1h"] = hour
    return out


def display_guess(model_id: str) -> str:
    """claude-opus-5-5 -> 'Claude Opus 5.5' (a guess; the maintainer fixes it)."""
    words: list[str] = []
    for token in model_id.split("-"):
        if token.isdigit() and words and re.fullmatch(r"[\d.]+", words[-1]):
            words[-1] = f"{words[-1]}.{token}"
        elif token in ("gpt", "glm"):
            words.append(token.upper())
        else:
            words.append(token if token[:1].isdigit() else token.capitalize())
    return " ".join(words)


def guess_provider(model_id: str, entry: Entry) -> str:
    """Our provider id for a catalogue entry (from the model id, else LiteLLM's field)."""
    for start, provider in ID_PROVIDERS:
        if model_id.startswith(start):
            return provider
    return LITELLM_PROVIDERS.get(str(entry.get("litellm_provider", "")), "unknown")


def build_skeleton(model_id: str, entry: Entry, source: str) -> Row:
    """Proposed v2 row from a catalogue entry. Always needs a vendor-page check."""
    row: Row = {
        "match": BENIGN_TAIL.sub("", model_id),
        "provider": guess_provider(model_id, entry),
    }
    row["display"] = display_guess(str(row["match"]))
    base = _fields(entry, "")
    row.update(base)
    variants: dict[str, dict[str, float]] = {}
    for suffix, tier in VARIANT_SUFFIXES.items():
        price_set = _fields(entry, f"_{suffix}")
        if price_set:
            variants[tier] = price_set
    if variants:
        row["variants"] = variants
    thresholds = sorted({int(m.group(1)) for k in entry if (m := BAND_FIELD.search(k))})
    bands: list[Row] = []
    for threshold in thresholds:
        band: Row = {"min_input_tokens": threshold * 1000 + 1}
        band.update(_fields(entry, f"_above_{threshold}k_tokens"))
        band_variants = {
            tier: price_set
            for suffix, tier in VARIANT_SUFFIXES.items()
            if (price_set := _fields(entry, f"_above_{threshold}k_tokens_{suffix}"))
        }
        if band_variants:
            band["variants"] = band_variants
        bands.append(band)
    if bands:
        row["bands"] = bands
    window = entry.get("max_input_tokens")
    if isinstance(window, int) and not isinstance(window, bool):
        row["context_window"] = window
    row["source"] = source
    row["verified"] = None
    row["note"] = "LiteLLM-derived skeleton -- needs a vendor-page check before use"
    return row


def load_rates(path: Path) -> Row:
    """rates.json as plain JSON (v1 or v2)."""
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict) or not isinstance(data.get("models"), list):
        raise CatalogError(f"{path}: not a rates file (no 'models' list)")
    return data


def load_catalog(location: str) -> dict[str, Entry]:
    """Read the LiteLLM catalogue from a local file or an http(s) URL."""
    try:
        if location.startswith(("http://", "https://")):
            request = urllib.request.Request(  # noqa: S310 - scheme checked above
                location, headers={"User-Agent": USER_AGENT}
            )
            with urllib.request.urlopen(request, timeout=FETCH_TIMEOUT_S) as response:  # noqa: S310  # nosec B310
                raw = response.read().decode("utf-8")
        else:
            raw = Path(location).read_text(encoding="utf-8")
        data = json.loads(raw)
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
        raise CatalogError(f"could not load catalogue {location!r}: {exc}") from exc
    if not isinstance(data, dict):
        raise CatalogError(f"catalogue {location!r} is not a JSON object")
    return {k: v for k, v in data.items() if isinstance(v, dict) and k != "sample_spec"}


def _rank(model_id: str, key: str) -> tuple[int, int, str]:
    """Prefer bare / first-party keys over cloud re-sellers; shorter keys first."""
    lowered = key.lower()
    first_party = lowered == model_id or lowered.startswith(FIRST_PARTY_PREFIXES)
    return (0 if first_party else 1, len(key), key)


def candidates(catalog: dict[str, Entry]) -> list[tuple[str, str, Entry]]:
    """(normalised id, raw key, entry) for text-model entries we can compare, best first."""
    found = []
    for key, entry in catalog.items():
        if entry.get("mode") not in TEXT_MODES or "input_cost_per_token" not in entry:
            continue
        model_id = normalise_key(key)
        # Regional endpoints (eu./us./global. ...) carry surcharges: never a price source.
        if model_id and not REGIONAL_ID.match(key.lower()):
            found.append((model_id, key, entry))
    found.sort(key=lambda item: _rank(item[0], item[1]))
    return found


def _active_period(row: Row, today: date) -> bool:
    for period in row.get("periods") or []:
        start = period.get("from")
        end = period.get("until")
        if (start is None or date.fromisoformat(start) <= today) and (
            end is None or today < date.fromisoformat(end)
        ):
            return True
    return False


def _differs(ours: float, theirs: float, rel_tol: float, abs_tol: float) -> bool:
    return abs(ours - theirs) > max(abs(theirs) * rel_tol, abs_tol)


def compare_prices(
    row: Row, entry: Entry, rel_tol: float = 0.005, abs_tol: float = 0.0001
) -> list[dict[str, Any]]:
    """Fields where our top-level price differs from the catalogue's (USD/M)."""
    theirs = _fields(entry, "")
    diffs = []
    for name in ("input", "output", "cache_read", "cache_write_5m", "cache_write_1h"):
        ours = row.get(name)
        if not isinstance(ours, int | float) or isinstance(ours, bool) or name not in theirs:
            continue
        if _differs(float(ours), theirs[name], rel_tol, abs_tol):
            diffs.append({"field": name, "ours": float(ours), "theirs": theirs[name]})
    return diffs


def _stale(row: Row, today: date, stale_days: int) -> tuple[bool, str | None]:
    verified = row.get("verified")
    if not verified:
        return True, None
    try:
        age = (today - date.fromisoformat(verified)).days
    except ValueError:
        return True, str(verified)
    return age > stale_days, str(verified)


def analyse(
    rates: Row,
    catalog: dict[str, Entry],
    *,
    today: date,
    stale_days: int = 30,
    rel_tol: float = 0.005,
    abs_tol: float = 0.0001,
    source: str = CATALOG_URL,
) -> dict[str, Any]:
    """Build the full report as plain data."""
    rows: list[Row] = [r for r in rates["models"] if isinstance(r, dict) and r.get("match")]
    matches = [str(r["match"]).lower() for r in rows]
    by_match = {str(r["match"]).lower(): r for r in rows}
    cands = candidates(catalog)

    missing: dict[str, tuple[str, Entry]] = {}
    row_entry: dict[str, tuple[str, Entry]] = {}
    for model_id, key, entry in cands:
        kind, match = classify(model_id, matches)
        if kind in ("exact", "suffix") and match is not None:
            row_entry.setdefault(match, (key, entry))
        else:
            skeleton_match = BENIGN_TAIL.sub("", model_id)
            missing.setdefault(skeleton_match, (model_id, entry))

    skeletons: dict[str, list[Row]] = {}
    for model_id, entry in missing.values():
        skeleton = build_skeleton(model_id, entry, source)
        if skeleton["provider"] == "unknown":
            continue  # re-sellers / vendors we do not track (fw-*, cohere, ai21, ...)
        skeletons.setdefault(str(skeleton["provider"]), []).append(skeleton)
    for rows_ in skeletons.values():
        rows_.sort(key=lambda s: str(s["match"]))

    drift: list[dict[str, Any]] = []
    skipped = 0
    retired_in_catalog: list[str] = []
    for match, row in by_match.items():
        if match not in row_entry:
            continue
        key, entry = row_entry[match]
        if row.get("status") == "retired":
            retired_in_catalog.append(match)
            skipped += 1
            continue
        if _active_period(row, today):
            skipped += 1
            continue
        diffs = compare_prices(row, entry, rel_tol, abs_tol)
        if diffs:
            drift.append({"match": match, "catalog_key": key, "diffs": diffs})

    preview = sorted(str(r["match"]) for r in rows if r.get("status") == "preview")

    stale = []
    for row in rows:
        if row.get("status") == "retired":
            continue
        is_stale, verified = _stale(row, today, stale_days)
        if is_stale:
            stale.append({"match": row["match"], "verified": verified})
    stale.sort(key=lambda s: (s["verified"] or "", str(s["match"])))

    return {
        "today": today.isoformat(),
        "catalog_source": source,
        "counts": {"rows": len(rows), "catalog_text_models": len(cands)},
        "missing": {p: skeletons[p] for p in sorted(skeletons)},
        "drift": sorted(drift, key=lambda d: d["match"]),
        "drift_skipped": skipped,
        "preview": preview,
        "retired_in_catalog": sorted(retired_in_catalog),
        "stale": {"count": len(stale), "oldest": stale[:10], "days": stale_days},
        "watchlist": watchlist(rates, catalog),
    }


def watchlist(rates: Row, catalog: dict[str, Entry]) -> list[dict[str, Any]]:
    """Watchlist entries (file + literals) and any catalogue models that now match them."""
    entries = {
        str(u["match"]).lower(): str(u.get("note", ""))
        for u in rates.get("unpriced_models") or []
        if isinstance(u, dict) and u.get("status") == "watchlist" and u.get("match")
    }
    for literal in WATCHLIST_LITERAL:
        entries.setdefault(literal, "built-in watchlist")
    out = []
    for match in sorted(entries):
        hits = []
        for key, entry in catalog.items():
            if entry.get("mode") not in TEXT_MODES:
                continue
            leaf = (normalise_key(key) or key.lower()).rsplit("/", 1)[-1]
            if leaf.startswith(match):
                hits.append(
                    {
                        "catalog_key": key,
                        "input": per_million(entry.get("input_cost_per_token")),
                        "output": per_million(entry.get("output_cost_per_token")),
                    }
                )
        hits.sort(key=lambda h: str(h["catalog_key"]))
        out.append({"match": match, "note": entries[match], "hit": bool(hits), "entries": hits})
    return out


def finding_count(report: dict[str, Any]) -> int:
    """Findings that count for --fail-on-findings: sections 1, 2 and 5."""
    missing = sum(len(v) for v in report["missing"].values())
    hits = sum(1 for w in report["watchlist"] if w["hit"])
    return missing + len(report["drift"]) + hits


def render_text(report: dict[str, Any]) -> str:
    """Human-readable report."""
    lines = [
        f"rates_diff  today={report['today']}  catalogue={report['catalog_source']}",
        f"our rows: {report['counts']['rows']}  catalogue text models: "
        f"{report['counts']['catalog_text_models']}",
        "",
        "== 1. Missing from our table ==",
    ]
    missing = report["missing"]
    if not missing:
        lines.append("none")
    for provider, skeletons in missing.items():
        lines.append(
            f"-- {provider} ({len(skeletons)}) -- proposals only: needs a vendor-page check"
        )
        for skeleton in skeletons:
            lines.append(json.dumps(skeleton, indent=2))
    lines += ["", "== 2. Price drift (USD per 1M tokens) =="]
    if not report["drift"]:
        lines.append("none")
    for item in report["drift"]:
        lines.append(f"{item['match']}  (catalogue: {item['catalog_key']})")
        for diff in item["diffs"]:
            lines.append(f"  {diff['field']}: ours {diff['ours']}  theirs {diff['theirs']}")
    lines.append(f"skipped (retired or active period): {report['drift_skipped']}")
    lines += ["", "== 3. Preview rows to re-check first =="]
    lines += [f"  {m}" for m in report["preview"]] or ["none"]
    lines += ["", "== 4. Retired / stale =="]
    lines += [f"retired but still in catalogue: {m}" for m in report["retired_in_catalog"]]
    stale = report["stale"]
    lines.append(f"unverified or older than {stale['days']} days: {stale['count']}")
    for item in stale["oldest"]:
        lines.append(f"  {item['match']}  verified={item['verified']}")
    lines += ["", "== 5. Watchlist =="]
    for watch in report["watchlist"]:
        if watch["hit"]:
            lines.append(f"WATCHLIST HIT {watch['match']}")
            for entry in watch["entries"]:
                lines.append(
                    f"  {entry['catalog_key']}  input {entry['input']}  output {entry['output']}"
                )
        else:
            lines.append(f"no hit: {watch['match']}")
    lines += ["", summary_line(report)]
    return "\n".join(lines)


def summary_line(report: dict[str, Any]) -> str:
    """One-line summary of counts."""
    missing = sum(len(v) for v in report["missing"].values())
    hits = sum(1 for w in report["watchlist"] if w["hit"])
    return (
        f"SUMMARY missing={missing} drift={len(report['drift'])} "
        f"preview={len(report['preview'])} retired_in_catalog={len(report['retired_in_catalog'])} "
        f"stale={report['stale']['count']} watchlist_hits={hits}"
    )


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    """CLI arguments."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else None)
    parser.add_argument("--rates", type=Path, default=DEFAULT_RATES, help="rates.json path")
    parser.add_argument("--catalog", default=CATALOG_URL, help="catalogue file path or URL")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--stale-days", type=int, default=30)
    parser.add_argument("--today", type=date.fromisoformat, default=None, help="YYYY-MM-DD")
    parser.add_argument("--fail-on-findings", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Entry point. Exit 0 always, 1 with --fail-on-findings and findings, 2 on load errors."""
    args = parse_args(argv)
    try:
        rates = load_rates(args.rates)
        catalog = load_catalog(args.catalog)
    except (CatalogError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    source = args.catalog if args.catalog.startswith(("http://", "https://")) else CATALOG_URL
    report = analyse(
        rates,
        catalog,
        today=args.today or date.today(),
        stale_days=args.stale_days,
        source=source,
    )
    report["summary"] = summary_line(report)
    report["findings"] = finding_count(report)
    if args.format == "json":
        print(json.dumps(report, indent=2))
    else:
        print(render_text(report))
    return 1 if args.fail_on_findings and report["findings"] else 0


if __name__ == "__main__":
    sys.exit(main())
