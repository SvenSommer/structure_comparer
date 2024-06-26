import argparse
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger import swagger
from structure_comparer.serve import (
    get_classifications_int,
    get_mapping_fields_int,
    get_mapping_int,
    get_mappings_int,
    init_project,
    post_mapping_classification_int,
)


def create_app(project_dir: Path):
    # create the app
    app = Flask(__name__)
    CORS(app, origins="http://localhost:4200")

    # project config
    project = init_project(project_dir)
    setattr(app, "project", project)

    @app.route("/", methods=["GET"])
    def hello_world():
        return "<p>Hello, World!</p>"

    @app.route("/classification", methods=["GET"])
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
        return jsonify(get_mappings_int(app.project))

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
                classifications_allowed
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
        fields = get_mapping_fields_int(app.project, id)
        if fields:
            return fields
        else:
            return "", 404

    @app.route(
        "/mapping/<mapping_id>/field/<field_id>/classification", methods=["POST"]
    )
    def post_mapping_classification(mapping_id: str, field_id: str):
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
        try:
            result = post_mapping_classification_int(
                app.project, mapping_id, field_id, request.get_json()
            )
        except ValueError as e:
            error = {"error": str(e)}
            return jsonify(error), 400
        else:
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
