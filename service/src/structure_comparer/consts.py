from .classification import Classification

REMARKS = {
    Classification.USE: "Eigenschaft und Wert werden übernommen",
    Classification.NOT_USE: "Wird nicht übernommen",
    Classification.EMPTY: "Bleibt vorerst leer, da keine Quellinformationen",
    Classification.EXTENSION: "Extension und Values werden übernommen",
    Classification.MANUAL: "",
    Classification.OTHER: "",
    Classification.COPY_FROM: "Wird aus {} übernommen",
    Classification.COPY_TO: "Wird in {} übernommen",
    Classification.FIXED: "Wird fix auf '{}' gesetzt",
    Classification.MEDICATION_SERVICE: "Wird durch den Medication Service selbst gesetzt",
}
