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


def write_mapping_json(structured_mapping: dict, output_file: Path):
    mapping_dict = gen_mapping_dict(structured_mapping)
    output_file.write_text(json.dumps(mapping_dict, indent=4))


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

    mapping_version = config.get("version", "unknown")
    mapping_modified = config.get("modified", "unknown")
    profiles_to_compare = config["profiles_to_compare"]
    data_dir = args.project_dir / config.get("data_dir", "data")
    structured_mapping = compare_profiles(profiles_to_compare, data_dir)

    if args.html:
        # Create the result html files
        show_remarks = config.get("show_remarks", True)
        html_output_dir = args.project_dir / config.get("html_output_dir", "html")
        create_results_html(mapping_version, mapping_modified, structured_mapping, html_output_dir, show_remarks)

    if args.json:
        # Generate the mapping dict and write to file
        mapping_output_file = args.project_dir / config.get(
            "mapping_output_file", "mapping.json"
        )
        write_mapping_json(structured_mapping, mapping_output_file)
