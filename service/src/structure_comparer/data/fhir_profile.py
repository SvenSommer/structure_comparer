import json
from pathlib import Path
from typing import Any, Dict, List

# TODO switch when type of `Element.id` was fixed
# from fhir.resources.R4B.structuredefinition import StructureDefinition


class FhirProfile:
    def __init__(
        self,
        data: dict,
        simplifier_url: str = None,
        file_download_url: str = None,
        **kwargs,
    ) -> None:
        if data is None:
            raise ValueError("'data' shall not be None")

        if "snapshot" not in data:
            raise ValueError("'snapshot' is needed in data")

        self._data = data
        self._simplifier_url = simplifier_url
        self._file_download_url = file_download_url

        self._elements: Dict[str, "FhirProfileElement"] = {
            element["id"]: FhirProfileElement(element)
            for element in data["snapshot"]["element"]
            if element["id"] != data["type"]
        }

    @staticmethod
    def from_json(file_path: Path, **kwargs) -> "FhirProfile":
        # TODO switch to `fhir.resources` for validation
        # currently raises validation errors on type sliced IDs
        # StructureDefinition.parse_file(file_path)

        data = json.loads(file_path.read_text())

        if data["resourceType"] != "StructureDefinition":
            raise ValueError("not a StructureDefinition")

        return FhirProfile(data, **kwargs)

    @property
    def simplifier_url(self) -> str:
        return self._simplifier_url

    @property
    def file_download_url(self) -> str:
        return self._file_download_url

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

        self._extensions: Dict[str, Any] = {}
        if extensions := data.get("extension"):
            for extension in extensions:
                url: str = extension.get("url")

                for key, value in extension.items():
                    if key.startswith("value"):
                        self._extensions[url] = value

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

    @property
    def extension(self) -> Dict[str, Any]:
        return self._extensions

    def diff(self, o: object) -> List[str]:
        diff = []

        if not isinstance(o, FhirProfileElement):
            raise TypeError(f"cannot compare FhirProfileElement with {type(o)}")

        if self.id != o.id:
            diff.append(f"id: {self.id} != {o.id}")

        if self.min != o.min:
            diff.append(f"min: {self.min} != {o.min}")

        if self.max != o.max:
            diff.append(f"max: {self.max} != {o.max}")

        if self.type != o.type:
            diff.append(f"type: {self.type} != {o.type}")

        if self.extension or o.extension:
            if self.extension and not o.extension:
                diff.append(
                    f"extension: this contains but other is empty: {','.join(list(self.extension.keys()))}"
                )
            elif not self.extension:
                diff.append(
                    f"extension: other contains but this is empty: {','.join(list(o.extension.keys()))}"
                )
            else:
                if (
                    len(set(self.extension.keys()).difference(set(o.extension.keys())))
                    > 0
                ):
                    diff.append(
                        f"extension: this {self.extension.keys()}, other {o.extension.keys()}"
                    )
                else:
                    for ext, value in self.extension.items():
                        if value != o.extension[ext]:
                            diff.append(f"extension: {ext}: {value} != {o.extension[ext]}")

        return diff
