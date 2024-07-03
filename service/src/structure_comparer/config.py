import json
from pathlib import Path
from typing import Dict, List


class Config:
    def __init__(self) -> None:
        self.manual_entries_file: str = None
        self.data_dir: str = None
        self.html_output_dir: str = None
        self.mapping_output_file: str = None
        self.profiles_to_compare: List[CompareConfig] = None
        self.show_remarks: bool = None

    @staticmethod
    def from_json(file: str | Path) -> "Config":
        file = Path(file)
        dict_ = json.loads(file.read_text())
        return Config.from_dict(dict_)

    @staticmethod
    def from_dict(dict_: Dict) -> "Config":
        config = Config()
        config.manual_entries_file = dict_.get(
            "manual_entries_file", "manual_entries.yaml"
        )
        config.data_dir = dict_.get("data_dir", "data")
        config.html_output_dir = dict_.get("html_output_dir", "docs")
        config.mapping_output_file = dict_.get("mapping_output_file", "mapping.json")
        config.profiles_to_compare = [
            CompareConfig.from_dict(compare)
            for compare in dict_.get("profiles_to_compare")
        ]
        config.show_remarks = dict_.get("show_remarks", False)
        return config


class CompareConfig:
    def __init__(self) -> None:
        self.id = None
        self.version: str = None
        self.status: str = None
        self.mappings: MappingConfig = None

    @staticmethod
    def from_dict(dict_: Dict) -> "CompareConfig":
        config = CompareConfig()
        config.id = dict_["id"]
        config.version = dict_["version"]
        config.status = dict_["status"]
        config.mappings = MappingConfig.from_dict(dict_.get("mappings"))
        return config


class MappingConfig:
    def __init__(self) -> None:
        self.source_profiles: List[ProfileConfig] = None
        self.target_profile: ProfileConfig = None

    @staticmethod
    def from_dict(dict_: Dict) -> "MappingConfig":
        config = MappingConfig()
        config.source_profiles = [
            ProfileConfig.from_dict(profile) for profile in dict_.get("sourceprofiles")
        ]
        config.target_profile = ProfileConfig.from_dict(dict_.get("targetprofile"))
        return config


class ProfileConfig:
    def __init__(self) -> None:
        self.file: str = None
        self.version: str = None
        self.simplifier_url: str = None
        self.file_download_url: str = None

    @staticmethod
    def from_dict(dict_: Dict) -> "ProfileConfig":
        config = ProfileConfig()
        config.file = dict_["file"]
        config.version = dict_["version"]
        config.simplifier_url = dict_["simplifier_url"]
        config.file_download_url = dict_["file_download_url"]
        return config