# Generate a structured version of the presence data
import argparse
import json
from pathlib import Path

from structure_comparer.io import mapping_json, static_html

from structure_comparer import MANUAL_ENTRIES, compare_profiles


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
    manual_entries_file = config.get("manual_entries_file", "manual_entries.yaml")
    MANUAL_ENTRIES.read(args.project_dir / manual_entries_file)

    profiles_to_compare = config["profiles_to_compare"]
    data_dir = args.project_dir / config.get("data_dir", "data")
    structured_mapping = compare_profiles(profiles_to_compare, data_dir)

    if args.html:
        # Create the result html files
        show_remarks = config.get("show_remarks", True)
        html_output_dir = args.project_dir / config.get("html_output_dir", "html")
        static_html.write(structured_mapping, html_output_dir, show_remarks)

    if args.json:
        # Generate the mapping dict and write to file
        mapping_output_file = args.project_dir / config.get(
            "mapping_output_file", "mapping.json"
        )
        mapping_json.write(structured_mapping, mapping_output_file)
