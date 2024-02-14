# Generate a structured version of the presence data
import json
from pathlib import Path

from structure_comparer import compare_profiles, gen_mapping_dict, create_results_html

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


structured_mapping = compare_profiles(profiles_to_compare, datapath)

# Create the result html files
create_results_html(structured_mapping, "./style.css")

# Generate the mapping dict and write to file
mapping_dict = gen_mapping_dict(structured_mapping)
Path("mapping.json").write_text(json.dumps(mapping_dict, indent=4))
