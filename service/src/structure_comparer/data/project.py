from pathlib import Path
from typing import Dict

from ..manual_entries import ManualEntries
from ..model.project import Project as ProjectModel
from ..model.project import ProjectOverview as ProjectOverviewModel
from .comparison import Comparison
from .config import ProjectConfig
from .package import Package
from .profile import ProfileMap


class Project:
    def __init__(self, path: Path):
        self.dir = path
        self.config = ProjectConfig.from_json(path / "config.json")

        self.comparisons: Dict[str, Comparison] = None
        self.manual_entries: ManualEntries = None

        self.pkgs: list[Package] = None

        # Get profiles to compare
        self.profiles_to_compare_list = self.config.profiles_to_compare

        self.__load_packages()

        # Load profiles
        self.__load_profiles()

        # Read the manual entries
        self.__read_manual_entries()

    def __load_packages(self) -> None:
        self.pkgs = [Package(dir) for dir in self.data_dir.iterdir() if dir.is_dir()]

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
    def create(path: Path, project_name: str) -> "Project":
        path.mkdir(parents=True, exist_ok=True)

        # Create empty manual_entries.yaml file
        manual_entries_file = path / "manual_entries.yaml"
        manual_entries_file.touch()

        # Create default config.json file
        config_file = path / "config.json"
        config_data = ProjectConfig(name=project_name)
        config_file.write_text(config_data.model_dump_json(indent=4), encoding="utf-8")

        return Project(path)

    @property
    def name(self) -> str:
        return self.config.name

    @property
    def key(self) -> str:
        return self.dir.name

    @property
    def url(self) -> str:
        return "/project/" + self.key

    @name.setter
    def name(self, value: str):
        self.config.name = value
        self.config.write()

    @property
    def data_dir(self) -> Path:
        return self.dir / self.config.data_dir

    def to_model(self) -> ProjectModel:
        mappings = [comp.to_model(self.key) for comp in self.comparisons.values()]
        pkgs = [p.to_model() for p in self.pkgs]

        return ProjectModel(name=self.name, mappings=mappings, packages=pkgs)

    def to_overview_model(self) -> ProjectOverviewModel:
        return ProjectOverviewModel(name=self.name, url=self.url)
