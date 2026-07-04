"""Metrics for MeasureMatch-Bench eval harness."""

from __future__ import annotations

from math import fsum


def accuracy(y_true: list[str], y_pred: list[str]) -> float:
    if not y_true:
        return 0.0
    hits = sum(1 for t, p in zip(y_true, y_pred) if t == p)
    return hits / len(y_true)


def retrieval_at_1(gold_files: list[str], pred_files: list[str]) -> float:
    if not gold_files:
        return 0.0
    hits = sum(1 for g, p in zip(gold_files, pred_files) if g == p)
    return hits / len(gold_files)


def value_score(gold_vals: list[float], pred_vals: list[float | None], tol: float = 0.05) -> float:
    if not gold_vals:
        return 0.0
    hits = 0
    for g, p in zip(gold_vals, pred_vals):
        if p is None:
            continue
        if abs(g - p) <= tol or abs(g - p) / max(abs(g), 1e-9) <= 0.001:
            hits += 1
    return hits / len(gold_vals)


def record_match_rate(gold_rows: list[dict], pred_rows: list[dict]) -> float:
    if not gold_rows:
        return 0.0
    hits = 0
    for g, p in zip(gold_rows, pred_rows):
        if (
            g.get("format") == p.get("format")
            and g.get("scenario") == p.get("scenario")
            and g.get("canonical_id") == p.get("canonical_id")
            and value_score([g.get("value") or 0.0], [p.get("value")], tol=0.05) == 1.0
        ):
            hits += 1
    return hits / len(gold_rows)


def aggregate_mean(rows: list[dict], field: str) -> float | None:
    vals = [r[field] for r in rows if r.get(field) is not None]
    return round(fsum(vals) / len(vals), 4) if vals else None
