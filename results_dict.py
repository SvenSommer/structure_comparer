import logging
import re

from classification import Classification
from consts import (
    REMARKS,
    STRUCT_CLASSIFICATION,
    STRUCT_EPA_PROFILE,
    STRUCT_EXTRA,
    STRUCT_FIELDS,
    STRUCT_KBV_PROFILES,
    STRUCT_REMARK,
)


DICT_MAPPINGS = "mappings"
DICT_FIXED = "fixed"

IGNORE_CLASSIFICATIONS = [Classification.NOT_USE, Classification.COPY_FROM]


logger = logging.getLogger(__name__)


def gen_mapping_dict(structured_mapping: dict):
    result = {}

    # Iterate over the different mappings
    for mappings in structured_mapping.values():
        epa_profile = mappings[STRUCT_EPA_PROFILE]

        # Iterate over the source profiles
        # These will be the roots of the mappings
        for kbv_profile in mappings[STRUCT_KBV_PROFILES]:
            profile_handling = {DICT_MAPPINGS: {}, DICT_FIXED: {}}
            for field, presences in mappings[STRUCT_FIELDS].items():
                classification = presences[STRUCT_CLASSIFICATION]
                remark = presences[STRUCT_REMARK]
                extra = presences[STRUCT_EXTRA]

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

                    # Do not handle when classification should be ignored
                    elif classification in IGNORE_CLASSIFICATIONS:
                        pass

                    # Do not handle when 'not use'
                    elif classification == Classification.NOT_USE:
                        pass
                    else:
                        # Log fall-through
                        logger.warning(
                            f"gen_mapping_dict: did not handle {kbv_profile}:{epa_profile}:{field}:{classification} {remark}"
                        )

            profile_handling[DICT_MAPPINGS] = {
                key: value
                for key, value in sorted(profile_handling[DICT_MAPPINGS].items())
            }
            profile_handling[DICT_FIXED] = {
                key: value
                for key, value in sorted(profile_handling[DICT_FIXED].items())
            }

            result[kbv_profile] = {epa_profile: profile_handling}

    return result
