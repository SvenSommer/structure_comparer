from pathlib import Path
from typing import Dict

from ..manual_entries import ManualEntries
from ..model.project import Project as ProjectModel
from ..model.project import ProjectOverview as ProjectOverviewModel
from .config import ProjectConfig
from .mapping import Mapping
from .package import Package


class Project:
    def __init__(self, path: Path):
        self.dir = path
        self.config = ProjectConfig.from_json(path / "config.json")

        self.mappings: Dict[str, Mapping] = None
        self.manual_entries: ManualEntries = None

        self.pkgs: list[Package] = None

        # Get profiles to compare
        self.mappings_list = self.config.mappings

        self.__load_packages()
        self.__load_mappings()
        self.__read_manual_entries()

    def __load_packages(self) -> None:
        self.pkgs = [Package(dir) for dir in self.data_dir.iterdir() if dir.is_dir()]

    def __load_mappings(self):
        self.mappings = {
            mapping_conf.id: Mapping(mapping_conf, self)
            for mapping_conf in self.mappings_list
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

    def get_profile(self, id: str, version: str):
        for pkg in self.pkgs:
            for profile in pkg.profiles:
                if profile.id == id and profile.version == version:
                    return profile

        return None

    def to_model(self) -> ProjectModel:
        mappings = [comp.to_overview_model() for comp in self.mappings.values()]
        pkgs = [p.to_model() for p in self.pkgs]

        return ProjectModel(name=self.name, mappings=mappings, packages=pkgs)

    def to_overview_model(self) -> ProjectOverviewModel:
        return ProjectOverviewModel(name=self.name, url=self.url)
