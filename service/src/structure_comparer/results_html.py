from pathlib import Path
import re
import shutil
from typing import Dict, List

from jinja2 import Environment, FileSystemLoader

from structure_comparer.helpers import split_parent_child


from .classification import Classification
from .data.comparison import Comparison


CSS_CLASS = {
    Classification.USE: "row-use",
    Classification.NOT_USE: "row-not-use",
    Classification.EMPTY: "row-not-use",
    Classification.EXTENSION: "row-extension",
    Classification.MANUAL: "row-manual",
    Classification.COPY_FROM: "row-manual",
    Classification.COPY_TO: "row-manual",
    Classification.FIXED: "row-manual",
    Classification.MEDICATION_SERVICE: "row-not-use",
}

STYLE_FILE_NAME = "style.css"
FILES_FOLDER = Path(__file__).parent / "files"


def flatten_profiles(profiles: List[str]) -> str:
    return "_".join(profiles)

# Define the custom filter function
def format_cardinality(value):
    if value == float("inf"):
        return "*"
    return value


def create_results_html(
    structured_mapping: Dict[str, Comparison],
    results_folder: str | Path,
    show_remarks: bool,
    show_warnings: bool,
):
    # Convert to Path object if necessary
    if isinstance(results_folder, str):
        results_folder = Path(results_folder)

    # Create the results folder if it does not exist
    if not results_folder.exists():
        results_folder.mkdir(parents=True)

    # Copy the style file to the results folder
    styles_file = FILES_FOLDER / STYLE_FILE_NAME
    shutil.copy(styles_file, results_folder / STYLE_FILE_NAME)

    env = Environment(loader=FileSystemLoader(FILES_FOLDER))
    env.filters["format_links"] = format_links
    env.filters["format_cardinality"] = format_cardinality  # Register the custom filter
    template = env.get_template("template.html.j2")

    for comp in structured_mapping.values():

        entries = {}
        number_of_warnings = 0  # Initialize the warning counter

        for field, entry in comp.fields.items():
            warnings = set()  # Use a set to collect unique warnings
            target_min_card = entry.profiles[comp.target.profile_key].min_cardinality
            target_max_card = entry.profiles[comp.target.profile_key].max_cardinality

            parent, _ = split_parent_child(field)
            comparison_parent = comp.fields.get(parent)

            for profile in comp.sources:
                source_min_card = entry.profiles[profile.profile_key].min_cardinality
                source_max_card = entry.profiles[profile.profile_key].max_cardinality

                if comparison_parent and comparison_parent.classification in [
                    Classification.USE
                ]:
                    # Skip the specific warning if the parent is being copied or extended
                    if target_max_card < source_max_card:
                        continue

                if source_max_card > target_max_card and entry.classification not in [
                    Classification.COPY_TO,
                    Classification.COPY_FROM,
                    Classification.EXTENSION,
                ]:
                    warnings.add(
                        "The maximum cardinality of one of the source profiles exceeds the maximum cardinality of the target profile"
                    )

                # Check if source_max_card is not 0 before considering source_min_card
                if source_max_card != 0 and source_min_card < target_min_card and entry.classification not in [
                    Classification.COPY_TO,
                    Classification.COPY_FROM,
                    Classification.EXTENSION,
                ]:
                    warnings.add(
                        "The minimum cardinality of one of the source profiles is less than the minimum cardinality of the target profile"
                    )

            number_of_warnings += len(warnings)  # Increment the warning counter

            entries[field] = {
                "classification": entry.classification,
                "css_class": CSS_CLASS[entry.classification],
                "extension": entry.extension,
                "extra": entry.extra,
                "profiles": entry.profiles,
                "remark": entry.remark,
                "warning": list(warnings),  # Convert set back to list
            }

        data = {
            "css_file": STYLE_FILE_NAME,
            "target_profile": {
                "key": comp.target.profile_key,
                "url": comp.target.simplifier_url,
            },
            "source_profiles": [
                {
                    "key": profile.profile_key,
                    "url": profile.simplifier_url,
                }
                for profile in comp.sources
            ],
            "entries": entries,
            "show_remarks": show_remarks,
            "show_warnings": show_warnings,
            "number_of_warnings": number_of_warnings,  # Add the warning count to the data
            "version": comp.version,
            "last_updated": comp.last_updated,
            "status": comp.status,
        }

        content = template.render(**data)

        source_profiles_flat = flatten_profiles(
            [profile["key"] for profile in data["source_profiles"]]
        )
        html_file = (
            results_folder
            / f"{source_profiles_flat}_to_{data['target_profile']['key']}.html"
        )
        html_file.write_text(content)


def format_links(text: str) -> str:
    if not text:
        return text

    # Regex zum Erkennen von URLs
    url_pattern = r"(https?://[\w\.\/\-\|]+)"
    # Ersetze URLs mit einem anklickbaren Link
    return re.sub(url_pattern, r'<a href="\1" target="_blank">\1</a>', text)
