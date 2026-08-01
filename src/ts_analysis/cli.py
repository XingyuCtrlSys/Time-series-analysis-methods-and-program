from __future__ import annotations

import argparse
import json
from pathlib import Path

from .pipeline import run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a reproducible air-quality time-series analysis pipeline."
    )
    parser.add_argument("--config", type=Path, help="Optional JSON configuration file.")
    parser.add_argument("--input", type=Path, help="Canonical input CSV file.")
    parser.add_argument("--output", type=Path, default=Path("results"))
    parser.add_argument("--frequency", default="1h")
    parser.add_argument("--interpolation-limit", type=int, default=12)
    parser.add_argument("--seasonal-period", type=int, default=24)
    parser.add_argument("--weekly-start", default=None)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    config = {}
    if args.config:
        config = json.loads(args.config.read_text(encoding="utf-8"))

    input_path = args.input or config.get("input")
    if not input_path:
        raise SystemExit("An input file is required via --input or --config.")

    result = run_pipeline(
        input_path=input_path,
        output_dir=config.get("output", args.output),
        frequency=config.get("frequency", args.frequency),
        interpolation_limit=config.get("interpolation_limit", args.interpolation_limit),
        seasonal_period=config.get("seasonal_period", args.seasonal_period),
        weekly_start=config.get("weekly_start", args.weekly_start),
    )
    print(f"Analysis completed. Results: {result['output_dir']}")


if __name__ == "__main__":
    main()
