import logging

from .classification import Classification
from .consts import (
    REMARKS,
    STRUCT_CLASSIFICATION,
    STRUCT_EPA_PROFILE,
    STRUCT_EXTRA,
    STRUCT_FIELDS,
    STRUCT_KBV_PROFILES,
    STRUCT_REMARK,
)
from .helpers import split_parent_child


DICT_MAPPINGS = "mappings"
DICT_FIXED = "fixed"
DICT_REMOVE = "remove"

IGNORE_CLASSIFICATIONS = [
    Classification.NOT_USE,
    Classification.EMPTY,
    Classification.COPY_FROM,
    Classification.MEDICATION_SERVICE,
]


logger = logging.getLogger(__name__)


def gen_mapping_dict(structured_mapping: dict):
    result = {}

    # Iterate over the different mappings
    for mappings in structured_mapping.values():
        epa_profile = mappings[STRUCT_EPA_PROFILE]

        # Iterate over the source profiles
        # These will be the roots of the mappings
        for kbv_profile in sorted(mappings[STRUCT_KBV_PROFILES]):
            profile_handling = {DICT_MAPPINGS: {}, DICT_FIXED: {}, DICT_REMOVE: []}
            for field, presences in mappings[STRUCT_FIELDS].items():
                classification = presences[STRUCT_CLASSIFICATION]
                remark = presences[STRUCT_REMARK]
                extra = presences[STRUCT_EXTRA]

                # If classification is the same as the parent, do not handle this entry
                parent, _ = split_parent_child(field)
                if _same_as_parent(presences, mappings[STRUCT_FIELDS].get(parent)):
                    continue

                # If 'manual' and should always be set to a fixed value
                if classification == Classification.FIXED:
                    profile_handling[DICT_FIXED][field] = extra

                # Otherwise only if value is present
                elif presences[kbv_profile]:
                    # If field should be used and remark was not changed
                    if (
                        classification in [Classification.USE, Classification.EXTENSION]
                        and remark == REMARKS[classification]
                    ):
                        # Put value in the same field
                        profile_handling[DICT_MAPPINGS][field] = field

                    # If 'copy_to' get the target field from extra field
                    elif classification == Classification.COPY_TO:
                        profile_handling[DICT_MAPPINGS][field] = extra

                    # Do not handle when classification should be ignored,
                    # or add to ignore if parent was not ignored or fixed
                    elif classification in IGNORE_CLASSIFICATIONS:
                        if (
                            parent_field := mappings[STRUCT_FIELDS].get(parent)
                        ) and parent_field[STRUCT_CLASSIFICATION] in [
                            Classification.USE,
                            Classification.EXTENSION,
                            Classification.COPY_TO,
                        ]:
                            profile_handling[DICT_REMOVE].append(field)

                    else:
                        # Log fall-through
                        logger.warning(
                            f"gen_mapping_dict: did not handle {kbv_profile}:{epa_profile}:{field}:{classification} {remark}"
                        )

            result[kbv_profile] = {epa_profile: profile_handling}

    return result


def _same_as_parent(presences: dict, parent_presences: dict | None):
    if not parent_presences:
        return False

    return presences[STRUCT_CLASSIFICATION] == parent_presences[STRUCT_CLASSIFICATION]
