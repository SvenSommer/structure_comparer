import json
from collections import OrderedDict
from pathlib import Path
from typing import Dict, List
from uuid import uuid4

from structure_comparer.config import CompareConfig, ProfileConfig

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
            Profile.from_dict(source, datapath) for source in sources
        ]
        profiles_map.target = Profile.from_dict(target, datapath)
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
    def __init__(
        self,
        name: str,
        version: str = None,
        simplifier_url: str = None,
        file_download_url: str = None,
    ) -> None:
        self.name: str = name
        self.version: str = version
        self.simplifier_url: str = simplifier_url
        self.file_download_url: str = file_download_url
        self.fields: OrderedDict[str, ProfileField] = OrderedDict()

    def __str__(self) -> str:
        return f"(name={self.name}, version={self.version}, simplifier_url={self.simplifier_url}, file_download_url={self.file_download_url}, fields={self.fields})"

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def from_dict(config: ProfileConfig, datapath: Path) -> "Profile":
        file_path = datapath / config.file
        if not file_path.exists():
            raise FileNotFoundError(
                f"The file {
                    file_path} does not exist. Please check the file path and try again."
            )

        content = json.loads(file_path.read_text())

        if not content.get("snapshot"):
            raise KeyError(
                f"The 'snapshot' element was not found in the profile file at {file_path}. Please check the file content."
            )

        profile = Profile(
            name=content["name"],
            version=config.version,
            simplifier_url=config.simplifier_url,
            file_download_url=config.file_download_url,
        )

        snapshot = content["snapshot"]
        if "element" not in snapshot:
            raise KeyError(
                f"The 'element' element was not found in the 'snapshot' of the profile file at {file_path}. Please check the file content."
            )

        extracted_elements = _extract_elements(content["snapshot"]["element"])
        profile.fields = OrderedDict(
            (field.name, field)
            for field in sorted(extracted_elements, key=lambda x: x.name)
        )

        return profile

    @property
    def profile_key(self) -> str:
        return f"{self.name}|{self.version}"

    def __lt__(self, other: "Profile") -> bool:
        return self.profile_key < other.profile_key


class ProfileField:
    def __init__(self, name: str, extension: str = None, min_cardinality: int = 0, max_cardinality: int = 0) -> None:
        self.name: str = name
        self.extension: str = extension
        self.min_cardinality: int = min_cardinality
        self.max_cardinality: int = max_cardinality
        self.id = str(uuid4())

    def __str__(self) -> str:
        return f"(name={self.name}, id={self.id}, min_cardinality={self.min_cardinality}, max_cardinality={self.max_cardinality}{f', extension={self.extension}' if self.extension else ''})"

    def __repr__(self) -> str:
        return str(self)


def _extract_elements(elements: List[Dict]) -> List[ProfileField]:
    result = []
    ignore_paths = []

    for element in elements:
        path: str = element["id"]
        path_split = path.split(".")

        # Skip base element
        if len(path_split) == 1:
            continue

        # Skip elements that are children of ignored nodes
        if _should_ignore(path, ignore_paths):
            continue

        # Ignore elements with having specific path endings
        if path_split[-1] in IGNORE_ENDS:
            continue

        # Ignore elements where the cardinality is set to zero
        if element["max"] == "0" or element["max"] == 0:
            # Extend list of nodes that are removed due to cardinality
            ignore_paths.append(path)
            continue

        min_cardinality = int(element.get("min", 0))
        max_cardinality = element.get("max", 0)
        if max_cardinality == '*':
            max_cardinality = float('inf')
        else:
            max_cardinality = int(max_cardinality)

        # Check for specific extensions
        if extension := _get_extension(element, path):
            # Further ignore sub-elements of the extensions
            ignore_paths.append(path)
            extension.min_cardinality = min_cardinality
            extension.max_cardinality = max_cardinality
            result.append(extension)
        else:
            # Add the base path of the element
            result.append(ProfileField(name=path, min_cardinality=min_cardinality, max_cardinality=max_cardinality))

        # Check for and add slices, ignoring 'slice(url)' endings
        if "slicing" in element and "discriminator" in element["slicing"]:
            for discriminator in element["slicing"]["discriminator"]:
                if isinstance(discriminator, dict) and "path" in discriminator:
                    slice_path = f"{path}.slice({discriminator['path']})"
                    slice_path_split = slice_path.split(".")
                    if not slice_path_split[-1] in IGNORE_SLICES:
                        result.append(ProfileField(name=slice_path, min_cardinality=min_cardinality, max_cardinality=max_cardinality))

    return result


def _should_ignore(path: str, ignore_paths: List[str]) -> bool:
    for ignored in ignore_paths:
        if path.startswith(ignored):
            return True
    return False


def _get_extension(element: dict, path: str) -> str:
    if "extension" in element and "type" in element:
        for type_entry in element["type"]:
            if type_entry.get("code") == "Extension" and "profile" in type_entry:
                for profile in type_entry["profile"]:
                    return ProfileField(name=path, extension=profile)
    return None
