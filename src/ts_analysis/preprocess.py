from __future__ import annotations

import pandas as pd

from .io import POLLUTANT_COLUMNS, TIMESTAMP_COLUMN


def quality_report(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a compact, machine-readable quality report for each pollutant."""
    rows = []
    for column in POLLUTANT_COLUMNS:
        series = frame[column]
        rows.append(
            {
                "variable": column,
                "observations": int(series.notna().sum()),
                "missing": int(series.isna().sum()),
                "missing_percent": round(float(series.isna().mean() * 100), 4),
                "minimum": series.min(skipna=True),
                "maximum": series.max(skipna=True),
            }
        )
    return pd.DataFrame(rows)


def regularize_hourly(
    frame: pd.DataFrame,
    frequency: str = "1h",
    interpolation_limit: int = 3,
) -> pd.DataFrame:
    """Create a regular time grid and interpolate only short internal gaps."""
    indexed = frame.set_index(TIMESTAMP_COLUMN).sort_index()
    full_index = pd.date_range(indexed.index.min(), indexed.index.max(), freq=frequency, tz="UTC")
    regular = indexed.reindex(full_index)
    regular.index.name = TIMESTAMP_COLUMN

    # Time interpolation is restricted so long gaps remain explicit rather than silently invented.
    regular[list(POLLUTANT_COLUMNS)] = regular[list(POLLUTANT_COLUMNS)].interpolate(
        method="time", limit=interpolation_limit, limit_area="inside"
    )
    return regular.reset_index()
