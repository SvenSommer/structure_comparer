## Comparison: KBV_PR_ERP_Prescription vs epa-medication-request
<style>
    .compTable tr:nth-child(1) { background: lightgreen; }
    .compTable tr:nth-child(2) { background: LightPink; }
    .compTable tr:nth-child(3) { background: LightPink; }
    .compTable tr:nth-child(4) { background: LightPink; }
    .compTable tr:nth-child(5) { background: LightPink; }
    .compTable tr:nth-child(6) { background: LightPink; }
    .compTable tr:nth-child(7) { background: lightgreen; }
    .compTable tr:nth-child(8) { background: LightPink; }
    .compTable tr:nth-child(9) { background: LightPink; }
    .compTable tr:nth-child(10) { background: LightPink; }
    .compTable tr:nth-child(11) { background: LightPink; }
    .compTable tr:nth-child(12) { background: LightPink; }
    .compTable tr:nth-child(13) { background: LightPink; }
    .compTable tr:nth-child(14) { background: LightPink; }
    .compTable tr:nth-child(15) { background: lightgreen; }
    .compTable tr:nth-child(16) { background: lightgreen; }
    .compTable tr:nth-child(17) { background: lightgreen; }
    .compTable tr:nth-child(18) { background: LightPink; }
    .compTable tr:nth-child(19) { background: lightgreen; }
    .compTable tr:nth-child(20) { background: LightPink; }
    .compTable tr:nth-child(21) { background: LightPink; }
    .compTable tr:nth-child(22) { background: lightgreen; }
    .compTable tr:nth-child(23) { background: LightPink; }
    .compTable tr:nth-child(24) { background: LightPink; }
    .compTable tr:nth-child(25) { background: LightPink; }
    .compTable tr:nth-child(26) { background: LightPink; }
    .compTable tr:nth-child(27) { background: LightPink; }
    .compTable tr:nth-child(28) { background: LightPink; }
    .compTable tr:nth-child(29) { background: yellow; }
    .compTable tr:nth-child(30) { background: LightPink; }
    .compTable tr:nth-child(31) { background: LightPink; }
    .compTable tr:nth-child(32) { background: LightPink; }
    .compTable tr:nth-child(33) { background: LightPink; }
    .compTable tr:nth-child(34) { background: lightgreen; }
    .compTable tr:nth-child(35) { background: LightPink; }
    .compTable tr:nth-child(36) { background: LightPink; }
    .compTable tr:nth-child(37) { background: LightPink; }
    .compTable tr:nth-child(38) { background: LightPink; }
    .compTable tr:nth-child(39) { background: LightPink; }
    .compTable tr:nth-child(40) { background: LightPink; }
    .compTable tr:nth-child(41) { background: yellow; }
    .compTable tr:nth-child(42) { background: yellow; }
    .compTable tr:nth-child(43) { background: yellow; }
    .compTable tr:nth-child(44) { background: yellow; }
    .compTable tr:nth-child(45) { background: yellow; }
    .compTable tr:nth-child(46) { background: LightPink; }
    .compTable tr:nth-child(47) { background: LightPink; }
    .compTable tr:nth-child(48) { background: LightPink; }
    .compTable tr:nth-child(49) { background: LightPink; }
    .compTable tr:nth-child(50) { background: LightPink; }
    .compTable tr:nth-child(51) { background: LightPink; }
    .compTable tr:nth-child(52) { background: lightgreen; }
    .compTable tr:nth-child(53) { background: lightcyan; }
    .compTable tr:nth-child(54) { background: lightgreen; }
    .compTable tr:nth-child(55) { background: LightPink; }
    .compTable tr:nth-child(56) { background: lightgreen; }
    .compTable tr:nth-child(57) { background: LightPink; }
    .compTable tr:nth-child(58) { background: LightPink; }
    .compTable tr:nth-child(59) { background: lightcyan; }
    .compTable tr:nth-child(60) { background: LightPink; }
    .compTable tr:nth-child(61) { background: yellow; }
    .compTable tr:nth-child(62) { background: lightcyan; }
    .compTable tr:nth-child(63) { background: lightgreen; }
    .compTable tr:nth-child(64) { background: lightcyan; }
    .compTable tr:nth-child(65) { background: lightgreen; }
    .compTable tr:nth-child(66) { background: LightPink; }
    .compTable tr:nth-child(67) { background: LightPink; }
    .compTable tr:nth-child(68) { background: LightPink; }
    .compTable tr:nth-child(69) { background: LightPink; }
    .compTable tr:nth-child(70) { background: LightPink; }
    .compTable tr:nth-child(71) { background: LightPink; }
    .compTable tr:nth-child(72) { background: LightPink; }
    .compTable tr:nth-child(73) { background: LightPink; }
    .compTable tr:nth-child(74) { background: LightPink; }
    .compTable tr:nth-child(75) { background: LightPink; }
    .compTable tr:nth-child(76) { background: lightgreen; }
    .compTable tr:nth-child(77) { background: lightcyan; }
    .compTable tr:nth-child(78) { background: lightgreen; }
    .compTable tr:nth-child(79) { background: LightPink; }
    .compTable tr:nth-child(80) { background: lightgreen; }
    .compTable tr:nth-child(81) { background: LightPink; }
    .compTable tr:nth-child(82) { background: LightPink; }
    .compTable tr:nth-child(83) { background: lightcyan; }
    .compTable tr:nth-child(84) { background: LightPink; }
    .compTable tr:nth-child(85) { background: lightgreen; }
    .compTable tr:nth-child(86) { background: lightgreen; }
    .compTable tr:nth-child(87) { background: yellow; }
    .compTable tr:nth-child(88) { background: LightPink; }
    .compTable tr:nth-child(89) { background: LightPink; }
</style>
<div class="compTable">

| Property | KBV_PR_ERP_Prescription | ePA | Bemerkungen |
|---|---|---|---|
| MedicationRequest.authoredOn | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.basedOn |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.category |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.contained |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.courseOfTherapyType |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.detectedIssue |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.dispenseRequest | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.dispenseRequest.dispenseInterval |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.dispenseRequest.expectedSupplyDuration |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.dispenseRequest.initialFill |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.dispenseRequest.initialFill.duration |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.dispenseRequest.initialFill.quantity |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.dispenseRequest.numberOfRepeatsAllowed |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.dispenseRequest.performer |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.dispenseRequest.quantity | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.dispenseRequest.quantity.code | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.dispenseRequest.quantity.system | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.dispenseRequest.quantity.unit |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.dispenseRequest.quantity.value | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.dispenseRequest.validityPeriod |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.doNotPerform |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.dosageInstruction | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.dosageInstruction.additionalInstruction |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.dosageInstruction.asNeeded[x] |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.dosageInstruction.doseAndRate |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.dosageInstruction.doseAndRate.dose[x] |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.dosageInstruction.doseAndRate.rate[x] |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.dosageInstruction.doseAndRate.type |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.dosageInstruction.extension:Dosierungskennzeichen<br>(https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_DosageFlag) | X |  | Extension und Values werden übernommen |
| MedicationRequest.dosageInstruction.maxDosePerAdministration |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.dosageInstruction.maxDosePerLifetime |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.dosageInstruction.maxDosePerPeriod |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.dosageInstruction.method |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.dosageInstruction.patientInstruction | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.dosageInstruction.route |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.dosageInstruction.sequence |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.dosageInstruction.site |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.dosageInstruction.timing |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.encounter |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.eventHistory |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.extension:BVG<br>(https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_BVG) | X |  | Extension und Values werden übernommen |
| MedicationRequest.extension:Mehrfachverordnung<br>(https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Multiple_Prescription) | X |  | Extension und Values werden übernommen |
| MedicationRequest.extension:Notdienstgebuehr<br>(https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_EmergencyServicesFee) | X |  | Extension und Values werden übernommen |
| MedicationRequest.extension:Unfallinformationen<br>(https://fhir.kbv.de/StructureDefinition/KBV_EX_FOR_Accident) | X |  | Extension und Values werden übernommen |
| MedicationRequest.extension:Zuzahlungsstatus<br>(https://fhir.kbv.de/StructureDefinition/KBV_EX_FOR_StatusCoPayment) | X |  | Extension und Values werden übernommen |
| MedicationRequest.groupIdentifier |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.identifier |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.identifier:rxPrescriptionProcessIdentifier |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.implicitRules |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.instantiatesCanonical |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.instantiatesUri |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.insurance | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.insurance.reference | X |  |  |
| MedicationRequest.intent | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.language |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.medication[x] | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.medication[x].display |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.medication[x].identifier |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.medication[x].reference |  | X |  |
| MedicationRequest.medication[x].type |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.medication[x]:medicationReference | X |  | Extension und Values werden übernommen |
| MedicationRequest.medication[x]:medicationReference.reference | X |  |  |
| MedicationRequest.meta | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.meta.profile | X |  |  |
| MedicationRequest.note | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.note.author[x] |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.note.time |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.performer |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.performerType |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.priorPrescription |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.priority |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.reasonCode |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.reasonReference |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.recorder |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.reported[x] |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.requester | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.requester.reference | X |  |  |
| MedicationRequest.status | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.statusReason |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.subject | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.subject.display |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.subject.identifier |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.subject.reference | X | X |  |
| MedicationRequest.subject.type |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.substitution | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.substitution.allowed[x] | X | X | Eigenschaft und Wert werden übernommen |
| MedicationRequest.substitution.allowed[x]:allowedBoolean | X |  | Extension und Values werden übernommen |
| MedicationRequest.substitution.reason |  | X | Bleibt vorerst leer, da keine Quellinformationen |
| MedicationRequest.supportingInformation |  | X | Bleibt vorerst leer, da keine Quellinformationen |
</div>