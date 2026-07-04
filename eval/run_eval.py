#!/usr/bin/env python3
"""MeasureMatch-Bench evaluation harness (v0.1.0)."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "benchmarks" / "measure-match-bench"
RESULTS = Path(__file__).resolve().parent / "results"
EVAL_DIR = Path(__file__).resolve().parent

sys.path.insert(0, str(EVAL_DIR))
sys.path.insert(0, str(BENCH / "lib"))

from metrics import aggregate_mean  # noqa: E402
from pipelines import PIPELINES  # noqa: E402

HARNESS_VERSION = "0.1.0"


def load_split(name: str) -> list[str]:
    path = BENCH / "splits" / f"{name}.txt"
    return [line.strip() for line in path.read_text().splitlines() if line.strip()]


def aggregate(rows: list[dict]) -> dict:
    return {
        "corpora": len(rows),
        "t1_accuracy": aggregate_mean(rows, "t1_accuracy"),
        "t2_record_match": aggregate_mean(rows, "t2_record_match"),
        "t3_retrieval_at_1": aggregate_mean(rows, "t3_retrieval_at_1"),
        "t3_value_score": aggregate_mean(rows, "t3_value_score"),
        "t4_value_score": aggregate_mean(rows, "t4_value_score"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run MeasureMatch-Bench eval")
    parser.add_argument("--split", choices=["dev", "test"], default="dev")
    parser.add_argument("--pipeline", choices=sorted(PIPELINES.keys()), default="R0")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    split_file = BENCH / "splits" / f"{args.split}.txt"
    if not split_file.exists():
        print(f"Split file missing: {split_file}", file=sys.stderr)
        return 1

    fn = PIPELINES[args.pipeline]
    corpus_ids = load_split(args.split)
    per_corpus = [fn(cid) for cid in corpus_ids]

    summary = {
        "benchmark": "measure-match-bench",
        "harness_version": HARNESS_VERSION,
        "split": args.split,
        "pipeline": args.pipeline,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "aggregate": aggregate(per_corpus),
        "corpora": per_corpus,
    }

    out = args.output
    if out is None:
        RESULTS.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        out = RESULTS / f"{args.split}-{args.pipeline}-{stamp}.json"
    out.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary["aggregate"], indent=2))
    print(f"wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
