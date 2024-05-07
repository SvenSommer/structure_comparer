import argparse
from pathlib import Path
from flask import Flask, jsonify, request
from flask_swagger import swagger
from flask_cors import CORS


from structure_comparer.serve import (
    get_mapping_fields_int,
    get_mapping_int,
    get_mappings_int,
    init_project,
    post_mapping_field_int,
)


def create_app(projects_dir: Path):
    # create the app
    app = Flask(__name__)
    CORS(app, origins="http://localhost:4200")
    setattr(app, "projects_dir", projects_dir)


    @app.route("/", methods=["GET"])
    def hello_world():
        if hasattr(app, "project") and hasattr(app.project, "dir"):
            project_name = app.project.dir
            return f"<p>Hello, World! Actual Project: {project_name}</p>"
        else:
            return "<p>Hello, World! No project loaded.</p>"
        

    @app.route("/projects", methods=["GET"])
    def list_projects():
        # Specify the base directory where project folders are located
        base_dir = Path(projects_dir)
        # List directories in the base directory
        projects = [d.name for d in base_dir.iterdir() if d.is_dir()]
        return jsonify(projects)

    @app.route("/project/<project>/load", methods=["POST"])
    def load_project(project: str):
        print("Loading project")
        # Get the project directory from the request
        data = request.get_json()
        print(data)
        project_dir_name = data.get('project')
        if project_dir_name:
            project_dir = projects_dir / project_dir_name
            # Check if the provided project directory exists
            if project_dir.exists() and project_dir.is_dir():
                # Initialize the project based on the concatenated directory
                project = init_project(project_dir)
                setattr(app, "project", project)
                return jsonify({"message": f"Project '{project_dir.name}' loaded successfully"})
            else:
                return jsonify({"error": f"Project directory '{project_dir_name}' does not exist"}), 404
        else:
            return jsonify({"error": "Project directory not specified"}), 400




    @app.route("/mappings", methods=["GET"])
    def get_mappings():
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
              properties:
                id:
                  type: string
                name:
                  type: string
                url:
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
        if not hasattr(app, "project") or not hasattr(app.project, "dir"):
            return jsonify({"error": "No project loaded"}), 404

        return get_mappings_int(app.project)


    @app.route("/mapping/<id>", methods=["GET"])
    def get_mapping(id: str):
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

        if not hasattr(app, "project") or not hasattr(app.project, "dir"):
            return jsonify({"error": "No project loaded"}), 404

        mapping = get_mapping_int(app.project, id)
          
        if mapping:
            return mapping
        else:
            return "", 404

    @app.route("/mapping/<id>/fields", methods=["GET"])
    def get_mapping_fields(id: str):
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
        if not hasattr(app, "project") or not hasattr(app.project, "dir"):
          return jsonify({"error": "No project loaded"}), 404

        fields = get_mapping_fields_int(app.project, id)
        if fields:
            return fields
        else:
            return "", 404

    @app.route("/mapping/<mapping_id>/field/<field_id>", methods=["POST"])
    def post_mapping_field(mapping_id: str, field_id: str):
        """
        Post a manual entry for a field
        Overrides the default classification of a field. A field can target a field with the same name or a different one to map the field, can point to 'null' to ignore it or can be set to a fixed value
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
              properties:
                target:
                  type: string
                  description: The target field
                fixed:
                  type: string
                  description: Fixed value to assign to the field
        responses:
          200:
            description: The field was updated
          404:
            description: Mapping or field not found
        """

        if not hasattr(app, "project") or not hasattr(app.project, "dir"):
          return jsonify({"error": "No project loaded"}), 404
        
        result = post_mapping_field_int(
            app.project, mapping_id, field_id, request.get_json()
        )
        if result is None:
            return "", 404

        return "", 200

    @app.route("/spec", methods=["GET"])
    def spec():
        swag = swagger(app)
        swag["info"]["version"] = "1.0"
        swag["info"]["title"] = "Structure Comparer"
        return jsonify(swag)

    return app


def get_args():
    parser = argparse.ArgumentParser(
        description="Compare profiles and generate mapping"
    )

    default_projects_dir = Path("./projects")

    parser.add_argument(
        "--projects-dir",
        type=Path,
        default=default_projects_dir,
        help="The directory the different projects. A project contains the profiles and config",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()

    app = create_app(projects_dir=args.projects_dir)
    app.run()
