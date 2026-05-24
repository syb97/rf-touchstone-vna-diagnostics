#!/usr/bin/env python3
"""Starter implementation for the RF Touchstone diagnostics task."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


UNIT_SCALE = {
    "HZ": 1.0,
    "KHZ": 1e3,
    "MHZ": 1e6,
    "GHZ": 1e9,
}


def _parse_header(path: Path) -> dict:
    suffix = path.suffix.lower()
    n_ports = int(suffix[2:-1])
    unit = "HZ"
    data_format = "MA"
    reference_ohm = 50.0
    freqs = []
    pending = []
    expected_values = 1 + 2 * n_ports * n_ports

    for raw_line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("!"):
            continue
        if "!" in line:
            line = line.split("!", 1)[0].strip()
        if not line:
            continue
        if line.startswith("#"):
            parts = line[1:].upper().split()
            if len(parts) >= 3:
                unit, data_format = parts[0], parts[2]
            if "R" in parts:
                idx = parts.index("R")
                if idx + 1 < len(parts):
                    reference_ohm = float(parts[idx + 1])
            continue
        try:
            pending.extend(float(x) for x in line.split())
        except ValueError:
            continue
        while len(pending) >= expected_values:
            row = pending[:expected_values]
            pending = pending[expected_values:]
            freqs.append(row[0] * UNIT_SCALE.get(unit, 1.0))

    return {
        "n_ports": n_ports,
        "n_points": len(freqs),
        "frequency_unit": unit,
        "data_format": data_format,
        "reference_ohm": reference_ohm,
        "freq_start_hz": freqs[0] if freqs else None,
        "freq_stop_hz": freqs[-1] if freqs else None,
        "monotonic_frequency": all(b > a for a, b in zip(freqs, freqs[1:])),
    }


def build_report(input_dir: str | Path) -> dict:
    root = Path(input_dir)
    files = sorted(
        p for p in root.iterdir()
        if p.is_file() and p.suffix.lower().startswith(".s") and p.suffix.lower().endswith("p")
    )
    return {
        "schema_version": "rfdiag.v1",
        "files": {path.name: _parse_header(path) for path in files},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    report = build_report(args.input_dir)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
