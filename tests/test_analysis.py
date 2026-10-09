import numpy as np
import pytest
from metal_ligand_energy.analysis import relative_energy_kcal, energy_summary

def test_relative_energy_kcal():
    result = relative_energy_kcal(np.array([-10.0, -9.99]), "hartree")
    assert result[0] == pytest.approx(0.0)
    assert result[1] == pytest.approx(6.27509474)

def test_unknown_unit():
    with pytest.raises(ValueError):
        relative_energy_kcal(np.array([1.0]), "eV")

def test_energy_summary():
    result = energy_summary(np.array([0.0, 2.0, 4.0]))
    assert result["n_points"] == 3
    assert result["maximum_relative_energy_kcal_mol"] == 4.0
