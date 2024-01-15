## Comparison: KBV_PR_ERP_Medication_Compounding, KBV_PR_ERP_Medication_FreeText, KBV_PR_ERP_Medication_Ingredient, KBV_PR_ERP_Medication_PZN vs epa-medication
| Property | KBV_PR_ERP_Medication_Compounding | KBV_PR_ERP_Medication_FreeText | KBV_PR_ERP_Medication_Ingredient | KBV_PR_ERP_Medication_PZN | ePA | Bemerkungen |
|---|---|---|---|---|---|---|
| Medication | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.amount | X |  | X | X | X |  |
| Medication.amount.denominator | X |  | X | X | X |  |
| Medication.amount.denominator.code |  |  |  |  | X |  |
| Medication.amount.denominator.comparator |  |  |  |  | X |  |
| Medication.amount.denominator.extension | X |  | X | X | X | Extension und Values werden übernommen |
| Medication.amount.denominator.system |  |  |  |  | X |  |
| Medication.amount.denominator.unit |  |  |  |  | X |  |
| Medication.amount.denominator.value | X |  | X | X | X |  |
| Medication.amount.extension | X |  | X | X | X | Extension und Values werden übernommen |
| Medication.amount.numerator | X |  | X | X | X |  |
| Medication.amount.numerator.code | X |  | X | X | X |  |
| Medication.amount.numerator.comparator |  |  |  |  | X |  |
| Medication.amount.numerator.extension | X |  | X | X | X | Extension und Values werden übernommen |
| Medication.amount.numerator.extension.extension | X |  | X | X |  | Extension und Values werden übernommen |
| Medication.amount.numerator.extension.url | X |  | X | X |  | Extension und Values werden übernommen |
| Medication.amount.numerator.extension.value[x] | X |  | X | X |  | Extension und Values werden übernommen |
| Medication.amount.numerator.extension:Gesamtmenge(https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Medication_PackagingSize) | X |  |  |  |  | Extension und Values werden übernommen |
| Medication.amount.numerator.extension:Packungsgroesse(https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Medication_PackagingSize) |  |  | X | X |  | Extension und Values werden übernommen |
| Medication.amount.numerator.system | X |  | X | X | X |  |
| Medication.amount.numerator.unit | X |  | X | X | X |  |
| Medication.amount.numerator.value |  |  |  |  | X |  |
| Medication.batch | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.batch.expirationDate | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.batch.extension | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.batch.lotNumber | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.batch.modifierExtension | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.code | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.code.coding | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.code.coding.code | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.code.coding.display | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.code.coding.extension | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.code.coding.system | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.code.coding.userSelected | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.code.coding.version | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.code.extension | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.code.text | X | X |  | X | X |  |
| Medication.contained |  |  |  |  | X |  |
| Medication.extension | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.extension.extension | X | X | X | X |  | Extension und Values werden übernommen |
| Medication.extension.url | X | X | X | X |  | Extension und Values werden übernommen |
| Medication.extension.value[x] | X | X | X | X |  | Extension und Values werden übernommen |
| Medication.extension.value[x].code | X | X | X | X |  | Extension und Values werden übernommen |
| Medication.extension.value[x].coding | X | X | X | X |  | Extension und Values werden übernommen |
| Medication.extension.value[x].coding.code | X | X | X | X |  | Extension und Values werden übernommen |
| Medication.extension.value[x].coding.display | X | X | X | X |  | Extension und Values werden übernommen |
| Medication.extension.value[x].coding.extension | X | X | X | X |  | Extension und Values werden übernommen |
| Medication.extension.value[x].coding.system | X | X | X | X |  | Extension und Values werden übernommen |
| Medication.extension.value[x].coding.userSelected |  | X | X |  |  | Extension und Values werden übernommen |
| Medication.extension.value[x].coding.version | X | X | X | X |  | Extension und Values werden übernommen |
| Medication.extension.value[x].extension | X | X | X | X |  | Extension und Values werden übernommen |
| Medication.extension.value[x].system | X | X | X | X |  | Extension und Values werden übernommen |
| Medication.extension.value[x].text |  | X | X |  |  | Extension und Values werden übernommen |
| Medication.extension:Arzneimittelkategorie(https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Medication_Category) | X | X | X | X |  | Extension und Values werden übernommen |
| Medication.extension:Herstellungsanweisung(https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Medication_CompoundingInstruction) | X |  |  |  |  | Extension und Values werden übernommen |
| Medication.extension:Impfstoff(https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Medication_Vaccine) | X | X | X | X |  | Extension und Values werden übernommen |
| Medication.extension:Kategorie(https://fhir.kbv.de/StructureDefinition/KBV_EX_Base_Medication_Type&#124;1.3.0) | X |  |  | X |  | Extension und Values werden übernommen |
| Medication.extension:Normgroesse(http://fhir.de/StructureDefinition/normgroesse) |  |  | X | X |  | Extension und Values werden übernommen |
| Medication.extension:RxPrescriptionProcessIdentifier(https://gematik.de/fhir/epa-medication/StructureDefinition/rx-prescription-process-identifier-extension) |  |  |  |  | X | Extension und Values werden übernommen |
| Medication.extension:Verpackung(https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Medication_Packaging) | X |  |  |  |  | Extension und Values werden übernommen |
| Medication.form | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.form.coding | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.form.coding.code | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.form.coding.display | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.form.coding.extension | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.form.coding.system | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.form.coding.userSelected | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.form.coding.version | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.form.extension | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.form.text | X | X | X |  | X |  |
| Medication.identifier |  |  |  |  | X |  |
| Medication.implicitRules |  |  |  |  | X |  |
| Medication.ingredient | X |  | X |  | X |  |
| Medication.ingredient.extension | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.ingredient.extension.extension | X |  |  |  |  | Extension und Values werden übernommen |
| Medication.ingredient.extension.url | X |  |  |  |  | Extension und Values werden übernommen |
| Medication.ingredient.extension.value[x] | X |  |  |  |  | Extension und Values werden übernommen |
| Medication.ingredient.extension:Darreichungsform(https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Medication_Ingredient_Form) | X |  |  |  |  | Extension und Values werden übernommen |
| Medication.ingredient.isActive |  | X |  | X | X |  |
| Medication.ingredient.item[x] | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.ingredient.item[x].coding | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.ingredient.item[x].coding.code | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.ingredient.item[x].coding.display | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.ingredient.item[x].coding.extension | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.ingredient.item[x].coding.system | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.ingredient.item[x].coding.userSelected | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.ingredient.item[x].coding.version | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.ingredient.item[x].display | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.ingredient.item[x].extension | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.ingredient.item[x].identifier | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.ingredient.item[x].reference | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.ingredient.item[x].text | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.ingredient.item[x].type | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.ingredient.modifierExtension | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.ingredient.strength | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.ingredient.strength.denominator | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.ingredient.strength.denominator.code |  | X |  | X | X |  |
| Medication.ingredient.strength.denominator.comparator |  | X |  | X | X |  |
| Medication.ingredient.strength.denominator.extension | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.ingredient.strength.denominator.system |  | X |  | X | X |  |
| Medication.ingredient.strength.denominator.unit |  | X |  | X | X |  |
| Medication.ingredient.strength.denominator.value | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.ingredient.strength.extension | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.ingredient.strength.extension.extension | X |  |  |  |  | Extension und Values werden übernommen |
| Medication.ingredient.strength.extension.url | X |  |  |  |  | Extension und Values werden übernommen |
| Medication.ingredient.strength.extension.value[x] | X |  |  |  |  | Extension und Values werden übernommen |
| Medication.ingredient.strength.extension:MengeFreitext(https://fhir.kbv.de/StructureDefinition/KBV_EX_ERP_Medication_Ingredient_Amount) | X |  |  |  |  | Extension und Values werden übernommen |
| Medication.ingredient.strength.numerator | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.ingredient.strength.numerator.code | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.ingredient.strength.numerator.comparator |  | X |  | X | X |  |
| Medication.ingredient.strength.numerator.extension | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.ingredient.strength.numerator.system | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.ingredient.strength.numerator.unit | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.ingredient.strength.numerator.value | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.language |  |  |  |  | X |  |
| Medication.manufacturer |  |  |  |  | X |  |
| Medication.manufacturer.display |  |  |  |  | X |  |
| Medication.manufacturer.extension |  |  |  |  | X | Extension und Values werden übernommen |
| Medication.manufacturer.identifier |  |  |  |  | X |  |
| Medication.manufacturer.reference |  |  |  |  | X |  |
| Medication.manufacturer.type |  |  |  |  | X |  |
| Medication.meta | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.meta.extension | X | X | X | X |  | Extension und Values werden übernommen |
| Medication.meta.profile | X | X | X | X |  |  |
| Medication.modifierExtension | X | X | X | X | X | Eigenschaft und Wert werden übernommen |
| Medication.status |  |  |  |  | X |  |
| Medication.text |  |  |  |  | X |  |
