from pathlib import Path
import re
import shutil

from jinja2 import Environment, FileSystemLoader

from .classification import Classification
from .consts import (
    STRUCT_CLASSIFICATION,
    STRUCT_EPA_PROFILE,
    STRUCT_FIELDS,
    STRUCT_KBV_PROFILES,
)


CSS_CLASS = {
    Classification.USE: "row-use",
    Classification.NOT_USE: "row-not-use",
    Classification.EMPTY: "row-not-use",
    Classification.EXTENSION: "row-extension",
    Classification.MANUAL: "row-manual",
    Classification.OTHER: "row-other",
    Classification.COPY_FROM: "row-use",
    Classification.COPY_TO: "row-use",
    Classification.FIXED: "row-manual",
    Classification.MEDICATION_SERVICE: "row-not-use",
}

STYLE_FILE_NAME = "style.css"
FILES_FOLDER = Path(__file__).parent / "files"


def create_results_html(
    structured_mapping, results_folder: str | Path, show_remarks: bool
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
    template = env.get_template("template.html.j2")

    for data in structured_mapping.values():
        clean_kbv_group = data[STRUCT_KBV_PROFILES]
        clean_epa_file = data[STRUCT_EPA_PROFILE]

        entries = {
            prop: {**entry, "css_class": CSS_CLASS[entry[STRUCT_CLASSIFICATION]]}
            for prop, entry in data[STRUCT_FIELDS].items()
        }

        data = {
            "css_file": STYLE_FILE_NAME,
            "target_profile": clean_epa_file,
            "source_profiles": clean_kbv_group,
            "entries": entries,
            "show_remarks": show_remarks,
        }

        content = template.render(**data)

        html_file = results_folder / f"{clean_epa_file}.html"
        html_file.write_text(content)


def format_links(text: str) -> str:
    # Regex zum Erkennen von URLs
    url_pattern = r"(https?://[\w\.\/\-\|]+)"
    # Ersetze URLs mit einem anklickbaren Link
    return re.sub(url_pattern, r'<a href="\1" target="_blank">\1</a>', text)
