from __future__ import annotations
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata

def plot_1d(coordinate: np.ndarray, relative_energy: np.ndarray, output: str | Path,
            coordinate_label: str = "Scan coordinate", title: str | None = None) -> None:
    order = np.argsort(coordinate)
    fig, ax = plt.subplots(figsize=(7.2, 4.8), constrained_layout=True)
    ax.plot(coordinate[order], relative_energy[order], marker="o", linewidth=1.6)
    ax.set_xlabel(coordinate_label)
    ax.set_ylabel("Relative energy (kcal/mol)")
    if title:
        ax.set_title(title)
    ax.grid(True, alpha=0.25)
    fig.savefig(output, dpi=300)
    plt.close(fig)

def plot_2d(x: np.ndarray, y: np.ndarray, relative_energy: np.ndarray, output: str | Path,
            x_label: str = "Coordinate 1", y_label: str = "Coordinate 2", grid_size: int = 150) -> None:
    if len(np.unique(x)) < 2 or len(np.unique(y)) < 2:
        raise ValueError("A 2D contour requires at least two distinct x and y values.")
    xi = np.linspace(np.min(x), np.max(x), grid_size)
    yi = np.linspace(np.min(y), np.max(y), grid_size)
    X, Y = np.meshgrid(xi, yi)
    Z = griddata((x, y), relative_energy, (X, Y), method="linear")
    if np.all(np.isnan(Z)):
        raise ValueError("Could not interpolate the supplied 2D scan points.")
    fig, ax = plt.subplots(figsize=(7.2, 5.8), constrained_layout=True)
    contour = ax.contourf(X, Y, Z, levels=30, cmap="viridis")
    fig.colorbar(contour, ax=ax, label="Relative energy (kcal/mol)")
    ax.scatter(x, y, s=16, c="black", alpha=0.75, label="Input scan points")
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.legend(loc="best")
    fig.savefig(output, dpi=300)
    plt.close(fig)
