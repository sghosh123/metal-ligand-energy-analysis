from __future__ import annotations
import argparse, csv, json
from pathlib import Path
import numpy as np
from .analysis import ENERGY_TO_KCAL_MOL, energy_summary, load_scan, relative_energy_kcal
from .plotting import plot_1d, plot_2d

def _write_outputs(data: np.ndarray, dimensions: int, energy_unit: str, output_dir: Path, labels: list[str]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    coordinates = data[:, :dimensions]
    relative = relative_energy_kcal(data[:, dimensions], energy_unit)
    with (output_dir / "relative_energies.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([*labels, "relative_energy_kcal_mol"])
        writer.writerows([*coords.tolist(), float(en)] for coords, en in zip(coordinates, relative))
    if dimensions == 1:
        plot_1d(coordinates[:, 0], relative, output_dir / "energy_profile.png", labels[0])
    else:
        plot_2d(coordinates[:, 0], coordinates[:, 1], relative, output_dir / "energy_contour.png", labels[0], labels[1])
    summary = energy_summary(relative)
    summary.update({
        "input_energy_unit": energy_unit,
        "relative_energy_unit": "kcal/mol",
        "conversion_factor_to_kcal_mol": ENERGY_TO_KCAL_MOL[energy_unit.lower()],
        "energy_reference": "minimum input energy",
        "input_points": int(data.shape[0]),
    })
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="metal-energy-scan", description="Analyze 1D or 2D metal-ligand scan tables.")
    subparsers = parser.add_subparsers(dest="dimension", required=True)
    for dimension in ("1d", "2d"):
        sub = subparsers.add_parser(dimension, help=f"Analyze a {dimension.upper()} scan.")
        sub.add_argument("input", help="CSV input with a header row.")
        sub.add_argument("--energy-unit", required=True, choices=["hartree", "kcal/mol", "kj/mol"])
        sub.add_argument("--output-dir", default="results", help="Output directory (default: results).")
        if dimension == "1d":
            sub.add_argument("--coordinate-label", default="Scan coordinate")
        else:
            sub.add_argument("--x-label", default="Coordinate 1")
            sub.add_argument("--y-label", default="Coordinate 2")
    return parser

def main() -> None:
    args = build_parser().parse_args()
    dimensions = 1 if args.dimension == "1d" else 2
    data = load_scan(args.input, dimensions)
    labels = [args.coordinate_label] if dimensions == 1 else [args.x_label, args.y_label]
    _write_outputs(data, dimensions, args.energy_unit, Path(args.output_dir), labels)
    print(f"Analysis complete. Results written to: {Path(args.output_dir).resolve()}")

if __name__ == "__main__":
    main()
