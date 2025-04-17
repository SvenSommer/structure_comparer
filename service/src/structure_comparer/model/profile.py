from pydantic import BaseModel


class Profile(BaseModel):
    profile_key: str
    name: str
    version: str


class ProfileField(BaseModel):
    min: int
    max: str
    must_support: bool
