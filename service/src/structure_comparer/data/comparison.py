from collections import OrderedDict
from dataclasses import dataclass
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
    source_profiles: List[str]
    target_profile: str
    fields: OrderedDict[str, ComparisonField]

    def __init__(self) -> None:
        self.source_profiles = []
        self.target_profile = None
        self.fields = OrderedDict()

    @property
    def name(self) -> str:
        return f"{', '.join(profile for profile in self.source_profiles)} -> {self.target_profile}"

    def dict(self) -> dict:
        return {
            "name": self.name,
            "source_profiles": self.source_profiles,
            "target_profile": self.target_profile,
            "fields": [field.dict() for field in self.fields.values()],
        }
