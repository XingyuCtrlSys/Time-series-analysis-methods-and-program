from pathlib import Path

import numpy as np
import pandas as pd

from ts_analysis.analysis import average_window_kurtosis, inverse_variance_series
from ts_analysis.io import load_air_quality_csv
from ts_analysis.preprocess import regularize_hourly


def test_load_sample_data() -> None:
    path = Path("data/raw/xuzhou_air_quality_2022.csv")
    frame = load_air_quality_csv(path)
    assert not frame.empty
    assert frame["timestamp"].is_monotonic_increasing
    assert frame["timestamp"].duplicated().sum() == 0


def test_regularize_hourly() -> None:
    frame = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(
                ["2024-01-01T00:00:00Z", "2024-01-01T02:00:00Z"], utc=True
            ),
            "CO_mg_m3": [1.0, 3.0],
            "NO2_ug_m3": [10.0, 12.0],
            "O3_ug_m3": [20.0, 22.0],
            "SO2_ug_m3": [5.0, 7.0],
        }
    )
    regular = regularize_hourly(frame, interpolation_limit=1)
    assert len(regular) == 3
    assert regular.loc[1, "CO_mg_m3"] == 2.0


def test_window_metrics() -> None:
    rng = np.random.default_rng(123)
    values = rng.normal(size=240)
    kurtosis = average_window_kurtosis(values, 24)
    beta = inverse_variance_series(values, 24)
    assert np.isfinite(kurtosis)
    assert len(beta) == 10
    assert np.all(beta > 0)
