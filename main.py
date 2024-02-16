# Generate a structured version of the presence data
import argparse
import json
from pathlib import Path

from structure_comparer import (
    compare_profiles,
    gen_mapping_dict,
    create_results_html,
    MANUAL_ENTRIES,
)


def write_mapping_json(structured_mapping: dict, results_folder: str | Path):
    # Convert to Path object if necessary
    if isinstance(results_folder, str):
        results_folder = Path(results_folder)

    mapping_dict = gen_mapping_dict(structured_mapping)
    (results_folder / "mapping.json").write_text(json.dumps(mapping_dict, indent=4))


def get_args():
    parser = argparse.ArgumentParser(
        description="Compare profiles and generate mapping"
    )

    parser.add_argument(
        "--project-dir",
        type=Path,
        help="The project directory containing the profiles and config",
    )
    parser.add_argument("--html", action="store_true", help="Generate html files")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Generate mapping json file",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()

    config = json.loads((args.project_dir / "config.json").read_text())

    # Read the manual entries
    MANUAL_ENTRIES.read(args.project_dir / "manual_entries.json")

    profiles_to_compare = config["profiles_to_compare"]
    structured_mapping = compare_profiles(
        profiles_to_compare, args.project_dir / "data"
    )

    if args.html:
        # Create the result html files
        create_results_html(structured_mapping, args.project_dir / "docs")

    if args.json:
        # Generate the mapping dict and write to file
        write_mapping_json(structured_mapping, args.project_dir)
