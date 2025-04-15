class ProjectAlreadyExists(Exception):
    def __init__(self, msg="Project with same name already exists", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class ProjectNotFound(Exception):
    def __init__(self, msg="Project not found", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class MappingNotFound(Exception):
    def __init__(self, msg="Mapping not found", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class MappingTargetNotFound(Exception):
    def __init__(self, msg="Target not found", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class FieldNotFound(Exception):
    def __init__(self, msg="Field not found", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class MappingActionNotAllowed(Exception):
    def __init__(self, msg="Mapping action not allowed", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class MappingTargetMissing(Exception):
    def __init__(self, msg="Mapping target missing", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class MappingValueMissing(Exception):
    def __init__(self, msg="Mapping value missing", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
