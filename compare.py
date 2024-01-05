import json

def load_fhir_structure(file_path):
    """
    Lädt die FHIR Strukturdefinition aus einer lokalen JSON-Datei.
    """
    with open(file_path, 'r') as file:
        return json.load(file)

def compare_structures(kbv_structure, epa_structure):
    """
    Vergleicht eine KBV-Strukturdefinition mit dem ePA-Profil.
    Es wird geprüft, ob alle Eigenschaften des KBV-Profils im ePA-Profil vorhanden sind.
    """
    kbv_elements = {element['path']: element for element in kbv_structure['snapshot']['element']}
    epa_elements = {element['path']: element for element in epa_structure['snapshot']['element']}
    missing_in_epa = []

    for path in kbv_elements:
        if path not in epa_elements:
            missing_in_epa.append(path)

    return missing_in_epa

def compare_all_kbv_to_epa(kbv_files, epa_file):
    """
    Vergleicht alle KBV-Profile mit dem ePA-Profil und berichtet über fehlende Eigenschaften im ePA-Profil.
    """
    epa_structure = load_fhir_structure(epa_file)
    for kbv_file in kbv_files:
        kbv_structure = load_fhir_structure(kbv_file)
        print(f"\nVergleich von {kbv_file} mit ePA-Profil:")
        missing_in_epa = compare_structures(kbv_structure, epa_structure)
        if not missing_in_epa:
            print("Alle Eigenschaften des KBV-Profils sind im ePA-Profil vorhanden.")
        else:
            print("Folgende Eigenschaften des KBV-Profils fehlen im ePA-Profil:")
            for path in missing_in_epa:
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
