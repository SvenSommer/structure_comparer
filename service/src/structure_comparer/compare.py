import logging
from collections import OrderedDict
from pathlib import Path
from typing import Dict, List

from .classification import Classification
from .model.comparison import Comparison, ComparisonField, ProfileField
from .model.profile import ProfileMap

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
    comparison.fill_classification_remark()

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
        field.fill_allowed_classifications(
            all_profiles_keys[:-1], all_profiles_keys[-1]
        )

    return comparison
