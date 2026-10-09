# Source audit: Cu–DTBA S–H scan

## Source files located in the uploaded archive

The source archive contains the following files under
`Scan_2D_solv/1d_scan_points/Cu_DTBA-SH_bond/100_sp/`:

- `line_scatter.py`
- `scan_coordinate.txt`
- `scan_coordinate_no_outlier.txt`
- `energy_final_sp_point1.dat` through `energy_final_sp_point6.dat`
- `bond_break_scan_energy.txt`
- `bond_break_scan_energy_no_tail.txt`
- `mean_and_range.py`
- `convert_function.py`
- `1D_bond_break_scan_no_tail.png`

## Coordinate definition

The six x coordinates in `bond_break_scan_energy_no_tail.txt` are 2.20995,
2.40995, 2.60995, 2.80993, 3.00990, and 3.20995. The original plotting script
labels this coordinate as `Cu-DTBA SH distance (ang)`. The data file alone does
not specify atom indices or the geometric measurement procedure, so this package
does not infer those details.

## Original energy processing convention

The original `mean_and_range.py` transforms each total energy E in Hartree using

`E' = (E + 7579.0) * 627.5`

where 627.5 is the conversion factor used in the original script. It then
filters the transformed per-frame values to retain only `E' > -130`, computes
the mean for each scan point, and the no-tail scan table reports the mean
energy difference relative to point 1. This is an empirical outlier filter and
reference convention from the source scripts, not a universal recommended
procedure.

Recomputing the means from the six `energy_final_sp_point*.dat` files with that
filter, rounding each point mean to three decimals, and then subtracting the
rounded point-1 mean reproduces the six energies in
`bond_break_scan_energy_no_tail.txt` to the table's displayed precision
(0.000, 2.739, 3.626, 3.712, 1.659, 1.090 kcal/mol). This is a numerical data-lineage check against the archived table.
It is not a comparison to a fresh quantum-chemistry calculation.

## Gaussian parser scope

`gaussian.py` extracts the last `SCF Done:` energy, method label, and whether
the output contains `Normal termination of Gaussian`. By default, a file without
the normal-termination marker is rejected. The uploaded
`point1_50water_5-ns.log` is a Gaussian 16 single-point output using
B3LYP/6-311+G(d,p) and water PCM; its final SCF energy is -7579.16974079 Hartree.
That individual log is a parser-validation example, not evidence that it is the
specific source of all six averaged scan points.

## Limitations

- The 1D figure uses six processed scan points and connects them in coordinate
  order; no additional points are interpolated.
- The plotted values are relative potential energies derived from the original
  processed scan table, not free energies.
- The six-point table uses an explicitly documented legacy filter/reference
  convention. Other analyses should choose and report their reference and
  filtering rules deliberately.
- No raw log for every frame is included in the public example dataset, so
  independent re-extraction of all six distributions is not possible from this
  repository alone.
