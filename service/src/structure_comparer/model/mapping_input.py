from pydantic import BaseModel


class MappingInput(BaseModel):
    # properties:
    #   action:
    #     type: string
    #     enum:
    #       - copy_from
    #       - copy_to
    #       - fixed
    #       - use
    #       - not_use
    #       - empty
    #     description: Which action should be performed
    #   target:
    #     type: string
    #     description: Field that is targetted (for copy actions)
    #   value:
    #     type: string
    #     description: The fixed value
    # pass
    action: str
    target: str | None = None
    value: str | None = None
