from pydantic import BaseModel

from .profile import Profile


class MappingOverview(BaseModel):
    id: str
    name: str
    url: str
    version: str
    last_updated: str
    status: str
    sources: list[Profile]
    target: Profile
