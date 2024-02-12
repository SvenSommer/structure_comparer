from typing import Tuple


def split_parent_child(field) -> Tuple[str, str]:
    """
    Split the field into the parent and child name

    The parent and child are separated either by the last `.` or `:`.
    """
    # Split the property in parent and child
    if (
        len(field.rsplit(".", 1)[0]) < len(field.rsplit(":", 1)[0])
        and len(field.rsplit(":", 1)) == 2
    ):
        parent, child = field.rsplit(":", 1)
    else:
        parent, child = field.rsplit(".", 1)

    return parent, child
