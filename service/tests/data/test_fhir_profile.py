import json
from pathlib import Path
from structure_comparer.data.fhir_profile import FhirProfile

PROFILE_FILE = (
    "service/tests/files/project/data/StructureDefinition-observation-de-vitalsign.json"
)


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
    assert (
        result.base_definition == "http://hl7.org/fhir/StructureDefinition/Observation"
    )

    assert "Observation" in result.elements
    assert result["Observation"].id == "Observation"
    assert result["Observation"].path == "Observation"
    assert result["Observation"].min == 0
    assert result["Observation"].max == "*"
    assert not result["Observation"].must_support
    assert result["Observation"].type is None

    assert "Observation.id" in result.elements
    assert result["Observation.id"].id == "Observation.id"
    assert result["Observation.id"].path == "Observation.id"
    assert result["Observation.id"].min == 0
    assert result["Observation.id"].max == "1"
    assert not result["Observation.id"].must_support
    assert result["Observation.id"].type == "http://hl7.org/fhirpath/System.String"

    assert "Observation.code.coding:loinc" in result.elements
    assert result["Observation.code.coding:loinc"].id == "Observation.code.coding:loinc"
    assert result["Observation.code.coding:loinc"].path == "Observation.code.coding"
    assert result["Observation.code.coding:loinc"].min == 1
    assert result["Observation.code.coding:loinc"].max == "*"
    assert not result["Observation.code.coding:loinc"].must_support
    assert result["Observation.code.coding:loinc"].type == "Coding"


def test_fhir_profile_init_snapshot_missing():
    input = json.loads(Path(PROFILE_FILE).read_text())

    del input["snapshot"]

    try:
        FhirProfile(input)
    except ValueError:
        pass
    else:
        assert False
