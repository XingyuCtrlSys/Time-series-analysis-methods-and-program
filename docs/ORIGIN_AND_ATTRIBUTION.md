# Origin and Attribution

## Source article

Benjamin Schäfer, Catherine M. Heppell, Hefin Rhys, and Christian Beck,
“Fluctuations of water quality time series in rivers follow superstatistics,”
*iScience*, vol. 24, no. 8, Art. no. 102881, 2021.

- DOI: https://doi.org/10.1016/j.isci.2021.102881
- Article page: https://www.sciencedirect.com/science/article/pii/S258900422100849X
- Original reproducibility code and data: https://osf.io/mxcrv/

The article’s Data and Code Availability statement reports that all code needed to reproduce its results, together with original, cleaned, and detrended River Chess data, is available in the OSF project above.

## Relationship to this repository

The original repository uploaded by the maintainer contained a monolithic air-quality script whose README explicitly stated that it referenced the article and its accompanying program code. The script retained methodological and implementation traces associated with the River Chess workflow, including seasonal detrending, EMD-related processing, q-Gaussian fitting, local average kurtosis, and local inverse-variance analysis.

The present repository is a cleaned and rewritten adaptation. It does not claim to reproduce the article’s figures or conclusions and does not include the River Chess data. Its current workflow:

1. validates and regularizes hourly air-quality records;
2. uses robust STL to separate trend, seasonal structure, and residual fluctuations;
3. compares residuals with Gaussian and q-Gaussian curves;
4. estimates a characteristic window using average local Pearson kurtosis;
5. fits local inverse-variance samples with candidate positive distributions;
6. exports reproducible tables and figures;
7. adds configuration, tests, and continuous integration.

## Important methodological differences

| Source article / original code | Current repository |
|---|---|
| River Chess dissolved oxygen and electrical conductivity | Xuzhou CO, NO2, O3, and SO2 demonstration data |
| 15-minute source measurements | Hourly observations |
| Seasonal decomposition and EMD are compared | Robust STL is used as the implemented detrending method |
| Study-specific River Chess stations and parameters | Configurable generic pollutant columns and output paths |
| Reproduction of article figures and findings | Exploratory software demonstration only |

## Attribution guidance

Use the following wording when describing this repository:

> This project adapts a superstatistical environmental time-series workflow motivated by Schäfer et al. (2021) and their accompanying OSF reproducibility materials. It applies a rewritten, modular pipeline to hourly air-quality data and does not reproduce the original River Chess study.

The article is open access under CC BY 4.0. This does not by itself establish that every file in the associated OSF code archive uses the same software license. Review the OSF project’s file-level or project-level licensing information before copying original source files.
