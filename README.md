# Metal–Ligand Energy Analysis

A small Python toolkit for plotting 1D/2D metal–ligand energy scans and extracting
final SCF energies from Gaussian output files.

## What is validated here?

The repository includes a real six-point Cu–DTBA S–H scan table located in the
uploaded source archive. The included figure is regenerated from the processed
table, and `docs/SOURCE_AUDIT.md` documents how that table relates to the original
per-point energy files and legacy reference convention.

This is a **processed-data reproduction**, not a claim that all original Gaussian
logs have been independently reprocessed. The separate Gaussian parser is
validated with test fixtures and can be run on Gaussian `.log`/`.out` files.

## Features

- Load CSV data for 1D and 2D scans.
- Convert Hartree, kJ/mol, or kcal/mol energies to relative kcal/mol.
- Plot 1D energy profiles and 2D interpolated contour visualizations.
- Parse the last `SCF Done:` energy from Gaussian output.
- Reject Gaussian logs lacking normal termination by default.
- Save CSV and JSON summaries from scan analyses.

## Installation

Python 3.9 or later is required.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

If your network proxy prevents build-isolation downloads, first verify that
`setuptools`, `wheel`, NumPy, Matplotlib, SciPy, and pytest are already installed
in the active environment. If they are, `python -m pip install --no-build-isolation
-e ".[dev]"` may avoid the build-dependency download; it does not solve a missing
dependency or a proxy-authentication problem.

## Example: reproduce the Cu–DTBA scan figure

The CSV stores the six original coordinates and processed relative energies.

```bash
metal-energy-scan 1d examples/cu_dtba_sh_bond_scan.csv   --energy-unit kcal/mol   --coordinate-label "Cu–DTBA S–H distance (Å)"   --output-dir results/cu_dtba
```

The command writes `energy_profile.png`, `relative_energies.csv`, and
`summary.json`. The committed version of the example figure is
`figures/cu_dtba_sh_bond_scan.png`.

## Example: parse Gaussian energies

```bash
gaussian-scf-energies point1/*.log --output point1_energies.csv
```

The parser selects the last `SCF Done:` line in each log and requires a
`Normal termination of Gaussian` marker. If the job is incomplete, the parser
reports an error instead of silently treating the last available energy as a
valid result. `--allow-incomplete` is available for diagnostic use only.

For a single log, the parser returns the method label and energy in Hartree.
It does not determine scan coordinates, convert energy differences to free
energies, or decide whether different calculations are comparable.

## Input formats

1D CSV:

```csv
coordinate,energy
2.20,-100.123
2.30,-100.120
2.40,-100.115
```

2D CSV:

```csv
x,y,energy
2.20,2.10,-100.123
2.30,2.10,-100.120
2.20,2.20,-100.121
```

The energy unit must be supplied explicitly. Coordinates are preserved as given;
include physical meaning and units in labels.

## Scientific cautions

- Keep electronic-structure method, basis set, charge, multiplicity, solvent
  model, and energy convention consistent across scan points.
- A potential-energy scan is not a free-energy surface.
- The 2D contour is an interpolation for visualization; it does not establish a
  reaction path.
- The legacy Cu–DTBA table uses the filter and reference convention documented
  in `docs/SOURCE_AUDIT.md`. Do not generalize that filtering rule to other data.
- The parser checks Gaussian's normal-termination marker but does not validate
  the chemistry, SCF stability, or physical adequacy of the calculation.

## Repository contents

- `src/metal_ligand_energy/`: reusable analysis, plotting, CLI, and Gaussian parser.
- `examples/cu_dtba_sh_bond_scan.csv`: processed scan data from the source archive.
- `figures/cu_dtba_sh_bond_scan.png`: reproducible example figure.
- `docs/SOURCE_AUDIT.md`: data-lineage and convention audit.
- `tests/`: unit tests for energy analysis and Gaussian parsing.

## License

No license is assigned. Choose a license only after confirming the redistribution
rights for all code and data included in the repository.
