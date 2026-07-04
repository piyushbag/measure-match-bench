#!/usr/bin/env python3
"""Backfill t2_normalized.jsonl and t4_qa.jsonl from raw measurement files."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lib"))

from corpus_utils import load_catalog, parse_measurement_file, resolve_canonical  # noqa: E402


def backfill_corpus(corpus_dir: Path) -> None:
    alias_map, _ = load_catalog(corpus_dir)
    raw_dir = corpus_dir / "raw"
    gold_dir = corpus_dir / "gold"
    gold_dir.mkdir(parents=True, exist_ok=True)

    t2_rows = []
    t4_rows = []
    for path in sorted(raw_dir.iterdir()):
        if not path.is_file():
            continue
        rec = parse_measurement_file(path)
        if rec is None:
            continue
        canonical = resolve_canonical(rec["product_alias"], alias_map)
        t2_rows.append(
            {
                "source_file": f"raw/{path.name}",
                "format": rec["format"],
                "scenario": rec["scenario"],
                "product_alias": rec["product_alias"],
                "canonical_id": canonical,
                "value": rec["value"],
            }
        )
        if canonical and rec["value"] is not None:
            t4_rows.append(
                {
                    "question": (
                        f"What is the {rec['scenario']} measurement value for {canonical}?"
                    ),
                    "canonical_id": canonical,
                    "scenario": rec["scenario"],
                    "answer": rec["value"],
                    "gold_file": f"raw/{path.name}",
                }
            )

    def write_jsonl(name: str, rows: list[dict]) -> None:
        (gold_dir / name).write_text("".join(json.dumps(r) + "\n" for r in rows))

    write_jsonl("t2_normalized.jsonl", t2_rows)
    write_jsonl("t4_qa.jsonl", t4_rows)


def main() -> None:
    instances = ROOT / "instances"
    for corpus_dir in sorted(instances.iterdir()):
        if corpus_dir.is_dir() and (corpus_dir / "raw").exists():
            backfill_corpus(corpus_dir)
            print(f"backfilled {corpus_dir.name}")


if __name__ == "__main__":
    main()
