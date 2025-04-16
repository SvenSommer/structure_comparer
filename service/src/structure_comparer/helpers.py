def get_field_by_id(mapping, field_id: str):
    for field in mapping.fields.values():
        if field.id == field_id:
            return field
    return None
