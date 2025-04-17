from pydantic import BaseModel

from ..classification import Classification
from .profile import Profile, ProfileField


class Mapping(BaseModel):
    id: str
    name: str
    url: str
    version: str
    last_updated: str
    status: str
    sources: list[Profile]
    target: Profile


class MappingField(BaseModel):
    id: str
    name: str
    classification: Classification
    extra: str | None = None
    profiles: dict[str, ProfileField]
    remark: str
    classifications_allowed: list[Classification]


class MappingFieldsOutput(BaseModel):
    id: str
    fields: list[MappingField]
