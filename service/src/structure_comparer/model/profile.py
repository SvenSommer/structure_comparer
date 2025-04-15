from pydantic import BaseModel


class Profile(BaseModel):
    profile_key: str
    name: str
    version: str
