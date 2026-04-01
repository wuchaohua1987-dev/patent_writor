"""Patent Writor - Multi-agent patent writing system.

Usage:
    uv run python main.py --input <input_file> --output <output_file> [--search-dir <directory>]

Example:
    uv run python main.py --input docs/invention.md --output output/patent.md
"""

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv

from src.crews import PatentCrew


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Patent Writor - Multi-agent patent writing system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
    uv run python main.py --input docs/invention.md --output output/patent.md
        """,
    )
    parser.add_argument(
        "--input",
        "-i",
        type=Path,
        required=True,
        help="Path to the input markdown file containing the invention description",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        required=True,
        help="Path for the output patent document",
    )
    parser.add_argument(
        "--search-dir",
        "-s",
        type=Path,
        default=None,
        help="Directory to search for prior art (default: same as input file directory)",
    )
    return parser.parse_args()


def main() -> int:
    """Main entry point for Patent Writor."""
    # Load environment variables from .env file
    load_dotenv()

    args = parse_args()

    # Validate input file exists
    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        return 1

    # Set default search directory
    search_dir = args.search_dir if args.search_dir else args.input.parent

    # Create output directory if it doesn't exist
    args.output.parent.mkdir(parents=True, exist_ok=True)

    print(f"Input file: {args.input}")
    print(f"Output file: {args.output}")
    print(f"Search directory: {search_dir}")
    print("-" * 50)

    # Initialize and run the crew
    crew = PatentCrew()

    inputs = {
        "input_file": str(args.input),
        "search_directory": str(search_dir),
        "output_file": str(args.output),
    }

    try:
        result = crew.run(inputs)
        print("-" * 50)
        print("Patent writing completed successfully!")
        print(f"Output saved to: {args.output}")
        return 0
    except Exception as e:
        print(f"Error during execution: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
