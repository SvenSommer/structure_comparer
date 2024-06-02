from enum import Enum


class Classification(Enum):
    USE = "use"
    NOT_USE = "not_use"
    EMPTY = "empty"
    EXTENSION = "extension"
    MANUAL = "manual"
    COPY_FROM = "copy_from"
    COPY_TO = "copy_to"
    FIXED = "fixed"
    MEDICATION_SERVICE = "medication_service"
