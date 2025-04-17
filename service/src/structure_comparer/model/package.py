from pydantic import BaseModel

from .profile import Profile as Profile


class Package(BaseModel):
    name: str
    version: str | None = None
    profiles: list[Profile]
