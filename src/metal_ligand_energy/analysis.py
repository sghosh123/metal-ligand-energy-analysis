from __future__ import annotations
from pathlib import Path
from typing import Literal
import numpy as np

ENERGY_TO_KCAL_MOL = {
    "hartree": 627.509474,
    "kcal/mol": 1.0,
    "kj/mol": 1.0 / 4.184,
}

def load_scan(path: str | Path, dimensions: Literal[1, 2]) -> np.ndarray:
    """Load a CSV with a header and 2 columns (1D) or 3 columns (2D)."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Input file not found: {path}")
    expected_cols = dimensions + 1
    try:
        data = np.genfromtxt(path, delimiter=",", names=True, dtype=float, encoding=None)
    except Exception as exc:
        raise ValueError(f"Could not parse CSV input {path}: {exc}") from exc
    if data.dtype.names is None or len(data.dtype.names) != expected_cols:
        raise ValueError(f"Expected a header and {expected_cols} comma-separated columns for a {dimensions}D scan.")
    values = np.column_stack([np.atleast_1d(data[name]) for name in data.dtype.names])
    if values.ndim != 2 or values.shape[1] != expected_cols or values.shape[0] < 2:
        raise ValueError(f"Expected at least two data rows and {expected_cols} columns.")
    if not np.isfinite(values).all():
        raise ValueError("Input contains missing or non-finite values.")
    return values

def relative_energy_kcal(energy: np.ndarray, energy_unit: str) -> np.ndarray:
    """Convert energies to relative kcal/mol, referenced to the minimum value."""
    unit = energy_unit.lower().strip()
    if unit not in ENERGY_TO_KCAL_MOL:
        raise ValueError(f"Unsupported energy unit {energy_unit!r}; choose one of {', '.join(ENERGY_TO_KCAL_MOL)}.")
    energy = np.asarray(energy, dtype=float)
    if energy.size < 1 or not np.isfinite(energy).all():
        raise ValueError("Energy array must contain finite values.")
    converted = energy * ENERGY_TO_KCAL_MOL[unit]
    return converted - np.min(converted)

def energy_summary(relative_energy: np.ndarray) -> dict[str, float]:
    values = np.asarray(relative_energy, dtype=float)
    if values.size == 0 or not np.isfinite(values).all():
        raise ValueError("Energy array must contain finite values.")
    return {
        "n_points": int(values.size),
        "minimum_relative_energy_kcal_mol": float(np.min(values)),
        "maximum_relative_energy_kcal_mol": float(np.max(values)),
        "mean_relative_energy_kcal_mol": float(np.mean(values)),
        "std_relative_energy_kcal_mol": float(np.std(values)),
    }
