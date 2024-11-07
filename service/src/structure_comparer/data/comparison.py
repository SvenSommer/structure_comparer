from collections import OrderedDict
from dataclasses import dataclass
import logging
from typing import Dict, List

from structure_comparer.classification import Classification
from structure_comparer.consts import REMARKS
from structure_comparer.data.fhir_profile import FhirProfile, FhirProfileElement
from structure_comparer.data.profile_map import ProfileMap
from structure_comparer.manual_entries import (
    MANUAL_ENTRIES,
    MANUAL_ENTRIES_CLASSIFICATION,
    MANUAL_ENTRIES_EXTRA,
    MANUAL_ENTRIES_REMARK,
)

logger = logging.getLogger()

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


class ProfileField:
    def __init__(self, elem: FhirProfileElement, profile_name: str) -> None:
        self.elem = elem
        self.profile_name = profile_name

    @property
    def min_cardinality(self) -> int:
        return self.elem.min

    @property
    def max_cardinality(self) -> int | float:
        return self.elem.max_safe


class ComparisonField:
    def __init__(self, elem: FhirProfileElement, comparison: "Comparison") -> None:
        self.name: str = elem.path
        self.extension = elem.extension
        self.profiles = {}
        self.id = elem.id
        self.comparison = comparison
        self.classification_derived = False
        self._classification: Classification = None
        self._manual_entry = None

    def dict(self) -> dict:
        result = {
            "classification": self.classification.value,
            "profiles": [field.__dict__ for field in self.profiles.values()],
            "remark": self.remark,
            "id": self.id,
            "name": self.name,
            "classifications_allowed": [c.value for c in self.allowed_classifications],
        }

        if self.extension:
            result["extension"] = self.extension

        if self.extra:
            result["extra"] = self.extra

        return result

    def profile_present(self, profile: FhirProfile) -> bool:
        return f"{profile.name}|{profile.version}" in self.profiles

    @property
    def elem_level(self) -> int:
        return len(self.name.split(".")) - 1

    @property
    def parent_name(self) -> str | None:
        return self.id.rsplit(".", 1)[0]

    @property
    def child_name(self) -> str:
        return self.id.rsplit(".", 1)[1]

    @property
    def source_profiles(self) -> List[FhirProfile]:
        return self.comparison.sources

    @property
    def target_profile(self) -> FhirProfile:
        return self.comparison.target

    @property
    def any_source_present(self) -> bool:
        return any([self.profile_present(profile) for profile in self.source_profiles])

    @property
    def target_present(self) -> bool:
        return self.profile_present(self.target_profile)

    @property
    def manual_entry(self):
        if self._manual_entry is not None:
            return self._manual_entry

        if self.comparison.manual_entries is None:
            return None

        self._manual_entry = self.comparison.manual_entries[self.id]
        return self._manual_entry

    @property
    def manual_classification(self) -> Classification:
        return (
            self.manual_entry.get(MANUAL_ENTRIES_CLASSIFICATION, Classification.MANUAL)
            if self.manual_entry is not None
            else None
        )

    @property
    def allowed_classifications(self) -> List[Classification]:
        allowed = set([c for c in Classification])

        if not self.any_source_present:
            allowed -= set(
                [Classification.USE, Classification.NOT_USE, Classification.COPY_TO]
            )
        else:
            allowed -= set([Classification.EMPTY])
        if not self.target_present:
            allowed -= set(
                [Classification.USE, Classification.EMPTY, Classification.COPY_FROM]
            )

        return sorted(allowed, key=lambda x: x.name)

    @property
    def parent(self):
        return self.comparison.fields.get(self.parent_name)

    @property
    def classification(self) -> Classification:
        """
        Classify and get the remark for the property

        First, the manual entries and manual suffixes are checked. If neither is the case, it classifies the property
        based on the presence of the property in the KBV and ePA profiles.
        """

        if self._classification is not None:
            return self._classification

        # If there is a manual entry for this property, use it
        if self.manual_classification is not None:
            classification = self.manual_classification

        # If the last element from the property is in the manual list, use the manual classification
        elif self.child_name in MANUAL_SUFFIXES:
            classification = Classification.MANUAL

        # If the parent has a classification that can be derived use the parent's classification
        elif (parent := self.parent) and (
            parent.classification in DERIVED_CLASSIFICATIONS or self.elem_level > 1
        ):
            self.classification_derived = True
            classification = parent.classification

        # If present in any of the source profiles
        elif self.any_source_present:
            if self.target_present:
                classification = Classification.USE
            else:
                classification = Classification.EXTENSION
        else:
            classification = Classification.EMPTY

        self._classification = classification
        return classification

    @property
    def remark(self):
        """
        Classify and get the remark for the property

        First, the manual entries and manual suffixes are checked. If neither is the case, it classifies the property
        based on the presence of the property in the KBV and ePA profiles.
        """

        # If there is a manual entry for this property, use it
        if self.manual_entry is not None:

            # If there is a remark in the manual entry, use it else use the default remark
            remark = self.manual_entry.get(
                MANUAL_ENTRIES_REMARK, REMARKS[self.classification]
            )

            # If the classification needs extra information, generate the remark with the extra information
            if self.classification in EXTRA_CLASSIFICATIONS:
                extra = self.manual_entry[MANUAL_ENTRIES_EXTRA]
                remark = REMARKS[self.classification].format(extra)

            return remark

        # If the parent has a classification that can be derived use the parent's classification
        elif self.classification_derived:
            parent_classification = self.parent.classification

            # If the classification needs extra information derived that information from the parent
            if parent_classification in EXTRA_CLASSIFICATIONS:

                # Cut away the common part with the parent and add the remainder to the parent's extra
                extra = self.parent.extra + self.name[len(self.parent_name) :]
                return REMARKS[parent_classification].format(extra)

            # Else use the parent's remark
            else:
                return self.parent.remark

        return REMARKS[self.classification]

    @property
    def extra(self):
        """
        Classify and get the remark for the property

        First, the manual entries and manual suffixes are checked. If neither is the case, it classifies the property
        based on the presence of the property in the KBV and ePA profiles.
        """

        # If there is a manual entry for this property, use it
        if self.manual_entry is not None:

            # If the classification needs extra information, generate the remark with the extra information
            if self.classification in EXTRA_CLASSIFICATIONS:
                return self.manual_entry[MANUAL_ENTRIES_EXTRA]

        # If the parent has a classification that can be derived use the parent's classification
        elif self.classification_derived:
            # If the classification needs extra information derived that information from the parent
            if self.classification in EXTRA_CLASSIFICATIONS:

                # Cut away the common part with the parent and add the remainder to the parent's extra
                return self.parent.extra + self.name[len(self.parent_name) :]


