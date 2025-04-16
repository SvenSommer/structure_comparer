from pydantic import BaseModel


class InitProjectInput(BaseModel):
    project_name: str
