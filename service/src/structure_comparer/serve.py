import json
from pathlib import Path

from flask import jsonify
from structure_comparer.consts import INSTRUCTIONS, REMARKS

from .classification import Classification
from .compare import generate_comparison
from .compare import load_profiles as _load_profiles
from .data.file import DataHandler


class Server:
    def __init__(self, project_dir: Path):
        self.dir = project_dir
        self.config = json.loads((project_dir / "config.json").read_text())
        self.data_dir = project_dir / self.config.get("data_dir", "data")

        # Get profiles to compare
        self.profiles_to_compare_list = self.config["profiles_to_compare"]

        self.data_handler = DataHandler(self.config, project_dir)

        # Load profiles
        self.load_profiles()

    def load_profiles(self):
        profile_maps = _load_profiles(self.profiles_to_compare_list, self.data_dir)
        self.comparisons = {
            entry.id: generate_comparison(entry) for entry in profile_maps.values()
        }

    def get_classifications(self):
        classifications = [
            {"value": c.value, "remark": REMARKS[c], "instruction": INSTRUCTIONS[c]}
            for c in Classification
        ]
        return jsonify({"classifications": classifications})

    def get_mappings(self):
        return {
            "mappings": [
                {
                    "id": id,
                    "name": profile_map.name,
                    "url": f"/mapping/{id}",
                    "version": profile_map.version,
                    "last_updated": profile_map.last_updated,
                    "status": profile_map.status,
                    "sources": [
                        {
                            "profile_key": profile.profile_key,
                            "name": profile.name,
                            "version": profile.version,
                            "simplifier_url": profile.simplifier_url,
                        }
                        for profile in profile_map.sources
                    ],
                    "target": {
                        "profile_key": profile_map.target.profile_key,
                        "name": profile_map.target.name,
                        "version": profile_map.target.version,
                        "simplifier_url": profile_map.target.simplifier_url,
                    },
                }
                for id, profile_map in self.comparisons.items()
            ]
        }

    def get_mapping(self, id: str):
        comparison = self.comparisons.get(id)

        if not comparison:
            return None

        comparison.fill_classification_remark()
        result = comparison.dict()

        result["id"] = id

        return result

    def get_mapping_fields(self, id: str):
        comparison = self.comparisons.get(id)

        if not comparison:
            return None

        comparison.fill_classification_remark()

        result = {"id": id}
        result["fields"] = [
            {"name": field.name, "id": field.id} for field in comparison.fields.values()
        ]

        return result

    def post_mapping_classification(
        self, mapping_id: str, field_id: str, content: dict
    ):
        comparison = self.comparisons.get(mapping_id)

        if not comparison:
            return None

        # Easiest way to get the fields
        comparison.fill_classification_remark()

        field = comparison.get_field_by_id(field_id)

        if field is None:
            return None

        action = Classification(content.get("action"))

        # Check if action is allowed for this field
        if action not in field.classifications_allowed:
            raise ValueError(
                f"action '{action.value}' not allowed for this field, allowed: {', '.join([field.value for field in field.classifications_allowed])}"
            )

        # Build the entry that should be created/updated
        extra = None
        if action == Classification.COPY_FROM or action == Classification.COPY_TO:
            if target_id := content.get("target"):
                target = comparison.get_field_by_id(target_id)

                if target is None:
                    raise ValueError("'target' does not exists")

                extra = target.name
            else:
                raise ValueError("field 'target' missing")
        elif action == Classification.FIXED:
            if fixed := content.get("fixed"):
                extra = fixed
            else:
                raise ValueError("field 'fixed' missing")

        self.data_handler.update_classification(mapping_id, field.name, action, extra)

        return True
