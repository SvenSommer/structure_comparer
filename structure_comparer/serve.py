from collections import OrderedDict
import json
from pathlib import Path
from uuid import uuid4

from .classification import Classification
from .data.comparison import Comparison
from .manual_entries import (
    MANUAL_ENTRIES,
    MANUAL_ENTRIES_CLASSIFICATION,
    MANUAL_ENTRIES_EXTRA,
)
from .compare import compare_profile, load_profiles as _load_profiles


def init_project(project_dir: Path):
    project_obj = lambda: None
    project_obj.dir = project_dir
    project_obj.config = json.loads((project_dir / "config.json").read_text())
    project_obj.data_dir = project_dir / project_obj.config.get("data_dir", "data")

    # Get profiles to compare
    project_obj.profiles_to_compare_list = project_obj.config["profiles_to_compare"]

    # Load profiles
    load_profiles(project_obj)

    # Read the manual entries
    read_manual_entries(project_obj)

    return project_obj


def read_manual_entries(project):
    manual_entries_file = project.dir / project.config.get(
        "manual_entries_file", "manual_entries.json"
    )
    MANUAL_ENTRIES.read(manual_entries_file)


def load_profiles(project):
    profile_maps = _load_profiles(project.profiles_to_compare_list, project.data_dir)
    project.profiles_to_compare = {
        str(uuid4()): entry for entry in profile_maps.values()
    }


def get_mappings_int(project):
    return {
        "mappings": [
            {"id": id, "name": profile_map.name, "url": f"/mapping/{id}"}
            for id, profile_map in project.profiles_to_compare.items()
        ]
    }


def get_mapping_int(project, id: str):
    profile_map = project.profiles_to_compare.get(id)

    if not profile_map:
        return None

    comparison = compare_profile(profile_map)
    result = comparison.dict()

    result["id"] = id

    return result


def get_mapping_fields_int(project, id: str):
    profile_map = project.profiles_to_compare.get(id)

    if not profile_map:
        return None

    comparison = compare_profile(profile_map)

    result = {"id": id}
    result["fields"] = [
        {"name": field.name, "id": field.id} for field in comparison.fields.values()
    ]

    return result


def post_mapping_field_int(project, mapping_id: str, field_id: str, content: dict):
    profile_map = project.profiles_to_compare.get(mapping_id)

    if not profile_map:
        return None

    # Easiest way to get the fields
    comparison = compare_profile(profile_map)

    name = _get_field_by_id(field_id, comparison)

    if name is None:
        return None

    # Clean up possible manual entry this was copied from before
    if name in MANUAL_ENTRIES.entries and MANUAL_ENTRIES_EXTRA in MANUAL_ENTRIES[name]:
        del MANUAL_ENTRIES.entries[MANUAL_ENTRIES[name][MANUAL_ENTRIES_EXTRA]]

    if (target := content.get("target")) and field_id != target:
        # Get target field name
        target = _get_field_by_id(target, comparison)

        if target is None:
            return None

        # Create the entries to copy from and to
        MANUAL_ENTRIES[name] = {
            MANUAL_ENTRIES_CLASSIFICATION: Classification.COPY_TO,
            MANUAL_ENTRIES_EXTRA: target,
        }
        MANUAL_ENTRIES[target] = {
            MANUAL_ENTRIES_CLASSIFICATION: Classification.COPY_FROM,
            MANUAL_ENTRIES_EXTRA: name,
        }
    else:
        # If entry is mapped to itself, simply mark it as "use"
        if target := content.get("target") and target == field_id:
            MANUAL_ENTRIES[name] = {MANUAL_ENTRIES_CLASSIFICATION: Classification.USE}

        # If mapped to nothing, mark it as "ignore"
        elif "target" in content and content["target"] is None:
            MANUAL_ENTRIES[name] = {
                MANUAL_ENTRIES_CLASSIFICATION: Classification.NOT_USE
            }

        # if fixed, mark it as "fixed" and add the fixed value
        elif "fixed" in content:
            MANUAL_ENTRIES[name] = {
                MANUAL_ENTRIES_CLASSIFICATION: Classification.FIXED,
                MANUAL_ENTRIES_EXTRA: content["fixed"],
            }

        else:
            return False

    # Save the changes
    MANUAL_ENTRIES.write()

    return True


def _get_field_by_id(field_id: str, comparison: Comparison) -> str | None:
    for field in comparison.fields.values():
        if field.id == field_id:
            return field.name
    return None
