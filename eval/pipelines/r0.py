"""R0: rules + fuzzy alias match + content/filename parsing."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

BENCH = Path(__file__).resolve().parents[2] / "benchmarks" / "measure-match-bench"
INSTANCES_ROOT = BENCH / "instances"
sys.path.insert(0, str(BENCH / "lib"))

from corpus_utils import (  # noqa: E402
    load_catalog,
    load_jsonl,
    parse_measurement_file,
    resolve_canonical,
)


def _load_rules() -> dict:
    path = BENCH / "rules" / "alias_patterns.yaml"
    return yaml.safe_load(path.read_text())


def run_t1(corpus_dir: Path, rules: dict) -> list[str]:
    alias_map, _ = load_catalog(corpus_dir)
    gold = load_jsonl(corpus_dir / "gold" / "t1_identity.jsonl")
    preds = []
    for row in gold:
        pred = resolve_canonical(row["alias"], alias_map, rules)
        preds.append(pred or "")
    return preds


def run_t2(corpus_dir: Path, rules: dict) -> dict[str, dict]:
    alias_map, _ = load_catalog(corpus_dir)
    by_src: dict[str, dict] = {}
    for path in sorted((corpus_dir / "raw").iterdir()):
        if not path.is_file():
            continue
        rec = parse_measurement_file(path)
        if rec is None:
            continue
        by_src[f"raw/{path.name}"] = {
            "source_file": f"raw/{path.name}",
            "format": rec["format"],
            "scenario": rec["scenario"],
            "product_alias": rec["product_alias"],
            "canonical_id": resolve_canonical(rec["product_alias"], alias_map, rules),
            "value": rec["value"],
        }
    return by_src


def _index_raw(corpus_dir: Path, rules: dict) -> list[dict]:
    alias_map, _ = load_catalog(corpus_dir)
    indexed = []
    for path in sorted((corpus_dir / "raw").iterdir()):
        if not path.is_file():
            continue
        rec = parse_measurement_file(path)
        if rec is None:
            continue
        canonical = resolve_canonical(rec["product_alias"], alias_map, rules)
        indexed.append(
            {
                "rel_path": f"raw/{path.name}",
                "canonical_id": canonical,
                "scenario": rec["scenario"],
                "value": rec["value"],
            }
        )
    return indexed


def run_t3(corpus_dir: Path, rules: dict) -> tuple[list[str], list[float | None]]:
    gold = load_jsonl(corpus_dir / "gold" / "t3_retrieval.jsonl")
    index = _index_raw(corpus_dir, rules)
    pred_files: list[str] = []
    pred_vals: list[float | None] = []
    for row in gold:
        match = next(
            (
                item
                for item in index
                if item["canonical_id"] == row["query_product"]
                and item["scenario"] == row["query_scenario"]
            ),
            None,
        )
        pred_files.append(match["rel_path"] if match else "")
        pred_vals.append(match["value"] if match else None)
    return pred_files, pred_vals


def run_t4(corpus_dir: Path, rules: dict) -> list[float | None]:
    gold = load_jsonl(corpus_dir / "gold" / "t4_qa.jsonl")
    index = _index_raw(corpus_dir, rules)
    preds: list[float | None] = []
    for row in gold:
        match = next(
            (
                item
                for item in index
                if item["canonical_id"] == row["canonical_id"]
                and item["scenario"] == row["scenario"]
            ),
            None,
        )
        preds.append(match["value"] if match else None)
    return preds


def evaluate_corpus(corpus_id: str) -> dict:
    rules = _load_rules()
    corpus_dir = INSTANCES_ROOT / corpus_id

    gold_t1 = load_jsonl(corpus_dir / "gold" / "t1_identity.jsonl")
    pred_t1 = run_t1(corpus_dir, rules)
    y_true_t1 = [r["canonical_id"] for r in gold_t1]

    gold_t2 = load_jsonl(corpus_dir / "gold" / "t2_normalized.jsonl")
    pred_t2_map = run_t2(corpus_dir, rules)
    pred_t2_aligned = [pred_t2_map.get(g["source_file"], {}) for g in gold_t2]

    gold_t3 = load_jsonl(corpus_dir / "gold" / "t3_retrieval.jsonl")
    pred_files_t3, pred_vals_t3 = run_t3(corpus_dir, rules)
    gold_files_t3 = [r["gold_file"] for r in gold_t3]
    gold_vals_t3 = [float(r["gold_value"]) for r in gold_t3]

    gold_t4 = load_jsonl(corpus_dir / "gold" / "t4_qa.jsonl")
    pred_t4 = run_t4(corpus_dir, rules)
    gold_vals_t4 = [float(r["answer"]) for r in gold_t4]

    from metrics import accuracy, record_match_rate, retrieval_at_1, value_score  # noqa: E402

    return {
        "corpus_id": corpus_id,
        "t1_accuracy": round(accuracy(y_true_t1, pred_t1), 4),
        "t2_record_match": round(record_match_rate(gold_t2, pred_t2_aligned), 4)
        if gold_t2
        else None,
        "t3_retrieval_at_1": round(retrieval_at_1(gold_files_t3, pred_files_t3), 4),
        "t3_value_score": round(value_score(gold_vals_t3, pred_vals_t3), 4),
        "t4_value_score": round(value_score(gold_vals_t4, pred_t4), 4) if gold_t4 else None,
        "counts": {
            "t1": len(gold_t1),
            "t2": len(gold_t2),
            "t3": len(gold_t3),
            "t4": len(gold_t4),
        },
    }
