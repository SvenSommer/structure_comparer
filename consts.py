from classification import Classification


STRUCT_KBV_PROFILES = "kbv_profiles"
STRUCT_EPA_PROFILE = "epa_profile"
STRUCT_FIELDS = "fields"
STRUCT_EXTENSION = "extension"
STRUCT_CLASSIFICATION = "classification"
STRUCT_REMARK = "remark"

REMARKS = {
    Classification.USE: "Eigenschaft und Wert werden übernommen",
    Classification.NOT_USE: "Bleibt vorerst leer, da keine Quellinformationen",
    Classification.EXTENSION: "Extension und Values werden übernommen",
    Classification.MANUAL: "",
    Classification.OTHER: "",
}
