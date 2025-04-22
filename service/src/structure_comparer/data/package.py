from pathlib import Path

from ..model.package import Package as PackageModel
from .config import PackageConfig
from .profile import Profile


class Package:
    def __init__(self, data_dir: Path, config: PackageConfig):
        self.data_dir = data_dir
        self.config = config
        self.profiles: list[Profile] = None
        self.__load_profiles()

    @property
    def name(self) -> str:
        return self.config.name

    @property
    def version(self) -> str | None:
        return self.config.version

    @property
    def id(self) -> str:
        return f"{self.name}#{self.version}"

    @property
    def display(self) -> str:
        return self.config.display

    def __load_profiles(self) -> None:
        self.profiles = [
            Profile.from_json(file, self)
            for file in (self.data_dir / self.id).iterdir()
            if file.is_file()
        ]

    def to_model(self) -> PackageModel:
        profiles = [p.to_model() for p in self.profiles]

        definition = {
            "name": self.name,
            "version": self.version,
            "profiles": profiles,
        }

        if self.display:
            definition["display"] = self.display

        return PackageModel(**definition)
