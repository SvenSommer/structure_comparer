import json

def load_json_file(file_path):
    """
    Lädt JSON-Daten aus einer Datei.
    """
    with open(file_path, 'r') as file:
        return json.load(file)

def map_medication_code_coding(kbv_medication, epa_medication):
    """
    Mappt das Medication.code.coding-Element von einem KBV-Profil zum ePA-Profil.
    """
    if 'code' in kbv_medication and 'coding' in kbv_medication['code']:
        epa_medication['code'] = {'coding': []}
        for coding in kbv_medication['code']['coding']:
            epa_medication['code']['coding'].append({
                'system': coding.get('system', ''),
                'code': coding.get('code', ''),
                'display': coding.get('display', '')
            })

def map_medication_amount(kbv_medication, epa_medication):
    """
    Mappt das Medication.amount-Element von einem KBV-Profil zum ePA-Profil.
    """
    if 'amount' in kbv_medication:
        epa_medication['amount'] = {
            'numerator': {
                'value': kbv_medication['amount'].get('numerator', {}).get('value', ''),
                'unit': kbv_medication['amount'].get('numerator', {}).get('unit', ''),
                'system': 'http://unitsofmeasure.org',
                'code': kbv_medication['amount'].get('numerator', {}).get('code', '')
            },
            'denominator': {
                'value': kbv_medication['amount'].get('denominator', {}).get('value', ''),
                'unit': kbv_medication['amount'].get('denominator', {}).get('unit', ''),
                'system': 'http://unitsofmeasure.org',
                'code': kbv_medication['amount'].get('denominator', {}).get('code', '')
            }
        }

def main():
    kbv_file_path = 'data/Instances/KBV_PR_ERP_Medication.json'
    epa_file_path = 'data/Instances/example-epa-medication-2.json'

    # Lade KBV- und ePA-Medikationsdaten
    kbv_medication = load_json_file(kbv_file_path)
    epa_medication = load_json_file(epa_file_path)

    # Mapping durchführen
    map_medication_code_coding(kbv_medication, epa_medication)
    map_medication_amount(kbv_medication, epa_medication)

    # Ergebnis ausgeben
    print("Mapped ePA Medication:", json.dumps(epa_medication, indent=4))

if __name__ == "__main__":
    main()
