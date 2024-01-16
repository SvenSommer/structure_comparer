import json
import os
from typing import List, Tuple
from enum import Enum


class Classification(Enum):
    USE = 1
    NOT_USE = 2
    EXTENSION = 3
    MANUAL = 4
    OTHER = 5

COLORS = {
    Classification.USE: "lightgreen",
    Classification.NOT_USE: "LightPink",
    Classification.EXTENSION: "yellow",
    Classification.MANUAL: "lightcyan",
    Classification.OTHER: "red"
}

REMARKS = {
    Classification.USE: "Eigenschaft und Wert werden übernommen",
    Classification.NOT_USE: "Bleibt vorerst leer, da keine Quellinformationen",
    Classification.EXTENSION: "Extension und Values werden übernommen",
    Classification.MANUAL: "",
    Classification.OTHER: ""
}

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

def get_extension(element: dict, path: str) -> str | None:
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

        # Skip elements that are children of ignored nodes
        if should_ignore(path, ignore_paths):
            continue

        # Ignore elements with having specific path endings
        ignore_ends = ['id', 'extension', 'modifierExtension', 'text']
        if path_split[-1] in ignore_ends:
            continue

        # TODO: reference

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
                    if not slice_path.endswith('slice(url)') and not slice_path.endswith('slice($this)'):
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

def gen_row(prop: str, presences: List[str]) -> Tuple[str, Classification]:
    """
    Generates a row for the MD file and returns classification for style entry
    """
    # Escape pipe symbols in property names
    prop_escaped = prop.replace('|', '&#124;')

    # Split presences into KBV and ePA ones
    kbv_presences, epa_presence = presences[1:], presences[0]

    # Determine classification based on presences
    if prop.split('.')[-1] in MANUAL_SUFFIXES:
        classification = Classification.MANUAL
    elif any(kbv_presences):
        if epa_presence:
            classification = Classification.USE
        else:
            classification = Classification.EXTENSION
    else:
        classification = Classification.NOT_USE

    row = row = [prop_escaped] + ["X" if presence else "" for presence in presences[1:]] + ["X" if presences[0] else "", REMARKS[classification]]
    row = "| " + " | ".join(row) + " |"
    return row, classification

def gen_table_style(classifications: List[Classification]) -> str:
    styles = [f"    .compTable tr:nth-child({idx+1}) {{ background: {COLORS[classification]}; }}" for idx, classification in enumerate(classifications)]
    style_lines = ["<style>"] + styles + ["</style>"]
    return "\n".join(style_lines)

def create_results_md(presence_data):
    """
    Creates individual Markdown files for each comparison result, sorted alphabetically by property.
    Files are named after the ePA profile and stored in a 'results' folder.
    Displays KBV profiles first, followed by the ePA profile, and adds an empty "Remarks" column.
    Removes '.json' from file names in the display. Escapes pipe symbols in property names.
    """
    results_folder = 'results'
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    for (kbv_group, epa_file), data in presence_data.items():
        clean_kbv_group = [kbv_file.replace('.json', '') for kbv_file in kbv_group]
        clean_epa_file = epa_file.replace('.json', '')
        file_path = os.path.join(results_folder, f"{clean_epa_file}.md")

        with open(file_path, 'w') as md_file:
            # Process the rows
            rows = [gen_row(prop, presences) for prop, presences in sorted(data.items())]
            # Extract the property rows and classifications
            property_lines, classifications = list(zip(*rows))
            lines = [
                f"## Comparison: {', '.join(clean_kbv_group)} vs {clean_epa_file}",
                gen_table_style(classifications),
                "<div class=\"compTable\">\n",
                "| Property | " + " | ".join([f"{kbv_file}" for kbv_file in clean_kbv_group]) + " | ePA | Bemerkungen |",
                "|---" * (len(clean_kbv_group) + 3) + "|",
                ]
            lines += property_lines
            lines.append("</div>")

            md_file.write('\n'.join(lines))


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

# Create the results.md file
create_results_md(presence_data)
