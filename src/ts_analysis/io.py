from __future__ import annotations

from pathlib import Path

import pandas as pd

TIMESTAMP_COLUMN = "timestamp"
POLLUTANT_COLUMNS = ("CO_mg_m3", "NO2_ug_m3", "O3_ug_m3", "SO2_ug_m3")


class DataValidationError(ValueError):
    """Raised when an input file does not satisfy the documented data schema."""


def load_air_quality_csv(path: str | Path) -> pd.DataFrame:
    """Load, validate, sort, and de-duplicate a canonical air-quality CSV file."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    frame = pd.read_csv(path)
    required = {TIMESTAMP_COLUMN, *POLLUTANT_COLUMNS}
    missing = sorted(required.difference(frame.columns))
    if missing:
        raise DataValidationError(
            "Missing required columns: " + ", ".join(missing) + ". See docs/DATA.md."
        )

    frame = frame[[TIMESTAMP_COLUMN, *POLLUTANT_COLUMNS]].copy()
    frame[TIMESTAMP_COLUMN] = pd.to_datetime(frame[TIMESTAMP_COLUMN], errors="coerce", utc=True)
    for column in POLLUTANT_COLUMNS:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
        frame.loc[frame[column] < 0, column] = pd.NA

    invalid_timestamps = int(frame[TIMESTAMP_COLUMN].isna().sum())
    if invalid_timestamps:
        raise DataValidationError(f"Found {invalid_timestamps} invalid timestamp value(s).")

    frame = (
        frame.sort_values(TIMESTAMP_COLUMN)
        .drop_duplicates(TIMESTAMP_COLUMN, keep="last")
        .reset_index(drop=True)
    )
    if frame.empty:
        raise DataValidationError("The input file contains no usable observations.")
    return frame
