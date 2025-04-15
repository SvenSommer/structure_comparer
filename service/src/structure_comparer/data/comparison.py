from collections import OrderedDict
from dataclasses import dataclass
from typing import Dict, List

from pydantic import ValidationError

from ..classification import Classification
from ..model.mapping import Mapping as MappingModel
from .profile import Profile, ProfileField, ProfileMap


@dataclass(init=False)
class ComparisonField:
    def __init__(self) -> None:
        self.classification: Classification = None
        self.extension: str = None
        self.extra: str = None
        self.profiles: Dict[str, ProfileField] = {}
        self.remark = None
        self.classifications_allowed: List[Classification] = []

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

    @property
    def id(self) -> str:
        return list(self.profiles.values())[0].id

    @property
    def name(self) -> str:
        return list(self.profiles.values())[0].path_full

    @property
    def name_child(self) -> str:
        return self.name.rsplit(".", 1)[1]

    @property
    def name_parent(self) -> str:
        return self.name.rsplit(".", 1)[0]


class Comparison:
    def __init__(self, profile_map: ProfileMap = None) -> None:
        self.id: str = None
        self.sources: List[Profile] = []
        self.target: Profile = None
        self.fields: OrderedDict[str, ComparisonField] = OrderedDict()
        self.version: str = None
        self.last_updated: str = None
        self.status: str = None

        if profile_map is not None:
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

    def to_model(self, proj_name: str) -> MappingModel:
        sources = [p.to_model() for p in self.sources]
        target = self.target.to_model()
        url = f"/project/{proj_name}/mapping/{self.id}"

        try:
            model = MappingModel(
                id=self.id,
                name=self.name,
                version=self.version,
                last_updated=self.last_updated,
                status=self.status,
                sources=sources,
                target=target,
                url=url,
            )

        except ValidationError as e:
            print(e.errors())

        else:
            return model


def get_field_by_id(comparison: Comparison, field_id: str) -> ComparisonField | None:
    for field in comparison.fields.values():
        if field.id == field_id:
            return field
    return None
