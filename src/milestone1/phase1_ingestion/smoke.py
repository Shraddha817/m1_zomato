from __future__ import annotations

import argparse
import json
import sys

from dotenv import load_dotenv

from .ingest import load_restaurants, restaurant_to_dict


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Phase 1 ingestion smoke test")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Number of restaurants to load (omit to load all; can be large)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print loaded restaurants as JSON (use --limit to keep output small)",
    )
    args = parser.parse_args(argv)

    load_dotenv(override=False)

    restaurants = load_restaurants(limit=args.limit)
    print(f"loaded_count={len(restaurants)}")

    if args.json:
        payload = [restaurant_to_dict(r) for r in restaurants]
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

