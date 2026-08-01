# Data format and limitations

## Canonical schema

Every input CSV must contain exactly one timestamp column and four pollutant columns:

| Column | Meaning | Unit |
|---|---|---|
| `timestamp` | Observation time in ISO 8601 format | UTC |
| `CO_mg_m3` | Carbon monoxide concentration | mg/m³ |
| `NO2_ug_m3` | Nitrogen dioxide concentration | µg/m³ |
| `O3_ug_m3` | Ozone concentration | µg/m³ |
| `SO2_ug_m3` | Sulfur dioxide concentration | µg/m³ |

## Included data

The repository contains cleaned demonstration data for 2022, 2023, and the available part of 2024. The original files used inconsistent headers, mixed date formats, redundant spreadsheet copies, and a 2024 CSV with a large number of empty trailing rows. The cleaned files:

- use consistent English, ASCII-safe filenames;
- use one timestamp representation;
- remove empty trailing rows and duplicate timestamps;
- convert invalid and negative concentrations to missing values;
- preserve genuine missing observations.

## Important limitation

The original data source could not be verified from the legacy project. Therefore, the included data must be treated as **demonstration data only**. It must not be used to make scientific, regulatory, health, or environmental claims without replacing it with a traceable authoritative dataset.

The example configuration interpolates internal gaps of at most 12 hourly samples. Longer gaps remain missing so that the analysis does not silently invent extended periods of observations.
