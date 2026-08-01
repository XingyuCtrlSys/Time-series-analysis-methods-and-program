from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import optimize, stats
from statsmodels.tsa.seasonal import STL

from .io import POLLUTANT_COLUMNS, TIMESTAMP_COLUMN


def descriptive_statistics(frame: pd.DataFrame) -> pd.DataFrame:
    """Return descriptive statistics in a tidy table."""
    stats_frame = frame[list(POLLUTANT_COLUMNS)].describe(percentiles=[0.25, 0.5, 0.75]).T
    stats_frame.index.name = "variable"
    return stats_frame.reset_index()


def correlation_matrix(frame: pd.DataFrame) -> pd.DataFrame:
    """Return Pearson correlations using pairwise complete observations."""
    return frame[list(POLLUTANT_COLUMNS)].corr(min_periods=24)


def stl_detrend(series: pd.Series, period: int = 24) -> pd.DataFrame:
    """Decompose a regularly sampled series and return observed/trend/seasonal/residual."""
    clean = series.astype(float)
    missing = int(clean.isna().sum())
    if missing:
        raise ValueError(
            f"STL detrending requires a complete regular series; {missing} values remain missing. "
            "Increase --interpolation-limit, choose a continuous subset, or preprocess the data explicitly."
        )
    if len(clean) < period * 3:
        raise ValueError(f"At least {period * 3} observations are required for STL detrending.")
    result = STL(clean, period=period, robust=True).fit()
    return pd.DataFrame(
        {
            "observed": clean,
            "trend": result.trend,
            "seasonal": result.seasonal,
            "residual": result.resid,
        },
        index=series.index,
    )


def average_window_kurtosis(values: np.ndarray, window: int) -> float:
    """Average Pearson kurtosis across non-overlapping windows."""
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    if window < 4 or window > len(values):
        return float("nan")
    usable = len(values) // window * window
    blocks = values[:usable].reshape(-1, window)
    block_values = stats.kurtosis(blocks, axis=1, fisher=False, bias=False, nan_policy="omit")
    return float(np.nanmean(block_values))


def kurtosis_curve(values: np.ndarray, windows: list[int]) -> pd.DataFrame:
    """Evaluate average window kurtosis for candidate time scales."""
    return pd.DataFrame(
        {
            "window_hours": windows,
            "average_kurtosis": [average_window_kurtosis(values, window) for window in windows],
        }
    )


def nearest_gaussian_time_scale(curve: pd.DataFrame, target: float = 3.0) -> int:
    """Select the tested window whose average Pearson kurtosis is closest to Gaussian."""
    valid = curve.dropna(subset=["average_kurtosis"])
    if valid.empty:
        raise ValueError("No valid kurtosis values were computed.")
    row = valid.loc[(valid["average_kurtosis"] - target).abs().idxmin()]
    return int(row["window_hours"])


def inverse_variance_series(values: np.ndarray, window: int) -> np.ndarray:
    """Compute local inverse variance beta on non-overlapping windows."""
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    usable = len(values) // window * window
    blocks = values[:usable].reshape(-1, window)
    variances = np.var(blocks, axis=1, ddof=1)
    beta = np.divide(1.0, variances, out=np.full_like(variances, np.nan), where=variances > 0)
    beta = beta[np.isfinite(beta) & (beta > 0)]
    if len(beta) > 20:
        beta = beta[beta <= np.quantile(beta, 0.99)]
    return beta


def fit_beta_distributions(beta: np.ndarray) -> pd.DataFrame:
    """Fit common positive distributions and rank them by AIC and KS statistic."""
    beta = np.asarray(beta, dtype=float)
    beta = beta[np.isfinite(beta) & (beta > 0)]
    if len(beta) < 8:
        raise ValueError("At least 8 positive beta values are required for distribution fitting.")

    candidates = {
        "gamma": stats.gamma,
        "lognormal": stats.lognorm,
        "inverse_gamma": stats.invgamma,
    }
    rows = []
    for name, distribution in candidates.items():
        params = distribution.fit(beta, floc=0)
        log_likelihood = float(np.sum(distribution.logpdf(beta, *params)))
        k = len(params)
        aic = 2 * k - 2 * log_likelihood
        ks_stat, ks_pvalue = stats.kstest(beta, distribution.cdf, args=params)
        rows.append(
            {
                "distribution": name,
                "aic": aic,
                "ks_statistic": ks_stat,
                "ks_pvalue": ks_pvalue,
                "parameters": repr(tuple(float(x) for x in params)),
            }
        )
    return pd.DataFrame(rows).sort_values(["aic", "ks_statistic"]).reset_index(drop=True)


def q_gaussian_pdf(x: np.ndarray, q: float, beta: float, amplitude: float) -> np.ndarray:
    """Unnormalized q-Gaussian curve used for robust histogram fitting."""
    base = 1.0 + (q - 1.0) * beta * np.square(x)
    return amplitude * np.power(base, -1.0 / (q - 1.0))


def fit_q_gaussian(values: np.ndarray, bins: int = 80) -> dict[str, float]:
    """Fit a centered q-Gaussian to a density histogram using bounded least squares."""
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    values = values - np.mean(values)
    density, edges = np.histogram(values, bins=bins, density=True)
    centers = (edges[:-1] + edges[1:]) / 2
    mask = np.isfinite(density) & (density > 0)
    scale = np.std(values) or 1.0
    initial = (1.2, 1.0 / (2 * scale * scale), float(np.max(density)))
    params, _ = optimize.curve_fit(
        q_gaussian_pdf,
        centers[mask],
        density[mask],
        p0=initial,
        bounds=([1.001, 1e-12, 1e-12], [2.95, np.inf, np.inf]),
        maxfev=30000,
    )
    return {"q": float(params[0]), "beta": float(params[1]), "amplitude": float(params[2])}
