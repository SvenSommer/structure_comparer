from classification import Classification

MANUAL_ENTRIES = {
    "MedicationRequest.insurance.reference": {
        "classification": Classification.OTHER,
        "remark": "Wird beim Mapping ignoriert",
    },
    "MedicationRequest.meta.profile": {
        "remark": "Wird fix auf 'https://gematik.de/fhir/epa-medication/StructureDefinition/epa-medication' gesetzt"
    },
    "MedicationRequest.requester.reference": {
        "remark": "Wird entfernt, später durch MedicationService selbst gesetzt"
    },
    "MedicationRequest.subject.reference": {
        "remark": "Wird entfernt, später durch MedicationService selbst gesetzt"
    },
    "MedicationRequest.identifier:rxPrescriptionProcessIdentifier": {
        "classification": Classification.NOT_USE,
        "remark": "Dieser Identifier setzt sich aus der Task-ID und dem MedicationRequest.authoredOn zusammen. Er wird durch den Medication Service vergeben.",
    },
    "MedicationRequest.medication[x]:medicationReference": {
        "classification": Classification.MANUAL,
        "remark": "Die Referenz der KBV-Medikation wird durch eine Referenz auf eine EPA-Medikation ersetzt.",
    },
    "MedicationRequest.medication[x].reference": {
        "classification": Classification.NOT_USE
    },
    "MedicationRequest.medication[x]:medicationReference.reference": {
        "classification": Classification.MANUAL,
        "remark": "Die Referenz ergibt sich aus der neu erzeugten EPA-Medikation.",
    },
    "MedicationRequest.substitution.allowed[x]:allowedBoolean": {
        "classification": Classification.NOT_USE,
        "remark": "Einschränkung wird nicht übernommen",
    },
    "Medication.code.coding:PZN": {
        "classification": Classification.USE,
        "remark": "Wert wird aus Medication.code.coding:pznCode übernommen",
    },
    "Medication.code.coding:PZN.code": {
        "classification": Classification.USE,
        "remark": "Wert wird aus Medication.code.coding:pznCode.code übernommen",
    },
    "Medication.code.coding:PZN.system": {
        "classification": Classification.USE,
        "remark": "Wert wird aus Medication.code.coding:pznCode.system übernommen",
    },
    "Medication.code.coding:pznCode": {
        "classification": Classification.USE,
        "remark": "Wert wird in Medication.code.coding:PZN übernommen",
    },
    "Medication.code.coding:pznCode.code": {
        "classification": Classification.USE,
        "remark": "Wert wird in Medication.code.coding:PZN.code übernommen",
    },
    "Medication.code.coding:pznCode.system": {
        "classification": Classification.USE,
        "remark": "Wert wird in Medication.code.coding:PZN.system übernommen",
    },
    "Medication.extension:RxPrescriptionProcessIdentifier<br>(https://gematik.de/fhir/epa-medication/StructureDefinition/rx-prescription-process-identifier-extension)": {
        "classification": Classification.NOT_USE,
        "remark": "Dieser Identifier setzt sich aus der Task-ID und dem MedicationRequest.authoredOn zusammen. Er wird durch den Medication Service vergeben.",
    },
    "Medication.form.coding:kbvDarreichungsform": {
        "classification": Classification.USE,
        "remark": "Wert wird in Medication.form.coding:KBVDarreichungsform übernommen",
    },
    "Medication.form.coding:kbvDarreichungsform.code": {
        "classification": Classification.USE,
        "remark": "Wert wird in Medication.form.coding:KBVDarreichungsform.code übernommen",
    },
    "Medication.form.coding:kbvDarreichungsform.display": {
        "classification": Classification.USE,
        "remark": "Wert wird in Medication.form.coding:KBVDarreichungsform.display übernommen",
    },
    "Medication.form.coding:kbvDarreichungsform.system": {
        "classification": Classification.USE,
        "remark": "Wert wird in Medication.form.coding:KBVDarreichungsform.system übernommen",
    },
    "Medication.form.coding:KBVDarreichungsform": {
        "classification": Classification.USE,
        "remark": "Wert wird in Medication.form.coding:kbvDarreichungsform übernommen",
    },
    "Medication.form.coding:KBVDarreichungsform.code": {
        "classification": Classification.USE,
        "remark": "Wert wird in Medication.form.coding:kbvDarreichungsform.code übernommen",
    },
    "Medication.form.coding:KBVDarreichungsform.display": {
        "classification": Classification.USE,
        "remark": "Wert wird in Medication.form.coding:kbvDarreichungsform.display übernommen",
    },
    "Medication.form.coding:KBVDarreichungsform.system": {
        "classification": Classification.USE,
        "remark": "Wert wird in Medication.form.coding:kbvDarreichungsform.system übernommen",
    },
    "Medication.identifier:ePAMedicationUniqueIdentifier": {
        "classification": Classification.NOT_USE,
        "remark": "Dieser Identifier wird vom Medication Service vergeben",
    },
    "Medication.ingredient.item[x]:itemCodeableConcept.coding:askCode": {
        "classification": Classification.USE,
        "remark": "Wert wird in Medication.ingredient.item[x]:itemCodeableConcept.coding:ASK übernommen",
    },
    "Medication.ingredient.item[x]:itemCodeableConcept.coding:askCode.code": {
        "classification": Classification.USE,
        "remark": "Wert wird in Medication.ingredient.item[x]:itemCodeableConcept.coding:ASK.code übernommen",
    },
    "Medication.ingredient.item[x]:itemCodeableConcept.coding:askCode.system": {
        "classification": Classification.USE,
        "remark": "Wert wird in Medication.ingredient.item[x]:itemCodeableConcept.coding:ASK.system übernommen",
    },
    "Medication.ingredient.item[x]:itemCodeableConcept.coding:pznCode": {
        "classification": Classification.USE,
        "remark": "Wert wird in Medication.ingredient.item[x]:itemCodeableConcept.coding:PZN übernommen",
    },
    "Medication.ingredient.item[x]:itemCodeableConcept.coding:pznCode.code": {
        "classification": Classification.USE,
        "remark": "Wert wird in Medication.ingredient.item[x]:itemCodeableConcept.coding:PZN.code übernommen",
    },
    "Medication.ingredient.item[x]:itemCodeableConcept.coding:pznCode.system": {
        "classification": Classification.USE,
        "remark": "Wert wird in Medication.ingredient.item[x]:itemCodeableConcept.coding:PZN.system übernommen",
    },
    "Medication.ingredient.item[x]:itemCodeableConcept.coding:ASK": {
        "classification": Classification.USE,
        "remark": "Wert wird aus Medication.ingredient.item[x]:itemCodeableConcept.coding:askCode übernommen",
    },
    "Medication.ingredient.item[x]:itemCodeableConcept.coding:ASK.code": {
        "classification": Classification.USE,
        "remark": "Wert wird aus Medication.ingredient.item[x]:itemCodeableConcept.coding:askCode.code übernommen",
    },
    "Medication.ingredient.item[x]:itemCodeableConcept.coding:ASK.system": {
        "classification": Classification.USE,
        "remark": "Wert wird aus Medication.ingredient.item[x]:itemCodeableConcept.coding:askCode.system übernommen",
    },
    "Medication.ingredient.item[x]:itemCodeableConcept.coding:PZN": {
        "classification": Classification.USE,
        "remark": "Wert wird aus Medication.ingredient.item[x]:itemCodeableConcept.coding:pznCode übernommen",
    },
    "Medication.ingredient.item[x]:itemCodeableConcept.coding:PZN.code": {
        "classification": Classification.USE,
        "remark": "Wert wird aus Medication.ingredient.item[x]:itemCodeableConcept.coding:pznCode.code übernommen",
    },
    "Medication.ingredient.item[x]:itemCodeableConcept.coding:PZN.system": {
        "classification": Classification.USE,
        "remark": "Wert wird aus Medication.ingredient.item[x]:itemCodeableConcept.coding:pznCode.system übernommen",
    },
    "Medication.ingredient.item[x]:itemReference.reference": {
        "classification": Classification.NOT_USE
    },
    "Medication.manufacturer.reference": {"classification": Classification.NOT_USE},
    "Medication.meta.profile": {
        "classification": Classification.MANUAL,
        "remark": "Wird fix auf 'https://gematik.de/fhir/epa-medication/StructureDefinition/epa-medication' gesetzt",
    },
    "Organization.identifier:Betriebsstaettennummer": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:BSNR übernommen",
    },
    "Organization.identifier:Betriebsstaettennummer.system": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:BSNR.system übernommen",
    },
    "Organization.identifier:Betriebsstaettennummer.type": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:BSNR.type übernommen",
    },
    "Organization.identifier:Betriebsstaettennummer.type.coding": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:BSNR.type.coding übernommen",
    },
    "Organization.identifier:Betriebsstaettennummer.type.coding.code": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:BSNR.type.coding.code übernommen",
    },
    "Organization.identifier:Betriebsstaettennummer.type.coding.system": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:BSNR.type.coding.system übernommen",
    },
    "Organization.identifier:Betriebsstaettennummer.use": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:BSNR.use übernommen",
    },
    "Organization.identifier:Betriebsstaettennummer.value": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:BSNR.value übernommen",
    },
    "Organization.identifier:BSNR": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:Betriebsstaettennummer übernommen",
    },
    "Organization.identifier:Institutionskennzeichen": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:IKNR übernommen",
    },
    "Organization.identifier:Institutionskennzeichen.system": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:IKNR.system übernommen",
    },
    "Organization.identifier:Institutionskennzeichen.type": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:IKNR.type übernommen",
    },
    "Organization.identifier:Institutionskennzeichen.type.coding": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:IKNR.type.coding übernommen",
    },
    "Organization.identifier:Institutionskennzeichen.type.coding.code": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:IKNR.type.coding.code übernommen",
    },
    "Organization.identifier:Institutionskennzeichen.type.coding.system": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:IKNR.type.coding.system übernommen",
    },
    "Organization.identifier:Institutionskennzeichen.use": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:IKNR.use übernommen",
    },
    "Organization.identifier:Institutionskennzeichen.value": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:IKNR.value übernommen",
    },
    "Organization.identifier:IKNR": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:Institutionskennzeichen übernommen",
    },
    "Organization.identifier:KZV-Abrechnungsnummer": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:KZVA übernommen",
    },
    "Organization.identifier:KZV-Abrechnungsnummer.system": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:KZVA.system übernommen",
    },
    "Organization.identifier:KZV-Abrechnungsnummer.type": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:KZVA.type übernommen",
    },
    "Organization.identifier:KZV-Abrechnungsnummer.type.coding": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:KZVA.type.coding übernommen",
    },
    "Organization.identifier:KZV-Abrechnungsnummer.type.coding.code": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:KZVA.type.coding.code übernommen",
    },
    "Organization.identifier:KZV-Abrechnungsnummer.type.coding.system": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:KZVA.type.coding.system übernommen",
    },
    "Organization.identifier:KZV-Abrechnungsnummer.use": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:KZVA.use übernommen",
    },
    "Organization.identifier:KZV-Abrechnungsnummer.value": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:KZVA.value übernommen",
    },
    "Organization.identifier:KZVA": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:KZV-Abrechnungsnummer übernommen",
    },
    "Organization.identifier:Telematik-ID": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:TelematikID übernommen",
    },
    "Organization.identifier:Telematik-ID.system": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:TelematikID.system übernommen",
    },
    "Organization.identifier:Telematik-ID.type": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:TelematikID.type übernommen",
    },
    "Organization.identifier:Telematik-ID.type.coding": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:TelematikID.type.coding übernommen",
    },
    "Organization.identifier:Telematik-ID.type.coding.code": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:TelematikID.type.coding.code übernommen",
    },
    "Organization.identifier:Telematik-ID.type.coding.system": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:TelematikID.type.coding.system übernommen",
    },
    "Organization.identifier:Telematik-ID.use": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:TelematikID.use übernommen",
    },
    "Organization.identifier:Telematik-ID.value": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:TelematikID.value übernommen",
    },
    "Organization.identifier:TelematikID": {
        "classification": Classification.USE,
        "remark": "Wird in Organization.identifier:Telematik-ID übernommen",
    },
    "Organization.meta.profile": {
        "classification": Classification.MANUAL,
        "remark": "Wird fix auf 'http://fhir.de/StructureDefinition/identifier-telematik-id' gesetzt",
    },
    "Practitioner.identifier:Telematik-ID": {
        "classification": Classification.USE,
        "remark": "Wird in Practitioner.identifier:TelematikID übernommen",
    },
    "Practitioner.identifier:Telematik-ID.system": {
        "classification": Classification.USE,
        "remark": "Wird in Practitioner.identifier:TelematikID.system übernommen",
    },
    "Practitioner.identifier:Telematik-ID.type": {
        "classification": Classification.USE,
        "remark": "Wird in Practitioner.identifier:TelematikID.type übernommen",
    },
    "Practitioner.identifier:Telematik-ID.type.coding": {
        "classification": Classification.USE,
        "remark": "Wird in Practitioner.identifier:TelematikID.type.coding übernommen",
    },
    "Practitioner.identifier:Telematik-ID.type.coding.code": {
        "classification": Classification.USE,
        "remark": "Wird in Practitioner.identifier:TelematikID.type.coding.code übernommen",
    },
    "Practitioner.identifier:Telematik-ID.type.coding.system": {
        "classification": Classification.USE,
        "remark": "Wird in Practitioner.identifier:TelematikID.type.coding.system übernommen",
    },
    "Practitioner.identifier:Telematik-ID.use": {
        "classification": Classification.USE,
        "remark": "Wird in Practitioner.identifier:TelematikID.use übernommen",
    },
    "Practitioner.identifier:Telematik-ID.value": {
        "classification": Classification.USE,
        "remark": "Wird in Practitioner.identifier:TelematikID.value übernommen",
    },
    "Practitioner.identifier:TelematikID": {
        "classification": Classification.USE,
        "remark": "Wird in Practitioner.identifier:Telematik-ID übernommen",
    },
    "Practitioner.identifier:ANR": {
        "classification": Classification.USE,
        "remark": "Wird in Practitioner.identifier:LANR übernommen",
    },
    "Practitioner.identifier:ANR.system": {
        "classification": Classification.USE,
        "remark": "Wird in Practitioner.identifier:LANR.system übernommen",
    },
    "Practitioner.identifier:ANR.type": {
        "classification": Classification.USE,
        "remark": "Wird in Practitioner.identifier:LANR.type übernommen",
    },
    "Practitioner.identifier:ANR.type.coding": {
        "classification": Classification.USE,
        "remark": "Wird in Practitioner.identifier:LANR.type.coding übernommen",
    },
    "Practitioner.identifier:ANR.type.coding.code": {
        "classification": Classification.USE,
        "remark": "Wird in Practitioner.identifier:LANR.type.coding.code übernommen",
    },
    "Practitioner.identifier:ANR.type.coding.system": {
        "classification": Classification.USE,
        "remark": "Wird in Practitioner.identifier:LANR.type.coding.system übernommen",
    },
    "Practitioner.identifier:ANR.use": {
        "classification": Classification.USE,
        "remark": "Wird in Practitioner.identifier:LANR.use übernommen",
    },
    "Practitioner.identifier:ANR.value": {
        "classification": Classification.USE,
        "remark": "Wird in Practitioner.identifier:LANR.value übernommen",
    },
    "Practitioner.identifier:LANR": {
        "classification": Classification.USE,
        "remark": "Wird in Practitioner.identifier:ANR übernommen",
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
        "classification": Classification.MANUAL,
        "remark": "Wird fix auf 'https://gematik.de/fhir/directory/StructureDefinition/PractitionerDirectory' gesetzt",
    },
    "Practitioner.name.family": {
        "classification": Classification.MANUAL,
        "remark": "Wert wird von Practitioner.name:name.family übernommen",
    },
    "Practitioner.name:name.family": {
        "classification": Classification.MANUAL,
        "remark": "Wert wird in Practitioner.name.family übernommen",
    },
    "Practitioner.name.given": {
        "classification": Classification.MANUAL,
        "remark": "Wert wird von Practitioner.name:name.given übernommen",
    },
    "Practitioner.name:name.given": {
        "classification": Classification.MANUAL,
        "remark": "Wert wird in Practitioner.name.given übernommen",
    },
    "Practitioner.name.prefix": {
        "classification": Classification.MANUAL,
        "remark": "Wert wird von Practitioner.name:name.prefix übernommen",
    },
    "Practitioner.name:name.prefix": {
        "classification": Classification.MANUAL,
        "remark": "Wert wird in Practitioner.name.prefix übernommen",
    },
    "Practitioner.name.use": {
        "classification": Classification.MANUAL,
        "remark": "Wert wird von Practitioner.name:name.use übernommen",
    },
    "Practitioner.name:name.use": {
        "classification": Classification.MANUAL,
        "remark": "Wert wird in Practitioner.name.use übernommen",
    },
    "Practitioner.name:name": {
        "classification": Classification.NOT_USE,
        "remark": "Wert wird nicht übernommen",
    },
    "Practitioner.name:name.family.extension:nachname<br>(http://hl7.org/fhir/StructureDefinition/humanname-own-name)": {
        "classification": Classification.NOT_USE,
        "remark": "Wert wird nicht übernommen",
    },
    "Practitioner.name:name.family.extension:namenszusatz<br>(http://fhir.de/StructureDefinition/humanname-namenszusatz)": {
        "classification": Classification.NOT_USE,
        "remark": "Wert wird nicht übernommen",
    },
    "Practitioner.name:name.family.extension:vorsatzwort<br>(http://hl7.org/fhir/StructureDefinition/humanname-own-prefix)": {
        "classification": Classification.NOT_USE,
        "remark": "Wert wird nicht übernommen",
    },
    "Practitioner.name:name.family.value": {
        "classification": Classification.NOT_USE,
        "remark": "Wert wird nicht übernommen",
    },
    "Practitioner.name:name.prefix.extension:prefix-qualifier<br>(http://hl7.org/fhir/StructureDefinition/iso21090-EN-qualifier)": {
        "classification": Classification.NOT_USE,
        "remark": "Wert wird nicht übernommen",
    },
    "Practitioner.name:name.prefix.value": {
        "classification": Classification.NOT_USE,
        "remark": "Wert wird nicht übernommen",
    },
    "Practitioner.qualification": {
        "classification": Classification.NOT_USE,
        "remark": "Wert wird nicht übernommen",
    },
    "Practitioner.qualification:ASV-Fachgruppennummer": {
        "classification": Classification.NOT_USE,
        "remark": "Extension und Values werden nicht übernommen",
    },
    "Practitioner.qualification:Berufsbezeichnung": {
        "classification": Classification.NOT_USE,
        "remark": "Extension und Values werden nicht übernommen",
    },
    "Practitioner.qualification:Typ": {
        "classification": Classification.NOT_USE,
        "remark": "Extension und Values werden nicht übernommen",
    },
}
