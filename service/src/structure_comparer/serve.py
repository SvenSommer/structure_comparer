import json
from pathlib import Path
from uuid import uuid4
from flask import jsonify
from structure_comparer.consts import INSTRUCTIONS, REMARKS

from .classification import Classification
from .data.comparison import Comparison, get_field_by_id
from .manual_entries import (
    MANUAL_ENTRIES,
    MANUAL_ENTRIES_CLASSIFICATION,
    MANUAL_ENTRIES_EXTRA,
)
from .compare import (
    load_profiles as _load_profiles,
    generate_comparison,
    fill_classification_remark,
)


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
    project.comparisons = {
        entry.id: generate_comparison(entry) for entry in profile_maps.values()
    }


def get_classifications_int():
    classifications = [
        {
            "value": c.value,
            "remark": REMARKS[c],
            "instruction": INSTRUCTIONS[c]
        }
        for c in Classification
    ]
    return jsonify({"classifications": classifications})


def get_mappings_int(project):
    return {
        "mappings": [
            {
                "id": id,
                "name": profile_map.name,
                "url": f"/mapping/{id}",
                "version": profile_map.version,
                "last_updated": profile_map.last_updated,
                "status": profile_map.status,
                "sources": [
                    {
                        "profile_key": profile.profile_key,
                        "name": profile.name,
                        "version": profile.version,
                        "simplifier_url": profile.simplifier_url
                    }
                    for profile in profile_map.sources
                ],
                "target": {
                    "profile_key": profile_map.target.profile_key,
                    "name": profile_map.target.name,
                    "version": profile_map.target.version,
                    "simplifier_url": profile_map.target.simplifier_url
                }
            }
            for id, profile_map in project.comparisons.items()
        ]
    }



def get_mapping_int(project, id: str):
    comparison = project.comparisons.get(id)

    if not comparison:
        return None

    fill_classification_remark(comparison)
    result = comparison.dict()

    result["id"] = id

    return result


def get_mapping_fields_int(project, id: str):
    comparison = project.comparisons.get(id)

    if not comparison:
        return None

    fill_classification_remark(comparison)

    result = {"id": id}
    result["fields"] = [
        {"name": field.name, "id": field.id} for field in comparison.fields.values()
    ]

    return result


def post_mapping_field_int(project, mapping_id: str, field_id: str, content: dict):
    comparison = project.comparisons.get(mapping_id)

    if not comparison:
        return None

    # Easiest way to get the fields
    fill_classification_remark(comparison)

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
        if (target := content.get("target")) and target == field_id:
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


def post_mapping_classification_int(
    project, mapping_id: str, field_id: str, content: dict
):
    comparison = project.comparisons.get(mapping_id)

    if not comparison:
        return None

    # Easiest way to get the fields
    fill_classification_remark(comparison)

    field = get_field_by_id(comparison, field_id)

    if field is None:
        return None

    action = Classification(content.get("action"))

    # Check if action is allowed for this field
    if action not in field.classifications_allowed:
        raise ValueError(
            f"action '{action.value}' not allowed for this field, allowed: {', '.join([field.value for field in field.classifications_allowed])}"
        )

    # Build the entry that should be created/updated
    manual_entry = {MANUAL_ENTRIES_CLASSIFICATION: action}
    if action == Classification.COPY_FROM or action == Classification.COPY_TO:
        if target_id := content.get("target"):
            target = get_field_by_id(comparison, target_id)

            if target is None:
                raise ValueError("'target' does not exists")

            manual_entry[MANUAL_ENTRIES_EXTRA] = target.name
        else:
            raise ValueError("field 'target' missing")
    elif action == Classification.FIXED:
        if fixed := content.get("fixed"):
            manual_entry[MANUAL_ENTRIES_EXTRA] = fixed
        else:
            raise ValueError("field 'fixed' missing")

    # Clean up possible manual entry this was copied from before
    if (
        field.name in MANUAL_ENTRIES.entries
        and MANUAL_ENTRIES_EXTRA in MANUAL_ENTRIES[field.name]
    ):
        del MANUAL_ENTRIES.entries[MANUAL_ENTRIES[field.name][MANUAL_ENTRIES_EXTRA]]

    # Apply the manual entry
    MANUAL_ENTRIES[field.name] = manual_entry

    # Handle the partner entry for copy actions
    if action == Classification.COPY_FROM:
        MANUAL_ENTRIES[target.name] = {
            MANUAL_ENTRIES_CLASSIFICATION: Classification.COPY_TO,
            MANUAL_ENTRIES_EXTRA: field.name,
        }
    elif action == Classification.COPY_TO:
        MANUAL_ENTRIES[target.name] = {
            MANUAL_ENTRIES_CLASSIFICATION: Classification.COPY_FROM,
            MANUAL_ENTRIES_EXTRA: field.name,
        }

    # Save the changes
    MANUAL_ENTRIES.write()

    return True


def _get_field_by_id(field_id: str, comparison: Comparison) -> Comparison | None:
    for field in comparison.fields.values():
        if field.id == field_id:
            return field.name
    return None
