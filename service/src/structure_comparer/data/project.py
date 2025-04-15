import json
from pathlib import Path
from typing import Dict

from ..compare import generate_comparison, load_profiles
from ..config import Config
from ..manual_entries import ManualEntries
from .comparison import Comparison


class Project:
    def __init__(self, path: Path):
        self.dir = path
        self.config = Config.from_json(path / "config.json")
        self.data_dir = path / self.config.data_dir

        self.comparisons: Dict[str, Comparison] = None
        self.manual_entries: ManualEntries = None

        # Get profiles to compare
        self.profiles_to_compare_list = self.config.profiles_to_compare

        # Load profiles
        self.__load_profiles()

        # Read the manual entries
        self.__read_manual_entries()

    def __load_profiles(self):
        profile_maps = load_profiles(self.profiles_to_compare_list, self.data_dir)
        self.comparisons = {
            entry.id: generate_comparison(entry) for entry in profile_maps.values()
        }

    def __read_manual_entries(self):
        manual_entries_file = self.dir / self.config.manual_entries_file

        if not manual_entries_file.exists():
            manual_entries_file.touch()

        self.manual_entries = ManualEntries()
        self.manual_entries.read(manual_entries_file)

    @staticmethod
    def create(path: Path) -> "Project":
        path.mkdir(parents=True, exist_ok=True)

        # Create empty manual_entries.yaml file
        manual_entries_file = path / "manual_entries.yaml"
        manual_entries_file.touch()

        # Create default config.json file
        config_file = path / "config.json"
        config_data = {
            "manual_entries_file": "manual_entries.yaml",
            "data_dir": "data",
            "html_output_dir": "docs",
            "mapping_output_file": "mapping.json",
            "profiles_to_compare": [],
        }
        config_file.write_text(json.dumps(config_data, indent=4))

        return Project(path)
