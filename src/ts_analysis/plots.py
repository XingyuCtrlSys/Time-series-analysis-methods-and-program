from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from .analysis import q_gaussian_pdf
from .io import POLLUTANT_COLUMNS, TIMESTAMP_COLUMN

LABELS = {
    "CO_mg_m3": "CO (mg/m³)",
    "NO2_ug_m3": "NO₂ (µg/m³)",
    "O3_ug_m3": "O₃ (µg/m³)",
    "SO2_ug_m3": "SO₂ (µg/m³)",
}


def _save(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def plot_overview(frame: pd.DataFrame, path: Path) -> None:
    fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
    for axis, column in zip(axes, POLLUTANT_COLUMNS):
        axis.plot(frame[TIMESTAMP_COLUMN], frame[column], linewidth=0.7)
        axis.set_ylabel(LABELS[column])
        axis.grid(alpha=0.25)
    axes[-1].set_xlabel("Time (UTC)")
    fig.suptitle("Air-quality time series")
    _save(fig, path)


def plot_week(frame: pd.DataFrame, start: str, path: Path) -> None:
    start_time = pd.Timestamp(start, tz="UTC")
    end_time = start_time + pd.Timedelta(days=7)
    week = frame[(frame[TIMESTAMP_COLUMN] >= start_time) & (frame[TIMESTAMP_COLUMN] < end_time)]
    if week.empty:
        raise ValueError(f"No observations were found in the requested week starting {start}.")
    fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True)
    for axis, column in zip(axes.flat, POLLUTANT_COLUMNS):
        axis.plot(week[TIMESTAMP_COLUMN], week[column], linewidth=1.1)
        axis.set_title(LABELS[column])
        axis.grid(alpha=0.25)
        axis.tick_params(axis="x", rotation=35)
    fig.suptitle(f"Seven-day detail from {start_time.date()}")
    _save(fig, path)


def plot_correlation(correlation: pd.DataFrame, path: Path) -> None:
    fig, axis = plt.subplots(figsize=(7, 6))
    image = axis.imshow(correlation.values, vmin=-1, vmax=1, cmap="coolwarm")
    short_labels = [LABELS.get(column, column) for column in correlation.columns]
    axis.set_xticks(range(len(correlation.columns)), short_labels, rotation=35, ha="right")
    axis.set_yticks(range(len(correlation.index)), short_labels)
    for i in range(len(correlation.index)):
        for j in range(len(correlation.columns)):
            axis.text(j, i, f"{correlation.iloc[i, j]:.2f}", ha="center", va="center")
    fig.colorbar(image, ax=axis, label="Pearson correlation")
    axis.set_title("Pollutant correlation matrix")
    _save(fig, path)


def plot_detrended_distribution(
    residual: pd.Series,
    column: str,
    q_fit: dict[str, float],
    path: Path,
) -> None:
    values = residual.dropna().to_numpy(dtype=float)
    centered = values - np.mean(values)
    fig, axis = plt.subplots(figsize=(8, 5))
    axis.hist(centered, bins=80, density=True, alpha=0.55, label="Residual data")
    x = np.linspace(np.quantile(centered, 0.005), np.quantile(centered, 0.995), 500)
    axis.plot(x, stats.norm.pdf(x, loc=0, scale=np.std(centered)), linewidth=2, label="Gaussian")
    axis.plot(
        x,
        q_gaussian_pdf(x, q_fit["q"], q_fit["beta"], q_fit["amplitude"]),
        linewidth=2,
        label=f"q-Gaussian (q={q_fit['q']:.3f})",
    )
    axis.set_yscale("log")
    axis.set_xlabel(f"Detrended {LABELS[column]}")
    axis.set_ylabel("Probability density")
    axis.grid(alpha=0.25)
    axis.legend()
    _save(fig, path)


def plot_kurtosis_curve(curve: pd.DataFrame, selected_window: int, path: Path) -> None:
    fig, axis = plt.subplots(figsize=(8, 5))
    axis.plot(curve["window_hours"], curve["average_kurtosis"], marker="o")
    axis.axhline(3.0, linestyle="--", label="Gaussian kurtosis = 3")
    axis.axvline(selected_window, linestyle=":", label=f"Selected scale = {selected_window} h")
    axis.set_xlabel("Window length (hours)")
    axis.set_ylabel("Average Pearson kurtosis")
    axis.grid(alpha=0.25)
    axis.legend()
    _save(fig, path)
