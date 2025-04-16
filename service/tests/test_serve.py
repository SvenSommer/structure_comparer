from pathlib import Path

from structure_comparer.data.config import Config
from structure_comparer.manual_entries import MANUAL_ENTRIES

from structure_comparer import handler


def test_init_project():
    project_dir = Path("service/tests/files/project")
    assert project_dir.exists()

    project = handler.init_project(project_dir)
    assert project is not None
    assert project.dir == project_dir

    assert project.config is not None
    assert isinstance(project.config, Config)

    assert project.data_dir == project_dir / "data"

    assert project.profiles_to_compare_list is not None
    assert len(project.profiles_to_compare_list) > 0

    assert project.comparisons is not None
    assert len(project.comparisons) == len(project.profiles_to_compare_list)

    assert MANUAL_ENTRIES._data is not None
