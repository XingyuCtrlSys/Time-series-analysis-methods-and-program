# Air Quality Time-Series Analysis Toolkit

A reproducible Python toolkit for cleaning, detrending, visualizing, and performing exploratory superstatistical diagnostics on hourly air-quality time series.

The included demonstration data cover Xuzhou air-quality observations from 2022, 2023, and part of 2024. **The original data provenance could not be independently verified; therefore, these files are provided only for software demonstration and must not be used for regulatory, health, or scientific claims.**

## Features

- validates timestamps and pollutant columns;
- reconstructs a regular hourly time grid;
- interpolates only bounded internal gaps;
- generates descriptive statistics and correlation analysis;
- performs robust STL detrending;
- compares residual fluctuations with Gaussian and q-Gaussian curves;
- estimates a characteristic time scale using average local kurtosis;
- fits local inverse-variance values with gamma, lognormal, and inverse-gamma distributions;
- exports all tables and figures to a predictable results directory;
- includes automated tests and a GitHub Actions workflow.

## Origin and attribution

This repository was developed from a legacy air-quality analysis script that referenced the methods and accompanying reproducibility code of the following article:

> B. Schäfer, C. M. Heppell, H. Rhys, and C. Beck, “Fluctuations of water quality time series in rivers follow superstatistics,” *iScience*, vol. 24, no. 8, Art. no. 102881, 2021. DOI: [10.1016/j.isci.2021.102881](https://doi.org/10.1016/j.isci.2021.102881).

- **Article:** [ScienceDirect / iScience](https://www.sciencedirect.com/science/article/pii/S258900422100849X)
- **Original reproducibility code and River Chess data:** [OSF project `mxcrv`](https://osf.io/mxcrv/)

The article studies dissolved oxygen and electrical conductivity in the River Chess using seasonal detrending, empirical mode decomposition, q-Gaussian fluctuation analysis, local kurtosis time-scale extraction, and distributions of the local inverse variance. The article states that the code and required original, cleaned, and detrended data are available in the linked OSF project.

This repository **does not reproduce the River Chess study** and does not redistribute its data. It adapts the broad analysis workflow to hourly air-quality observations and substantially rewrites the legacy project into a modular package. In particular, the present implementation uses robust STL detrending rather than the article’s seasonal-decomposition/EMD comparison, corrects the sampling-frequency assumptions for hourly data, and adds validation, configuration, testing, and reproducible output management.

For a more detailed relationship between the source article, the legacy script, and this implementation, see [`docs/ORIGIN_AND_ATTRIBUTION.md`](docs/ORIGIN_AND_ATTRIBUTION.md).

## Repository structure

```text
.
├── .github/workflows/        # Continuous-integration tests
├── data/
│   ├── raw/                  # Yearly demonstration data
│   └── processed/            # Combined data and cleaning summary
├── docs/
│   ├── DATA.md               # Input schema and data limitations
│   ├── METHODS.md            # Implemented analysis workflow
│   ├── ORIGIN_AND_ATTRIBUTION.md
│   └── assets/               # README figures
├── results/                  # Generated locally; ignored except .gitkeep
├── src/ts_analysis/          # Reusable Python package
├── tests/                    # Automated tests
├── .gitignore
├── config.example.json
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── run_analysis.py
└── README.md
```

## Quick start

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
source .venv/bin/activate       # macOS/Linux
# .venv\Scripts\activate      # Windows PowerShell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Run the included demonstration:

```bash
python run_analysis.py --config config.example.json
```

Generated CSV tables and PNG figures are written to `results/`.

The package can also be installed in editable mode:

```bash
pip install -e .
air-ts-analysis --config config.example.json
```

## Use another dataset

Prepare a CSV that follows [`docs/DATA.md`](docs/DATA.md), then run:

```bash
python run_analysis.py \
  --input path/to/your_data.csv \
  --output results/my_analysis \
  --seasonal-period 24 \
  --weekly-start 2024-01-01
```

## Example outputs

### Full time-series overview

![Full time-series overview](docs/assets/time_series_overview.png)

### Correlation matrix

![Correlation matrix](docs/assets/correlation_matrix.png)

### Example fluctuation distribution

![O3 fluctuation distribution](docs/assets/o3_fluctuation_distribution.png)

## Reproducibility and interpretation

The pipeline is deterministic for a fixed input file and configuration. Missing values, interpolation, detrending, and fitted distributions are exported for inspection. Results are exploratory and must not be interpreted as causal findings, official air-quality assessments, or a reproduction of the cited article.

## Tests

```bash
pip install -r requirements-dev.txt
pytest -q
```

## Citation and reuse

When discussing the superstatistical methodology that motivated this project, cite the original article above and consult its OSF repository for the authors’ original code and data. When reusing this repository, describe it as an air-quality adaptation and software refactoring rather than as the original River Chess implementation.

No separate software license is asserted here for the source article’s accompanying code. Users should review the licensing information supplied by the original authors in the OSF project before copying or redistributing material from that project.
