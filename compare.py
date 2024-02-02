import json
from typing import List
import logging

from classification import Classification
from consts import (
    REMARKS,
    STRUCT_CLASSIFICATION,
    STRUCT_EPA_PROFILE,
    STRUCT_EXTENSION,
    STRUCT_FIELDS,
    STRUCT_KBV_PROFILES,
    STRUCT_REMARK,
)
from manual_entries import MANUAL_ENTRIES


IGNORE_ENDS = ["id", "extension", "modifierExtension"]

IGNORE_SLICES = [
    "slice(url)",
    "slice($this)",
    "slice(system)",
    "slice(type)",
    "slice(use)",
    # workaround for 'slice(code.coding.system)'
    "system)",
]

MANUAL_SUFFIXES = ["reference", "profile"]


logger = logging.getLogger()


def compare_profiles(profiles_to_compare, datapath):
    """
    Compares the presence of properties in KBV and ePA profiles.
    """

    # Determine which properties are present in each profile
    all_properties = _determine_property_presence(profiles_to_compare, datapath)

    # Check the presence of each property in each profile
    presence_data = _check_property_presence(
        all_properties, profiles_to_compare, datapath
    )

    # Generate a structured version of the presence data
    structured_results = _gen_structured_results(presence_data)

    return structured_results


def _load_fhir_structure(file_path):
    """
    Loads the FHIR structure definition from a local JSON file.
    """
    with open(file_path, "r") as file:
        return json.load(file)


def _should_ignore(path: str, ignore_paths: List[str]) -> bool:
    for ignored in ignore_paths:
        if path.startswith(ignored):
            return True
    return False


def _get_extension(element: dict, path: str) -> str:
    if "extension" in element and "type" in element:
        for type_entry in element["type"]:
            if type_entry.get("code") == "Extension" and "profile" in type_entry:
                for profile in type_entry["profile"]:
                    extension_path = f"{path}<br>({profile})"
                    # Ignore extensions ending with 'slice(url)'
                    if not extension_path.endswith(
                        "slice(url)"
                    ) and not extension_path.endswith("slice($this)"):
                        return extension_path


def _extract_elements(structure):
    elements = set()

    ignore_paths = []

    for element in structure["snapshot"]["element"]:
        path: str = element["id"]
        path_split = path.split(".")

        # Skip base element
        if len(path_split) == 1:
            continue

        # Skip elements that are children of ignored nodes
        if _should_ignore(path, ignore_paths):
            continue

        # Ignore elements with having specific path endings
        if path_split[-1] in IGNORE_ENDS:
            continue

        # Ignore elements where the cardinality is set to zero
        if element["max"] == "0" or element["max"] == 0:
            # Extend list of nodes that are remove due cardinality
            ignore_paths.append(path)
            continue

        # Check for specific extensions
        if extension := _get_extension(element, path):
            # Further ignore sub-elements of the extensions
            ignore_paths.append(path)
            elements.add(extension)
        else:
            # Add the base path of the element
            elements.add(path)

        # Check for and add slices, ignoring 'slice(url)' endings
        if "slicing" in element and "discriminator" in element["slicing"]:
            for discriminator in element["slicing"]["discriminator"]:
                if isinstance(discriminator, dict) and "path" in discriminator:
                    slice_path = f"{path}.slice({discriminator['path']})"
                    slice_path_split = slice_path.split(".")
                    if not slice_path_split[-1] in IGNORE_SLICES:
                        elements.add(slice_path)

    return elements


def _compare_structures(kbv_structure, epa_structure):
    """
    Returns a set of all properties, extensions, and slices from both structures.
    """

    kbv_elements = _extract_elements(kbv_structure)
    epa_elements = _extract_elements(epa_structure)

    return kbv_elements | epa_elements


def _determine_property_presence(profiles_to_compare, datapath):
    """
    Determines which properties are present in each set of KBV and ePA profiles.
    """
    all_properties = {}
    for kbv_group, epa_file in profiles_to_compare:
        epa_structure = _load_fhir_structure(datapath + epa_file)
        combined_properties = set()

        for kbv_file in kbv_group:
            kbv_structure = _load_fhir_structure(datapath + kbv_file)
            combined_properties |= _compare_structures(kbv_structure, epa_structure)

        all_properties[(tuple(kbv_group), epa_file)] = combined_properties

    return all_properties


