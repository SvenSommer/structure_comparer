import json
from pathlib import Path
from typing import List

# from fhir.resources.R4B.structuredefinition import StructureDefinition


class FhirProfile:
    def __init__(self, data: dict) -> None:
        if data is None:
            raise ValueError("'data' shall not be None")

        if "snapshot" not in data:
            raise ValueError("'snapshot' is needed in data")

        self._data = data

        self._elements = {
            element["id"]: FhirProfileElement(element)
            for element in data["snapshot"]["element"]
        }

    @staticmethod
    def from_json(file_path: Path) -> "FhirProfile":
        # TODO switch to `fhir.resources` for validation
        # currently raises validation errors on type sliced IDs
        # StructureDefinition.parse_file(file_path)

        data = json.loads(file_path.read_text())

        if data["resourceType"] != "StructureDefinition":
            raise ValueError("not a StructureDefinition")

        return FhirProfile(data)

    @property
    def url(self) -> str:
        return self._data["url"]

    @property
    def version(self) -> str:
        return self._data["version"]

    @property
    def name(self) -> str:
        return self._data["name"]

    @property
    def title(self) -> str:
        return self._data["title"]

    @property
    def status(self) -> str:
        return self._data["status"]

    @property
    def date(self) -> str:
        return self._data["date"]

    @property
    def type(self) -> str:
        return self._data["type"]

    @property
    def base_definition(self) -> str:
        return self._data["baseDefinition"]

    @property
    def element_names(self) -> List[str]:
        return list(self._elements.keys())

    @property
    def elements(self) -> List["FhirProfileElement"]:
        return list(self._elements.values())

    def __getitem__(self, id: str) -> "FhirProfileElement":
        return self._elements.get(id)


class FhirProfileElement:
    def __init__(self, data: dict) -> None:
        if data is None:
            raise ValueError("'data' shall not be None")

        self._data = data
