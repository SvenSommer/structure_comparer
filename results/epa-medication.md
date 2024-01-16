## Comparison: KBV_PR_ERP_Medication_Compounding, KBV_PR_ERP_Medication_FreeText, KBV_PR_ERP_Medication_Ingredient, KBV_PR_ERP_Medication_PZN vs epa-medication
| Property | KBV_PR_ERP_Medication_Compounding | KBV_PR_ERP_Medication_FreeText | KBV_PR_ERP_Medication_Ingredient | KBV_PR_ERP_Medication_PZN | ePA | Bemerkungen |
|---|---|---|---|---|---|---|
| Medication | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.amount | X |  | X | X | X |  |
| Medication.amount.denominator | X |  | X | X | X |  |
| Medication.amount.denominator.code |  |  |  |  | X |  |
| Medication.amount.denominator.comparator |  |  |  |  | X |  |
| Medication.amount.denominator.system |  |  |  |  | X |  |
| Medication.amount.denominator.unit |  |  |  |  | X |  |
| Medication.amount.denominator.value | X |  | X | X | X |  |
| Medication.amount.numerator | X |  | X | X | X |  |
| Medication.amount.numerator.code | X |  | X | X | X |  |
| Medication.amount.numerator.comparator |  |  |  |  | X |  |
| Medication.amount.numerator.extension:Gesamtmenge<br>(https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Medication_PackagingSize) | X |  |  |  |  | Extension und Values werden übernommen |
| Medication.amount.numerator.extension:Packungsgroesse<br>(https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Medication_PackagingSize) |  |  | X | X |  | Extension und Values werden übernommen |
| Medication.amount.numerator.system | X |  | X | X | X |  |
| Medication.amount.numerator.unit | X |  | X | X | X |  |
| Medication.amount.numerator.value |  |  |  |  | X |  |
| Medication.batch | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.batch.expirationDate | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.batch.lotNumber | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.code | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.code.coding | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.code.coding:ASK |  |  |  |  | X |  |
| Medication.code.coding:ASK.code |  |  |  |  | X |  |
| Medication.code.coding:ASK.display |  |  |  |  | X |  |
| Medication.code.coding:ASK.system |  |  |  |  | X |  |
| Medication.code.coding:ASK.userSelected |  |  |  |  | X |  |
| Medication.code.coding:ASK.version |  |  |  |  | X |  |
| Medication.code.coding:ATC-DE |  |  |  |  | X |  |
| Medication.code.coding:ATC-DE.code |  |  |  |  | X |  |
| Medication.code.coding:ATC-DE.display |  |  |  |  | X |  |
| Medication.code.coding:ATC-DE.system |  |  |  |  | X |  |
| Medication.code.coding:ATC-DE.userSelected |  |  |  |  | X |  |
| Medication.code.coding:ATC-DE.version |  |  |  |  | X |  |
| Medication.code.coding:PZN |  |  |  |  | X |  |
| Medication.code.coding:PZN.code |  |  |  |  | X |  |
| Medication.code.coding:PZN.display |  |  |  |  | X |  |
| Medication.code.coding:PZN.system |  |  |  |  | X |  |
| Medication.code.coding:PZN.userSelected |  |  |  |  | X |  |
| Medication.code.coding:PZN.version |  |  |  |  | X |  |
| Medication.code.coding:WG14 |  |  |  |  | X |  |
| Medication.code.coding:WG14.code |  |  |  |  | X |  |
| Medication.code.coding:WG14.display |  |  |  |  | X |  |
| Medication.code.coding:WG14.system |  |  |  |  | X |  |
| Medication.code.coding:WG14.userSelected |  |  |  |  | X |  |
| Medication.code.coding:WG14.version |  |  |  |  | X |  |
| Medication.code.coding:pznCode |  |  |  | X |  |  |
| Medication.code.coding:pznCode.code |  |  |  | X |  |  |
| Medication.code.coding:pznCode.system |  |  |  | X |  |  |
| Medication.code.coding:verordnungskategorieCode | X | X | X |  | X |  |
| Medication.code.coding:verordnungskategorieCode.code | X | X | X |  | X |  |
| Medication.code.coding:verordnungskategorieCode.display |  |  |  |  | X |  |
| Medication.code.coding:verordnungskategorieCode.system | X | X | X |  | X |  |
| Medication.code.coding:verordnungskategorieCode.userSelected |  |  |  |  | X |  |
| Medication.code.coding:verordnungskategorieCode.version |  |  |  |  | X |  |
| Medication.contained |  |  |  |  | X |  |
| Medication.extension:Arzneimittelkategorie<br>(https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Medication_Category) | X | X | X | X |  | Extension und Values werden übernommen |
| Medication.extension:Herstellungsanweisung<br>(https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Medication_CompoundingInstruction) | X |  |  |  |  | Extension und Values werden übernommen |
| Medication.extension:Impfstoff<br>(https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Medication_Vaccine) | X | X | X | X |  | Extension und Values werden übernommen |
| Medication.extension:Kategorie<br>(https://fhir.kbv.de/StructureDefinition/KBV_EX_Base_Medication_Type&#124;1.3.0) | X |  |  | X |  | Extension und Values werden übernommen |
| Medication.extension:Normgroesse<br>(http://fhir.de/StructureDefinition/normgroesse) |  |  | X | X |  | Extension und Values werden übernommen |
| Medication.extension:RxPrescriptionProcessIdentifier<br>(https://gematik.de/fhir/epa-medication/StructureDefinition/rx-prescription-process-identifier-extension) |  |  |  |  | X | Extension und Values werden übernommen |
| Medication.extension:Verpackung<br>(https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Medication_Packaging) | X |  |  |  |  | Extension und Values werden übernommen |
| Medication.form | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.form.coding |  |  |  | X | X |  |
| Medication.form.coding:EDQM |  |  |  |  | X |  |
| Medication.form.coding:EDQM.code |  |  |  |  | X |  |
| Medication.form.coding:EDQM.display |  |  |  |  | X |  |
| Medication.form.coding:EDQM.system |  |  |  |  | X |  |
| Medication.form.coding:EDQM.userSelected |  |  |  |  | X |  |
| Medication.form.coding:EDQM.version |  |  |  |  | X |  |
| Medication.form.coding:KBVDarreichungsform |  |  |  |  | X |  |
| Medication.form.coding:KBVDarreichungsform.code |  |  |  |  | X |  |
| Medication.form.coding:KBVDarreichungsform.display |  |  |  |  | X |  |
| Medication.form.coding:KBVDarreichungsform.system |  |  |  |  | X |  |
| Medication.form.coding:KBVDarreichungsform.userSelected |  |  |  |  | X |  |
| Medication.form.coding:KBVDarreichungsform.version |  |  |  |  | X |  |
| Medication.form.coding:kbvDarreichungsform |  |  |  | X |  |  |
| Medication.form.coding:kbvDarreichungsform.code |  |  |  | X |  |  |
| Medication.form.coding:kbvDarreichungsform.display |  |  |  | X |  |  |
| Medication.form.coding:kbvDarreichungsform.system |  |  |  | X |  |  |
| Medication.identifier |  |  |  |  | X |  |
| Medication.identifier:ePAMedicationUniqueIdentifier |  |  |  |  | X |  |
| Medication.implicitRules |  |  |  |  | X |  |
| Medication.ingredient | X |  | X |  | X |  |
| Medication.ingredient.extension:Darreichungsform<br>(https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Medication_Ingredient_Form) | X |  |  |  |  | Extension und Values werden übernommen |
| Medication.ingredient.isActive |  |  |  |  | X |  |
| Medication.ingredient.item[x] | X |  | X |  | X |  |
| Medication.ingredient.item[x]:itemCodeableConcept | X |  | X |  | X |  |
| Medication.ingredient.item[x]:itemCodeableConcept.coding | X |  | X |  | X |  |
| Medication.ingredient.item[x]:itemCodeableConcept.coding:ASK |  |  |  |  | X |  |
| Medication.ingredient.item[x]:itemCodeableConcept.coding:ASK.code |  |  |  |  | X |  |
| Medication.ingredient.item[x]:itemCodeableConcept.coding:ASK.display |  |  |  |  | X |  |
| Medication.ingredient.item[x]:itemCodeableConcept.coding:ASK.system |  |  |  |  | X |  |
| Medication.ingredient.item[x]:itemCodeableConcept.coding:ASK.userSelected |  |  |  |  | X |  |
| Medication.ingredient.item[x]:itemCodeableConcept.coding:ASK.version |  |  |  |  | X |  |
| Medication.ingredient.item[x]:itemCodeableConcept.coding:ATC-DE |  |  |  |  | X |  |
| Medication.ingredient.item[x]:itemCodeableConcept.coding:ATC-DE.code |  |  |  |  | X |  |
| Medication.ingredient.item[x]:itemCodeableConcept.coding:ATC-DE.display |  |  |  |  | X |  |
| Medication.ingredient.item[x]:itemCodeableConcept.coding:ATC-DE.system |  |  |  |  | X |  |
| Medication.ingredient.item[x]:itemCodeableConcept.coding:ATC-DE.userSelected |  |  |  |  | X |  |
| Medication.ingredient.item[x]:itemCodeableConcept.coding:ATC-DE.version |  |  |  |  | X |  |
| Medication.ingredient.item[x]:itemCodeableConcept.coding:PZN |  |  |  |  | X |  |
| Medication.ingredient.item[x]:itemCodeableConcept.coding:PZN.code |  |  |  |  | X |  |
| Medication.ingredient.item[x]:itemCodeableConcept.coding:PZN.display |  |  |  |  | X |  |
| Medication.ingredient.item[x]:itemCodeableConcept.coding:PZN.system |  |  |  |  | X |  |
| Medication.ingredient.item[x]:itemCodeableConcept.coding:PZN.userSelected |  |  |  |  | X |  |
| Medication.ingredient.item[x]:itemCodeableConcept.coding:PZN.version |  |  |  |  | X |  |
| Medication.ingredient.item[x]:itemCodeableConcept.coding:WG14 |  |  |  |  | X |  |
| Medication.ingredient.item[x]:itemCodeableConcept.coding:WG14.code |  |  |  |  | X |  |
| Medication.ingredient.item[x]:itemCodeableConcept.coding:WG14.display |  |  |  |  | X |  |
| Medication.ingredient.item[x]:itemCodeableConcept.coding:WG14.system |  |  |  |  | X |  |
| Medication.ingredient.item[x]:itemCodeableConcept.coding:WG14.userSelected |  |  |  |  | X |  |
| Medication.ingredient.item[x]:itemCodeableConcept.coding:WG14.version |  |  |  |  | X |  |
| Medication.ingredient.item[x]:itemCodeableConcept.coding:askCode |  |  | X |  |  |  |
| Medication.ingredient.item[x]:itemCodeableConcept.coding:askCode.code |  |  | X |  |  |  |
| Medication.ingredient.item[x]:itemCodeableConcept.coding:askCode.system |  |  | X |  |  |  |
| Medication.ingredient.item[x]:itemCodeableConcept.coding:pznCode | X |  |  |  |  |  |
| Medication.ingredient.item[x]:itemCodeableConcept.coding:pznCode.code | X |  |  |  |  |  |
| Medication.ingredient.item[x]:itemCodeableConcept.coding:pznCode.system | X |  |  |  |  |  |
| Medication.ingredient.item[x]:itemReference |  |  |  |  | X |  |
| Medication.ingredient.item[x]:itemReference.display |  |  |  |  | X |  |
| Medication.ingredient.item[x]:itemReference.identifier |  |  |  |  | X |  |
| Medication.ingredient.item[x]:itemReference.reference |  |  |  |  | X |  |
| Medication.ingredient.item[x]:itemReference.type |  |  |  |  | X |  |
| Medication.ingredient.strength | X |  | X |  | X |  |
| Medication.ingredient.strength.denominator | X |  | X |  | X |  |
| Medication.ingredient.strength.denominator.code |  |  |  |  | X |  |
| Medication.ingredient.strength.denominator.comparator |  |  |  |  | X |  |
| Medication.ingredient.strength.denominator.system |  |  |  |  | X |  |
| Medication.ingredient.strength.denominator.unit |  |  |  |  | X |  |
| Medication.ingredient.strength.denominator.value | X |  | X |  | X |  |
| Medication.ingredient.strength.extension:MengeFreitext<br>(https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Medication_Ingredient_Amount) | X |  |  |  |  | Extension und Values werden übernommen |
| Medication.ingredient.strength.numerator | X |  | X |  | X |  |
| Medication.ingredient.strength.numerator.code | X |  | X |  | X |  |
| Medication.ingredient.strength.numerator.comparator |  |  |  |  | X |  |
| Medication.ingredient.strength.numerator.system | X |  | X |  | X |  |
| Medication.ingredient.strength.numerator.unit | X |  | X |  | X |  |
| Medication.ingredient.strength.numerator.value | X |  | X |  | X |  |
| Medication.language |  |  |  |  | X |  |
| Medication.manufacturer |  |  |  |  | X |  |
| Medication.manufacturer.display |  |  |  |  | X |  |
| Medication.manufacturer.identifier |  |  |  |  | X |  |
| Medication.manufacturer.reference |  |  |  |  | X |  |
| Medication.manufacturer.type |  |  |  |  | X |  |
| Medication.meta | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.meta.profile | X | X | X | X |  |  |
| Medication.status |  |  |  |  | X |  |
