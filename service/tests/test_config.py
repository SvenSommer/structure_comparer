from datetime import datetime, timedelta
from structure_comparer.config import CompareConfig, Config, ProfileConfig

SOURCE_PROFILE = {
    "file": "source1.json",
    "version": "1.0",
    "simplifier_url": "https://simplifier.net/packages/source1",
    "file_download_url": "https://simplifier.net/ui/packagefile/downloadsnapshotas?packageFileId=1234format=json",
}

TARGET_PROFILE = {
    "file": "target.json",
    "version": "2.0",
    "simplifier_url": "https://simplifier.net/packages/target",
    "file_download_url": "https://simplifier.net/ui/packagefile/downloadsnapshotas?packageFileId=4321format=json",
}

MAPPINGS = {
    "id": "91db64da-9777-4c5f-a7d4-e0601ab51ad1",
    "version": "1.0",
    "status": "active",
    "last_updated": "2024-01-01 00:00:00",
    "mappings": {
        "sourceprofiles": [SOURCE_PROFILE],
        "targetprofile": TARGET_PROFILE,
    },
}

FULL_EXAMPLE = {
    "manual_entries_file": "manual_entries.json",
    "data_dir": "data",
    "html_output_dir": "docs",
    "mapping_output_file": "mapping.json",
    "profiles_to_compare": [MAPPINGS],
    "show_remarks": True,
    "show_warnings": False,
}


def test_config_from_dict():
    result = Config.from_dict(FULL_EXAMPLE)

    assert result.manual_entries_file == "manual_entries.json"
    assert result.data_dir == "data"
    assert result.html_output_dir == "docs"
    assert result.mapping_output_file == "mapping.json"
    assert result.show_remarks is True
    assert result.show_warnings is False
    assert len(result.profiles_to_compare) == 1


def test_config_from_dict_defaults():
    input = {
        "profiles_to_compare": [],
    }

    result = Config.from_dict(input)

    assert result.manual_entries_file == "manual_entries.yaml"
    assert result.data_dir == "data"
    assert result.html_output_dir == "docs"
    assert result.mapping_output_file == "mapping.json"
    assert result.show_remarks is True
    assert result.show_warnings is True
    assert len(result.profiles_to_compare) == 0


def test_compare_config_from_dict():
    result = CompareConfig.from_dict(MAPPINGS)

    assert result.id == "91db64da-9777-4c5f-a7d4-e0601ab51ad1"
    assert result.version == "1.0"
    assert result.status == "active"
    assert result.mappings is not None
    assert result.last_updated == "2024-01-01 00:00:00"

    assert len(result.mappings.source_profiles) == 1
    assert result.mappings.target_profile is not None


def test_compare_config_from_dict_defaults():
    input = {
        "id": "91db64da-9777-4c5f-a7d4-e0601ab51ad1",
        "version": "1.0",
        "mappings": {
            "sourceprofiles": [],
            "targetprofile": TARGET_PROFILE,
        }
    }

    now = datetime.now()
    result = CompareConfig.from_dict(input)

    assert result.id == "91db64da-9777-4c5f-a7d4-e0601ab51ad1"
    assert result.version == "1.0"
    assert result.status == "draft"
    assert result.mappings is not None
    assert datetime.strptime(result.last_updated, "%Y-%m-%d %H:%M:%S") - \
        timedelta(hours=2) - now < timedelta(minutes=5)

    assert len(result.mappings.source_profiles) == 0
    assert result.mappings.target_profile is not None


def test_profile_config_from_dict():
    result = ProfileConfig.from_dict(SOURCE_PROFILE)

    assert result.file == "source1.json"
    assert result.version == "1.0"
    assert result.simplifier_url == "https://simplifier.net/packages/source1"
    assert (
        result.file_download_url
        == "https://simplifier.net/ui/packagefile/downloadsnapshotas?packageFileId=1234format=json"
    )


def test_profile_config_from_dict_defaults():
    input = {
        "file": "foo.json"
    }

    result = ProfileConfig.from_dict(input)

    assert result.file == "foo.json"
    assert result.version is None
    assert result.simplifier_url is None
    assert result.file_download_url is None
