import copy
import json
import logging
from pathlib import Path
from typing import Dict

import yaml
from pydantic import BaseModel

from .classification import Classification

MANUAL_ENTRIES_CLASSIFICATION = "classification"
MANUAL_ENTRIES_REMARK = "remark"
MANUAL_ENTRIES_EXTRA = "extra"

logger = logging.getLogger(__name__)


class ManualMapping(BaseModel):
    classification: Classification
    extra: str = None
    remark: str = None


class ManualMappings:
    def __init__(self, data: Dict[str, dict]) -> None:
        self.data = {k: ManualMapping(**v) for k, v in data.items()}

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, key) -> "ManualEntries":
        return self.data.get(key)

    def __setitem__(self, key, value) -> None:
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def to_dict(self) -> Dict:
        data = copy.deepcopy(self.data)
        for name, value in data.items():
            try:
                value[MANUAL_ENTRIES_CLASSIFICATION] = value[
                    MANUAL_ENTRIES_CLASSIFICATION
                ].value
            except TypeError as e:
                e.add_note(f"converting field {name}")
                raise
        return data


class ManualEntries:
    _data = {}
    _file: Path = None

    @property
    def entries(self) -> Dict[str, ManualMappings] | None:
        return self._data.get("entries")

    def read(self, file: str | Path):
        self._file = Path(file)
        content = self._file.read_text(encoding="utf-8")

        if self._file.suffix == ".json":
            data = json.loads(content)
        elif self._file.suffix == ".yaml":
            data = yaml.safe_load(content)

        self._data["entries"] = {}
        if data is not None:
            self._data["entries"] = {
                id: ManualMappings(mappings) for id, mappings in data.items()
            }

    def write(self):
        data = {}
        for id, mappings in self.entries.items():
            try:
                data[id] = mappings.to_dict()
            except TypeError as e:
                e.add_note(f"with ID {id}")
                raise
        if self._file.suffix == ".json":
            content = json.dumps(data, indent=4)
        elif self._file.suffix == ".yaml":
            content = yaml.safe_dump(data)

        if content is not None:
            self._file.write_text(content, encoding="utf-8")

    def __iter__(self):
        return iter(self._data["entries"])

    def __getitem__(self, key):
        return self._data["entries"].get(key)

    def __setitem__(self, key, value):
        self._data["entries"][key] = value
