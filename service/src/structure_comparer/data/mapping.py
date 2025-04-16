from collections import OrderedDict
from dataclasses import dataclass
from typing import Dict, List

from pydantic import ValidationError

from ..classification import Classification
from ..consts import REMARKS
from ..manual_entries import (
    MANUAL_ENTRIES_CLASSIFICATION,
    MANUAL_ENTRIES_EXTRA,
    MANUAL_ENTRIES_REMARK,
    ManualEntries,
)
from ..model.mapping import Mapping as MappingModel
from .profile import Profile, ProfileField, ProfileMap

MANUAL_SUFFIXES = ["reference", "profile"]

# These classification generate a remark with extra information
EXTRA_CLASSIFICATIONS = [
    Classification.COPY_FROM,
    Classification.COPY_TO,
    Classification.FIXED,
]

# These classifications can be derived from their parents
DERIVED_CLASSIFICATIONS = [
    Classification.EMPTY,
    Classification.NOT_USE,
] + EXTRA_CLASSIFICATIONS


@dataclass(init=False)
class MappingField:
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

    def fill_allowed_classifications(
        self, source_profiles: List[str], target_profile: str
    ):
        allowed = set([c for c in Classification])

        any_source_present = any(
            [self.profiles[profile] is not None for profile in source_profiles]
        )
        target_present = self.profiles[target_profile] is not None

        if not any_source_present:
            allowed -= set(
                [Classification.USE, Classification.NOT_USE, Classification.COPY_TO]
            )
        else:
            allowed -= set([Classification.EMPTY])
        if not target_present:
            allowed -= set(
                [Classification.USE, Classification.EMPTY, Classification.COPY_FROM]
            )

        self.classifications_allowed = list(allowed)

    def classify_remark_field(
        self, comparison: "Mapping", manual_entries: Dict
    ) -> None:
        """
        Classify and get the remark for the property

        First, the manual entries and manual suffixes are checked. If neither is the case, it classifies the property
        based on the presence of the property in the KBV and ePA profiles.
        """

        classification = None
        remark = None
        extra = None

        # If there is a manual entry for this property, use it
        if manual_entries is not None and (manual_entry := manual_entries[self.name]):
            classification = manual_entry.get(
                MANUAL_ENTRIES_CLASSIFICATION, Classification.MANUAL
            )

            # If there is a remark in the manual entry, use it else use the default remark
            remark = manual_entry.get(MANUAL_ENTRIES_REMARK, REMARKS[classification])

            # If the classification needs extra information, generate the remark with the extra information
            if classification in EXTRA_CLASSIFICATIONS:
                extra = manual_entry[MANUAL_ENTRIES_EXTRA]
                remark = REMARKS[classification].format(extra)

        # If the last element from the property is in the manual list, use the manual classification
        elif self.name_child in MANUAL_SUFFIXES:
            classification = Classification.MANUAL

        # If the parent has a classification that can be derived use the parent's classification
        elif (
            parent_update := comparison.fields.get(self.name_parent)
        ) and parent_update.classification in DERIVED_CLASSIFICATIONS:
            classification = parent_update.classification

            # If the classification needs extra information derived that information from the parent
            if classification in EXTRA_CLASSIFICATIONS:

                # Cut away the common part with the parent and add the remainder to the parent's extra
                extra = parent_update.extra + self.name[len(self.name_parent) :]
                remark = REMARKS[classification].format(extra)

            # Else use the parent's remark
            else:
                remark = parent_update.remark

        # If present in any of the source profiles
        elif any(
            [self.profiles[profile.key] is not None for profile in comparison.sources]
        ):
            if self.profiles[comparison.target.key] is not None:
                classification = Classification.USE
            else:
                classification = Classification.EXTENSION
        else:
            classification = Classification.EMPTY

        if not remark:
            remark = REMARKS[classification]

        self.classification = classification
        self.remark = remark
        self.extra = extra


class Mapping:
    def __init__(self, profile_map: ProfileMap = None) -> None:
        self.id: str = None
        self.sources: List[Profile] = []
        self.target: Profile = None
        self.fields: OrderedDict[str, MappingField] = OrderedDict()
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

    @staticmethod
    def create(profile_map: ProfileMap) -> "Mapping":
        comparison = Mapping(profile_map)

        all_profiles = [profile_map.target] + profile_map.sources

        for profile in all_profiles:
            for field in profile.fields.values():
                # Check if field already exists or needs to be created
                if field not in comparison.fields:
                    comparison.fields[field.path_full] = MappingField()

                comparison.fields[field.path_full].profiles[profile.key] = field

        # Sort the fields by name
        comparison.fields = OrderedDict(
            sorted(comparison.fields.items(), key=lambda x: x[0])
        )

        # Fill the absent profiles
        all_profiles_keys = [profile.key for profile in all_profiles]
        for field in comparison.fields.values():
            for profile_key in all_profiles_keys:
                if profile_key not in field.profiles:
                    field.profiles[profile_key] = None

        # Add remarks and classifications for each field
        for field in comparison.fields.values():
            field.fill_allowed_classifications(
                all_profiles_keys[:-1], all_profiles_keys[-1]
            )

        return comparison

    def fill_classification_remark(self, manual_entries: ManualEntries):
        manual_entries = manual_entries.entries.get(self.id)
        for field in self.fields.values():
            field.classify_remark_field(self, manual_entries)
