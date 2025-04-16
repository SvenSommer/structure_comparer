from pathlib import Path

from ..model.package import Package as PackageModel
from .profile import Profile


class Package:
    def __init__(self, path: Path):
        self.path = path
        self.profiles: list[Profile] = None
        self.__load_profiles()

    @property
    def name(self) -> str:
        return self.path.name.split("#")[0]

    @property
    def version(self) -> str | None:
        return self.path.name.split("#")[1] if "#" in self.path.name else None

    def __load_profiles(self) -> None:
        self.profiles = [
            Profile.from_json(file, self)
            for file in self.path.iterdir()
            if file.is_file()
        ]

    def to_model(self) -> PackageModel:
        profiles = [p.to_model() for p in self.profiles]
        return PackageModel(name=self.name, version=self.version, profiles=profiles)
