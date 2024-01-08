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

    return set(missing_in_epa)

def compare_all_kbv_to_epa(kbv_files, epa_file):
    """
    Compares all KBV profiles with the ePA profile and reports on properties from the KBV profiles missing in the ePA profile.
    """
    epa_structure = load_fhir_structure(epa_file)
    individual_missing = {}
    common_missing = None

    for kbv_file in kbv_files:
        kbv_structure = load_fhir_structure(kbv_file)
        missing_in_epa = compare_structures(kbv_structure, epa_structure)
        individual_missing[kbv_file] = missing_in_epa

        if common_missing is None:
            common_missing = missing_in_epa
        else:
            common_missing.intersection_update(missing_in_epa)

    # Display properties missing in all KBV profiles
    print("\nProperties missing in the ePA profile and present in all KBV profiles:")
    for path in sorted(common_missing):
        print(path)

    # Display specific properties missing in each KBV profile, not included in the common list
    for kbv_file, missing in individual_missing.items():
        specific_missing = sorted(missing - common_missing)
        if specific_missing:
            print(f"\nAdditional properties missing in KBV Profile '{kbv_file}', not in common missing list:")
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
