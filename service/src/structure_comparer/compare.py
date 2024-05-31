from collections import OrderedDict
from pathlib import Path
from typing import Dict, List
import logging

from .classification import Classification
from .data.comparison import Comparison, ComparisonField, ProfileField
from .data.profile import ProfileMap
from .consts import REMARKS
from .helpers import split_parent_child
from .manual_entries import (
    MANUAL_ENTRIES,
    MANUAL_ENTRIES_CLASSIFICATION,
    MANUAL_ENTRIES_REMARK,
    MANUAL_ENTRIES_EXTRA,
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


def generate_profile_key(profile) -> str:
    return f"{profile.name}|{profile.version}"

def generate_comparison(profile_map: ProfileMap) -> Comparison:
    # Iterate over all mappings (each entry are mapping to the same profile)
    comparison = Comparison()

    # Generate the profile names and versions
    source_profiles = [generate_profile_key(profile) for profile in profile_map.sources]
    target_profile = generate_profile_key(profile_map.target)

    # Extract which profiles are Source Profiles and which is the target one
    comparison.source_profiles = source_profiles
    comparison.target_profile = target_profile
    comparison.version = profile_map.version
    comparison.last_updated = profile_map.last_updated
    comparison.status = profile_map.status

    for source_profile in [profile_map.target] + profile_map.sources:
        for _, field in source_profile.fields.items():
            # Check if field already exists or needs to be created
            if (
                not (field_entry := comparison.fields.get(field.name))
                or field_entry.extension != field.extension
            ):
                comparison.fields[field.name] = ComparisonField(field.name, field.id)
                comparison.fields[field.name].extension = field.extension

            profile_key = generate_profile_key(source_profile)
            comparison.fields[field.name].profiles[profile_key] = ProfileField(
                name=profile_key, present=True
            )

    # Sort the fields by name
    comparison.fields = OrderedDict(
        sorted(comparison.fields.items(), key=lambda x: x[0])
    )

    # Fill the absent profiles
    all_profiles = source_profiles + [target_profile]
    for field in comparison.fields.values():
        for profile in all_profiles:
            if profile not in field.profiles:
                field.profiles[profile] = ProfileField(name=profile, present=False)

    # Add remarks and classifications for each field
    for field in comparison.fields.values():
        _fill_allowed_classifications(field, source_profiles, target_profile)

    return comparison


def fill_classification_remark(comparison: Comparison):
    for field in comparison.fields.values():
        _classify_remark_field(
            field, comparison.source_profiles, comparison.target_profile, comparison
        )


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
    field: ComparisonField,
    source_profiles: List[str],
    target_profile: str,
    comparison: Comparison,
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
    if field.name in MANUAL_ENTRIES:
        manual_entry = MANUAL_ENTRIES[field.name]
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

            # Cut away the common part with the parent and add the remainer to the parents extra
            extra = parent_update.extra + field.name[len(parent) :]
            remark = REMARKS[classification].format(extra)

        # Else use the parents remark
        else:
            remark = parent_update.remark

    # If present in any of the source profiles
    elif any([field.profiles[profile].present for profile in source_profiles]):
        if field.profiles[target_profile].present:
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
