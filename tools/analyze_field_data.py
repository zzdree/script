#!/usr/bin/env python3
"""
analyze_field_data.py - Olah CSV pengukuran lapangan (41 kolom) menjadi
statistik deskriptif siap salin ke tabel Bab 4.

Skema CSV mengikuti markdowns/script_test_protocols.md bagian 2.4.
Satu baris = satu paket/transisi terpilih dalam satu sesi.

Kolom yang dibaca:
    run_id, trial_id, scenario, tx_to_light_ms, ui_to_light_ms,
    run_tx_count, run_rx_unique_count, run_loss_count, run_loss_rate_pct,
    rx_valid

Aturan kejujuran:
- Baris dengan nilai 'NA' pada kolom numerik dikeluarkan dari statistik dan
  dihitung sebagai tidak terukur, bukan nol.
- Jika kolom inti kosong seluruhnya, skrip melaporkan "tidak terukur" alih-alih
  mencetak angka yang menyesatkan.

Penggunaan:
    python3 tools/analyze_field_data.py path/ke/measurement.csv
    python3 tools/analyze_field_data.py path/ke/measurement.csv --json
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

NUMERIC_COLUMNS = (
    "tx_to_light_ms",
    "ui_to_light_ms",
    "run_tx_count",
    "run_rx_unique_count",
    "run_loss_count",
    "run_loss_rate_pct",
)

NA_TOKENS = {"", "na", "n/a", "none", "null", "-"}


def parse_number(raw: Optional[str]) -> Optional[float]:
    """Return a float, or None when the cell is empty/NA/non-numeric."""
    if raw is None:
        return None
    token = str(raw).strip()
    if token.lower() in NA_TOKENS:
        return None
    try:
        return float(token)
    except ValueError:
        return None


def describe(values: List[float]) -> Dict[str, Any]:
    """Descriptive statistics for a non-empty list."""
    return {
        "n": len(values),
        "mean": round(statistics.fmean(values), 4),
        "stdev": round(statistics.stdev(values), 4) if len(values) > 1 else None,
        "min": round(min(values), 4),
        "max": round(max(values), 4),
    }


def load_rows(csv_path: Path) -> List[Dict[str, str]]:
    with csv_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("CSV tidak memiliki baris header")
        return [dict(row) for row in reader]


def summarise(rows: List[Dict[str, str]]) -> Dict[str, Any]:
    result: Dict[str, Any] = {
        "total_rows": len(rows),
        "runs": sorted({row.get("run_id", "") for row in rows if row.get("run_id")}),
        "latency": {},
        "packet_loss": {},
        "unmeasurable": {},
    }

    for column in ("tx_to_light_ms", "ui_to_light_ms"):
        present = [v for v in (parse_number(r.get(column)) for r in rows) if v is not None]
        missing = len(rows) - len(present)
        if present:
            result["latency"][column] = describe(present)
            result["latency"][column]["unmeasurable_rows"] = missing
        else:
            result["latency"][column] = {"status": "tidak terukur", "unmeasurable_rows": missing}

    # Packet loss is summarised per run window using the run_* aggregate columns.
    per_run: Dict[str, Dict[str, Optional[float]]] = {}
    for row in rows:
        run = row.get("run_id", "")
        if not run:
            continue
        bucket = per_run.setdefault(run, {})
        for column in ("run_tx_count", "run_rx_unique_count", "run_loss_count", "run_loss_rate_pct"):
            value = parse_number(row.get(column))
            if value is not None:
                bucket[column] = value

    if per_run:
        result["packet_loss"]["per_run"] = per_run
        rates = [b["run_loss_rate_pct"] for b in per_run.values() if b.get("run_loss_rate_pct") is not None]
        if rates:
            result["packet_loss"]["overall"] = describe(rates)
        else:
            result["packet_loss"]["overall"] = {"status": "tidak terukur"}
    else:
        result["packet_loss"]["overall"] = {"status": "tidak terukur"}

    rx_valid_values = [str(r.get("rx_valid", "")).strip() for r in rows]
    result["unmeasurable"]["rx_valid_blank"] = sum(1 for v in rx_valid_values if v.lower() in NA_TOKENS)

    return result


def render_markdown(summary: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append("## Ringkasan Data Lapangan (siap salin ke Bab 4)\n")
    lines.append(f"Total baris CSV: {summary['total_rows']}")
    lines.append(f"Sesi (run_id): {', '.join(summary['runs']) if summary['runs'] else 'tidak ada'}\n")

    lines.append("### Tabel 4.13 - Statistik Deskriptif Latensi (ms)\n")
    lines.append("| Metrik | n valid | Tidak terukur | Rata-rata | Simpangan baku | Min | Maks |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for column, label in (("tx_to_light_ms", "tx_to_light (TX ke cahaya)"),
                          ("ui_to_light_ms", "ui_to_light (UI ke cahaya)")):
        entry = summary["latency"].get(column, {})
        if entry.get("status") == "tidak terukur" or not entry.get("n"):
            lines.append(f"| {label} | 0 | {entry.get('unmeasurable_rows', 0)} | tidak terukur | - | - | - |")
        else:
            stdev = entry["stdev"] if entry["stdev"] is not None else "-"
            lines.append(
                f"| {label} | {entry['n']} | {entry['unmeasurable_rows']} | "
                f"{entry['mean']} | {stdev} | {entry['min']} | {entry['max']} |"
            )

    lines.append("\n### Tabel 4.14 - Rekapitulasi Packet Loss\n")
    per_run = summary["packet_loss"].get("per_run")
    if not per_run:
        lines.append("Packet loss: **tidak terukur** (kolom run_* tidak terisi).\n")
    else:
        lines.append("| Sesi | Paket terkirim | Paket valid diterima | Hilang | Loss (%) |")
        lines.append("|---|---:|---:|---:|---:|")
        for run, bucket in per_run.items():
            lines.append(
                f"| {run} | {bucket.get('run_tx_count', '-')} | "
                f"{bucket.get('run_rx_unique_count', '-')} | "
                f"{bucket.get('run_loss_count', '-')} | "
                f"{bucket.get('run_loss_rate_pct', '-')} |"
            )
        overall = summary["packet_loss"].get("overall", {})
        if overall.get("n"):
            lines.append(
                f"\nRata-rata loss lintas sesi: {overall['mean']}% "
                f"(n={overall['n']}, min {overall['min']}%, maks {overall['max']}%)"
            )

    lines.append("\n### Catatan Kejujuran\n")
    lines.append(
        "Sel yang bernilai 'NA' atau kosong dihitung sebagai **tidak terukur**, "
        "bukan nol. Jangan mengisi tabel Bab 4 dengan angka dari baris yang "
        "titik ukurnya belum tervalidasi.\n"
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Olah CSV pengukuran lapangan menjadi statistik Bab 4.")
    parser.add_argument("csv_path", type=Path, help="Berkas CSV 41 kolom hasil pengukuran lapangan")
    parser.add_argument("--json", action="store_true", help="Keluarkan ringkasan dalam bentuk JSON")
    args = parser.parse_args()

    if not args.csv_path.is_file():
        print(f"Berkas tidak ditemukan: {args.csv_path}", file=sys.stderr)
        return 1

    rows = load_rows(args.csv_path)
    summary = summarise(rows)

    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print(render_markdown(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
