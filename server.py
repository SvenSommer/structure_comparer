import argparse
from pathlib import Path
from flask import Flask, jsonify, request
from flask_swagger import swagger

from structure_comparer.serve import (
    get_mapping_fields_int,
    get_mapping_int,
    get_mappings_int,
    init_project,
)


def create_app(project_dir: Path):
    # create the app
    app = Flask(__name__)

    # project config
    project = init_project(project_dir)
    setattr(app, "project", project)

    @app.route("/", methods=["GET"])
    def hello_world():
        return "<p>Hello, World!</p>"

    @app.route("/mappings", methods=["GET"])
    def get_mappings():
        """
        Get the available mappings
        Returns a list with all mappings, including the name and the url to access it.
        ---
        produces:
          - application/json
        responses:
          200:
            description: Available mappings
            schema:
              required:
                - id
              properties:
                id:
                  type: object
                  required:
                    - name
                    - url
                  properties:
                    name:
                      type: string
                    url:
                      type: string
        """
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
              properties:
                present:
                    type: boolean
          - schema:
              id: MappingFieldProfiles
              type: object
              additionalProperties:
                $ref: "#/definitions/MappingFieldProfile"
          - schema:
              id: MappingField
              required:
                - classification
                - profiles
                - remark
              type: object
              properties:
                classification:
                  type: string
                extension:
                  type: string
                extra:
                  type: string
                profiles:
                  $ref: "#/definitions/MappingFieldProfiles"
                remark:
                  type: string
          - schema:
              id: MappingFields
              type: object
              additionalProperties:
                $ref: "#/definitions/MappingField"
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
                  $ref: "#/definitions/MappingFields"
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
              id: FieldInfoFields
              type: object
              additionalProperties:
                type: object
          - schema:
              id: FieldInfo
              type: object
              required:
                - id
                - fields
              properties:
                fields:
                  $ref: "#/definitions/FieldInfoFields"
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
              $ref: "#/definitions/FieldInfo"
          404:
            description: Mapping not found
        """
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
        print(request.get_json())
        return "", 501

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

    parser.add_argument(
        "--project-dir",
        type=Path,
        help="The project directory containing the profiles and config",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()

    app = create_app(project_dir=args.project_dir)
    app.run()
