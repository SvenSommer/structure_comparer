from collections import OrderedDict
from dataclasses import dataclass
from typing import Dict, List

from structure_comparer.classification import Classification
from structure_comparer.data.profile import Profile, ProfileMap


@dataclass
class ProfileField:
    name: str
    present: bool
    min_cardinality: int = 0
    max_cardinality: int = 0


@dataclass(init=False)
class ComparisonField:
    classification: Classification
    extension: str
    extra: str
    profiles: Dict[str, ProfileField]
    remark: str
    classifications_allowed: List[Classification]

    def __init__(self, name: str, id: str) -> None:
        self.name: str = name
        self.classification = None
        self.extension = None
        self.extra = None
        self.profiles = {}
        self.remark = None
        self.id = id
        self.classifications_allowed = []

    def dict(self) -> dict:
        result = {
            "classification": self.classification.value,
            "profiles": [field.__dict__ for field in self.profiles.values()],
            "remark": self.remark,
            "id": self.id,
            "name": self.name,
            "classifications_allowed": [c.value for c in self.classifications_allowed],
        }

        if self.extension:
            result["extension"] = self.extension

        if self.extra:
            result["extra"] = self.extra

        return result


class Comparison:
    def __init__(self, profile_map: ProfileMap = None) -> None:
        self.id: str = None
        self.sources: List[Profile] = []
        self.target: Profile = None
        self.fields: OrderedDict[str, ComparisonField] = OrderedDict()
        self.version: str = None
        self.last_updated: str = None
        self.status: str = None

        if not profile_map is None:
            self.id = profile_map.id
            self.sources = profile_map.sources
            self.target = profile_map.target
            self.version = profile_map.version
            self.last_updated = profile_map.last_updated
            self.status = profile_map.status

    @property
    def name(self) -> str:
        source_profiles = ", ".join(
            f"{profile.name}|{profile.version}" for profile in self.sources
        )
        target_profile = f"{self.target.name}|{self.target.version}"
        return f"{source_profiles} -> {target_profile}"

    def dict(self) -> dict:
        return {
            "name": self.name,
            "sources": [
                {
                    "name": profile.name,
                    "profile_key": profile.key,
                    "version": profile.version,
                    "simplifier_url": profile.simplifier_url,
                }
                for profile in self.sources
            ],
            "target": {
                "name": self.target.name,
                "profile_key": self.target.key,
                "version": self.target.version,
                "simplifier_url": self.target.simplifier_url,
            },
            "fields": [field.dict() for field in self.fields.values()],
            "version": self.version,
            "last_updated": self.last_updated,
            "status": self.status,
        }


def get_field_by_id(comparison: Comparison, field_id: str) -> ComparisonField | None:
    for field in comparison.fields.values():
        if field.id == field_id:
            return field
    return None
