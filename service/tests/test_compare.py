from structure_comparer.classification import Classification
from structure_comparer.compare import __fill_allowed_classifications
from structure_comparer.data.mapping import MappingField, ProfileField

PROFILE_SOURCE1 = "source1"
PROFILE_SOURCE2 = "source2"
PROFILE_TARGET = "target"


def test_fill_allowed_classifications_all_present():
    sources = [PROFILE_SOURCE1, PROFILE_SOURCE2]
    target = PROFILE_TARGET

    field = MappingField("field", "1")
    field.profiles = {
        PROFILE_SOURCE1: ProfileField(PROFILE_SOURCE1, True),
        PROFILE_SOURCE2: ProfileField(PROFILE_SOURCE2, True),
        PROFILE_TARGET: ProfileField(PROFILE_TARGET, True),
    }

    __fill_allowed_classifications(field, sources, target)

    assert Classification.USE in field.classifications_allowed
    assert Classification.NOT_USE in field.classifications_allowed
    assert Classification.COPY_FROM in field.classifications_allowed
    assert Classification.COPY_TO in field.classifications_allowed

    assert Classification.EMPTY not in field.classifications_allowed


def test_fill_allowed_classifications_target_present():
    sources = [PROFILE_SOURCE1, PROFILE_SOURCE2]
    target = PROFILE_TARGET

    field = MappingField("field", "1")
    field.profiles = {
        PROFILE_SOURCE1: ProfileField(PROFILE_SOURCE1, False),
        PROFILE_SOURCE2: ProfileField(PROFILE_SOURCE2, False),
        PROFILE_TARGET: ProfileField(PROFILE_TARGET, True),
    }

    __fill_allowed_classifications(field, sources, target)

    assert Classification.COPY_FROM in field.classifications_allowed
    assert Classification.EMPTY in field.classifications_allowed

    assert Classification.USE not in field.classifications_allowed
    assert Classification.NOT_USE not in field.classifications_allowed
    assert Classification.COPY_TO not in field.classifications_allowed


def test_fill_allowed_classifications_source_present():
    sources = [PROFILE_SOURCE1, PROFILE_SOURCE2]
    target = PROFILE_TARGET

    field = MappingField("field", "1")
    field.profiles = {
        PROFILE_SOURCE1: ProfileField(PROFILE_SOURCE1, True),
        PROFILE_SOURCE2: ProfileField(PROFILE_SOURCE2, True),
        PROFILE_TARGET: ProfileField(PROFILE_TARGET, False),
    }

    __fill_allowed_classifications(field, sources, target)

    assert Classification.NOT_USE in field.classifications_allowed
    assert Classification.COPY_TO in field.classifications_allowed

    assert Classification.USE not in field.classifications_allowed
    assert Classification.COPY_FROM not in field.classifications_allowed
    assert Classification.EMPTY not in field.classifications_allowed
