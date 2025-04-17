from pydantic import BaseModel

from .profile import Profile as Profile


class Package(BaseModel):
    display: str | None = None
    name: str
    version: str
    profiles: list[Profile]
