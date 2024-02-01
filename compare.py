import json
import os
import re
from typing import List, Tuple, Dict, Any
import logging
import re
from pathlib import Path

from manual_entries import MANUAL_ENTRIES
from classification import Classification


CSS_CLASS = {
    Classification.USE: "row-use",
    Classification.NOT_USE: "row-not-use",
    Classification.EXTENSION: "row-extension",
    Classification.MANUAL: "row-manual",
    Classification.OTHER: "row-other",
}

REMARKS = {
    Classification.USE: "Eigenschaft und Wert werden übernommen",
    Classification.NOT_USE: "Bleibt vorerst leer, da keine Quellinformationen",
    Classification.EXTENSION: "Extension und Values werden übernommen",
    Classification.MANUAL: "",
    Classification.OTHER: "",
}

IGNORE_ENDS = ["id", "extension", "modifierExtension"]

IGNORE_SLICES = [
    "slice(url)",
    "slice($this)",
    "slice(system)",
    "slice(type)",
    "slice(use)",
    # workaround for 'slice(code.coding.system)'
    "system)",
]

MANUAL_SUFFIXES = ["reference", "profile"]

STRUCT_KBV_PROFILES = "kbv_profiles"
STRUCT_EPA_PROFILE = "epa_profile"
STRUCT_FIELDS = "fields"
STRUCT_EXTENSION = "extension"
STRUCT_CLASSIFICATION = "classification"
STRUCT_REMARK = "remark"

DICT_MAPPINGS = "mappings"
DICT_VALUES = "values"

logger = logging.getLogger()


def load_fhir_structure(file_path):
    """
    Loads the FHIR structure definition from a local JSON file.
    """
    with open(file_path, "r") as file:
        return json.load(file)


def should_ignore(path: str, ignore_paths: List[str]) -> bool:
    for ignored in ignore_paths:
        if path.startswith(ignored):
            return True
    return False


def get_extension(element: dict, path: str) -> str:
    if "extension" in element and "type" in element:
        for type_entry in element["type"]:
            if type_entry.get("code") == "Extension" and "profile" in type_entry:
                for profile in type_entry["profile"]:
                    extension_path = f"{path}<br>({profile})"
                    # Ignore extensions ending with 'slice(url)'
                    if not extension_path.endswith(
                        "slice(url)"
                    ) and not extension_path.endswith("slice($this)"):
                        return extension_path


def extract_elements(structure):
    elements = set()

    ignore_paths = []

    for element in structure["snapshot"]["element"]:
        path: str = element["id"]
        path_split = path.split(".")

        # Skip base element
        if len(path_split) == 1:
            continue

        # Skip elements that are children of ignored nodes
        if should_ignore(path, ignore_paths):
            continue

        # Ignore elements with having specific path endings
        if path_split[-1] in IGNORE_ENDS:
            continue

        # Ignore elements where the cardinality is set to zero
        if element["max"] == "0" or element["max"] == 0:
            # Extend list of nodes that are remove due cardinality
            ignore_paths.append(path)
            continue

        # Check for specific extensions
        if extension := get_extension(element, path):
            # Further ignore sub-elements of the extensions
            ignore_paths.append(path)
            elements.add(extension)
        else:
            # Add the base path of the element
            elements.add(path)

        # Check for and add slices, ignoring 'slice(url)' endings
        if "slicing" in element and "discriminator" in element["slicing"]:
            for discriminator in element["slicing"]["discriminator"]:
                if isinstance(discriminator, dict) and "path" in discriminator:
                    slice_path = f"{path}.slice({discriminator['path']})"
                    slice_path_split = slice_path.split(".")
                    if not slice_path_split[-1] in IGNORE_SLICES:
                        elements.add(slice_path)

    return elements


def compare_structures(kbv_structure, epa_structure):
    """
    Returns a set of all properties, extensions, and slices from both structures.
    """

    kbv_elements = extract_elements(kbv_structure)
    epa_elements = extract_elements(epa_structure)

    return kbv_elements | epa_elements


