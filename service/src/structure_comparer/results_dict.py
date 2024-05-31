import logging
from typing import Dict

from .classification import Classification
from .data.comparison import Comparison
from .consts import REMARKS
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


def gen_mapping_dict(mapping_version: str, mapping_modified: str, mapping_status: str, structured_mapping: Dict[str, Comparison]):
    result = {}

    # Iterate over the different mappings
    for mappings in structured_mapping.values():
        # Iterate over the source profiles
        # These will be the roots of the mappings
        for source_profile in sorted(mappings.source_profiles):
            profile_handling = {DICT_MAPPINGS: {}, DICT_FIXED: {}, DICT_REMOVE: []}
            for field, presences in mappings.fields.items():

                # If classification is the same as the parent, do not handle this entry
                parent, _ = split_parent_child(field)
                comparison_parent = mappings.fields.get(parent)
                if (
                    not comparison_parent is None
                    and presences.classification == comparison_parent.classification
                ):
                    continue

                # If 'manual' and should always be set to a fixed value
                if presences.classification == Classification.FIXED:
                    profile_handling[DICT_FIXED][field] = presences.extra

                # Otherwise only if value is present
                elif presences.profiles[source_profile].present:
                    # If field should be used and remark was not changed
                    if (
                        presences.classification
                        in [Classification.USE, Classification.EXTENSION]
                        and presences.remark == REMARKS[presences.classification]
                    ):
                        # Put value in the same field
                        profile_handling[DICT_MAPPINGS][field] = field

                    # If 'copy_to' get the target field from extra field
                    elif presences.classification == Classification.COPY_TO:
                        profile_handling[DICT_MAPPINGS][field] = presences.extra

                    # Do not handle when classification should be ignored,
                    # or add to ignore if parent was not ignored or fixed
                    elif presences.classification in IGNORE_CLASSIFICATIONS:
                        if (
                            parent_field := mappings.fields.get(parent)
                        ) and parent_field.classification in [
                            Classification.USE,
                            Classification.EXTENSION,
                            Classification.COPY_TO,
                        ]:
                            profile_handling[DICT_REMOVE].append(field)

                    else:
                        # Log fall-through
                        logger.warning(
                            f"gen_mapping_dict: did not handle {source_profile}:{mappings.target_profile}:{field}:{presences.classification} {presences.remark}"
                        )

            if source_profile not in result:
                result[source_profile] = {}
            result[source_profile][mappings.target_profile] = {
                "version": mapping_version,
                "status": mapping_status,
                "last_updated": mapping_modified,
                "mappings": profile_handling[DICT_MAPPINGS],
                "fixed": profile_handling[DICT_FIXED],
                "remove": profile_handling[DICT_REMOVE],
            }

    return result