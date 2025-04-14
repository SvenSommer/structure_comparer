# Generate a structured version of the presence data
import argparse
import json
from pathlib import Path

from structure_comparer.config import Config

from structure_comparer import (
    MANUAL_ENTRIES,
    compare_profiles,
    create_results_html,
    gen_mapping_dict,
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
    parser.add_argument("--html", action="store_true",
                        help="Generate html files")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Generate mapping json file",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()

    config = Config.from_json(args.project_dir / "config.json")

    # Read the manual entries
    manual_entries_file = config.manual_entries_file
    MANUAL_ENTRIES.read(args.project_dir / manual_entries_file)

    data_dir = args.project_dir / config.data_dir
    structured_mapping = compare_profiles(config.profiles_to_compare, data_dir)

    if args.html:
        # Create the result html files
        show_remarks = config.show_remarks
        show_warnings = config.show_warnings
        html_output_dir = args.project_dir / \
            config.html_output_dir
        create_results_html(structured_mapping, html_output_dir, show_remarks, show_warnings)

    if args.json:
        # Generate the mapping dict and write to file
        mapping_output_file = args.project_dir / config.mapping_output_file
        write_mapping_json(structured_mapping, mapping_output_file)
