import json
import logging
from pathlib import Path
from typing import Dict, List
from uuid import uuid4

from fhir.resources.R4B.elementdefinition import ElementDefinition
from fhir.resources.R4B.structuredefinition import StructureDefinition
from pydantic import ValidationError
from structure_comparer.config import CompareConfig

from ..model.profile import Profile as ProfileModel

IGNORE_ENDS = ["id", "extension", "modifierExtension"]
IGNORE_SLICES = [
    "slice(url)",
    "slice($this)",
    "slice(system)",
    "slice(type)",
    "slice(use)",
    # workaround for 'slice(code.coding.system)'
    "system)",
]

logger = logging.getLogger(__name__)


class ProfileMap:
    def __init__(self) -> None:
        self.id: str = None
        self.sources: List[Profile] = []
        self.target: Profile = None
        self.version: str = None
        self.last_updated: str = None
        self.status: str = None

    @staticmethod
    def from_json(compare_config: CompareConfig, datapath: Path) -> "ProfileMap":
        sources = compare_config.mappings.source_profiles
        target = compare_config.mappings.target_profile

        profiles_map = ProfileMap()
        profiles_map.id = compare_config.id
        profiles_map.sources = [
            Profile.from_json(datapath / source.file) for source in sources
        ]
        profiles_map.target = Profile.from_json(datapath / target.file)
        profiles_map.version = compare_config.version
        profiles_map.last_updated = compare_config.last_updated
        profiles_map.status = compare_config.status

        return profiles_map

    @property
    def name(self) -> str:
        source_profiles = ", ".join(
            f"{profile.name}|{profile.version}" for profile in self.sources
        )
        target_profile = f"{self.target.name}|{self.target.version}"
        return f"{source_profiles} -> {target_profile}"


class Profile:
    def __init__(self, data: dict) -> None:
        self.__data = StructureDefinition.model_validate(data)
        self.__fields: List[str, ProfileField] = None
        self.__init_fields()

    def __str__(self) -> str:
        return f"(name={self.name}, version={self.version}, fields={self.fields})"

    def __repr__(self) -> str:
        return str(self)

    def __init_fields(self) -> None:
        self.__fields: Dict[str, ProfileField] = {}
        for elem in self.__data.snapshot.element:
            field = ProfileField(elem)
            if field.path is not None:
                self.__fields[field.id] = field

    @staticmethod
    def from_json(path: Path) -> "Profile":
        if not path.exists():
            raise FileNotFoundError(
                f"The file {path} does not exist. Please check the file path and try again."
            )

        try:
            return Profile(data=json.loads(path.read_text(encoding="utf-8")))

        except Exception as e:
            logger.error("failed to read file '%s'", str(path))
            logger.exception(e)

    @property
    def name(self) -> str:
        return self.__data.name

    @property
    def version(self) -> str:
        return self.__data.version

    @property
    def fields(self) -> Dict[str, "ProfileField"]:
        return self.__fields

    @property
    def key(self) -> str:
        return f"{self.name}|{self.version}"

    def __lt__(self, other: "Profile") -> bool:
        return self.key < other.key

    def to_model(self) -> ProfileModel:
        try:
            model = ProfileModel(
                profile_key=self.key, name=self.name, version=self.version
            )
        except ValidationError as e:
            logger.exception(e)

        else:
            return model


class ProfileField:
    def __init__(
        self,
        data: ElementDefinition,
    ) -> None:
        self.__data = data
        self.__id = str(uuid4())

    def __str__(self) -> str:
        return f"(name={self.name}, id={self.id}, min={self.min}, max={self.max})"

    def __repr__(self) -> str:
        return str(self)

    @property
    def id(self) -> str:
        return self.__id

    @property
    def path_full(self) -> str:
        return self.__data.id

    @property
    def path(self) -> str:
        return (
            ("." + self.path_full.split(".", 1)[1]) if "." in self.path_full else None
        )

    @property
    def min(self) -> int:
        return self.__data.min

    @property
    def max(self) -> str:
        return self.__data.max

    @property
    def must_support(self):
        return self.__data.mustSupport


# def _extract_elements(elements: List[Dict]) -> List[ProfileField]:
#     result = []
#     ignore_paths = []

#     for element in elements:
#         path: str = element["id"]
#         path_split = path.split(".")

#         # Skip base element
#         if len(path_split) == 1:
#             continue

#         # Skip elements that are children of ignored nodes
#         if _should_ignore(path, ignore_paths):
#             continue

#         # Ignore elements with having specific path endings
#         if path_split[-1] in IGNORE_ENDS:
#             continue

#         # Ignore elements where the cardinality is set to zero
#         if element["max"] == "0" or element["max"] == 0:
#             # Extend list of nodes that are removed due to cardinality
#             ignore_paths.append(path)
#             continue

#         min_cardinality = int(element.get("min", 0))
#         max_cardinality = element.get("max", 0)

#         # Check for specific extensions
#         if extension := _get_extension(element, path):
#             # Further ignore sub-elements of the extensions
#             ignore_paths.append(path)
#             extension.min_cardinality = min_cardinality
#             extension.max_cardinality = max_cardinality
#             result.append(extension)
#         else:
#             # Add the base path of the element
#             result.append(
#                 ProfileField(
#                     name=path,
#                     min_cardinality=min_cardinality,
#                     max_cardinality=max_cardinality,
#                 )
#             )

#         # Check for and add slices, ignoring 'slice(url)' endings
#         if "slicing" in element and "discriminator" in element["slicing"]:
#             for discriminator in element["slicing"]["discriminator"]:
#                 if isinstance(discriminator, dict) and "path" in discriminator:
#                     slice_path = f"{path}.slice({discriminator['path']})"
#                     slice_path_split = slice_path.split(".")
#                     if not slice_path_split[-1] in IGNORE_SLICES:
#                         result.append(
#                             ProfileField(
#                                 name=slice_path,
#                                 min_cardinality=min_cardinality,
#                                 max_cardinality=max_cardinality,
#                             )
#                         )

#     return result


# def _should_ignore(path: str, ignore_paths: List[str]) -> bool:
#     for ignored in ignore_paths:
#         if path.startswith(ignored):
#             return True
#     return False


# def _get_extension(element: dict, path: str) -> str:
#     if "extension" in element and "type" in element:
#         for type_entry in element["type"]:
#             if type_entry.get("code") == "Extension" and "profile" in type_entry:
#                 for profile in type_entry["profile"]:
#                     return ProfileField(name=path, extension=profile)
#     return None
