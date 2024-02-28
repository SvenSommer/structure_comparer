import json
from typing import Dict, List
import logging

from .classification import Classification
from .data.comparison import Comparison, ComparisonField, ProfileField
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

    profile_maps = _load_profiles(profiles_to_compare, datapath)


def _load_profiles(profiles_to_compare: List, datapath: Path) -> Dict[str, ProfileMap]:
    """
    Loads the FHIR structure definitions from the local JSON files.
    """
    profiles_maps = {
        str(profiles): ProfileMap.from_json(profiles, datapath)
        for profiles in profiles_to_compare
    }
    return profiles_maps

    return presence_data


def _classify_remark_property(
    comparison_field: ComparisonField,
    prop: str,
    kbv_presences: List[str],
    epa_presence: str,
    fields_updates: Dict[str, ComparisonField],
) -> Dict[str, str]:
    """
    Classify and get the remark for the property

    First, the manual entries and manual suffixes are checked. If neither is the case, it classifies the property
    based on the presence of the property in the KBV and ePA profiles.
    """

    classification = None
    remark = None
    extra = None

    # Split the property in parent and child
    parent, child = split_parent_child(prop)

    # If there is a manual entry for this property, use it
    if prop in MANUAL_ENTRIES:
        manual_entry = MANUAL_ENTRIES[prop]
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
        parent_update := fields_updates.get(parent)
    ) and parent_update.classification in DERIVED_CLASSIFICATIONS:
        classification = parent_update.classification

        # If the classification needs extra information derived that information from the parent
        if classification in EXTRA_CLASSIFICATIONS:

            # Cut away the common part with the parent and add the remainer to the parents extra
            extra = parent_update.extra + prop[len(parent) :]
            remark = REMARKS[classification].format(extra)

        # Else use the parents remark
        else:
            remark = parent_update.remark

    # If present in any of the KBV profiles
    elif any(kbv_presences):
        if epa_presence:
            classification = Classification.USE
        else:
            classification = Classification.EXTENSION
    else:
        classification = Classification.EMPTY

    if not remark:
        remark = REMARKS[classification]

    comparison_field.classification = classification
    comparison_field.remark = remark
    comparison_field.extra = extra


def _is_light_color(hex_color: str) -> bool:
    r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return luminance > 0.5


def _gen_structured_results(presence_data: dict) -> Comparison:
    """
    Generate a structured representation containing the rules for each target profile.

    The returned dictionary contains one item for each item in the argument `presence_data`. Each of these items
    contains the names of KBV and ePA profiles, presence information for each of their fields and their
    classifications and remarks.
    """
    mapping = {}
    # Iterate over all mappings (each entry are mapping to the same profile)
    for profiles, presences in presence_data.items():
        comparison = Comparison()

        # Generate the profile names
        source_profiles = [profile.replace(".json", "") for profile in profiles[0]]
        target_profile = profiles[1].replace(".json", "")

        # Extract which profiles are KBV and which is the ePA one
        comparison.source_profiles = source_profiles
        comparison.target_profile = target_profile

        # Generate the mapping for all fields in those profiles
        for field, field_presences in sorted(presences.items()):
            field_update = ComparisonField()

            field_updated = field
            extension_url = None

            # Get the field name while extracting the canonical for extensions
            if "extension" in field and "<br>" in field:
                field_updated, extension_url = field.split("<br>")
                extension_url = extension_url.strip("()")
            if extension_url:
                field_update.extension = extension_url

            # Extract the presences for KBV and ePA profiles
            target_presence, source_presences = field_presences[0], field_presences[1:]
            field_update.profiles[target_profile] = ProfileField(
                present=target_presence
            )
            for profile, presence in zip(source_profiles, source_presences):
                field_update.profiles[profile] = ProfileField(present=presence)

            # Fill the classification and remark for this field
            _classify_remark_property(
                field_update,
                field,
                source_presences,
                target_presence,
                comparison.fields,
            )

            # Set the field update
            comparison.fields[field_updated] = field_update

        mapping[profiles] = comparison

    return mapping
