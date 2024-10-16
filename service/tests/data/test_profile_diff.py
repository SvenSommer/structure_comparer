from pathlib import Path
from structure_comparer.data.fhir_profile import FhirProfile
from structure_comparer.data.profile_diff import (
    ProfileDiff,
    EntryClassification as EntryClass,
)


FILE_LEFT = (
    "service/tests/files/project/data/StructureDefinition-observation-de-vitalsign.json"
)
FILE_RIGHT = "service/tests/files/project/data/StructureDefinition-observation-de-vitalsign-atemfrequenz.json"


def test_profile_diff_compare():
    left = FhirProfile.from_json(Path(FILE_LEFT))
    right = FhirProfile.from_json(Path(FILE_RIGHT))

    diff = ProfileDiff.compare(left, right)

    only_right = [
        "Observation.code.coding:loinc.id",
        "Observation.code.coding:loinc.extension",
        "Observation.code.coding:loinc.system",
        "Observation.code.coding:loinc.version",
        "Observation.code.coding:loinc.code",
        "Observation.code.coding:loinc.display",
        "Observation.code.coding:loinc.userSelected",
        "Observation.code.coding:snomed.id",
        "Observation.code.coding:snomed.extension",
        "Observation.code.coding:snomed.system",
        "Observation.code.coding:snomed.version",
        "Observation.code.coding:snomed.code",
        "Observation.code.coding:snomed.display",
        "Observation.code.coding:snomed.userSelected",
    ]

    for elem, entry in diff._data.items():
        if elem in only_right:
            assert entry.classification == EntryClass.ONLY_RIGHT
        else:
            assert entry.classification == EntryClass.SAME
