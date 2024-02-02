import logging
import re

from classification import Classification
from consts import (
    REMARKS,
    STRUCT_CLASSIFICATION,
    STRUCT_EPA_PROFILE,
    STRUCT_FIELDS,
    STRUCT_KBV_PROFILES,
    STRUCT_REMARK,
)


DICT_MAPPINGS = "mappings"
DICT_VALUES = "values"


logger = logging.getLogger(__name__)


def gen_mapping_dict(structured_mapping: dict):
    result = {}

    # Regex to extract the field to copy this value to
    move_rexgex = re.compile(r"[wW]ird in ([\w\.\[\]:]+)")

    # Regex to extract the fixed value to set
    fix_regex = re.compile(r"Wird fix auf \'([\w:/\.-]+)' gesetzt")

    # Iterate over the different mappings
    for mappings in structured_mapping.values():
        epa_profile = mappings[STRUCT_EPA_PROFILE]

        # Iterate over the source profiles
        # These will be the roots of the mappings
        for kbv_profile in mappings[STRUCT_KBV_PROFILES]:
            profile_handling = {DICT_MAPPINGS: {}, DICT_VALUES: {}}
            for field, presences in mappings[STRUCT_FIELDS].items():
                classification = presences[STRUCT_CLASSIFICATION]
                remark = presences[STRUCT_REMARK]

                # If 'manual' and should always be set to a fixed value
                if classification == Classification.MANUAL and (
                    match := fix_regex.search(remark)
                ):
                    profile_handling[DICT_VALUES][field] = match.group(1)

                # Otherwise only if value is present
                elif presences[kbv_profile]:
                    # If field should be used and remark was not changed
                    if (
                        classification in [Classification.USE, Classification.EXTENSION]
                        and remark == REMARKS[classification]
                    ):
                        # Put value in the same field
                        profile_handling[DICT_MAPPINGS][field] = field

                    # If the field should be placed in other field
                    elif classification in [
                        Classification.USE,
                        Classification.EXTENSION,
                        Classification.MANUAL,
                    ] and (match := move_rexgex.search(remark)):
                        # Get new field from regex
                        profile_handling[DICT_MAPPINGS][field] = match.group(1)

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
            profile_handling[DICT_VALUES] = {
                key: value
                for key, value in sorted(profile_handling[DICT_VALUES].items())
            }

            result[kbv_profile] = {epa_profile: profile_handling}

    return result
