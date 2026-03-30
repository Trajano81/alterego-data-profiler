"""CLI entry point for alterego-profiler."""

from __future__ import annotations

import argparse
import sys

from .profiler import profile_dataset


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="alterego-profiler",
        description="Profile a dataset file and output structured metadata.",
    )
    parser.add_argument("file", help="Path to the data file to profile")
    parser.add_argument(
        "--sample-size",
        type=int,
        default=1000,
        help="Maximum rows to sample (default: 1000)",
    )
    parser.add_argument(
        "--output",
        choices=["json", "yaml"],
        default="json",
        help="Output format (default: json)",
    )
    args = parser.parse_args()

    try:
        result = profile_dataset(
            args.file, sample_size=args.sample_size, output=args.output
        )
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.output == "yaml":
        print(result.to_yaml())
    else:
        print(result.to_json())


if __name__ == "__main__":
    main()
