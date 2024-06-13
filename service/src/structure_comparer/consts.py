from .classification import Classification

REMARKS = {
    Classification.USE: "Property and value(s) will be retained",
    Classification.NOT_USE: "Property and value(s) will NOT be retained",
    Classification.EMPTY: "Will remain empty for now, as no source information is available",
    Classification.EXTENSION: "Extension and value(s) will be retained",
    Classification.MANUAL: "",
    Classification.COPY_FROM: "Mapped from '{}'",
    Classification.COPY_TO: "Mapped to '{}'",
    Classification.FIXED: "Set to '{}' fixed value",
    Classification.MEDICATION_SERVICE: "Set by the Medication Service",
}

INSTRUCTIONS = {
    Classification.USE: "Property and value(s) will be RETAINED",
    Classification.NOT_USE: "Property and value(s) will NOT be retained",
    Classification.EMPTY: "Will remain EMPTY for now, as no source information is available",
    Classification.EXTENSION: "Extension and value(s) will be RETAINED",
    Classification.MANUAL: "Make your own NOTE",
    Classification.COPY_FROM: "Value(s) will be MAPPED FROM another field",
    Classification.COPY_TO: "Value(s) will be MAPPED TO another field",
    Classification.FIXED: "Value will be FIXED",
    Classification.MEDICATION_SERVICE: "Value set by the MEDICATION SERVICE",
}
