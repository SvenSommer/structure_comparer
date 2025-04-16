from pathlib import Path
from typing import Dict, List

from .classification import Classification
from .consts import INSTRUCTIONS, REMARKS
from .data.project import Project
from .errors import (
    FieldNotFound,
    MappingNotFound,
    MappingTargetMissing,
    MappingTargetNotFound,
    MappingValueMissing,
    ProjectNotFound,
)
from .helpers import get_field_by_id
from .manual_entries import MANUAL_ENTRIES_CLASSIFICATION, MANUAL_ENTRIES_EXTRA
from .model.mapping import Mapping as MappingModel
from .model.mapping_input import MappingInput
from .model.project import Project as ProjectModel


class ProjectsHandler:
    def __init__(self, projects_dir: Path):
        self.__projs_dir = projects_dir
        self.__projs: Dict[str, Project] = None

    @property
    def project_keys(self) -> List[str]:
        return list(self.__projs.keys())

    def load_projects(self) -> None:
        self.__projs = {}

        for path in self.__projs_dir.iterdir():
            # Only handle directories
            if path.is_dir():
                self.__projs[path.name] = Project(path)

    def new_project(self, proj_name: str) -> None:
        project_path = self.__projs_dir / proj_name

        # Load the newly created project
        self.__projs[proj_name] = Project.create(project_path)

    @staticmethod
    def get_classifications() -> Dict[str, List[Dict[str, str]]]:
        classifications = [
            {"value": c.value, "remark": REMARKS[c], "instruction": INSTRUCTIONS[c]}
            for c in Classification
        ]
        return {"classifications": classifications}

    def get_project(self, project_name: str) -> ProjectModel:
        proj = self.__projs.get(project_name)

        if proj is None:
            raise ProjectNotFound()

        return proj.to_model(project_name)

    def get_mappings(self, project_name: str) -> List[MappingModel]:
        proj = self.__projs.get(project_name)

        if proj is None:
            raise ProjectNotFound()

        return [comp.to_model(project_name) for comp in proj.comparisons.values()]

    def get_mapping(self, project_name: str, mapping_id: str) -> MappingModel:
        mapping = self.__get_mapping(project_name, mapping_id)
        return mapping.to_model(project_name)

    def get_mapping_fields(self, project_name: str, mapping_id: str):
        mapping = self.__get_mapping(project_name, mapping_id)

        result = {"id": mapping_id}
        result["fields"] = [
            {"name": field.name, "id": field.id} for field in mapping.fields.values()
        ]

        return result

    def set_mapping_classification(
        self, project_name: str, mapping_id: str, field_id: str, mapping: MappingInput
    ):
        proj = self.__projs.get(project_name)

        # Easiest way to get the fields is from mapping
        mapping = self.__get_mapping(project_name, mapping_id, proj)
        field = get_field_by_id(mapping, field_id)

        if field is None:
            raise FieldNotFound()

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
                target = get_field_by_id(mapping, target_id)

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
        manual_entries = proj.manual_entries[mapping_id]
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
        manual_entries.write()

        return True

    def __get_mapping(self, project_name, mapping_id, proj: Project = None):
        if proj is None:
            proj = self.__projs.get(project_name)

        if proj is None:
            raise ProjectNotFound()

        mapping = proj.comparisons.get(mapping_id)

        if not mapping:
            raise MappingNotFound()

        mapping.fill_classification_remark(proj.manual_entries)

        return mapping
