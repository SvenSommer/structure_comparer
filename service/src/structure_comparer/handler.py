from pathlib import Path

from .classification import Classification
from .compare import fill_classification_remark, generate_comparison
from .compare import load_profiles as _load_profiles
from .config import Config
from .consts import INSTRUCTIONS, REMARKS
from .data.comparison import Comparison, get_field_by_id
from .manual_entries import (
    MANUAL_ENTRIES,
    MANUAL_ENTRIES_CLASSIFICATION,
    MANUAL_ENTRIES_EXTRA,
)
from .model.mapping_input import MappingInput


def init_project(project_dir: Path):
    def project_obj():
        return None

    project_obj.dir = project_dir
    project_obj.config = Config.from_json(project_dir / "config.json")
    project_obj.data_dir = project_dir / project_obj.config.data_dir

    # Get profiles to compare
    project_obj.profiles_to_compare_list = project_obj.config.profiles_to_compare

    # Load profiles
    load_profiles(project_obj)

    # Read the manual entries
    read_manual_entries(project_obj)

    return project_obj


def read_manual_entries(project):
    manual_entries_file = project.dir / project.config.manual_entries_file

    if not manual_entries_file.exists():
        manual_entries_file.touch()

    MANUAL_ENTRIES.read(manual_entries_file)


def load_profiles(project):
    profile_maps = _load_profiles(project.profiles_to_compare_list, project.data_dir)
    project.comparisons = {
        entry.id: generate_comparison(entry) for entry in profile_maps.values()
    }


def get_classifications_int():
    classifications = [
        {"value": c.value, "remark": REMARKS[c], "instruction": INSTRUCTIONS[c]}
        for c in Classification
    ]
    return {"classifications": classifications}


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
                        "simplifier_url": profile.simplifier_url,
                    }
                    for profile in profile_map.sources
                ],
                "target": {
                    "profile_key": profile_map.target.profile_key,
                    "name": profile_map.target.name,
                    "version": profile_map.target.version,
                    "simplifier_url": profile_map.target.simplifier_url,
                },
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


def post_mapping_classification_int(
    project, mapping_id: str, field_id: str, mapping: MappingInput
):
    comparison = project.comparisons.get(mapping_id)

    if not comparison:
        return None

    # Easiest way to get the fields
    fill_classification_remark(comparison)

    field = get_field_by_id(comparison, field_id)

    if field is None:
        return None

    action = Classification(mapping.action)

    # Check if action is allowed for this field
    if action not in field.classifications_allowed:
        raise ValueError(
            f"action '{action.value}' not allowed for this field, allowed: {
                ', '.join([field.value for field in field.classifications_allowed])}"
        )

    # Build the entry that should be created/updated
    new_entry = {MANUAL_ENTRIES_CLASSIFICATION: action}
    if action == Classification.COPY_FROM or action == Classification.COPY_TO:
        if target_id := mapping.target:
            target = get_field_by_id(comparison, target_id)

            if target is None:
                raise ValueError("'target' does not exists")

            new_entry[MANUAL_ENTRIES_EXTRA] = target.name
        else:
            raise ValueError("field 'target' missing")
    elif action == Classification.FIXED:
        if fixed := mapping.value:
            new_entry[MANUAL_ENTRIES_EXTRA] = fixed
        else:
            raise ValueError("field 'fixed' missing")

    # Clean up possible manual entry this was copied from before
    manual_entries = MANUAL_ENTRIES[mapping_id]
    if (manual_entry := manual_entries[field.name]) and (
        manual_entry[MANUAL_ENTRIES_CLASSIFICATION] == Classification.COPY_FROM
        or manual_entry[MANUAL_ENTRIES_CLASSIFICATION] == Classification.COPY_TO
    ):
        del manual_entries[manual_entry[MANUAL_ENTRIES_EXTRA]]

    # Apply the manual entry
    manual_entries[field.name] = new_entry

    # Handle the partner entry for copy actions
    if action == Classification.COPY_FROM:
        manual_entries[target.name] = {
            MANUAL_ENTRIES_CLASSIFICATION: Classification.COPY_TO,
            MANUAL_ENTRIES_EXTRA: field.name,
        }
    elif action == Classification.COPY_TO:
        manual_entries[target.name] = {
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
