import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path

from pydantic import BaseModel, ValidationError

from ..errors import InitializationError

logger = logging.getLogger(__name__)


class ProfileConfig(BaseModel):
    file: Path
    version: str = None
    simplifier_url: str = None
    file_download_url: str = None


class MappingConfig(BaseModel):
    sourceprofiles: list[ProfileConfig]
    targetprofile: ProfileConfig


class CompareConfig(BaseModel):
    id: str
    version: str
    status: str = "draft"
    mappings: MappingConfig = []
    last_updated: str = (datetime.now(timezone.utc) + timedelta(hours=2)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


class ProjectConfig(BaseModel):
    name: str | None = None
    manual_entries_file: str = "manual_entries.yaml"
    data_dir: str = "data"
    html_output_dir: str = "docs"
    mapping_output_file: str = "mapping.json"
    profiles_to_compare: list[CompareConfig] = []
    show_remarks: bool = True
    show_warnings: bool = True
    _file_path: Path

    @staticmethod
    def from_json(file: str | Path) -> "ProjectConfig":
        file = Path(file)

        try:
            content = file.read_text(encoding="utf-8")
            config = ProjectConfig.model_validate_json(content)

        except ValidationError as e:
            msg = f"failed to load config from {str(file)}"
            logger.error(msg)
            logger.error(e.errors())
            raise InitializationError(msg)

        else:
            config._file_path = file

            # Fix name if missing
            if config.name is None:
                config.name = file.parent.name

            config.write()
            return config

    def write(self):
        content = self.model_dump_json(indent=4)
        self._file_path.write_text(content, encoding="utf-8")
