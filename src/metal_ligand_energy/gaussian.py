from __future__ import annotations
import argparse
import csv
import re
from pathlib import Path

_SCF_RE = re.compile(
    r"SCF Done:\s+E\((?P<method>[^)]+)\)\s*=\s*"
    r"(?P<energy>[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[DdEe][+-]\d+)?)\s+A\.U\."
)

def parse_gaussian_scf(path: str | Path, require_normal_termination: bool = True) -> dict[str, object]:
    """Return the last Gaussian SCF energy in Hartree.

    If required, a log must contain Gaussian's normal-termination marker.
    Multiple SCF lines are allowed; the last one is returned. Missing energies
    and abnormal/incomplete jobs raise ValueError rather than silently passing.
    """
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Gaussian output not found: {path}")
    last = None
    normal = False
    with path.open("r", errors="replace", encoding="utf-8") as handle:
        for line in handle:
            match = _SCF_RE.search(line)
            if match:
                last = match
            if "Normal termination of Gaussian" in line:
                normal = True
    if last is None:
        raise ValueError(f"No 'SCF Done:' energy found in {path}")
    if require_normal_termination and not normal:
        raise ValueError(f"Gaussian output has an SCF energy but no normal-termination marker: {path}")
    value = last.group("energy").replace("D", "E").replace("d", "e")
    return {
        "file": path.name,
        "method": last.group("method"),
        "energy_hartree": float(value),
        "normal_termination": normal,
    }

def main() -> None:
    parser = argparse.ArgumentParser(description="Extract the last SCF Done energy from Gaussian log files.")
    parser.add_argument("logs", nargs="+", help="Gaussian .log/.out files; glob patterns are expanded by the shell.")
    parser.add_argument("--allow-incomplete", action="store_true",
                        help="Allow logs without Gaussian normal termination (not recommended for validated data).")
    parser.add_argument("--output", default="gaussian_scf_energies.csv", help="Output CSV path.")
    args = parser.parse_args()
    rows, errors = [], []
    for name in args.logs:
        try:
            rows.append(parse_gaussian_scf(name, require_normal_termination=not args.allow_incomplete))
        except (OSError, ValueError) as exc:
            errors.append((name, str(exc)))
    with Path(args.output).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["file", "method", "energy_hartree", "normal_termination"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} energy record(s) to {Path(args.output).resolve()}")
    if errors:
        for name, message in errors:
            print(f"ERROR {name}: {message}")
        raise SystemExit(2)

if __name__ == "__main__":
    main()
