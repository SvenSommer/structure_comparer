from enum import Enum
from typing import Dict

from .fhir_profile import FhirProfile


class Meta:
    def __init__(self, name: str = None, url: str = None, version: str = None) -> None:
        self.name = name
        self.url = url
        self.version = version

    @staticmethod
    def from_profile(profile: FhirProfile) -> "Meta":
        return Meta(profile.name, profile.url, profile.version)


class EntryClassification(Enum):
    ONLY_LEFT = "only left"
    ONLY_RIGHT = "only right"
    SAME = "same"
    DIFFERENT = "different"


class DiffEntry:
    def __init__(
        self, classification: EntryClassification, details: str = None
    ) -> None:
        self._classification = classification
        self._details = details

    @property
    def classification(self) -> EntryClassification:
        return self._classification

    @property
    def details(self) -> str:
        return self._details

    def __str__(self) -> str:
        return (
            f"{self.classification.name}:{self.details}"
            if self.details is not None
            else self.classification.name
        )

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def only_left() -> "DiffEntry":
        return DiffEntry(EntryClassification.ONLY_LEFT)

    @staticmethod
    def only_right() -> "DiffEntry":
        return DiffEntry(EntryClassification.ONLY_RIGHT)

    @staticmethod
    def same() -> "DiffEntry":
        return DiffEntry(EntryClassification.SAME)

    @staticmethod
    def different(details: str) -> "DiffEntry":
        return DiffEntry(EntryClassification.DIFFERENT, details)


class ProfileDiff:
    def __init__(self, left: FhirProfile, right: FhirProfile) -> None:
        self.meta_left = Meta.from_profile(left)
        self.meta_right = Meta.from_profile(right)

        self._data: Dict[str, DiffEntry] = {}

    def __getitem__(self, key) -> DiffEntry | None:
        return self._data.get(key)

    def __setitem__(self, key, value: DiffEntry) -> None:
        self._data[key] = value

    def items(self) -> Dict[str, DiffEntry]:
        return self._data.items()

    @staticmethod
    def compare(left: FhirProfile, right: FhirProfile) -> "ProfileDiff":
        diff = ProfileDiff(left, right)

        # check for all elements in 'left'
        for key, value in left.elements.items():

            # only left
            if key not in right.elements:
                diff[key] = DiffEntry.only_left()
                continue

            right_value = right.elements[key]

            elem_diff = value.diff(right_value)
            # same
            if len(elem_diff) == 0:
                diff[key] = DiffEntry.same()
                continue

            else:
                diff[key] = DiffEntry.different(",".join(elem_diff))
                continue

        for key, _ in right.elements.items():

            # only right
            if key not in left.elements:
                diff[key] = DiffEntry.only_right()

        return diff
