import json

def load_fhir_structure(file_path):
    """
    Loads the FHIR structure definition from a local JSON file.
    """
    with open(file_path, 'r') as file:
        return json.load(file)

def compare_structures(kbv_structure, epa_structure):
    """
    Returns a set of all properties from both structures.
    """
    kbv_elements = {element['path']: element for element in kbv_structure['snapshot']['element']}
    epa_elements = {element['path']: element for element in epa_structure['snapshot']['element']}

    return set(kbv_elements.keys()) | set(epa_elements.keys())

def determine_property_presence(profiles_to_compare, datapath):
    """
    Determines which properties are present in each profile.
    """
    all_properties = {}
    for kbv_group, epa_file in profiles_to_compare:
        epa_structure = load_fhir_structure(datapath + epa_file)
        properties = set()

        for kbv_file in kbv_group:
            kbv_structure = load_fhir_structure(datapath + kbv_file)
            properties |= compare_structures(kbv_structure, epa_structure)

        all_properties[(tuple(kbv_group), epa_file)] = properties

    return all_properties

def check_property_presence(all_properties, profiles_to_compare, datapath):
    """
    Checks presence of each property in each profile.
    """
    presence_data = {}
    for (kbv_group, epa_file), properties in all_properties.items():
        epa_structure = load_fhir_structure(datapath + epa_file)
        epa_elements = {element['path']: element for element in epa_structure['snapshot']['element']}

        presence_data[(tuple(kbv_group), epa_file)] = {}
        for prop in properties:
            presence_data[(tuple(kbv_group), epa_file)][prop] = [prop in epa_elements]

            for kbv_file in kbv_group:
                kbv_structure = load_fhir_structure(datapath + kbv_file)
                kbv_elements = {element['path']: element for element in kbv_structure['snapshot']['element']}
                presence_data[(tuple(kbv_group), epa_file)][prop].append(prop in kbv_elements)

    return presence_data

def create_results_md(presence_data):
    """
    Creates a Markdown file with comparison results, sorted alphabetically by property.
    """
    with open('results.md', 'w') as md_file:
        for (kbv_group, epa_file), data in presence_data.items():
            md_file.write(f"## Comparison: {', '.join(kbv_group)} vs {epa_file}\n")
            md_file.write("| Property | ePA | " + " | ".join([f"{kbv_file}" for kbv_file in kbv_group]) + " |\n")
            md_file.write("|---" * (len(kbv_group) + 2) + "|\n")

            # Sort properties alphabetically
            for prop in sorted(data.keys()):
                presences = data[prop]
                row = f"| {prop} | " + " | ".join(["X" if presence else "" for presence in presences]) + " |\n"
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