def _check_property_presence(all_properties, profiles_to_compare, datapath):
    """
    Checks the presence of each property in each profile.
    """
    presence_data = {}
    for (kbv_group, epa_file), properties in all_properties.items():
        epa_structure = _load_fhir_structure(datapath + epa_file)
        epa_elements = _extract_elements(epa_structure)

        presence_data[(tuple(kbv_group), epa_file)] = {}
        for prop in properties:
            presence_data[(tuple(kbv_group), epa_file)][prop] = [prop in epa_elements]

            for kbv_file in kbv_group:
                kbv_structure = _load_fhir_structure(datapath + kbv_file)
                kbv_elements = _extract_elements(kbv_structure)
                presence_data[(tuple(kbv_group), epa_file)][prop].append(
                    prop in kbv_elements
                )

    return presence_data


def _get_remark(prop: str, classification: Classification) -> str:
    return (
        MANUAL_ENTRIES[prop]["remark"]
        if prop in MANUAL_ENTRIES and "remark" in MANUAL_ENTRIES[prop]
        else REMARKS[classification]
    )


def _classify_property(prop, kbv_presences, epa_presence):
    if prop in MANUAL_ENTRIES:
        return MANUAL_ENTRIES[prop].get("classification", Classification.MANUAL)
    if prop.split(".")[-1] in MANUAL_SUFFIXES:
        return Classification.MANUAL
    if any(kbv_presences):
        return Classification.USE if epa_presence else Classification.EXTENSION
    return Classification.NOT_USE


def _is_light_color(hex_color: str) -> bool:
    r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return luminance > 0.5


def _gen_structured_results(presence_data: dict) -> dict:
    """
    Generate a structured representation containing the rules for each target profile.

    The returned dictionary contains one item for each item in the argument `presence_data`. Each of these items
    contains the names of KBV and ePA profiles, presence information for each of their fields and their
    classifications and remarks.
    """
    mapping = {}
    # Iterate over all mappings (each entry are mapping to the same profile)
    for profiles, presences in presence_data.items():
        mapping[profiles] = {}

        # Generate the profile names
        kbv_profiles = [profile.replace(".json", "") for profile in profiles[0]]
        epa_profile = profiles[1].replace(".json", "")

        # Extract which profiles are KBV and which is the ePA one
        mapping[profiles][STRUCT_KBV_PROFILES] = kbv_profiles
        mapping[profiles][STRUCT_EPA_PROFILE] = epa_profile

        # Generate the mapping for all fields in those profiles
        mapping[profiles][STRUCT_FIELDS] = {}
        for field, field_presences in presences.items():
            field_updated = field
            extension_url = None

            # Get the field name while extracting the canonical for extensions
            if "extension" in field and "<br>" in field:
                field_updated, extension_url = field.split("<br>")
            mapping[profiles][STRUCT_FIELDS][field_updated] = {}
            if extension_url:
                mapping[profiles][STRUCT_FIELDS][field_updated][
                    STRUCT_EXTENSION
                ] = extension_url

            # Extract the presences for KBV and ePA profiles
            epa_presence, kbv_presences = field_presences[0], field_presences[1:]
            mapping[profiles][STRUCT_FIELDS][field_updated][epa_profile] = epa_presence
            for profile, presence in zip(kbv_profiles, kbv_presences):
                mapping[profiles][STRUCT_FIELDS][field_updated][profile] = presence

            # Fill the classification and remark for this field
            classification = _classify_property(field, kbv_presences, epa_presence)
            mapping[profiles][STRUCT_FIELDS][field_updated][
                STRUCT_CLASSIFICATION
            ] = classification
            mapping[profiles][STRUCT_FIELDS][field_updated][STRUCT_REMARK] = _get_remark(
                field, classification
            )

    return mapping
