import json
import logging
from pathlib import Path
from typing import Dict, List
from uuid import uuid4

from fhir.resources.R4B.elementdefinition import ElementDefinition
from fhir.resources.R4B.structuredefinition import StructureDefinition
from pydantic import ValidationError

from ..model.profile import Profile as ProfileModel
from ..model.profile import ProfileField as ProfileFieldModel

logger = logging.getLogger(__name__)


class Profile:
    def __init__(self, data: dict, package=None) -> None:
        self.__data = StructureDefinition.model_validate(data)
        self.__fields: List[str, ProfileField] = None
        self.__init_fields()
        self.__package = package

    def __str__(self) -> str:
        return f"(name={self.name}, version={self.version}, fields={self.fields})"

    def __repr__(self) -> str:
        return str(self)

    def __init_fields(self) -> None:
        self.__fields: Dict[str, ProfileField] = {}
        for elem in self.__data.snapshot.element:
            field = ProfileField(elem)
            if field.path is not None:
                self.__fields[field.id] = field

    @staticmethod
    def from_json(path: Path, package=None) -> "Profile":
        if not path.exists():
            raise FileNotFoundError(
                f"The file {path} does not exist. Please check the file path and try again."
            )

        try:
            return Profile(
                data=json.loads(path.read_text(encoding="utf-8")), package=package
            )

        except Exception as e:
            logger.error("failed to read file '%s'", str(path))
            logger.exception(e)

    @property
    def name(self) -> str:
        return self.__data.name

    @property
    def version(self) -> str:
        return self.__data.version

    @property
    def fields(self) -> Dict[str, "ProfileField"]:
        return self.__fields

    @property
    def key(self) -> str:
        return f"{self.name}|{self.version}"

    @property
    def id(self) -> str:
        return self.__data.id

    def __lt__(self, other: "Profile") -> bool:
        return self.key < other.key

    def to_model(self) -> ProfileModel:
        try:
            model = ProfileModel(
                profile_key=self.key, name=self.name, version=self.version
            )
        except ValidationError as e:
            logger.exception(e)

        else:
            return model


class ProfileField:
    def __init__(
        self,
        data: ElementDefinition,
    ) -> None:
        self.__data = data
        self.__id = str(uuid4())

    def __str__(self) -> str:
        return f"(name={self.name}, id={self.id}, min={self.min}, max={self.max})"

    def __repr__(self) -> str:
        return str(self)

    @property
    def id(self) -> str:
        return self.__id

    @property
    def path_full(self) -> str:
        return self.__data.id

    @property
    def path(self) -> str:
        return (
            ("." + self.path_full.split(".", 1)[1]) if "." in self.path_full else None
        )

    @property
    def min(self) -> int:
        return self.__data.min

    @property
    def max(self) -> str:
        return self.__data.max

    @property
    def must_support(self) -> bool:
        return self.__data.mustSupport if self.__data.mustSupport else False

    def to_model(self) -> ProfileFieldModel:
        return ProfileFieldModel(
            min=self.min, max=self.max, must_support=self.must_support
        )
