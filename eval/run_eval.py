#!/usr/bin/env python3
"""MeasureMatch-Bench evaluation harness (scaffold v0.0.1)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "benchmarks" / "measure-match-bench"
RESULTS = Path(__file__).resolve().parent / "results"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run MeasureMatch-Bench eval")
    parser.add_argument("--split", choices=["dev", "test"], default="dev")
    parser.add_argument("--pipeline", choices=["R0", "R1", "R2", "R3"], default="R0")
    parser.add_argument("--version", default="0.0.1")
    args = parser.parse_args()

    split_file = BENCH / "splits" / f"{args.split}.txt"
    if not split_file.exists():
        print(f"Split file missing: {split_file}", file=sys.stderr)
        print("Next: run benchmarks/measure-match-bench/scripts/generate_corpus.py", file=sys.stderr)
        return 1

    RESULTS.mkdir(parents=True, exist_ok=True)
    out = {
        "benchmark": "measure-match-bench",
        "harness_version": args.version,
        "split": args.split,
        "pipeline": args.pipeline,
        "status": "scaffold",
        "tasks": {
            "T1_identity": None,
            "T2_normalize": None,
            "T3_retrieval": None,
            "T4_qa": None,
        },
    }
    out_path = RESULTS / f"{args.split}-{args.pipeline}-v{args.version}.json"
    out_path.write_text(json.dumps(out, indent=2) + "\n")
    print(f"Wrote scaffold result: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
