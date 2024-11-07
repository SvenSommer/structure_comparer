import logging
from pathlib import Path
from typing import Dict, List

from .config import CompareConfig
from .data.comparison import Comparison
from .data.profile_map import ProfileMap


logger = logging.getLogger()


def compare_profiles(profiles_to_compare: List[CompareConfig], datapath: Path):
    """
    Compares the presence of properties in KBV and ePA profiles.
    """

    profile_maps = load_profiles(profiles_to_compare, datapath)
    structured_results = {
        map.name: compare_profile(map) for map in profile_maps.values()
    }

    return structured_results


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


def compare_profile(profile_map: ProfileMap) -> Comparison:
    """
    Generate a structured representation containing the rules for each target profile.

    The returned dictionary contains one item for each item in the argument `presence_data`. Each of these items
    contains the names of KBV and ePA profiles, presence information for each of their fields and their
    classifications and remarks.
    """

    comparison = Comparison(profile_map)

    all_profiles = [profile_map.target] + profile_map.sources

    for source_profile in all_profiles:
        for _, field in source_profile.elements.items():
            comparison.add_field_profile(field, source_profile.profile_key)

    comparison.sort_fields()
    return comparison
