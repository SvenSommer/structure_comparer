from pathlib import Path
import re
import shutil
from typing import Dict

from jinja2 import Environment, FileSystemLoader


from .classification import Classification
from .data import Comparison


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
    structured_mapping: Dict[str, Comparison],
    results_folder: str | Path,
    show_remarks: bool,
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

    for comp in structured_mapping.values():

        entries = {
            prop: {
                "classificaion": entry.classification,
                "css_class": CSS_CLASS[entry.classification],
                "extension": entry.extension,
                "extra": entry.extra,
                "profiles": entry.profiles,
                "remark": entry.remark,
            }
            for prop, entry in comp.fields.items()
        }

        data = {
            "css_file": STYLE_FILE_NAME,
            "target_profile": comp.target_profile,
            "source_profiles": comp.source_profiles,
            "entries": entries,
            "show_remarks": show_remarks,
        }

        content = template.render(**data)

        html_file = results_folder / f"{comp.target_profile}.html"
        html_file.write_text(content)


def format_links(text: str) -> str:
    if not text:
        return text

    # Regex zum Erkennen von URLs
    url_pattern = r"(https?://[\w\.\/\-\|]+)"
    # Ersetze URLs mit einem anklickbaren Link
    return re.sub(url_pattern, r'<a href="\1" target="_blank">\1</a>', text)
