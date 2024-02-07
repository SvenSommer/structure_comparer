from enum import Enum


class Classification(Enum):
    USE = 1
    NOT_USE = 2
    EXTENSION = 3
    MANUAL = 4
    OTHER = 5
    COPY_FROM = "copy_from"
    COPY_TO = "copy_to"
