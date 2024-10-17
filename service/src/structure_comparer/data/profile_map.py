from pathlib import Path
from typing import List

from structure_comparer.config import CompareConfig

from .fhir_profile import FhirProfile


class ProfileMap:
    def __init__(self) -> None:
        self.id: str = None
        self.sources: List[FhirProfile] = []
        self.target: FhirProfile = None
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
            FhirProfile.from_json(
                file_path=datapath / source.file,
                simplifier_url=source.simplifier_url,
                file_download_url=source.file_download_url,
            )
            for source in sources
        ]
        profiles_map.target = FhirProfile.from_json(
            file_path=datapath / target.file,
            simplifier_url=target.simplifier_url,
            file_download_url=target.file_download_url,
        )
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
