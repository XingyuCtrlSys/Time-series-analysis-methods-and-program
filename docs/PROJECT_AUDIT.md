# Project audit and reconstruction summary

## Major issues found in the legacy repository

1. **Repository pollution**: `.idea/`, a local virtual environment (`Myenv/`), generated archives, and console output were committed.
2. **Unclear directory hierarchy**: source code, raw data, processed data, figures, and environment files were mixed inside nested folders.
3. **Filename corruption**: Chinese paths were stored as literal `#Uxxxx` sequences, reducing portability across operating systems.
4. **Redundant and oversized data**: several XLSX files duplicated CSV content; the 2024 CSV contained more than one million trailing empty rows.
5. **Monolithic code**: the main script contained 933 lines, duplicate imports and functions, global state, and analysis that executed immediately during import.
6. **Hard-coded assumptions**: paths, date ranges, plot titles, array indices, and four samples per hour were fixed in code even though the included data is hourly.
7. **Unsafe or deprecated patterns**: the script used `eval`, deprecated `seaborn.distplot`, broad `except` blocks, and unnecessary dependencies.
8. **Weak reproducibility**: output paths were inconsistent, no tests existed, and a fresh environment could not reliably reproduce the analysis.
9. **Data credibility risk**: the data source was explicitly unknown, but the limitation was not consistently enforced throughout the workflow.
10. **Privacy risk**: personal phone numbers and multiple email addresses were exposed in the public README and remain visible in Git history unless the history is removed.

## Reconstruction decisions

- Created a standard `src/` package layout with separate modules for I/O, preprocessing, analysis, plotting, the pipeline, and the CLI.
- Standardized all datasets to a documented schema and ASCII-safe names.
- Removed empty trailing rows, invalid timestamps, duplicate timestamps, and redundant spreadsheet copies.
- Replaced implicit frequency assumptions with a configurable hourly grid.
- Added bounded interpolation, robust STL detrending, q-Gaussian diagnostics, kurtosis time-scale analysis, and distribution comparison.
- Added deterministic result paths, a command-line interface, tests, and GitHub Actions.
- Replaced the legacy README with installation, usage, data limitations, and reproducibility documentation.
- Removed private contact details, IDE metadata, virtual environments, nested output ZIP files, and generated output from version control.

## Validation performed

- All three automated tests pass.
- The complete example pipeline runs successfully on the combined 2022–2024 demonstration dataset.
- The project contains fewer than 100 uploadable files, and every file is below GitHub's browser upload limit.
