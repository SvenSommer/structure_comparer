import json
from pathlib import Path
from uuid import uuid4

from .manual_entries import MANUAL_ENTRIES
from .compare import load_profiles as _load_profiles


def init_project(project_dir: Path):
    project_obj = lambda: None
    project_obj.dir = project_dir
    project_obj.config = json.loads((project_dir / "config.json").read_text())
    project_obj.data_dir = project_dir / project_obj.config.get("data_dir", "data")

    # Get profiles to compare
    project_obj.profiles_to_compare_list = project_obj.config["profiles_to_compare"]

    # Load profiles
    load_profiles(project_obj)

    # Read the manual entries
    read_manual_entries(project_obj)

    return project_obj


def read_manual_entries(project):
    manual_entries_file = project.dir / project.config.get(
        "manual_entries_file", "manual_entries.json"
    )
    MANUAL_ENTRIES.read(manual_entries_file)


def load_profiles(project):
    profile_maps = _load_profiles(project.profiles_to_compare_list, project.data_dir)
    project.profiles_to_compare = {
        str(uuid4()): entry for entry in profile_maps.values()
    }


def get_mappings_int(project):
    return {
        id: {"name": profile_map.name, "url": f"/mapping/{id}"}
        for id, profile_map in project.profiles_to_compare.items()
    }
