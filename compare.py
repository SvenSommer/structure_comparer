import json

def load_fhir_structure(file_path):
    """
    Loads the FHIR structure definition from a local JSON file.
    """
    with open(file_path, 'r') as file:
        return json.load(file)

def compare_structures(kbv_structure, epa_structure):
    """
    Compares a KBV structure definition with the ePA profile.
    Checks if all properties of the KBV profile are present in the ePA profile.
    """
    kbv_elements = {element['path']: element for element in kbv_structure['snapshot']['element']}
    epa_elements = {element['path']: element for element in epa_structure['snapshot']['element']}
    missing_in_epa = []

    for path in kbv_elements:
        if path not in epa_elements:
            missing_in_epa.append(path)

    return sorted(missing_in_epa)

def compare_all_kbv_to_epa(kbv_files, epa_file):
    """
    Compares all KBV profiles with the ePA profile and reports on properties from the KBV profiles missing in the ePA profile.
    """
    epa_structure = load_fhir_structure(epa_file)
    all_missing = []
    individual_missing = {}

    for kbv_file in kbv_files:
        kbv_structure = load_fhir_structure(kbv_file)
        missing_in_epa = compare_structures(kbv_structure, epa_structure)
        individual_missing[kbv_file] = missing_in_epa
        all_missing.extend(missing_in_epa)

    # Find properties from KBV profiles missing in the ePA profile
    missing_in_all = set(all_missing)
    for missing in individual_missing.values():
        missing_in_all.intersection_update(missing)

    # Sort and display properties from KBV profiles missing in the ePA profile
    print("\nProperties from KBV profiles missing in the ePA profile:")
    for path in sorted(missing_in_all):
        print(path)

    # Display specific properties from each KBV profile missing in the ePA profile
    for kbv_file, missing in individual_missing.items():
        specific_missing = sorted(set(missing) - missing_in_all)
        print(f"\nProperties from KBV Profile '{kbv_file}' missing in the ePA profile:")
        for path in specific_missing:
            print(path)

def main():
    epa_file = 'data/StructureDefinition/epa-medication.json'
    kbv_files = [
        'data/StructureDefinition/KBV_PR_ERP_Medication_Compounding.json',
        'data/StructureDefinition/KBV_PR_ERP_Medication_FreeText.json',
        'data/StructureDefinition/KBV_PR_ERP_Medication_Ingredient.json',
        'data/StructureDefinition/KBV_PR_ERP_Medication_PZN.json'
    ]

    compare_all_kbv_to_epa(kbv_files, epa_file)

if __name__ == "__main__":
    main()
