import json
import os
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from .handler import (
    get_classifications_int,
    get_mapping_fields_int,
    get_mapping_int,
    get_mappings_int,
    init_project,
    post_mapping_classification_int,
)
from .model.mapping_input import MappingInput

origins = ["http://localhost:4200"]
projects_dir = Path(os.environ["PROJECTS_DIR"])
projects = {}
cur_project: str = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global projects

    # Set up
    if not projects_dir.exists():
        raise Exception("PROJECT_DIR does not point to a valid directory")

    projects = {p.name: init_project(p) for p in projects_dir.iterdir() if p.is_dir()}

    # Let the app do its job
    yield

    # Tear down
    pass


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.get("/projects")
def list_projects():
    return list(projects.keys())


@app.post(
    "/init_project",
    status_code=200,
    responses={400: {"error": {}}, 404: {"error": {}}},
)
def init_project_endpoint(project_name: str, response: Response):
    global cur_project
    if not project_name:
        response.status_code = 400
        return {"error": "Project name is required"}

    if project_name not in projects:
        response.status_code = 404
        return {"error": "Project does not exist"}

    # Set current project name
    cur_project = project_name

    return {"message": "Project initialized successfully"}


@app.post("/create_project", status_code=201, responses={400: {}, 409: {}})
def create_project(project_name: str, response: Response):
    global projects

    if not project_name:
        response.status_code = 400
        return {"error": "Project name is required"}

    project_path = projects_dir / project_name

    if project_path.exists():
        response.status_code = 409
        return {"error": "Project with same name already exists"}

    project_path.mkdir(parents=True, exist_ok=True)

    # Create empty manual_entries.yaml file
    manual_entries_file = project_path / "manual_entries.yaml"
    manual_entries_file.touch()

    # Create default config.json file
    config_file = project_path / "config.json"
    config_data = {
        "manual_entries_file": "manual_entries.yaml",
        "data_dir": "data",
        "html_output_dir": "docs",
        "mapping_output_file": "mapping.json",
        "profiles_to_compare": [],
    }
    config_file.write_text(json.dumps(config_data, indent=4))

    # Load the newly created project
    projects[project_name] = init_project(project_path)

    return {"message": "Project created successfully"}


@app.get("/classification")
def get_classifications():
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
    return get_classifications_int()


@app.get("/mappings", responses={412: {}})
def get_mappings(response: Response):
    """
    Get the available mappings
    Returns a list with all mappings, including the name and the url to access it.
    ---
    produces:
      - application/json
    definitions:
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
                $ref: "#/definitions/OverviewMapping"
    """
    if cur_project is None:
        response.status_code = 412
        return {"error": "project needs to be initialized before accessing"}

    return get_mappings_int(projects[cur_project])


@app.get("/mapping/{id}", responses={404: {}, 412: {}})
def get_mapping(id: str, response: Response):
    """
    Get a specific mapping
    Returns the mapping with the given id. This includes all details like classifications, presences in profiles, etc.
    ---
    produces:
      - application/json
    definitions:
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
                $ref: "#/definitions/MappingFieldProfile"
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
                $ref: "#/definitions/MappingField"
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
          $ref: "#/definitions/Mapping"
      404:
        description: Mapping not found
    """
    if cur_project is None:
        response.status_code = 412
        return {"error": "project needs to be initialized before accessing"}

    if mapping := get_mapping_int(projects[cur_project], id):
        return mapping
    else:
        response.status_code = 404
        return ""


@app.get("/mapping/{id}/fields", responses={404: {}, 412: {}})
def get_mapping_fields(id: str, response: Response):
    """
    Get the fields of a mapping
    Returns a brief list of the fields
    ---
    produces:
      - application/json
    definitions:
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
                $ref: "#/definitions/MappingFieldShort"
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
          $ref: "#/definitions/MappingShort"
      404:
        description: Mapping not found
    """
    if cur_project is None:
        response.status_code = 412
        return {"error": "project needs to be initialized before accessing"}

    if fields := get_mapping_fields_int(projects[cur_project], id):
        return fields
    else:
        response.status_code = 404
        return ""


@app.post(
    "/mapping/{mapping_id}/field/{field_id}/classification",
    responses={400: {}, 404: {}, 412: {}},
)
def post_mapping_classification(
    mapping_id: str, field_id: str, mapping: MappingInput, response: Response
):
    """
    Post a manual classification for a field
    Overrides the default action of a field. `action` that should set for the field, `target` is the target of copy action and `value` may be a fixed value.
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
    if cur_project is None:
        response.status_code = 412
        return {"error": "project needs to be initialized before accessing"}

    try:
        result = post_mapping_classification_int(
            projects[cur_project], mapping_id, field_id, mapping
        )
    except ValueError as e:
        error = {"error": str(e)}
        response.status_code = 400
        return error
    else:
        if result is None:
            response.status_code = 404
            return

        return


def serve():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    serve()
