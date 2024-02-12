from typing import Tuple


def split_parent_child(field) -> Tuple[str, str]:
    """
    Split the field into the parent and child name

    The parent and child are separated by the last `.`.
    """

    parent, child = field.rsplit(".", 1)

    return parent, child
