from pydantic import BaseModel

from .mapping import MappingOverview


class GetMappingsOutput(BaseModel):
    mappings: list[MappingOverview]
