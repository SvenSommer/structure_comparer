# Generate a structured version of the presence data
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


if __name__ == "__main__":
    project_dir = Path("projects/erp")

    config = json.loads((project_dir / "config.json").read_text())

    # Read the manual entries
    MANUAL_ENTRIES.read(project_dir / "manual_entries.json")

    profiles_to_compare = config["profiles_to_compare"]
    structured_mapping = compare_profiles(profiles_to_compare, project_dir / "data")

    # Create the result html files
    create_results_html(structured_mapping, project_dir / "docs")

    # Generate the mapping dict and write to file
    write_mapping_json(structured_mapping, project_dir)
