from __future__ import annotations

from pathlib import Path

import pandas as pd

from .analysis import (
    correlation_matrix,
    descriptive_statistics,
    fit_beta_distributions,
    fit_q_gaussian,
    inverse_variance_series,
    kurtosis_curve,
    nearest_gaussian_time_scale,
    stl_detrend,
)
from .io import POLLUTANT_COLUMNS, TIMESTAMP_COLUMN, load_air_quality_csv
from .plots import (
    plot_correlation,
    plot_detrended_distribution,
    plot_kurtosis_curve,
    plot_overview,
    plot_week,
)
from .preprocess import quality_report, regularize_hourly


def run_pipeline(
    input_path: str | Path,
    output_dir: str | Path,
    frequency: str = "1h",
    interpolation_limit: int = 3,
    seasonal_period: int = 24,
    weekly_start: str | None = None,
) -> dict[str, Path]:
    """Run the complete reproducible analysis and write tables and figures."""
    output_dir = Path(output_dir)
    figures_dir = output_dir / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    raw = load_air_quality_csv(input_path)
    quality_report(raw).to_csv(output_dir / "quality_report_before_interpolation.csv", index=False)
    frame = regularize_hourly(raw, frequency=frequency, interpolation_limit=interpolation_limit)
    quality_report(frame).to_csv(output_dir / "quality_report_after_interpolation.csv", index=False)
    frame.to_csv(output_dir / "regularized_data.csv", index=False, date_format="%Y-%m-%dT%H:%M:%SZ")

    descriptive_statistics(frame).to_csv(output_dir / "descriptive_statistics.csv", index=False)
    correlations = correlation_matrix(frame)
    correlations.to_csv(output_dir / "correlation_matrix.csv")

    plot_overview(frame, figures_dir / "01_time_series_overview.png")
    plot_correlation(correlations, figures_dir / "02_correlation_matrix.png")
    if weekly_start is None:
        weekly_start = str(frame[TIMESTAMP_COLUMN].iloc[0].date())
    plot_week(frame, weekly_start, figures_dir / "03_weekly_detail.png")

    residual_frame = pd.DataFrame({TIMESTAMP_COLUMN: frame[TIMESTAMP_COLUMN]})
    fit_rows = []
    for column in POLLUTANT_COLUMNS:
        decomposition = stl_detrend(frame[column], period=seasonal_period)
        residual_frame[column] = decomposition["residual"].to_numpy()

        q_fit = fit_q_gaussian(decomposition["residual"].to_numpy())
        fit_rows.append({"variable": column, **q_fit})
        plot_detrended_distribution(
            decomposition["residual"],
            column,
            q_fit,
            figures_dir / f"04_{column}_fluctuation_distribution.png",
        )

        windows = [6, 12, 24, 48, 72, 96, 120, 168, 240, 336]
        curve = kurtosis_curve(decomposition["residual"].to_numpy(), windows)
        selected = nearest_gaussian_time_scale(curve)
        curve.to_csv(output_dir / f"kurtosis_curve_{column}.csv", index=False)
        plot_kurtosis_curve(curve, selected, figures_dir / f"05_{column}_kurtosis_scale.png")

        beta = inverse_variance_series(decomposition["residual"].to_numpy(), selected)
        distribution_fits = fit_beta_distributions(beta)
        distribution_fits.insert(0, "variable", column)
        distribution_fits.insert(1, "window_hours", selected)
        distribution_fits.to_csv(output_dir / f"beta_distribution_fits_{column}.csv", index=False)

    residual_frame.to_csv(output_dir / "stl_residuals.csv", index=False, date_format="%Y-%m-%dT%H:%M:%SZ")
    pd.DataFrame(fit_rows).to_csv(output_dir / "q_gaussian_fits.csv", index=False)

    return {
        "output_dir": output_dir,
        "figures_dir": figures_dir,
        "regularized_data": output_dir / "regularized_data.csv",
    }
