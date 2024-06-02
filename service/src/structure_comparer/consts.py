from .classification import Classification

REMARKS = {
    Classification.USE: "Eigenschaft und Wert(e) werden übernommen",
    Classification.NOT_USE: "Eigenschaft und Wert(e) werden NICHT übernommen",
    Classification.EMPTY: "Bleibt vorerst leer, da keine Quellinformationen vorhanden sind",
    Classification.EXTENSION: "Extension und Wert(e) werden übernommen",
    Classification.MANUAL: "",
    Classification.COPY_FROM: "Wird aus {} übernommen",
    Classification.COPY_TO: "Wird in {} übernommen",
    Classification.FIXED: "Wird fix auf '{}' gesetzt",
    Classification.MEDICATION_SERVICE: "Wird durch den Medication Service gesetzt",
}

INSTRUCTIONS = {
    Classification.USE: "Eigenschaft und Wert(e) werden ÜBERNOMMEN",
    Classification.NOT_USE: "Eigenschaft und Wert(e) werden NICHT übernommen",
    Classification.EMPTY: "Bleibt vorerst LEER, da keine Quellinformationen vorhanden sind",
    Classification.EXTENSION: "Extension und Wert(e) werden ÜBERNOMMEN",
    Classification.MANUAL: "Eigenen VERMERK machen",
    Classification.COPY_FROM: "Wert(e) werden AUS einem anderen Feld übernommen",
    Classification.COPY_TO: "Wert(e) werden IN einem anderen Feld übernommen",
    Classification.FIXED: "Wert wird FIX festgelegt",
    Classification.MEDICATION_SERVICE: "Wert durch den MEDICATION SERVICE gesetzt",
}
