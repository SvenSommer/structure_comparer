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
    source_profiles: List[Profile]
    target_profile: Profile
    fields: OrderedDict[str, ComparisonField]
    version: str
    last_updated: str
    status: str

    def __init__(self) -> None:
        self.source_profiles = []
        self.target_profile = None
        self.fields = OrderedDict()
        self.version = None
        self.last_updated = None
        self.status = None

    @property
    def name(self) -> str:
        return f"{', '.join(profile.name for profile in self.source_profiles)} -> {self.target_profile.name}"

    def dict(self) -> dict:
        return {
            "name": self.name,
            "source_profiles": [{
                "name": profile.name,
                "version": profile.version,
                "simplifier_url": profile.simplifier_url
            } for profile in self.source_profiles],
            "target_profile": {
                "name": self.target_profile.name,
                "version": self.target_profile.version,
                "simplifier_url": self.target_profile.simplifier_url
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