def determine_property_presence(profiles_to_compare, datapath):
    """
    Determines which properties are present in each set of KBV and ePA profiles.
    """
    all_properties = {}
    for kbv_group, epa_file in profiles_to_compare:
        epa_structure = load_fhir_structure(datapath + epa_file)
        combined_properties = set()

        for kbv_file in kbv_group:
            kbv_structure = load_fhir_structure(datapath + kbv_file)
            combined_properties |= compare_structures(kbv_structure, epa_structure)

        all_properties[(tuple(kbv_group), epa_file)] = combined_properties

    return all_properties


def check_property_presence(all_properties, profiles_to_compare, datapath):
    """
    Checks the presence of each property in each profile.
    """
    presence_data = {}
    for (kbv_group, epa_file), properties in all_properties.items():
        epa_structure = load_fhir_structure(datapath + epa_file)
        epa_elements = extract_elements(epa_structure)

        presence_data[(tuple(kbv_group), epa_file)] = {}
        for prop in properties:
            presence_data[(tuple(kbv_group), epa_file)][prop] = [prop in epa_elements]

            for kbv_file in kbv_group:
                kbv_structure = load_fhir_structure(datapath + kbv_file)
                kbv_elements = extract_elements(kbv_structure)
                presence_data[(tuple(kbv_group), epa_file)][prop].append(
                    prop in kbv_elements
                )

    return presence_data


