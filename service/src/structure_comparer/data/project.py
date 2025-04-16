from pathlib import Path
from typing import Dict

from ..manual_entries import ManualEntries
from ..model.project import Project as ProjectModel
from .comparison import Comparison
from .config import Config
from .profile import ProfileMap


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
        self.comparisons = {
            profiles.id: Comparison.create(
                ProfileMap.from_json(profiles, self.data_dir)
            )
            for profiles in self.profiles_to_compare_list
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
        config_data = Config()
        config_file.write_text(config_data.model_dump_json(indent=4), encoding="utf-8")

        return Project(path)

    def to_model(self, proj_name: str) -> ProjectModel:
        mappings = [comp.to_model(proj_name) for comp in self.comparisons.values()]

        model = ProjectModel(name=proj_name, mappings=mappings)
        return model
