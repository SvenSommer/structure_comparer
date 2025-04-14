import json
from pathlib import Path
from typing import Any, Dict, List

from .classification import Classification
from .compare import fill_classification_remark, generate_comparison
from .compare import load_profiles as _load_profiles
from .config import Config
from .consts import INSTRUCTIONS, REMARKS
from .data.comparison import Comparison, get_field_by_id
from .errors import (
    MappingNotFound,
    MappingTargetMissing,
    MappingTargetNotFound,
    MappingValueMissing,
    ProjectAlreadyExists,
    ProjectNotFound,
)
from .manual_entries import (
    MANUAL_ENTRIES,
    MANUAL_ENTRIES_CLASSIFICATION,
    MANUAL_ENTRIES_EXTRA,
)
from .model.mapping_input import MappingInput


class ProjectHandler:
    def __init__(self, projects_dir: Path):
        self.__projs_dir = projects_dir
        self.__projs: Dict[str, Any] = None

    @property
    def project_names(self) -> List[str]:
        return list(self.__projs.keys())

    def load_projects(self) -> None:
        self.__projs = {}

        for path in self.__projs_dir.iterdir():
            # Only handle directories
            if not path.is_dir():
                continue

            self.__load_project(path)

    def __load_project(self, path: Path) -> None:

        def project_obj():
            return None

        project_obj.dir = path
        project_obj.config = Config.from_json(path / "config.json")
        project_obj.data_dir = path / project_obj.config.data_dir

        # Get profiles to compare
        project_obj.profiles_to_compare_list = project_obj.config.profiles_to_compare

        # Load profiles
        load_profiles(project_obj)

        # Read the manual entries
        read_manual_entries(project_obj)

        if not self.__projs_dir.exists():
            raise Exception("PROJECT_DIR does not point to a valid directory")

        # Add project to list
        self.__projs[path.name] = project_obj

    def new_project(self, proj_name: str) -> None:
        project_path = self.__projs_dir / proj_name

        if project_path.exists():
            raise ProjectAlreadyExists()

        project_path.mkdir(parents=True, exist_ok=True)

        # Create empty manual_entries.yaml file
        manual_entries_file = project_path / "manual_entries.yaml"
        manual_entries_file.touch()

        # Create default config.json file
        config_file = project_path / "config.json"
        config_data = {
            "manual_entries_file": "manual_entries.yaml",
            "data_dir": "data",
            "html_output_dir": "docs",
            "mapping_output_file": "mapping.json",
            "profiles_to_compare": [],
        }
        config_file.write_text(json.dumps(config_data, indent=4))

        # Load the newly created project
        self.__projs[proj_name] = self.__load_project(project_path)

    @staticmethod
    def get_classifications() -> Dict[str, List[Dict[str, str]]]:
        classifications = [
            {"value": c.value, "remark": REMARKS[c], "instruction": INSTRUCTIONS[c]}
            for c in Classification
        ]
        return {"classifications": classifications}

    def get_mappings(self, project_name: str):
        proj = self.__projs.get(project_name)

        if proj is None:
            raise ProjectNotFound()

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
                for id, profile_map in proj.comparisons.items()
            ]
        }

    def get_mapping(self, project_name: str, id: str):
        proj = self.__projs.get(project_name)

        if proj is None:
            raise ProjectNotFound()

        comparison = proj.comparisons.get(id)

        if not comparison:
            raise MappingNotFound()

        fill_classification_remark(comparison)
        result = comparison.dict()

        result["id"] = id

        return result

    def get_mapping_fields(self, project_name: str, id: str):
        proj = self.__projs.get(project_name)

        if proj is None:
            raise ProjectNotFound()

        comparison = proj.comparisons.get(id)

        if not comparison:
            raise MappingNotFound()

        fill_classification_remark(comparison)

        result = {"id": id}
        result["fields"] = [
            {"name": field.name, "id": field.id} for field in comparison.fields.values()
        ]

        return result

    def set_mapping_classification(
        self, project_name: str, mapping_id: str, field_id: str, mapping: MappingInput
    ):
        proj = self.__projs.get(project_name)

        if proj is None:
            raise ProjectNotFound()

        comparison = proj.comparisons.get(mapping_id)

        if not comparison:
            raise MappingNotFound()

        # Easiest way to get the fields
        fill_classification_remark(comparison)

        field = get_field_by_id(comparison, field_id)

        if field is None:
            return None

        action = Classification(mapping.action)

        # Check if action is allowed for this field
        if action not in field.classifications_allowed:
            raise MappingNotFound(
                f"action '{action.value}' not allowed for this field, allowed: {
                    ', '.join([field.value for field in field.classifications_allowed])}"
            )

        # Build the entry that should be created/updated
        new_entry = {MANUAL_ENTRIES_CLASSIFICATION: action}
        if action == Classification.COPY_FROM or action == Classification.COPY_TO:
            if target_id := mapping.target:
                target = get_field_by_id(comparison, target_id)

                if target is None:
                    raise MappingTargetNotFound()

                new_entry[MANUAL_ENTRIES_EXTRA] = target.name
            else:
                raise MappingTargetMissing()
        elif action == Classification.FIXED:
            if fixed := mapping.value:
                new_entry[MANUAL_ENTRIES_EXTRA] = fixed
            else:
                raise MappingValueMissing()

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


def _get_field_by_id(field_id: str, comparison: Comparison) -> Comparison | None:
    for field in comparison.fields.values():
        if field.id == field_id:
            return field.name
    return None
