import json
from pathlib import Path

from .classification import Classification

MANUAL_ENTRIES_CLASSIFICATION = "classification"
MANUAL_ENTRIES_REMARK = "remark"
MANUAL_ENTRIES_EXTRA = "extra"


class ManualEntries:
    _data = {}

    @property
    def entries(self):
        return self._data.get("entries")

    def read(self, file: str | Path):
        data = json.loads(Path(file).read_text())

        # Interpret the classification as an enum
        for value in data.values():
            value[MANUAL_ENTRIES_CLASSIFICATION] = Classification(
                value[MANUAL_ENTRIES_CLASSIFICATION]
            )

        self._data["entries"] = data

    def __iter__(self):
        return iter(self._data["entries"])

    def __getitem__(self, key):
        return self._data["entries"].get(key)


MANUAL_ENTRIES = ManualEntries()
