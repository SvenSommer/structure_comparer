from pathlib import Path

from structure_comparer.data.config import ProjectConfig
from structure_comparer.manual_entries import MANUAL_ENTRIES

from structure_comparer import handler


def test_init_project():
    project_dir = Path("service/tests/files/project")
    assert project_dir.exists()

    project = handler.init_project(project_dir)
    assert project is not None
    assert project.dir == project_dir

    assert project.config is not None
    assert isinstance(project.config, ProjectConfig)

    assert project.data_dir == project_dir / "data"

    assert project.mappings_list is not None
    assert len(project.mappings_list) > 0

    assert project.comparisons is not None
    assert len(project.comparisons) == len(project.mappings_list)

    assert MANUAL_ENTRIES._data is not None
