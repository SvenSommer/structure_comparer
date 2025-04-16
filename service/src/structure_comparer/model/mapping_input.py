from pydantic import BaseModel

from ..classification import Classification


class MappingInput(BaseModel):
    action: Classification
    target: str | None = None
    value: str | None = None
