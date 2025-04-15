from pydantic import BaseModel


class Profile(BaseModel):
    profile_key: str
    name: str
    version: str


class Mapping(BaseModel):
    id: str
    name: str
    url: str
    version: str
    last_updated: str
    status: str
    sources: list[Profile]
    target: Profile
