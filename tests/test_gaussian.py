from pathlib import Path
import pytest
from metal_ligand_energy.gaussian import parse_gaussian_scf

def test_parse_last_energy_and_normal_termination(tmp_path: Path):
    p = tmp_path / "ok.log"
    p.write_text(
        "SCF Done:  E(RHF) = -10.00000000 A.U. after 5 cycles\n"
        "SCF Done:  E(RB3LYP) = -10.12500000 A.U. after 8 cycles\n"
        "Normal termination of Gaussian 16 at Fri Jan 1 00:00:00 2021.\n"
    )
    result = parse_gaussian_scf(p)
    assert result["method"] == "RB3LYP"
    assert result["energy_hartree"] == pytest.approx(-10.125)
    assert result["normal_termination"] is True

def test_missing_normal_termination_is_rejected(tmp_path: Path):
    p = tmp_path / "incomplete.log"
    p.write_text("SCF Done:  E(RB3LYP) = -10.12500000 A.U. after 8 cycles\n")
    with pytest.raises(ValueError, match="no normal-termination"):
        parse_gaussian_scf(p)

def test_missing_energy_is_rejected(tmp_path: Path):
    p = tmp_path / "bad.log"
    p.write_text("Normal termination of Gaussian 16\n")
    with pytest.raises(ValueError, match="No 'SCF Done:'"):
        parse_gaussian_scf(p)
