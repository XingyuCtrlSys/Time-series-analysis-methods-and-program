# Methods

> **Methodological origin.** The broad superstatistical workflow is motivated by Schäfer et al. (2021) and the authors’ OSF reproducibility materials. This implementation is an adaptation for hourly air-quality data, not a reproduction of the River Chess study. See [ORIGIN_AND_ATTRIBUTION.md](ORIGIN_AND_ATTRIBUTION.md).

The pipeline performs the following steps:

1. **Schema validation**: timestamps and pollutant columns are checked, sorted, and de-duplicated.
2. **Hourly regularization**: the time index is reconstructed at a configurable frequency.
3. **Conservative interpolation**: only short internal gaps are filled.
4. **Exploratory analysis**: descriptive statistics, missingness, correlations, full-history plots, and a seven-day detail plot are produced.
5. **STL detrending**: trend and seasonal components are separated using a robust 24-hour seasonal period by default.
6. **Fluctuation analysis**: residual distributions are compared with Gaussian and q-Gaussian curves.
7. **Time-scale analysis**: average Pearson kurtosis is evaluated over candidate windows; the window closest to Gaussian kurtosis is selected.
8. **Superstatistical diagnostic**: local inverse variance values are fitted with gamma, lognormal, and inverse-gamma distributions and ranked by AIC and the Kolmogorov–Smirnov statistic.

## Improvements over the legacy script

- Sampling frequency is inferred from the data design rather than hard-coded as four samples per hour.
- All plotting and analysis functions are separated from file loading and command-line handling.
- Deprecated `seaborn.distplot` usage and unsafe `eval` calls are removed.
- Duplicate imports, unused dependencies, hard-coded absolute paths, and IDE/virtual-environment files are removed.
- Every generated table and figure has a deterministic output path.
- The project includes tests and a GitHub Actions workflow.

These methods are exploratory. Distribution fits and q-Gaussian parameters should not be interpreted as causal or regulatory evidence.
