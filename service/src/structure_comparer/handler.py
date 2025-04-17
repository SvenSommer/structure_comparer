import logging
from pathlib import Path
from typing import Dict, List

from pydantic import ValidationError

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
from .model.mapping import MappingOverview as MappingOverviewModel
from .model.mapping_input import MappingInput
from .model.project import Project as ProjectModel
from .model.project import ProjectInput as ProjectInputModel
from .model.project import ProjectList as ProjectListModel

logger = logging.getLogger(__name__)


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
                try:
                    self.__projs[path.name] = Project(path)
                except ValidationError as e:
                    logger.error(e.errors())
                    raise e

    def get_project_list(self) -> ProjectListModel:
        projects = [p.to_overview_model() for p in self.__projs.values()]
        return ProjectListModel(projects=projects)

    def get_project(self, project_key: str) -> ProjectModel:
        proj = self.__projs.get(project_key)

        if proj is None:
            raise ProjectNotFound()

        return proj.to_model()

    def update_or_create_project(
        self, proj_key: str, input: ProjectInputModel
    ) -> ProjectModel:

        # Check if update
        if proj := self.__projs.get(proj_key):
            proj.name = input.name

        # Create new one otherwise
        else:
            project_path = self.__projs_dir / proj_key

            # Load the newly created project
            proj = Project.create(project_path, input.name)
            self.__projs[proj_key] = proj

        return proj.to_model()

    @staticmethod
    def get_classifications() -> Dict[str, List[Dict[str, str]]]:
        classifications = [
            {"value": c.value, "remark": REMARKS[c], "instruction": INSTRUCTIONS[c]}
            for c in Classification
        ]
        return {"classifications": classifications}

    def get_mappings(self, project_key: str) -> List[MappingOverviewModel]:
        proj = self.__projs.get(project_key)

        if proj is None:
            raise ProjectNotFound()

        return [comp.to_overview_model() for comp in proj.mappings.values()]

    def get_mapping(self, project_key: str, mapping_id: str) -> MappingOverviewModel:
        mapping = self.__get_mapping(project_key, mapping_id)
        return mapping.to_overview_model()

    def get_mapping_fields(self, project_key: str, mapping_id: str):
        mapping = self.__get_mapping(project_key, mapping_id)

        result = {"id": mapping_id}
        result["fields"] = [
            {"name": field.name, "id": field.id} for field in mapping.fields.values()
        ]

        return result

    def set_mapping_classification(
        self, project_key: str, mapping_id: str, field_id: str, mapping: MappingInput
    ):
        proj = self.__projs.get(project_key)

        # Easiest way to get the fields is from mapping
        mapping = self.__get_mapping(project_key, mapping_id, proj)
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

    def __get_mapping(self, project_key, mapping_id, proj: Project = None):
        if proj is None:
            proj = self.__projs.get(project_key)

        if proj is None:
            raise ProjectNotFound()

        mapping = proj.mappings.get(mapping_id)

        if not mapping:
            raise MappingNotFound()

        mapping.fill_classification_remark(proj.manual_entries)

        return mapping
