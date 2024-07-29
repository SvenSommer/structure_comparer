import json
from pathlib import Path
from typing import Dict

# TODO switch when type of `Element.id` was fixed
# from fhir.resources.R4B.structuredefinition import StructureDefinition


class FhirProfile:
    def __init__(self, data: dict) -> None:
        if data is None:
            raise ValueError("'data' shall not be None")

        if "snapshot" not in data:
            raise ValueError("'snapshot' is needed in data")

        self._data = data

        self._elements: Dict[str, "FhirProfileElement"] = {
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
    def elements(self) -> Dict[str, "FhirProfileElement"]:
        return self._elements

    def __getitem__(self, id: str) -> "FhirProfileElement":
        return self._elements.get(id)


class FhirProfileElement:
    def __init__(self, data: dict) -> None:
        if data is None:
            raise ValueError("'data' shall not be None")

        self._data = data

    @property
    def id(self) -> str:
        return self._data["id"]

    @property
    def path(self) -> str:
        return self._data["path"]

    @property
    def short(self) -> str:
        return self._data["short"]

    @property
    def min(self) -> int:
        return self._data["min"]

    @property
    def max(self) -> str:
        return self._data["max"]

    @property
    def type(self) -> str:
        value = self._data.get("type")
        return None if value is None else value[0]["code"]

    @property
    def must_support(self) -> bool:
        return self._data.get("mustSupport", False)
