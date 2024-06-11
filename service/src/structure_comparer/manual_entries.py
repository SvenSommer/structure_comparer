import copy
import json
from pathlib import Path
from typing import Dict

import yaml

from .classification import Classification

MANUAL_ENTRIES_CLASSIFICATION = "classification"
MANUAL_ENTRIES_REMARK = "remark"
MANUAL_ENTRIES_EXTRA = "extra"


class ManualEntries:
    _data = {}
    _file: Path = None

    @property
    def entries(self):
        return self._data.get("entries")

    def read(self, file: str | Path):
        self._file = Path(file)

        if self._file.suffix == ".json":
            data = json.loads(self._file.read_text(encoding="utf-8"))
        elif self._file.suffix == ".yaml":
            data = yaml.safe_load(self._file.read_text(encoding="utf-8"))

        self._data["entries"] = {}
        for id, mappings in data.items():
            for value in mappings.values():
                # Interpret the classification as an enum
                value[MANUAL_ENTRIES_CLASSIFICATION] = Classification(
                    value[MANUAL_ENTRIES_CLASSIFICATION]
                )
            self._data["entries"][id] = mappings

    def write(self):
        data = copy.deepcopy(self.entries)
        for mapping in data.values():
            for value in mapping.values():
                value[MANUAL_ENTRIES_CLASSIFICATION] = value[
                    MANUAL_ENTRIES_CLASSIFICATION
                ].value

        if self._file.suffix == ".json":
            self._file.write_text(json.dumps(data, indent=4), encoding="utf-8")
        elif self._file.suffix == ".yaml":
            self._file.write_text(yaml.safe_dump(data), encoding="utf-8")

    def __iter__(self):
        return iter(self._data["entries"])

    def __getitem__(self, key):
        return self._data["entries"].get(key)

    def __setitem__(self, key, value):
        self._data["entries"][key] = value


class ManualMappings:
    def __init__(self, data: Dict) -> None:
        self.data = data

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, key):
        return self.data.get(key)

    def __setitem__(self, key, value):
        self.data[key] = value


MANUAL_ENTRIES = ManualEntries()