class Comparison:
    def __init__(self, profile_map: ProfileMap = None) -> None:
        self.id: str = None
        self.sources: List[FhirProfile] = []
        self.target: FhirProfile = None
        self.fields: OrderedDict[str, ComparisonField] = OrderedDict()
        self.version: str = None
        self.last_updated: str = None
        self.status: str = None
        self._manual_entries = None

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

    @property
    def source_names(self) -> List[str]:
        return [source.name for source in self.sources]

    @property
    def target_name(self) -> str:
        return self.target.name

    @property
    def manual_entries(self):
        if self._manual_entries is not None:
            return self._manual_entries

        self._manual_entries = MANUAL_ENTRIES[self.id]
        return self._manual_entries

    def add_field_profile(self, field: FhirProfileElement, profile_name: str) -> None:
        # Check if field already exists or needs to be created
        field_key = field.id
        if (
            not (field_entry := self.fields.get(field_key))
            or field_entry.extension != field.extension
        ):
            if field_entry is not None and field_entry.extension != field.extension:
                logger.warning(
                    f"reinit field with different extension: {str(field_entry.extension)} != {str(field.extension)}"
                )
            self.fields[field_key] = ComparisonField(field, self)

        self.fields[field_key].profiles[profile_name] = ProfileField(
            field, profile_name
        )

    def sort_fields(self) -> None:
        self.fields = OrderedDict(sorted(self.fields.items(), key=lambda x: x[0]))

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


def get_field_by_id(comparison: Comparison, field_id: str) -> ComparisonField | None:
    for field in comparison.fields.values():
        if field.id == field_id:
            return field
    return None
