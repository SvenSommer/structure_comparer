import logging
from collections import OrderedDict
from pathlib import Path
from profile import Profile
from typing import Dict, List

from .classification import Classification
from .consts import REMARKS
from .data.comparison import Comparison, ComparisonField, ProfileField
from .data.profile import ProfileMap
from .helpers import split_parent_child
from .manual_entries import (
    MANUAL_ENTRIES,
    MANUAL_ENTRIES_CLASSIFICATION,
    MANUAL_ENTRIES_EXTRA,
    MANUAL_ENTRIES_REMARK,
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


def compare_profiles(profiles_to_compare: List, datapath: Path):
    """
    Compares the presence of properties in KBV and ePA profiles.
    """

    profile_maps = load_profiles(profiles_to_compare, datapath)
    structured_results = _compare_profiles(profile_maps)

    return structured_results


def load_profiles(profiles_to_compare: List, datapath: Path) -> Dict[str, ProfileMap]:
    """
    Loads the FHIR structure definitions from the local JSON files.
    """
    profiles_maps = {
        str(profiles): ProfileMap.from_json(profiles, datapath)
        for profiles in profiles_to_compare
    }
    return profiles_maps


def _compare_profiles(profile_maps: Dict[str, ProfileMap]) -> Dict[str, Comparison]:
    mapping = {}
    for map in profile_maps.values():
        sources_key = tuple((entry.name, entry.version) for entry in map.sources)
        target_key = (map.target.name, map.target.version)
        key = str((sources_key, target_key))
        mapping[key] = compare_profile(map)
    return mapping


def compare_profile(profile_map: ProfileMap) -> Comparison:
    """
    Generate a structured representation containing the rules for each target profile.

    The returned dictionary contains one item for each item in the argument `presence_data`. Each of these items
    contains the names of KBV and ePA profiles, presence information for each of their fields and their
    classifications and remarks.
    """

    # Iterate over all mappings (each entry are mapping to the same profile)
    comparison = generate_comparison(profile_map)
    fill_classification_remark(comparison)

    return comparison


def generate_comparison(profile_map: ProfileMap) -> Comparison:
    comparison = Comparison(profile_map)

    all_profiles = [profile_map.target] + profile_map.sources

    for source_profile in all_profiles:
        for _, field in source_profile.fields.items():
            # Check if field already exists or needs to be created
            if (
                not (field_entry := comparison.fields.get(field.name))
                or field_entry.extension != field.extension
            ):
                comparison.fields[field.name] = ComparisonField(field.name, field.id)
                comparison.fields[field.name].extension = field.extension

            profile_key = source_profile.profile_key
            comparison.fields[field.name].profiles[profile_key] = ProfileField(
                name=profile_key, present=True
            )

    # Sort the fields by name
    comparison.fields = OrderedDict(
        sorted(comparison.fields.items(), key=lambda x: x[0])
    )

    # Fill the absent profiles
    all_profiles_keys = [profile.profile_key for profile in all_profiles]
    for field in comparison.fields.values():
        for profile_key in all_profiles_keys:
            if profile_key not in field.profiles:
                field.profiles[profile_key] = ProfileField(
                    name=profile_key, present=False
                )

    # Add remarks and classifications for each field
    for field in comparison.fields.values():
        _fill_allowed_classifications(
            field, all_profiles_keys[:-1], all_profiles_keys[-1]
        )

    return comparison


def fill_classification_remark(comparison: Comparison):
    manual_entries = MANUAL_ENTRIES.entries.get(comparison.id)
    for field in comparison.fields.values():
        _classify_remark_field(field, comparison, manual_entries)


def _fill_allowed_classifications(
    field: ComparisonField, source_profiles: List[str], target_profile: str
):
    allowed = set([c for c in Classification])

    any_source_present = any(
        [field.profiles[profile].present for profile in source_profiles]
    )
    target_present = field.profiles[target_profile].present

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


def _classify_remark_field(
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

    # Split the property in parent and child
    parent, child = split_parent_child(field.name)

    # If there is a manual entry for this property, use it
    if manual_entries is not None and field.name in manual_entries:
        manual_entry = manual_entries[field.name]
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
            extra = parent_update.extra + field.name[len(parent) :]
            remark = REMARKS[classification].format(extra)

        # Else use the parent's remark
        else:
            remark = parent_update.remark

    # If present in any of the source profiles
    elif any(
        [field.profiles[profile.profile_key].present for profile in comparison.sources]
    ):
        if field.profiles[comparison.target.profile_key].present:
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
