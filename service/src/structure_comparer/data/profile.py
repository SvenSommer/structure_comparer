from collections import OrderedDict
import json
from pathlib import Path
from typing import Dict, List
from uuid import uuid4


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
        self.sources: List[Profile] = []
        self.target: Profile = None

    @staticmethod
    def from_json(profiles_to_compare: List, datapath: Path) -> "ProfileMap":
        sources = profiles_to_compare[0]
        target = profiles_to_compare[1]

        profiles_map = ProfileMap()
        profiles_map.sources = [
            Profile.from_dict(source, datapath) for source in sources
        ]
        profiles_map.target = Profile.from_dict(target, datapath)

        return profiles_map
    
    @property
    def name(self) -> str:
        return f"{', '.join(profile.name for profile in self.sources)} -> {self.target.name}"


class Profile:
    def __init__(self, name: str, version: str = None, canonical: str = None, simplifier_url: str = None, file_download_url: str = None) -> None:
        self.name: str = name
        self.version: str = version
        self.canonical: str = canonical
        self.simplifier_url: str = simplifier_url
        self.file_download_url: str = file_download_url
        self.fields: OrderedDict[str, ProfileField] = OrderedDict()

    def __str__(self) -> str:
        return f"(name={self.name}, version={self.version}, canonical={self.canonical}, simplifier_url={self.simplifier_url}, file_download_url={self.file_download_url}, fields={self.fields})"

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def from_dict(data: Dict, datapath: Path) -> "Profile":
        file_path = datapath / data["file"]
        
        if not file_path.exists():
            raise FileNotFoundError(f"The file {file_path} does not exist. Please check the file path and try again.")

        content = json.loads(file_path.read_text())

        profile = Profile(
            name=content["name"],
            version=data.get("version"),
            canonical=data.get("canonical"),
            simplifier_url=data.get("simplifier_url"),
            file_download_url=data.get("file_download_url")
        )

        extracted_elements = _extract_elements(content["snapshot"]["element"])
        profile.fields = OrderedDict(
            (field.name, field)
            for field in sorted(extracted_elements, key=lambda x: x.name)
        )

        return profile








class ProfileField:
    def __init__(self, name: str, extension: str = None) -> None:
        self.name: str = name
        self.extension: str = extension
        self.id = str(uuid4())

    def __str__(self) -> str:
        return f"(name={self.name}, id={self.id}{f', extension={self.extension}' if self.extension else ''})"

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
            # Extend list of nodes that are remove due cardinality
            ignore_paths.append(path)
            continue

        # Check for specific extensions
        if extension := _get_extension(element, path):
            # Further ignore sub-elements of the extensions
            ignore_paths.append(path)
            result.append(extension)
        else:
            # Add the base path of the element
            result.append(ProfileField(name=path))

        # Check for and add slices, ignoring 'slice(url)' endings
        if "slicing" in element and "discriminator" in element["slicing"]:
            for discriminator in element["slicing"]["discriminator"]:
                if isinstance(discriminator, dict) and "path" in discriminator:
                    slice_path = f"{path}.slice({discriminator['path']})"
                    slice_path_split = slice_path.split(".")
                    if not slice_path_split[-1] in IGNORE_SLICES:
                        result.append(ProfileField(name=slice_path))

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
