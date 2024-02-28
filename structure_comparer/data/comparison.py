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


@dataclass(init=False)
class Comparison:
    source_profiles: List[str]
    target_profile: str
    fields: Dict[str, ComparisonField]

    def __init__(self) -> None:
        self.source_profiles = []
        self.target_profile = None
        self.fields = {}
