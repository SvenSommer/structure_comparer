import json
import os
from typing import List, Tuple

from manual_entries import MANUAL_ENTRIES
from classification import Classification


COLORS = {
    Classification.USE: "#E3FCEF",
    Classification.NOT_USE: "#FFEBE6",
    Classification.EXTENSION: "#FFFAE6",
    Classification.MANUAL: "#B3F5FF",
    Classification.OTHER: "#FFBDAD"
}

REMARKS = {
    Classification.USE: "Eigenschaft und Wert werden übernommen",
    Classification.NOT_USE: "Bleibt vorerst leer, da keine Quellinformationen",
    Classification.EXTENSION: "Extension und Values werden übernommen",
    Classification.MANUAL: "",
    Classification.OTHER: ""
}

IGNORE_ENDS = [
    'id',
    'extension',
    'modifierExtension'
]

IGNORE_SLICES = [
    'slice(url)',
    'slice($this)',
    'slice(system)',
    'slice(type)',
    'slice(use)',
    # workaround for 'slice(code.coding.system)'
    'system)'
]

MANUAL_SUFFIXES = [
    "reference",
    "profile"
]

def load_fhir_structure(file_path):
    """
    Loads the FHIR structure definition from a local JSON file.
    """
    with open(file_path, 'r') as file:
        return json.load(file)

def should_ignore(path: str, ignore_paths: List[str]) -> bool:
    for ignored in ignore_paths:
        if path.startswith(ignored):
            return True
    return False

def get_extension(element: dict, path: str) -> str :
    if 'extension' in element and 'type' in element:
        for type_entry in element['type']:
            if type_entry.get('code') == 'Extension' and 'profile' in type_entry:
                for profile in type_entry['profile']:
                    extension_path = f"{path}<br>({profile})"
                    # Ignore extensions ending with 'slice(url)'
                    if not extension_path.endswith('slice(url)') and not extension_path.endswith('slice($this)') :
                        return extension_path

def extract_elements(structure):
    elements = set()

    ignore_paths = []

    for element in structure['snapshot']['element']:
        path: str = element['id']
        path_split = path.split('.')

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
        if element['max'] == '0' or element['max'] == 0:
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
        if 'slicing' in element and 'discriminator' in element['slicing']:
            for discriminator in element['slicing']['discriminator']:
                if isinstance(discriminator, dict) and 'path' in discriminator:
                    slice_path = f"{path}.slice({discriminator['path']})"
                    slice_path_split = slice_path.split('.')
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
                presence_data[(tuple(kbv_group), epa_file)][prop].append(prop in kbv_elements)

    return presence_data

def gen_row(prop: str, presences: List[str]) -> Tuple[List[str], Classification]:
    kbv_presences, epa_presence = presences[1:], presences[0]
    
    classification = classify_property(prop, kbv_presences, epa_presence)
    remark = MANUAL_ENTRIES[prop]['remark'] if prop in MANUAL_ENTRIES and 'remark' in MANUAL_ENTRIES[prop] else REMARKS[classification]
    row_data = [prop] + ["X" if presence else "" for presence in presences[1:]] + [remark]
    
    return row_data, classification

def classify_property(prop, kbv_presences, epa_presence):
    if prop in MANUAL_ENTRIES:
        return MANUAL_ENTRIES[prop].get("classification", Classification.MANUAL)
    if prop.split('.')[-1] in MANUAL_SUFFIXES:
        return Classification.MANUAL
    if any(kbv_presences):
        return Classification.USE if epa_presence else Classification.EXTENSION
    return Classification.NOT_USE

def is_light_color(hex_color: str) -> bool:
    r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return luminance > 0.5

def gen_table_style(classifications: List[Classification]) -> str:
    styles = []
    for idx, classification in enumerate(classifications):
        bg_color = COLORS.get(classification, "#FFFFFF")
        text_color = "#000000" if is_light_color(bg_color) else "#FFFFFF"
        # Increased specificity by targeting the tbody and using !important
        styles.append(f"#resultsTable tbody tr:nth-child({idx + 1}) {{ background-color: {bg_color} !important; color: {text_color} !important; }}")

    return "<style>\n" + "\n".join(styles) + "\n</style>"



def generate_html_table(rows: List[Tuple[List[str], Classification]], clean_kbv_group) -> str:
    header = "<thead><tr><th>Property</th>" + "".join(f"<th>{file}</th>" for file in clean_kbv_group) + "<th>ePA</th><th>Remarks</th></tr></thead>"
    body = "<tbody>\n" + "\n".join("<tr>" + "".join(f"<td>{item}</td>" for item in row_data) + "</tr>" for row_data, _ in rows) + "</tbody>"
    return "<table id='resultsTable' class='display' style='width:100%'>\n" + header + "\n" + body + "\n</table>"

def create_results_html(presence_data):
    results_folder = 'docs'
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    for (kbv_group, epa_file), data in presence_data.items():
        clean_kbv_group = [file.replace('.json', '') for file in kbv_group]
        clean_epa_file = epa_file.replace('.json', '')
        file_path = os.path.join(results_folder, f"{clean_epa_file}.html")
        with open(file_path, 'w') as html_file:
            rows = [gen_row(prop, presences) for prop, presences in sorted(data.items())]
            _, classifications = zip(*rows)

            html_table = [
                "<html><head><title>Comparison Results</title>",
                "<link rel='stylesheet' type='text/css' href='https://cdn.datatables.net/1.11.3/css/jquery.dataTables.min.css'>",
                "<script type='text/javascript' src='https://code.jquery.com/jquery-3.6.0.min.js'></script>",
                "<script type='text/javascript' src='https://cdn.datatables.net/1.11.3/js/jquery.dataTables.min.js'></script>",
                "</head><body>",
                gen_table_style(classifications),
                f"<h2>Comparison: {', '.join(clean_kbv_group)} vs {clean_epa_file}</h2>",
                generate_html_table(rows, clean_kbv_group),
                "<script>",
                "$(document).ready(function() {",
                "    $('#resultsTable').DataTable();",
                "});",
                "</script>",
                "</body></html>"
            ]

            html_file.write('\n'.join(html_table))






# Define the datapath
datapath = 'data/StructureDefinition/'

# Define the profiles to compare
profiles_to_compare = [
    ([
        'KBV_PR_ERP_Medication_Compounding.json',
        'KBV_PR_ERP_Medication_FreeText.json',
        'KBV_PR_ERP_Medication_Ingredient.json',
        'KBV_PR_ERP_Medication_PZN.json'
    ], 'epa-medication.json'),
    (['KBV_PR_FOR_Practitioner.json'], 'PractitionerDirectory.json'),
    (['KBV_PR_ERP_Prescription.json'], 'epa-medication-request.json'),
    (['KBV_PR_FOR_Organization.json'], 'OrganizationDirectory.json')
]

# Determine which properties are present in each profile
all_properties = determine_property_presence(profiles_to_compare, datapath)

# Check the presence of each property in each profile
presence_data = check_property_presence(all_properties, profiles_to_compare, datapath)

# Create the result html files
create_results_html(presence_data)
