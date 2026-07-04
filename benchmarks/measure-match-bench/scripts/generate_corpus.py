#!/usr/bin/env python3
"""Generate synthetic MeasureMatch-Bench corpora (scaffold).

Target v1.0.0: 24 corpora, ~250 files each (~6000 total), 46 scenario types.
"""

from __future__ import annotations

import argparse
import json
import random
import string
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTANCES = ROOT / "instances"
SPLITS = ROOT / "splits"

SCENARIO_TYPES = [
    # PSU (8)
    "psu_wall_power_idle",
    "psu_wall_power_line_rate",
    "psu_internal_rail_12v",
    "psu_internal_rail_3v3",
    "psu_efficiency_20pct",
    "psu_efficiency_50pct",
    "psu_efficiency_80pct",
    "psu_transient_step",
    # Thermal (10)
    "thermal_inlet_delta",
    "thermal_outlet_delta",
    "thermal_hotspot_asic",
    "thermal_hotspot_psu",
    "thermal_ambient_25c",
    "thermal_ambient_35c",
    "thermal_ambient_45c",
    "thermal_soak_30min",
    "thermal_ramp_up",
    "thermal_ramp_down",
    # Fan (10)
    "fan_rpm_min",
    "fan_rpm_50pct",
    "fan_rpm_max",
    "fan_cfm_vs_pwm",
    "fan_acoustic_proxy",
    "fan_redundancy_failover",
    "fan_zone_front",
    "fan_zone_rear",
    "fan_stall_detection",
    "fan_power_draw",
    # Throughput (12)
    "throughput_line_rate_100g",
    "throughput_line_rate_400g",
    "throughput_packet_64b",
    "throughput_packet_1518b",
    "throughput_packet_imix",
    "throughput_buffer_occupancy",
    "throughput_latency_p99",
    "throughput_drop_rate",
    "throughput_warmup",
    "throughput_steady_state",
    "throughput_oversubscription",
    "throughput_power_correlation",
    # Environmental (6) — included in 46
    "env_altitude_sea",
    "env_altitude_3000ft",
    "env_humidity_low",
    "env_humidity_high",
    "env_chamber_profile_a",
    "env_chamber_profile_b",
]


def _rand_alias(canonical: str, rng: random.Random) -> str:
    mutations = [
        canonical.replace("-", "_"),
        canonical.upper(),
        canonical.lower(),
        f"proto_{canonical}",
        f"{canonical}_revB",
        canonical.replace("SKU", "PN"),
    ]
    return rng.choice(mutations)


def _write_csv(path: Path, scenario: str, product: str, value: float) -> None:
    path.write_text(
        f"# scenario={scenario}\nproduct_alias,{product}\nmetric,value\n{scenario},{value:.4f}\n"
    )


def generate_corpus(corpus_id: str, seed: int, files_per_corpus: int) -> None:
    rng = random.Random(seed)
    out = INSTANCES / corpus_id
    raw = out / "raw"
    gold = out / "gold"
    raw.mkdir(parents=True, exist_ok=True)
    gold.mkdir(parents=True, exist_ok=True)

    n_products = rng.randint(40, 80)
    products = [f"SKU-{corpus_id}-{i:04d}" for i in range(n_products)]
    catalog = []
    t1_rows = []
    t3_rows = []

    for p in products:
        aliases = list({_rand_alias(p, rng) for _ in range(rng.randint(2, 5))})
        catalog.append({"canonical_id": p, "aliases": aliases})
        for a in aliases:
            t1_rows.append({"alias": a, "canonical_id": p})

    for i in range(files_per_corpus):
        scenario = rng.choice(SCENARIO_TYPES)
        product = rng.choice(products)
        alias = _rand_alias(product, rng)
        fmt = rng.choice(["csv", "txt"])
        fname = f"{alias}_{scenario}_{i:04d}.{fmt}"
        fpath = raw / fname
        value = rng.uniform(10.0, 500.0)
        if fmt == "csv":
            _write_csv(fpath, scenario, alias, value)
        else:
            fpath.write_text(f"SCENARIO={scenario}\nALIAS={alias}\nVALUE={value:.4f}\n")
        t3_rows.append(
            {
                "query_product": product,
                "query_scenario": scenario,
                "gold_file": str(fpath.relative_to(out)),
                "gold_value": value,
            }
        )

    (out / "catalog" / "products.json").parent.mkdir(parents=True, exist_ok=True)
    (out / "catalog" / "products.json").write_text(json.dumps(catalog, indent=2) + "\n")

    def _jsonl(path: Path, rows: list[dict]) -> None:
        path.write_text("".join(json.dumps(r) + "\n" for r in rows))

    _jsonl(gold / "t1_identity.jsonl", t1_rows)
    _jsonl(gold / "t3_retrieval.jsonl", t3_rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpora", type=int, default=24)
    parser.add_argument("--files-per-corpus", type=int, default=250)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    SPLITS.mkdir(parents=True, exist_ok=True)
    all_ids = [f"corpus-{i:03d}" for i in range(1, args.corpora + 1)]
    dev_ids = all_ids[:4]
    test_ids = all_ids[4:]

    (SPLITS / "dev.txt").write_text("\n".join(dev_ids) + "\n")
    (SPLITS / "test.txt").write_text("\n".join(test_ids) + "\n")

    for idx, cid in enumerate(all_ids):
        generate_corpus(cid, args.seed + idx, args.files_per_corpus)
        print(f"Generated {cid}")

    print(f"Done: {args.corpora} corpora, {len(SCENARIO_TYPES)} scenario types")


if __name__ == "__main__":
    main()
