from __future__ import annotations

import argparse
import json

from signal_detection.pipeline import run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the signal detection pipeline.")
    parser.add_argument(
        "--source",
        action="append",
        dest="sources",
        default=[],
        help="Path or URL for an RSS/Atom/HTML source. Can be passed multiple times.",
    )
    parser.add_argument(
        "--json-output",
        default="outputs/signals.json",
        help="Path to the JSON output file.",
    )
    parser.add_argument(
        "--sqlite-output",
        default="outputs/signals.db",
        help="Path to the SQLite output file.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    results = run_pipeline(
        sources=args.sources or None,
        json_output=args.json_output,
        sqlite_output=args.sqlite_output,
    )
    print(json.dumps([signal.to_dict() for signal in results], indent=2))
    return 0
