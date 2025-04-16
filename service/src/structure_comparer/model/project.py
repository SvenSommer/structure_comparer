from pydantic import BaseModel

from .mapping import Mapping


class Project(BaseModel):
    name: str
    mappings: list[Mapping]


class ProjectInput(BaseModel):
    name: str
