import os
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from .errors import (
    FieldNotFound,
    MappingActionNotAllowed,
    MappingNotFound,
    MappingTargetMissing,
    MappingTargetNotFound,
    MappingValueMissing,
    ProjectAlreadyExists,
    ProjectNotFound,
)
from .handler import ProjectsHandler
from .model.get_mappings_output import GetMappingsOutput
from .model.init_project_input import InitProjectInput
from .model.mapping import Mapping as MappingModel
from .model.mapping_input import MappingInput
from .model.project import Project as ProjectModel

origins = ["http://localhost:4200"]
handler: ProjectsHandler = None
cur_proj: str = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global handler

    # Set up
    handler = ProjectsHandler(Path(os.environ["PROJECTS_DIR"]))
    handler.load_projects()

    # Let the app do its job
    yield

    # Tear down
    pass


app = FastAPI(title="Structure Comparer", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def ping():
    return "pong"


@app.get("/projects", tags=["Projects"], deprecated=True)
async def get_projects_old():
    return handler.project_keys


@app.get("/project", tags=["Projects"])
async def get_project_keys() -> list[str]:
    return handler.project_keys


@app.get("/project/{project_key}", tags=["Projects"])
async def get_project(project_key: str, response: Response) -> ProjectModel:
    try:
        proj = handler.get_project(project_key)
        return proj

    except ProjectNotFound:
        response.status_code = 404
        return {"error": "Project not found"}


@app.post(
    "/init_project",
    tags=["Projects"],
    status_code=200,
    responses={400: {"error": {}}, 404: {"error": {}}},
    deprecated=True,
)
async def post_init_project(data: InitProjectInput, response: Response):
    global cur_proj

    if not data.project_name:
        response.status_code = 400
        return {"error": "Project name is required"}

    if data.project_name not in handler.project_keys:
        response.status_code = 404
        return {"error": "Project does not exist"}

    # Set current project name
    cur_proj = data.project_name

    return {"message": "Project initialized successfully"}


@app.post(
    "/create_project",
    tags=["Projects"],
    status_code=201,
    responses={400: {}, 409: {}},
    deprecated=True,
)
async def create_project_old(project_name: str, response: Response):

    if not project_name:
        response.status_code = 400
        return {"error": "Project name is required"}

    try:
        handler.new_project(project_name)

    except ProjectAlreadyExists as e:
        response.status_code = 409
        return {"error": str(e)}

    return {"message": "Project created successfully"}


@app.post(
    "/project/{project_key}",
    tags=["Projects"],
    status_code=201,
    responses={400: {}, 409: {}},
)
async def create_project(project_key: str, response: Response):

    if not project_key:
        response.status_code = 400
        return {"error": "Project name is required"}

    try:
        handler.new_project(project_key)

    except ProjectAlreadyExists as e:
        response.status_code = 409
        return {"error": str(e)}

    return {"message": "Project created successfully"}


@app.get("/classification", tags=["Classification"])
async def get_classifications():
    """
    Get all classifications
    ---
    produces:
      - application/json
    responses:
      200:
        description: Classifications
        schema:
          required:
            - classifications
          properties:
            classifications:
              type: array
              items:
                type: object
                properties:
                  value:
                    type: string
                  remark:
                    type: string
                  instruction:
                    type: string
    """
    return handler.get_classifications()


@app.get("/mappings", tags=["Mappings"], responses={412: {}}, deprecated=True)
async def get_mappings_old(response: Response) -> GetMappingsOutput:
    """
    Get the available mappings
    Returns a list with all mappings, including the name and the url to access it.
    ---
    produces:
      - application/json
    async definitions:
      - schema:
          id: OverviewMapping
          type: object
          required:
            - id
            - name
            - url
            - version
            - last_updated
            - status
            - sources
            - target
          properties:
            id:
              type: string
            name:
              type: string
            url:
              type: string
            version:
              type: string
            last_updated:
              type: string
            status:
              type: string
            sources:
              type: array
              items:
                type: object
                properties:
                  name:
                    type: string
                  profile_key:
                    type: string
                  simplifier_url:
                    type: string
                  version:
                    type: string
            target:
              type: object
              properties:
                name:
                  type: string
                profile_key:
                  type: string
                simplifier_url:
                  type: string
                version:
                  type: string
    responses:
      200:
        description: Available mappings
        schema:
          required:
            - mappings
          properties:
            mappings:
              type: array
              items:
                $ref: "#/async definitions/OverviewMapping"
    """
    if cur_proj is None:
        response.status_code = 412
        return {"error": "Project needs to be initialized before accessing"}

    try:
        mappings = handler.get_mappings(cur_proj)
        return GetMappingsOutput(mappings=mappings)

    except ProjectNotFound:
        response.status_code = 404
        return {"error": "Project not found"}


@app.get(
    "/project/{project_key}/mapping",
    tags=["Mappings"],
    responses={404: {}},
    deprecated=True,
)
async def get_mappings(project_key: str, response: Response) -> GetMappingsOutput:
    """
    Get the available mappings
    Returns a list with all mappings, including the name and the url to access it.
    ---
    produces:
      - application/json
    async definitions:
      - schema:
          id: OverviewMapping
          type: object
          required:
            - id
            - name
            - url
            - version
            - last_updated
            - status
            - sources
            - target
          properties:
            id:
              type: string
            name:
              type: string
            url:
              type: string
            version:
              type: string
            last_updated:
              type: string
            status:
              type: string
            sources:
              type: array
              items:
                type: object
                properties:
                  name:
                    type: string
                  profile_key:
                    type: string
                  simplifier_url:
                    type: string
                  version:
                    type: string
            target:
              type: object
              properties:
                name:
                  type: string
                profile_key:
                  type: string
                simplifier_url:
                  type: string
                version:
                  type: string
    responses:
      200:
        description: Available mappings
        schema:
          required:
            - mappings
          properties:
            mappings:
              type: array
              items:
                $ref: "#/async definitions/OverviewMapping"
    """
    try:
        mappings = handler.get_mappings(project_key)
        return GetMappingsOutput(mappings=mappings)

    except ProjectNotFound:
        response.status_code = 404
        return {"error": "Project not found"}


@app.get(
    "/mapping/{id}", tags=["Mappings"], responses={404: {}, 412: {}}, deprecated=True
)
async def get_mapping_old(id: str, response: Response) -> MappingModel:
    """
    Get a specific mapping
    Returns the mapping with the given id. This includes all details like classifications, presences in profiles, etc.
    ---
    produces:
      - application/json
    async definitions:
      - schema:
          id: MappingFieldProfile
          type: object
          required:
            - name
            - present
          properties:
            name:
              type: string
            present:
                type: boolean
      - schema:
          id: MappingField
          required:
            - id
            - name
            - classification
            - profiles
            - remark
          type: object
          properties:
            id:
              type: string
            name:
              type: string
            classification:
              type: string
            classifications_allowed:
              type: array
              items:
                string
            extension:
              type: string
            extra:
              type: string
            profiles:
              type: array
              items:
                $ref: "#/async definitions/MappingFieldProfile"
            remark:
              type: string
      - schema:
          id: Mapping
          type: object
          required:
            - id
            - name
            - source_profiles
            - target_profile
            - fields
          properties:
            fields:
              type: array
              items:
                $ref: "#/async definitions/MappingField"
            id:
              type: string
            name:
              type: string
            source_profiles:
              type: array
              items:
                type: string
            target_profile:
              type: string
    parameters:
      - in: path
        name: id
        type: string
        required: true
        description: The id of the mapping
    responses:
      200:
        description: The mapping with the given id
        schema:
          $ref: "#/async definitions/Mapping"
      404:
        description: Mapping not found
    """
    if cur_proj is None:
        response.status_code = 412
        return {"error": "Project needs to be initialized before accessing"}

    try:
        return handler.get_mapping(cur_proj, id)

    except (ProjectNotFound, MappingNotFound) as e:
        response.status_code = 404
        return {"error": str(e)}


@app.get(
    "/project/{project_key}/mapping/{mapping_id}",
    tags=["Mappings"],
    responses={404: {}},
)
async def get_mapping(
    project_key: str, mapping_id: str, response: Response
) -> MappingModel:
    """
    Get the available mappings
    Returns a list with all mappings, including the name and the url to access it.
    ---
    produces:
      - application/json
    async definitions:
      - schema:
          id: OverviewMapping
          type: object
          required:
            - id
            - name
            - url
            - version
            - last_updated
            - status
            - sources
            - target
          properties:
            id:
              type: string
            name:
              type: string
            url:
              type: string
            version:
              type: string
            last_updated:
              type: string
            status:
              type: string
            sources:
              type: array
              items:
                type: object
                properties:
                  name:
                    type: string
                  profile_key:
                    type: string
                  simplifier_url:
                    type: string
                  version:
                    type: string
            target:
              type: object
              properties:
                name:
                  type: string
                profile_key:
                  type: string
                simplifier_url:
                  type: string
                version:
                  type: string
    responses:
      200:
        description: Available mappings
        schema:
          required:
            - mappings
          properties:
            mappings:
              type: array
              items:
                $ref: "#/async definitions/OverviewMapping"
    """
    try:
        return handler.get_mapping(project_key, mapping_id)

    except (ProjectNotFound, MappingNotFound) as e:
        response.status_code = 404
        return {"error": str(e)}


@app.get(
    "/mapping/{id}/fields",
    tags=["Fields"],
    responses={404: {}, 412: {}},
    deprecated=True,
)
async def get_mapping_fields_old(id: str, response: Response):
    """
    Get the fields of a mapping
    Returns a brief list of the fields
    ---
    produces:
      - application/json
    async definitions:
      - schema:
          id: MappingFieldShort
          type: object
          reuqired:
            - id
            - name
          properties:
            id:
              type: string
            name:
              type: string
      - schema:
          id: MappingShort
          type: object
          required:
            - id
            - fields
          properties:
            fields:
              type: array
              items:
                $ref: "#/async definitions/MappingFieldShort"
            id:
              type: string
    parameters:
      - in: path
        name: id
        type: string
        required: true
        description: The id of the mapping
    responses:
      200:
        description: The fields of the mapping
        schema:
          $ref: "#/async definitions/MappingShort"
      404:
        description: Mapping not found
    """
    if cur_proj is None:
        response.status_code = 412
        return {"error": "Project needs to be initialized before accessing"}

    try:
        return handler.get_mapping_fields(cur_proj, id)

    except (ProjectNotFound, MappingNotFound) as e:
        response.status_code = 404
        return {"error": str(e)}


@app.get(
    "/project/{project_key}/mapping/{mapping_id}/field",
    tags=["Fields"],
    responses={404: {}},
)
async def get_mapping_fields(project_key: str, mapping_id: str, response: Response):
    """
    Get the fields of a mapping
    Returns a brief list of the fields
    ---
    produces:
      - application/json
    async definitions:
      - schema:
          id: MappingFieldShort
          type: object
          reuqired:
            - id
            - name
          properties:
            id:
              type: string
            name:
              type: string
      - schema:
          id: MappingShort
          type: object
          required:
            - id
            - fields
          properties:
            fields:
              type: array
              items:
                $ref: "#/async definitions/MappingFieldShort"
            id:
              type: string
    parameters:
      - in: path
        name: id
        type: string
        required: true
        description: The id of the mapping
    responses:
      200:
        description: The fields of the mapping
        schema:
          $ref: "#/async definitions/MappingShort"
      404:
        description: Mapping not found
    """
    try:
        return handler.get_mapping_fields(project_key, mapping_id)

    except (ProjectNotFound, MappingNotFound) as e:
        response.status_code = 404
        return {"error": str(e)}


@app.post(
    "/mapping/{mapping_id}/field/{field_id}/classification",
    tags=["Fields"],
    responses={400: {}, 404: {}, 412: {}},
    deprecated=True,
)
async def post_mapping_field_classification_old(
    mapping_id: str, field_id: str, mapping: MappingInput, response: Response
):
    """
    Post a manual classification for a field
    Overrides the async default action of a field. `action` that should set for the field, `target` is the target of copy action and `value` may be a fixed value.
    ---
    consumes:
      - application/json
    parameters:
      - in: path
        name: mapping_id
        type: string
        required: true
        description: The id of the mapping
      - in: path
        name: field_id
        type: string
        required: true
        description: The id of the field
      - in: body
        name: body
        schema:
          required:
            - action
          properties:
            action:
              type: string
              enum:
                - copy_from
                - copy_to
                - fixed
                - use
                - not_use
                - empty
              description: Which action should be performed
            target:
              type: string
              description: Field that is targetted (for copy actions)
            value:
              type: string
              description: The fixed value
    responses:
      200:
        description: The field was updated
      400:
        description: There was something wrong with the request
        schema:
          properties:
            error:
              type: string
              description: An error message
      404:
        description: Mapping or field not found
    """
    if cur_proj is None:
        response.status_code = 412
        return {"error": "Project needs to be initialized before accessing"}

    try:
        return handler.set_mapping_classification(
            cur_proj, mapping_id, field_id, mapping
        )

    except (ProjectNotFound, MappingNotFound, FieldNotFound) as e:
        response.status_code = 404
        return {"error": str(e)}

    except (
        MappingActionNotAllowed,
        MappingTargetMissing,
        MappingTargetNotFound,
        MappingValueMissing,
    ) as e:
        response.status_code = 400
        return {"error": str(e)}


@app.post(
    "/project/{project_key}/mapping/{mapping_id}/field/{field_id}/classification",
    tags=["Fields"],
    responses={400: {}, 404: {}},
)
async def post_mapping_field_classification(
    project_key: str,
    mapping_id: str,
    field_id: str,
    mapping: MappingInput,
    response: Response,
):
    """
    Post a manual classification for a field
    Overrides the async default action of a field. `action` that should set for the field, `target` is the target of copy action and `value` may be a fixed value.
    ---
    consumes:
      - application/json
    parameters:
      - in: path
        name: mapping_id
        type: string
        required: true
        description: The id of the mapping
      - in: path
        name: field_id
        type: string
        required: true
        description: The id of the field
      - in: body
        name: body
        schema:
          required:
            - action
          properties:
            action:
              type: string
              enum:
                - copy_from
                - copy_to
                - fixed
                - use
                - not_use
                - empty
              description: Which action should be performed
            target:
              type: string
              description: Field that is targetted (for copy actions)
            value:
              type: string
              description: The fixed value
    responses:
      200:
        description: The field was updated
      400:
        description: There was something wrong with the request
        schema:
          properties:
            error:
              type: string
              description: An error message
      404:
        description: Mapping or field not found
    """
    try:
        return handler.set_mapping_classification(
            project_key, mapping_id, field_id, mapping
        )

    except (ProjectNotFound, MappingNotFound, FieldNotFound) as e:
        response.status_code = 404
        return {"error": str(e)}

    except (
        MappingActionNotAllowed,
        MappingTargetMissing,
        MappingTargetNotFound,
        MappingValueMissing,
    ) as e:
        response.status_code = 400
        return {"error": str(e)}


def serve():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    serve()
