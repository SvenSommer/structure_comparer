import json
from pathlib import Path
from structure_comparer.data.fhir_profile import FhirProfile

PROFILE_FILE = "service/tests/files/project/data/StructureDefinition-observation-de-vitalsign.json"


def test_fhir_profile_from_json():
    file = Path(PROFILE_FILE)

    assert file.exists()

    result = FhirProfile.from_json(file)

    assert result.name == "VitalSignDE"
    assert result.title == "Observation-Profil VitalSignDE"
    assert result.version == "1.5.0"
    assert result.status == "active"
    assert result.url == "http://fhir.de/StructureDefinition/observation-de-vitalsign"
    assert result.date == "2023-11-30"
    assert result.type == "Observation"
    assert result.base_definition == "http://hl7.org/fhir/StructureDefinition/Observation"


def test_fhir_profile_init_snapshot_missing():
    input = json.loads(Path(PROFILE_FILE).read_text())

    del input["snapshot"]

    try:
        FhirProfile(input)
    except ValueError:
        pass
    else:
        assert False
