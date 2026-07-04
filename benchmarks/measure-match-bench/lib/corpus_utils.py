"""Shared corpus parsing for generator, gold backfill, and eval harness."""

from __future__ import annotations

import csv
import difflib
import io
import json
import re
from pathlib import Path

SCENARIO_TYPES = [
    "psu_wall_power_idle",
    "psu_wall_power_line_rate",
    "psu_internal_rail_12v",
    "psu_internal_rail_3v3",
    "psu_efficiency_20pct",
    "psu_efficiency_50pct",
    "psu_efficiency_80pct",
    "psu_transient_step",
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
    "env_altitude_sea",
    "env_altitude_3000ft",
    "env_humidity_low",
    "env_humidity_high",
    "env_chamber_profile_a",
    "env_chamber_profile_b",
]

_SCENARIOS_BY_LEN = sorted(SCENARIO_TYPES, key=len, reverse=True)


def load_catalog(corpus_dir: Path) -> tuple[dict[str, str], list[dict]]:
    """Return alias->canonical map and raw catalog entries."""
    path = corpus_dir / "catalog" / "products.json"
    entries = json.loads(path.read_text())
    alias_map: dict[str, str] = {}
    for row in entries:
        canonical = row["canonical_id"]
        alias_map[canonical.lower()] = canonical
        for alias in row.get("aliases", []):
            alias_map[alias.lower()] = canonical
    return alias_map, entries


def normalize_alias(alias: str, rules: dict | None = None) -> str:
    s = alias.strip()
    if rules:
        for prefix in rules.get("prefix_strip", []):
            if s.lower().startswith(prefix.lower()):
                s = s[len(prefix) :]
        for pair in rules.get("token_replace", []):
            s = s.replace(pair["from"], pair["to"])
        cn = rules.get("char_normalize", {})
        if cn.get("underscore_to_hyphen"):
            s = s.replace("_", "-")
        if cn.get("lowercase"):
            s = s.lower()
    else:
        s = s.replace("_", "-").lower()
        if s.startswith("proto_"):
            s = s[6:]
        s = s.replace("pn-", "sku-")
    return s


def resolve_canonical(alias: str, alias_map: dict[str, str], rules: dict | None = None) -> str | None:
    candidates = [alias, normalize_alias(alias, rules)]
    for cand in candidates:
        key = cand.lower()
        if key in alias_map:
            return alias_map[key]
    if rules and rules.get("fuzzy", {}).get("enabled", True):
        cutoff = rules.get("fuzzy", {}).get("cutoff", 0.82)
        keys = list(alias_map.keys())
        for cand in candidates:
            matches = difflib.get_close_matches(cand.lower(), keys, n=1, cutoff=cutoff)
            if matches:
                return alias_map[matches[0]]
    return None


def parse_filename(name: str) -> tuple[str | None, str | None, str]:
    stem = Path(name).stem
    ext = Path(name).suffix.lstrip(".").lower()
    for scenario in _SCENARIOS_BY_LEN:
        marker = f"_{scenario}_"
        idx = stem.find(marker)
        if idx > 0:
            return stem[:idx], scenario, ext
    return None, None, ext


def parse_measurement_file(path: Path) -> dict | None:
    ext = path.suffix.lstrip(".").lower()
    text = path.read_text(errors="replace")
    alias = scenario = None
    value = None

    if ext == "txt":
        for line in text.splitlines():
            if line.startswith("SCENARIO="):
                scenario = line.split("=", 1)[1].strip()
            elif line.startswith("ALIAS="):
                alias = line.split("=", 1)[1].strip()
            elif line.startswith("VALUE="):
                try:
                    value = float(line.split("=", 1)[1].strip())
                except ValueError:
                    value = None
    elif ext == "csv":
        m = re.search(r"^#\s*scenario=(\S+)", text, re.MULTILINE)
        if m:
            scenario = m.group(1)
        reader = csv.reader(io.StringIO(text))
        rows = [r for r in reader if r and not r[0].startswith("#")]
        for row in rows:
            if len(row) >= 2 and row[0].lower() == "product_alias":
                alias = row[1]
            if len(row) >= 2 and row[0] in SCENARIO_TYPES:
                scenario = row[0]
                try:
                    value = float(row[1])
                except ValueError:
                    value = None
    else:
        return None

    if alias is None or scenario is None:
        fa, fs, _ = parse_filename(path.name)
        alias = alias or fa
        scenario = scenario or fs

    if alias is None or scenario is None:
        return None

    return {
        "format": ext,
        "product_alias": alias,
        "scenario": scenario,
        "value": value,
        "source_file": path.name,
    }


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text().splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows
