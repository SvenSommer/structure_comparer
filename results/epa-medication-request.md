## Comparison: KBV_PR_ERP_Prescription vs epa-medication-request
| Property | KBV_PR_ERP_Prescription | ePA | Bemerkungen |
|---|---|---|---|
| MedicationRequest | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.authoredOn | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.basedOn |  | X |  |
| MedicationRequest.category |  | X |  |
| MedicationRequest.contained |  | X |  |
| MedicationRequest.courseOfTherapyType |  | X |  |
| MedicationRequest.detectedIssue |  | X |  |
| MedicationRequest.dispenseRequest | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.dispenseRequest.dispenseInterval |  | X |  |
| MedicationRequest.dispenseRequest.expectedSupplyDuration |  | X |  |
| MedicationRequest.dispenseRequest.initialFill |  | X |  |
| MedicationRequest.dispenseRequest.initialFill.duration |  | X |  |
| MedicationRequest.dispenseRequest.initialFill.quantity |  | X |  |
| MedicationRequest.dispenseRequest.numberOfRepeatsAllowed |  | X |  |
| MedicationRequest.dispenseRequest.performer |  | X |  |
| MedicationRequest.dispenseRequest.quantity | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.dispenseRequest.quantity.code | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.dispenseRequest.quantity.system | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.dispenseRequest.quantity.unit |  | X |  |
| MedicationRequest.dispenseRequest.quantity.value | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.dispenseRequest.validityPeriod |  | X |  |
| MedicationRequest.doNotPerform |  | X |  |
| MedicationRequest.dosageInstruction | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.dosageInstruction.additionalInstruction |  | X |  |
| MedicationRequest.dosageInstruction.asNeeded[x] |  | X |  |
| MedicationRequest.dosageInstruction.doseAndRate |  | X |  |
| MedicationRequest.dosageInstruction.doseAndRate.dose[x] |  | X |  |
| MedicationRequest.dosageInstruction.doseAndRate.rate[x] |  | X |  |
| MedicationRequest.dosageInstruction.doseAndRate.type |  | X |  |
| MedicationRequest.dosageInstruction.extension:Dosierungskennzeichen<br>(https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_DosageFlag) | X |  | Extension und Values werden übernommen |
| MedicationRequest.dosageInstruction.maxDosePerAdministration |  | X |  |
| MedicationRequest.dosageInstruction.maxDosePerLifetime |  | X |  |
| MedicationRequest.dosageInstruction.maxDosePerPeriod |  | X |  |
| MedicationRequest.dosageInstruction.method |  | X |  |
| MedicationRequest.dosageInstruction.patientInstruction | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.dosageInstruction.route |  | X |  |
| MedicationRequest.dosageInstruction.sequence |  | X |  |
| MedicationRequest.dosageInstruction.site |  | X |  |
| MedicationRequest.dosageInstruction.timing |  | X |  |
| MedicationRequest.encounter |  | X |  |
| MedicationRequest.eventHistory |  | X |  |
| MedicationRequest.extension:BVG<br>(https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_BVG) | X |  | Extension und Values werden übernommen |
| MedicationRequest.extension:Mehrfachverordnung<br>(https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Multiple_Prescription) | X |  | Extension und Values werden übernommen |
| MedicationRequest.extension:Notdienstgebuehr<br>(https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_EmergencyServicesFee) | X |  | Extension und Values werden übernommen |
| MedicationRequest.extension:Unfallinformationen<br>(https://fhir.kbv.de/StructureDefinition/KBV_EX_FOR_Accident) | X |  | Extension und Values werden übernommen |
| MedicationRequest.extension:Zuzahlungsstatus<br>(https://fhir.kbv.de/StructureDefinition/KBV_EX_FOR_StatusCoPayment) | X |  | Extension und Values werden übernommen |
| MedicationRequest.groupIdentifier |  | X |  |
| MedicationRequest.identifier |  | X |  |
| MedicationRequest.identifier:rxPrescriptionProcessIdentifier |  | X |  |
| MedicationRequest.implicitRules |  | X |  |
| MedicationRequest.instantiatesCanonical |  | X |  |
| MedicationRequest.instantiatesUri |  | X |  |
| MedicationRequest.insurance | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.insurance.reference | X |  |  |
| MedicationRequest.intent | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.language |  | X |  |
| MedicationRequest.medication[x] | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.medication[x].display |  | X |  |
| MedicationRequest.medication[x].identifier |  | X |  |
| MedicationRequest.medication[x].reference |  | X |  |
| MedicationRequest.medication[x].type |  | X |  |
| MedicationRequest.medication[x]:medicationReference | X |  |  |
| MedicationRequest.medication[x]:medicationReference.reference | X |  |  |
| MedicationRequest.meta | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.meta.profile | X |  |  |
| MedicationRequest.note | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.note.author[x] |  | X |  |
| MedicationRequest.note.time |  | X |  |
| MedicationRequest.performer |  | X |  |
| MedicationRequest.performerType |  | X |  |
| MedicationRequest.priorPrescription |  | X |  |
| MedicationRequest.priority |  | X |  |
| MedicationRequest.reasonCode |  | X |  |
| MedicationRequest.reasonReference |  | X |  |
| MedicationRequest.recorder |  | X |  |
| MedicationRequest.reported[x] |  | X |  |
| MedicationRequest.requester | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.requester.reference | X |  |  |
| MedicationRequest.status | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.statusReason |  | X |  |
| MedicationRequest.subject | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.subject.display |  | X |  |
| MedicationRequest.subject.identifier |  | X |  |
| MedicationRequest.subject.reference | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.subject.type |  | X |  |
| MedicationRequest.substitution | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.substitution.allowed[x] | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.substitution.allowed[x]:allowedBoolean | X |  |  |
| MedicationRequest.substitution.reason |  | X |  |
| MedicationRequest.supportingInformation |  | X |  |
