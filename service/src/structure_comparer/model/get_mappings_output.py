from pydantic import BaseModel

from .mapping import Mapping


class GetMappingsOutput(BaseModel):
    mappings: list[Mapping]
