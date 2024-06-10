from collections import OrderedDict
from dataclasses import dataclass
from profile import Profile
from typing import Dict, List

from structure_comparer.classification import Classification


@dataclass
class ProfileField:
    name: str
    present: bool


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


@dataclass(init=False)
class Comparison:
    sources: List[Profile]
    target: Profile
    fields: OrderedDict[str, ComparisonField]
    version: str
    last_updated: str
    status: str

    def __init__(self) -> None:
        self.sources = []
        self.target = None
        self.fields = OrderedDict()
        self.version = None
        self.last_updated = None
        self.status = None

    @property
    def name(self) -> str:
        source_profiles = ', '.join(f"{profile.name}|{profile.version}" for profile in self.sources)
        target_profile = f"{self.target.name}|{self.target.version}"
        return f"{source_profiles} -> {target_profile}"
    def dict(self) -> dict:
        return {
            "name": self.name,
            "sources": [{
                "name": profile.name,
                "profile_key": profile.profile_key,
                "version": profile.version,
                "simplifier_url": profile.simplifier_url
            } for profile in self.sources],
            "target": {
                "name": self.target.name,
                "profile_key": self.target.profile_key,
                "version": self.target.version,
                "simplifier_url": self.target.simplifier_url
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