def get_remark(prop: str, classification: Classification) -> str:
    return (
        MANUAL_ENTRIES[prop]["remark"]
        if prop in MANUAL_ENTRIES and "remark" in MANUAL_ENTRIES[prop]
        else REMARKS[classification]
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
    url_pattern = r"(https?://[^\s'\"<>]+)"
    # Ersetze URLs mit einem anklickbaren Link
    return re.sub(url_pattern, r'<a href="\1" target="_blank">\1</a>', text)


def classify_property(prop, kbv_presences, epa_presence):
    if prop in MANUAL_ENTRIES:
        return MANUAL_ENTRIES[prop].get("classification", Classification.MANUAL)
    if prop.split(".")[-1] in MANUAL_SUFFIXES:
        return Classification.MANUAL
    if any(kbv_presences):
        return Classification.USE if epa_presence else Classification.EXTENSION
    return Classification.NOT_USE


def is_light_color(hex_color: str) -> bool:
    r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return luminance > 0.5


def generate_html_table(
    rows: List[Tuple[List[str], Classification]], clean_kbv_group
) -> str:
    header = (
        "<thead><tr><th>Property</th>"
        + "".join(f"<th>{file}</th>" for file in clean_kbv_group)
        + "<th>ePA</th><th>Remarks</th></tr></thead>"
    )
    body = "<tbody>\n" + "\n".join(rows) + "</tbody>"
    return (
        "<table id='resultsTable' class='display' style='width:100%'>\n"
        + header
        + "\n"
        + body
        + "\n</table>"
    )


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
                generate_html_table(rows, clean_kbv_group),
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


def gen_structured_results(presence_data: dict) -> dict:
    """
    Generate a structured representation containing the rules for each target profile.

    The returned dictionary contains one item for each item in the argument `presence_data`. Each of these items
    contains the names of KBV and ePA profiles, presence information for each of their fields and their
    classifications and remarks.
    """
    mapping = {}
    # Iterate over all mappings (each entry are mapping to the same profile)
    for profiles, presences in presence_data.items():
        mapping[profiles] = {}

        # Generate the profile names
        kbv_profiles = [profile.replace(".json", "") for profile in profiles[0]]
        epa_profile = profiles[1].replace(".json", "")

        # Extract which profiles are KBV and which is the ePA one
        mapping[profiles][STRUCT_KBV_PROFILES] = kbv_profiles
        mapping[profiles][STRUCT_EPA_PROFILE] = epa_profile

        # Generate the mapping for all fields in those profiles
        mapping[profiles][STRUCT_FIELDS] = {}
        for field, field_presences in presences.items():
            field_updated = field
            extension_url = None

            # Get the field name while extracting the canonical for extensions
            if "extension" in field and "<br>" in field:
                field_updated, extension_url = field.split("<br>")
            mapping[profiles][STRUCT_FIELDS][field_updated] = {}
            if extension_url:
                mapping[profiles][STRUCT_FIELDS][field_updated][
                    STRUCT_EXTENSION
                ] = extension_url

            # Extract the presences for KBV and ePA profiles
            epa_presence, kbv_presences = field_presences[0], field_presences[1:]
            mapping[profiles][STRUCT_FIELDS][field_updated][epa_profile] = epa_presence
            for profile, presence in zip(kbv_profiles, kbv_presences):
                mapping[profiles][STRUCT_FIELDS][field_updated][profile] = presence

            # Fill the classification and remark for this field
            classification = classify_property(field, kbv_presences, epa_presence)
            mapping[profiles][STRUCT_FIELDS][field_updated][
                STRUCT_CLASSIFICATION
            ] = classification
            mapping[profiles][STRUCT_FIELDS][field_updated][STRUCT_REMARK] = get_remark(
                field, classification
            )

    return mapping


def gen_mapping_dict(structured_mapping: dict):
    result = {}

    # Regex to extract the field to copy this value to
    move_rexgex = re.compile(r"[wW]ird in ([\w\.\[\]:]+)")

    # Regex to extract the fixed value to set
    fix_regex = re.compile(r"Wird fix auf \'([\w:/\.-]+)' gesetzt")

    # Iterate over the different mappings
    for mappings in structured_mapping.values():
        epa_profile = mappings[STRUCT_EPA_PROFILE]

        # Iterate over the source profiles
        # These will be the roots of the mappings
        for kbv_profile in mappings[STRUCT_KBV_PROFILES]:
            profile_handling = {DICT_MAPPINGS: {}, DICT_VALUES: {}}
            for field, presences in mappings[STRUCT_FIELDS].items():
                classification = presences[STRUCT_CLASSIFICATION]
                remark = presences[STRUCT_REMARK]

                # If 'manual' and should always be set to a fixed value
                if classification == Classification.MANUAL and (
                    match := fix_regex.search(remark)
                ):
                    profile_handling[DICT_VALUES][field] = match.group(1)

                # Otherwise only if value is present
                elif presences[kbv_profile]:
                    # If field should be used and remark was not changed
                    if (
                        classification in [Classification.USE, Classification.EXTENSION]
                        and remark == REMARKS[classification]
                    ):
                        # Put value in the same field
                        profile_handling[DICT_MAPPINGS][field] = field

                    # If the field should be placed in other field
                    elif classification in [
                        Classification.USE,
                        Classification.EXTENSION,
                        Classification.MANUAL,
                    ] and (match := move_rexgex.search(remark)):
                        # Get new field from regex
                        profile_handling[DICT_MAPPINGS][field] = match.group(1)

                    # Do not handle when 'not use'
                    elif classification == Classification.NOT_USE:
                        pass
                    else:
                        # Log fall-through
                        logger.warning(
                            f"gen_mapping_dict: did not handle {kbv_profile}:{epa_profile}:{field}:{classification} {remark}"
                        )

            profile_handling[DICT_MAPPINGS] = {
                key: value
                for key, value in sorted(profile_handling[DICT_MAPPINGS].items())
            }
            profile_handling[DICT_VALUES] = {
                key: value
                for key, value in sorted(profile_handling[DICT_VALUES].items())
            }

            result[kbv_profile] = {epa_profile: profile_handling}

    return result


# Define the datapath
datapath = "data/StructureDefinition/"

# Define the profiles to compare
profiles_to_compare = [
    (
        [
            "KBV_PR_ERP_Medication_Compounding.json",
            "KBV_PR_ERP_Medication_FreeText.json",
            "KBV_PR_ERP_Medication_Ingredient.json",
            "KBV_PR_ERP_Medication_PZN.json",
        ],
        "epa-medication.json",
    ),
    (["KBV_PR_FOR_Practitioner.json"], "PractitionerDirectory.json"),
    (["KBV_PR_ERP_Prescription.json"], "epa-medication-request.json"),
    (["KBV_PR_FOR_Organization.json"], "OrganizationDirectory.json"),
]

# Determine which properties are present in each profile
all_properties = determine_property_presence(profiles_to_compare, datapath)

# Check the presence of each property in each profile
presence_data = check_property_presence(all_properties, profiles_to_compare, datapath)

# Generate a structured version of the presence data
structured_mapping = gen_structured_results(presence_data)

# Create the result html files
create_results_html(structured_mapping, "./style.css")

# Generate the mapping dict and write to file
mapping_dict = gen_mapping_dict(structured_mapping)
Path("mapping.json").write_text(json.dumps(mapping_dict, indent=4))
