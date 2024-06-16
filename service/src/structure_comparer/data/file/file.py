from pathlib import Path
from typing import Dict

from structure_comparer.classification import Classification

from .manual_entries import (
    MANUAL_ENTRIES,
    MANUAL_ENTRIES_CLASSIFICATION,
    MANUAL_ENTRIES_EXTRA,
)


class DataHandler:
    def __init__(self, config: Dict, project_dir: Path) -> None:
        self.config = config
        self._init_manual_files(project_dir)

    def _init_manual_files(self, project_dir: Path) -> None:
        manual_entries_file = project_dir / self.config.get(
            "manual_entries_file", "manual_entries.json"
        )
        MANUAL_ENTRIES.read(manual_entries_file)

    def update_classification(
        self,
        mapping_id: str,
        field_name: str,
        classification: Classification,
        extra: str = None,
    ):
        if classification is None:
            raise ValueError("'classification' is None")
        if mapping_id is None:
            raise ValueError("'mapping_id' is None")
        if field_name is None:
            raise ValueError("'field_name' is None")

        new_entry = {MANUAL_ENTRIES_CLASSIFICATION: classification}
        if not extra is None:
            new_entry[MANUAL_ENTRIES_EXTRA] = extra

        # Clean up possible manual entry this was copied from before
        manual_entries = MANUAL_ENTRIES[mapping_id]
        if (manual_entry := manual_entries[field_name]) and (
            manual_entry[MANUAL_ENTRIES_CLASSIFICATION] == Classification.COPY_FROM
            or manual_entry[MANUAL_ENTRIES_CLASSIFICATION] == Classification.COPY_TO
        ):
            del manual_entries[manual_entry[MANUAL_ENTRIES_EXTRA]]

        # Apply the manual entry
        manual_entries[field_name] = new_entry

        # Handle the partner entry for copy actions
        if classification == Classification.COPY_FROM:
            if extra is None:
                raise ValueError("'extra' is None")

            manual_entries[extra] = {
                MANUAL_ENTRIES_CLASSIFICATION: Classification.COPY_TO,
                MANUAL_ENTRIES_EXTRA: field_name,
            }
        elif classification == Classification.COPY_TO:
            if extra is None:
                raise ValueError("'extra' is None")

            manual_entries[extra] = {
                MANUAL_ENTRIES_CLASSIFICATION: Classification.COPY_FROM,
                MANUAL_ENTRIES_EXTRA: field_name,
            }

        # Save the changes
        MANUAL_ENTRIES.write()
