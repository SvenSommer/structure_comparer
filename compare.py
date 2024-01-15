import json
import os

def load_fhir_structure(file_path):
    """
    Loads the FHIR structure definition from a local JSON file.
    """
    with open(file_path, 'r') as file:
        return json.load(file)

def extract_elements(structure):
    elements = set()
    for element in structure['snapshot']['element']:
        path = element['path']
        path_split = path.split('.')

        # Ignore elements with having specific path endings
        ignore_ends = ['id']
        if path_split[-1] == 'id':
            continue

        # Ignore elements where the cardinality is set to zero
        if element['max'] == '0' or element['max'] == 0:
            continue

        # Add the base path of the element
        elements.add(path)

        # Check for specific extensions
        if 'extension' in element and 'type' in element:
            for type_entry in element['type']:
                if type_entry.get('code') == 'Extension' and 'profile' in type_entry:
                    for profile in type_entry['profile']:
                        extension_path = f"{path}:{element.get('sliceName', '')}({profile})"
                        # Ignore extensions ending with 'slice(url)'
                        if not extension_path.endswith('slice(url)') and not extension_path.endswith('slice($this)') :
                            elements.add(extension_path)

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

def determine_remark(prop, presences):
    """
    Generates a remark based on the presence of the property in all profiles
    and if it's an extension in the KBV profiles.
    """
    if all(presences):
        return "Eigenschaft und Wert werden übernommen"
    elif any("extension" in prop for presence in presences if presence):
        return "Extension und Values werden übernommen"
    else:
        return ""

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
            md_file.write(f"## Comparison: {', '.join(clean_kbv_group)} vs {clean_epa_file}\n")
            md_file.write("| Property | " + " | ".join([f"{kbv_file}" for kbv_file in clean_kbv_group]) + " | ePA | Bemerkungen |\n")
            md_file.write("|---" * (len(clean_kbv_group) + 3) + "|\n")

            for prop in sorted(data.keys()):
                # Escape pipe symbols in property names
                prop_escaped = prop.replace('|', '&#124;')
                presences = data[prop]
                remark = determine_remark(prop, presences)
                row = f"| {prop_escaped} | " + " | ".join(["X" if presence else "" for presence in presences[1:]]) + " | " + ("X" if presences[0] else "") + f" | {remark} |\n"
                md_file.write(row)


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
