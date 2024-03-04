from collections import OrderedDict
from dataclasses import dataclass
from typing import Dict, List

from structure_comparer.classification import Classification


@dataclass
class ProfileField:
    present: bool


@dataclass(init=False)
class ComparisonField:
    classification: Classification
    extension: str
    extra: str
    profiles: Dict[str, ProfileField]
    remark: str

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.classification = None
        self.extension = None
        self.extra = None
        self.profiles = {}
        self.remark = None

    def dict(self) -> dict:
        result = {
            "classification": self.classification.value,
            "profiles": {
                profile: field.__dict__ for profile, field in self.profiles.items()
            },
            "remark": self.remark,
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
            "fields": OrderedDict(
                {name: field.dict() for name, field in self.fields.items()}
            ),
        }
