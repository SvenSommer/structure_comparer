from classification import Classification

MANUAL_ENTRIES = {
    "MedicationRequest.insurance.reference": {
        "classification": Classification.OTHER,
        "remark": "Wird beim Mapping ignoriert",
    },
    "MedicationRequest.meta.profile": {
        "classification": Classification.FIXED,
        "extra": "https://gematik.de/fhir/epa-medication/StructureDefinition/epa-medication",
    },
    "MedicationRequest.requester.reference": {
        "classification": Classification.MEDICATION_SERVICE,
    },
    "MedicationRequest.subject.reference": {
        "classification": Classification.MEDICATION_SERVICE,
    },
    "MedicationRequest.identifier:rxPrescriptionProcessIdentifier": {
        "classification": Classification.EMPTY,
        "remark": "Dieser Identifier setzt sich aus der Task-ID und dem MedicationRequest.authoredOn zusammen. Er wird durch den Medication Service vergeben.",
    },
    "MedicationRequest.medication[x]:medicationReference": {
        "classification": Classification.MANUAL,
        "remark": "Die Referenz der KBV-Medikation wird durch eine Referenz auf eine EPA-Medikation ersetzt.",
    },
    "MedicationRequest.medication[x].reference": {
        "classification": Classification.EMPTY
    },
    "MedicationRequest.medication[x]:medicationReference.reference": {
        "classification": Classification.MANUAL,
        "remark": "Die Referenz ergibt sich aus der neu erzeugten EPA-Medikation.",
    },
    "MedicationRequest.substitution.allowed[x]:allowedBoolean": {
        "classification": Classification.EMPTY,
        "remark": "Einschränkung wird nicht übernommen",
    },
    "Medication.code.coding:PZN": {
        "classification": Classification.COPY_FROM,
        "extra": "Medication.code.coding:pznCode",
    },
    "Medication.code.coding:PZN.display": {
        "classification": Classification.EMPTY,
    },
    "Medication.code.coding:PZN.userSelected": {
        "classification": Classification.EMPTY,
    },
    "Medication.code.coding:PZN.version": {
        "classification": Classification.EMPTY,
    },
    "Medication.code.coding:pznCode": {
        "classification": Classification.COPY_TO,
        "extra": "Medication.code.coding:PZN",
    },
    "Medication.code.coding:pznCode.display": {
        "classification": Classification.EMPTY,
    },
    "Medication.code.coding:pznCode.userSelected": {
        "classification": Classification.EMPTY,
    },
    "Medication.code.coding:pznCode.version": {
        "classification": Classification.EMPTY,
    },
    "Medication.extension:RxPrescriptionProcessIdentifier<br>(https://gematik.de/fhir/epa-medication/StructureDefinition/rx-prescription-process-identifier-extension)": {
        "classification": Classification.MEDICATION_SERVICE,
    },
    "Medication.form.coding:kbvDarreichungsform": {
        "classification": Classification.COPY_TO,
        "extra": "Medication.form.coding:KBVDarreichungsform",
    },
    "Medication.form.coding:KBVDarreichungsform": {
        "classification": Classification.COPY_FROM,
        "extra": "Medication.form.coding:kbvDarreichungsform",
    },
    "Medication.form.coding:KBVDarreichungsform.userSelected": {
        "classification": Classification.EMPTY,
    },
    "Medication.form.coding:KBVDarreichungsform.version": {
        "classification": Classification.EMPTY,
    },
    "Medication.identifier:ePAMedicationUniqueIdentifier": {
        "classification": Classification.MEDICATION_SERVICE,
    },
    "Medication.ingredient.item[x]:itemCodeableConcept.coding:askCode": {
        "classification": Classification.COPY_TO,
        "extra": "Medication.ingredient.item[x]:itemCodeableConcept.coding:ASK",
    },
    "Medication.ingredient.item[x]:itemCodeableConcept.coding:ASK": {
        "classification": Classification.COPY_FROM,
        "extra": "Medication.ingredient.item[x]:itemCodeableConcept.coding:askCode",
    },
    "Medication.ingredient.item[x]:itemCodeableConcept.coding:ASK.display": {
        "classification": Classification.EMPTY,
    },
    "Medication.ingredient.item[x]:itemCodeableConcept.coding:ASK.userSelected": {
        "classification": Classification.EMPTY,
    },
    "Medication.ingredient.item[x]:itemCodeableConcept.coding:ASK.version": {
        "classification": Classification.EMPTY,
    },
    "Medication.ingredient.item[x]:itemCodeableConcept.coding:pznCode": {
        "classification": Classification.COPY_TO,
        "extra": "Medication.ingredient.item[x]:itemCodeableConcept.coding:PZN",
    },
    "Medication.ingredient.item[x]:itemCodeableConcept.coding:PZN": {
        "classification": Classification.COPY_FROM,
        "extra": "Medication.ingredient.item[x]:itemCodeableConcept.coding:pznCode",
    },
    "Medication.ingredient.item[x]:itemCodeableConcept.coding:PZN.display": {
        "classification": Classification.EMPTY,
    },
    "Medication.ingredient.item[x]:itemCodeableConcept.coding:PZN.userSelected": {
        "classification": Classification.EMPTY,
    },
    "Medication.ingredient.item[x]:itemCodeableConcept.coding:PZN.version": {
        "classification": Classification.EMPTY,
    },
    "Medication.ingredient.item[x]:itemReference.reference": {
        "classification": Classification.EMPTY
    },
    "Medication.manufacturer.reference": {"classification": Classification.EMPTY},
    "Medication.meta.profile": {
        "classification": Classification.FIXED,
        "extra": "https://gematik.de/fhir/epa-medication/StructureDefinition/epa-medication",
    },
    "Organization.identifier:Betriebsstaettennummer": {
        "classification": Classification.COPY_TO,
        "extra": "Organization.identifier:BSNR",
    },
    "Organization.identifier:BSNR": {
        "classification": Classification.COPY_FROM,
        "extra": "Organization.identifier:Betriebsstaettennummer",
    },
    "Organization.identifier:Institutionskennzeichen": {
        "classification": Classification.COPY_TO,
        "extra": "Organization.identifier:IKNR",
    },
    "Organization.identifier:IKNR": {
        "classification": Classification.COPY_FROM,
        "extra": "Organization.identifier:Institutionskennzeichen",
    },
    "Organization.identifier:KZV-Abrechnungsnummer": {
        "classification": Classification.COPY_TO,
        "extra": "Organization.identifier:KZVA",
    },
    "Organization.identifier:KZVA": {
        "classification": Classification.COPY_FROM,
        "extra": "Organization.identifier:KZV-Abrechnungsnummer",
    },
    "Organization.identifier:Telematik-ID": {
        "classification": Classification.COPY_TO,
        "extra": "Organization.identifier:TelematikID",
    },
    "Organization.identifier:TelematikID": {
        "classification": Classification.COPY_FROM,
        "extra": "Organization.identifier:Telematik-ID",
    },
    "Organization.meta.profile": {
        "classification": Classification.FIXED,
        "extra": "http://fhir.de/StructureDefinition/identifier-telematik-id",
    },
    "Practitioner.identifier:ANR": {
        "classification": Classification.COPY_TO,
        "extra": "Practitioner.identifier:LANR",
    },
    "Practitioner.identifier:LANR": {
        "classification": Classification.COPY_FROM,
        "extra": "Practitioner.identifier:ANR",
    },
    "Practitioner.identifier:Telematik-ID": {
        "classification": Classification.COPY_TO,
        "extra": "Practitioner.identifier:TelematikID",
    },
    "Practitioner.identifier:TelematikID": {
        "classification": Classification.COPY_FROM,
        "extra": "Practitioner.identifier:Telematik-ID",
    },
    "Practitioner.identifier:ZANR.system": {"classification": Classification.USE},
    "Practitioner.identifier:ZANR.type": {"classification": Classification.USE},
    "Practitioner.identifier:ZANR.type.coding": {"classification": Classification.USE},
    "Practitioner.identifier:ZANR.type.coding.code": {
        "classification": Classification.USE
    },
    "Practitioner.identifier:ZANR.type.coding.system": {
        "classification": Classification.USE
    },
    "Practitioner.identifier:ZANR.use": {"classification": Classification.USE},
    "Practitioner.identifier:ZANR.value": {"classification": Classification.USE},
    "Practitioner.meta.profile": {
        "classification": Classification.FIXED,
        "extra": "https://gematik.de/fhir/directory/StructureDefinition/PractitionerDirectory",
    },
    "Practitioner.name.family": {
        "classification": Classification.COPY_FROM,
        "extra": "Practitioner.name:name.family",
    },
    "Practitioner.name:name.family": {
        "classification": Classification.COPY_TO,
        "extra": "Practitioner.name.family",
    },
    "Practitioner.name.given": {
        "classification": Classification.COPY_FROM,
        "extra": "Practitioner.name:name.given",
    },
    "Practitioner.name:name.given": {
        "classification": Classification.COPY_TO,
        "extra": "Practitioner.name.given",
    },
    "Practitioner.name.prefix": {
        "classification": Classification.COPY_FROM,
        "extra": "Practitioner.name:name.prefix",
    },
    "Practitioner.name:name.prefix": {
        "classification": Classification.COPY_TO,
        "extra": "Practitioner.name.prefix",
    },
    "Practitioner.name.use": {
        "classification": Classification.COPY_FROM,
        "extra": "Practitioner.name:name.use",
    },
    "Practitioner.name:name.use": {
        "classification": Classification.COPY_TO,
        "extra": "Practitioner.name.use",
    },
    "Practitioner.name:name": {
        "classification": Classification.NOT_USE,
    },
    "Practitioner.name:name.family.extension:nachname<br>(http://hl7.org/fhir/StructureDefinition/humanname-own-name)": {
        "classification": Classification.NOT_USE,
    },
    "Practitioner.name:name.family.extension:namenszusatz<br>(http://fhir.de/StructureDefinition/humanname-namenszusatz)": {
        "classification": Classification.NOT_USE,
    },
    "Practitioner.name:name.family.extension:vorsatzwort<br>(http://hl7.org/fhir/StructureDefinition/humanname-own-prefix)": {
        "classification": Classification.NOT_USE,
    },
    "Practitioner.name:name.family.value": {
        "classification": Classification.NOT_USE,
    },
    "Practitioner.name:name.prefix.extension:prefix-qualifier<br>(http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier)": {
        "classification": Classification.NOT_USE,
    },
    "Practitioner.name:name.prefix.value": {
        "classification": Classification.NOT_USE,
    },
    "Practitioner.qualification": {
        "classification": Classification.NOT_USE,
    },
    "Practitioner.qualification:ASV-Fachgruppennummer": {
        "classification": Classification.NOT_USE,
    },
    "Practitioner.qualification:Berufsbezeichnung": {
        "classification": Classification.NOT_USE,
    },
    "Practitioner.qualification:Typ": {
        "classification": Classification.NOT_USE,
    },
}
