from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]

def test_real_processed_scan_example_has_expected_points():
    path = ROOT / "examples" / "cu_dtba_sh_bond_scan.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 6
    x = [float(row["cu_dtba_sh_distance_angstrom"]) for row in rows]
    y = [float(row["relative_energy_kcal_mol"]) for row in rows]
    assert x == [2.20995, 2.40995, 2.60995, 2.80993, 3.00990, 3.20995]
    assert y == [0.0, 2.739, 3.626, 3.712, 1.659, 1.09]
