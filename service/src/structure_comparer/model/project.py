from pydantic import BaseModel

from .mapping import MappingOverview
from .package import Package


class Project(BaseModel):
    name: str
    mappings: list[MappingOverview]
    packages: list[Package]


class ProjectInput(BaseModel):
    name: str


class ProjectOverview(BaseModel):
    name: str
    url: str


class ProjectList(BaseModel):
    projects: list[ProjectOverview]
