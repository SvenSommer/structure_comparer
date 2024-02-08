import os
import re
from typing import Any, Dict, List, Tuple

from classification import Classification
from consts import (
    STRUCT_CLASSIFICATION,
    STRUCT_EPA_PROFILE,
    STRUCT_EXTENSION,
    STRUCT_FIELDS,
    STRUCT_KBV_PROFILES,
    STRUCT_REMARK,
)


CSS_CLASS = {
    Classification.USE: "row-use",
    Classification.NOT_USE: "row-not-use",
    Classification.EXTENSION: "row-extension",
    Classification.MANUAL: "row-manual",
    Classification.OTHER: "row-other",
    Classification.COPY_FROM: "row-use",
    Classification.COPY_TO: "row-use",
    Classification.FIXED: "row-manual",
}


def create_results_html(structured_mapping, css_file_path):
    results_folder = "docs"
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    for data in structured_mapping.values():
        clean_kbv_group = data[STRUCT_KBV_PROFILES]
        clean_epa_file = data[STRUCT_EPA_PROFILE]
        profile_headers = data[STRUCT_KBV_PROFILES] + [data[STRUCT_EPA_PROFILE]]
        file_path = os.path.join(results_folder, f"{clean_epa_file}.html")
        with open(file_path, "w") as html_file:
            rows = [
                gen_row(prop, details, profile_headers)
                for prop, details in sorted(data[STRUCT_FIELDS].items())
            ]

            html_table = [
                "<!DOCTYPE html>",
                f"<html><head><title>Mapping: {clean_epa_file}</title>",
                f"<link rel='stylesheet' type='text/css' href='{css_file_path}'>",
                "<link rel='stylesheet' type='text/css' href='https://cdn.datatables.net/1.11.3/css/jquery.dataTables.min.css'>",
                "<script type='text/javascript' src='https://code.jquery.com/jquery-3.6.0.min.js'></script>",
                "<script type='text/javascript' src='https://cdn.datatables.net/1.11.3/js/jquery.dataTables.min.js'></script>",
                "</head><body>",
                f"<h2>Mapping: {', '.join(clean_kbv_group)} in {clean_epa_file}</h2>",
                generate_html_table(rows, clean_kbv_group, clean_epa_file),
                "<script>",
                "$(document).ready(function() {",
                "    $('#resultsTable').DataTable({",
                "        'pageLength': 25,",
                "        'lengthMenu': [[10, 25, 50, 100, 500, -1], [10, 25, 50, 100, 150, 'All']]",
                "    });",
                "});",
                "</script>",
                "</body></html>",
            ]

            html_file.write("\n".join(html_table))


def generate_html_table(
    rows: List[Tuple[List[str], Classification]],
    clean_kbv_group: List[str],
    clean_epa_file: str,
) -> str:
    header = (
        "<thead><tr><th>Property</th>"
        + "".join(f"<th>{file}</th>" for file in clean_kbv_group)
        + f"<th>{clean_epa_file}</th><th>Remarks</th></tr></thead>"
    )
    body = "<tbody>\n" + "\n".join(rows) + "</tbody>"
    return (
        "<table id='resultsTable' class='display' style='width:100%'>\n"
        + header
        + "\n"
        + body
        + "\n</table>"
    )


def gen_row(
    prop: str, details: Dict[str, Any], profile_headers: List[str]
) -> Tuple[List[str], Classification]:
    # Erkenne und formatiere URLs in den Bemerkungen
    remark = format_links(details[STRUCT_REMARK])

    # Erkenne und formatiere URLs in den Property-Werten
    if ext := details.get(STRUCT_EXTENSION):
        prop = format_links(prop + "<br>" + ext)

    formatted_presences = [
        "X" if details[profile] else "" for profile in profile_headers
    ]
    row_data = f"""<tr class="{CSS_CLASS[details[STRUCT_CLASSIFICATION]]}">
    <td>{prop}</td>
    {"".join(f"<td>{item}</td>" for item in formatted_presences)}
    <td>{remark}</td>
</tr>"""

    return row_data


def format_links(text: str) -> str:
    # Regex zum Erkennen von URLs
    url_pattern = r"(https?://[\w\.\/\-\|]+)"
    # Ersetze URLs mit einem anklickbaren Link
    return re.sub(url_pattern, r'<a href="\1" target="_blank">\1</a>', text)
