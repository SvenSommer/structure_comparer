import logging
from collections import OrderedDict
from pathlib import Path
from typing import Dict, List

from .classification import Classification
from .config import CompareConfig
from .consts import REMARKS
from .data.comparison import Comparison, ComparisonField
from .data.profile import ProfileMap
from .helpers import split_parent_child
from .manual_entries import (
    MANUAL_ENTRIES_CLASSIFICATION,
    MANUAL_ENTRIES_EXTRA,
    MANUAL_ENTRIES_REMARK,
    ManualEntries,
)

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


logger = logging.getLogger()


def load_profiles(
    profiles_to_compare: List[CompareConfig], datapath: Path
) -> Dict[str, ProfileMap]:
    """
    Loads the FHIR structure definitions from the local JSON files.
    """
    profiles_maps = {
        str(profiles): ProfileMap.from_json(profiles, datapath)
        for profiles in profiles_to_compare
    }
    return profiles_maps


def generate_comparison(profile_map: ProfileMap) -> Comparison:
    comparison = Comparison(profile_map)

    all_profiles = [profile_map.target] + profile_map.sources

    for profile in all_profiles:
        for field in profile.fields.values():
            # Check if field already exists or needs to be created
            if field not in comparison.fields:
                comparison.fields[field.path_full] = ComparisonField()

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
        __fill_allowed_classifications(
            field, all_profiles_keys[:-1], all_profiles_keys[-1]
        )

    return comparison


def fill_classification_remark(comparison: Comparison, manual_entries: ManualEntries):
    manual_entries = manual_entries.entries.get(comparison.id)
    for field in comparison.fields.values():
        __classify_remark_field(field, comparison, manual_entries)


def __fill_allowed_classifications(
    field: ComparisonField, source_profiles: List[str], target_profile: str
):
    allowed = set([c for c in Classification])

    any_source_present = any(
        [field.profiles[profile] is not None for profile in source_profiles]
    )
    target_present = field.profiles[target_profile] is not None

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

    field.classifications_allowed = list(allowed)


def __classify_remark_field(
    field: ComparisonField, comparison: Comparison, manual_entries: Dict
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
    if manual_entries is not None and (manual_entry := manual_entries[field.name]):
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
    elif field.name_child in MANUAL_SUFFIXES:
        classification = Classification.MANUAL

    # If the parent has a classification that can be derived use the parent's classification
    elif (
        parent_update := comparison.fields.get(field.name_parent)
    ) and parent_update.classification in DERIVED_CLASSIFICATIONS:
        classification = parent_update.classification

        # If the classification needs extra information derived that information from the parent
        if classification in EXTRA_CLASSIFICATIONS:

            # Cut away the common part with the parent and add the remainder to the parent's extra
            extra = parent_update.extra + field.name[len(field.name_parent) :]
            remark = REMARKS[classification].format(extra)

        # Else use the parent's remark
        else:
            remark = parent_update.remark

    # If present in any of the source profiles
    elif any(
        [field.profiles[profile.key] is not None for profile in comparison.sources]
    ):
        if field.profiles[comparison.target.key] is not None:
            classification = Classification.USE
        else:
            classification = Classification.EXTENSION
    else:
        classification = Classification.EMPTY

    if not remark:
        remark = REMARKS[classification]

    field.classification = classification
    field.remark = remark
    field.extra = extra
