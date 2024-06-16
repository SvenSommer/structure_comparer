from collections import OrderedDict
from dataclasses import dataclass
from typing import Dict, List

from structure_comparer.classification import Classification
from structure_comparer.consts import REMARKS
from structure_comparer.data.file.manual_entries import (
    MANUAL_ENTRIES,
    MANUAL_ENTRIES_CLASSIFICATION,
    MANUAL_ENTRIES_EXTRA,
    MANUAL_ENTRIES_REMARK,
)
from structure_comparer.helpers import split_parent_child
from structure_comparer.model.profile import Profile, ProfileMap

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


@dataclass
class ProfileField:
    name: str
    present: bool


class ComparisonField:
    def __init__(self, name: str, id: str) -> None:
        self.name: str = name
        self.classification: Classification = None
        self.extension: str = None
        self.extra: str = None
        self.profiles: Dict[str, ProfileField] = {}
        self.remark: str = None
        self.id: str = id
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

    def classify_remark(self, comparison: "Comparison", manual_entries: Dict) -> None:
        """
        Classify and get the remark for the property

        First, the manual entries and manual suffixes are checked. If neither is the case, it classifies the property
        based on the presence of the property in the KBV and ePA profiles.
        """

        classification = None
        remark = None
        extra = None

        # Split the property in parent and child
        parent, child = split_parent_child(self.name)

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
        elif child in MANUAL_SUFFIXES:
            classification = Classification.MANUAL

        # If the parent has a classification that can be derived use the parent's classification
        elif (
            parent_update := comparison.fields.get(parent)
        ) and parent_update.classification in DERIVED_CLASSIFICATIONS:
            classification = parent_update.classification

            # If the classification needs extra information derived that information from the parent
            if classification in EXTRA_CLASSIFICATIONS:

                # Cut away the common part with the parent and add the remainder to the parent's extra
                extra = parent_update.extra + self.name[len(parent) :]
                remark = REMARKS[classification].format(extra)

            # Else use the parent's remark
            else:
                remark = parent_update.remark

        # If present in any of the source profiles
        elif any(
            [
                self.profiles[profile.profile_key].present
                for profile in comparison.sources
            ]
        ):
            if self.profiles[comparison.target.profile_key].present:
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

    def fill_allowed_classifications(
        self, source_profiles: List[str], target_profile: str
    ):
        allowed = set([c for c in Classification])

        any_source_present = any(
            [self.profiles[profile].present for profile in source_profiles]
        )
        target_present = self.profiles[target_profile].present

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
                    "profile_key": profile.profile_key,
                    "version": profile.version,
                    "simplifier_url": profile.simplifier_url,
                }
                for profile in self.sources
            ],
            "target": {
                "name": self.target.name,
                "profile_key": self.target.profile_key,
                "version": self.target.version,
                "simplifier_url": self.target.simplifier_url,
            },
            "fields": [field.dict() for field in self.fields.values()],
            "version": self.version,
            "last_updated": self.last_updated,
            "status": self.status,
        }

    def fill_classification_remark(self):
        manual_entries = MANUAL_ENTRIES.entries.get(self.id)
        for field in self.fields.values():
            field.classify_remark(self, manual_entries)

    def get_field_by_id(self, field_id: str) -> ComparisonField | None:
        for field in self.fields.values():
            if field.id == field_id:
                return field
        return None
