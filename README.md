# Medication Profile Comparison
## Overview
This document provides a summary of the differences between the KBV Medication profiles and the ePA Medication profile, as identified by the compare.py script. The differences are predominantly in the metadata and extension elements of the FHIR Medication resource.

## Differences
### Properties missing in the ePA profile and present in all KBV profiles:
```
Medication.meta.extension
Medication.meta.id
Medication.meta.lastUpdated
Medication.meta.profile
Medication.meta.security
Medication.meta.source
Medication.meta.tag
Medication.meta.versionId

Medication.extension.extension
Medication.extension.id
Medication.extension.url

Medication.extension.value[x].code
Medication.extension.value[x].coding
Medication.extension.value[x].coding.code
Medication.extension.value[x].coding.display
Medication.extension.value[x].coding.extension
Medication.extension.value[x].coding.id
Medication.extension.value[x].coding.system
Medication.extension.value[x].coding.userSelected
Medication.extension.value[x].coding.version

Medication.extension.value[x]
Medication.extension.value[x].display
Medication.extension.value[x].extension
Medication.extension.value[x].id
Medication.extension.value[x].system
Medication.extension.value[x].text
Medication.extension.value[x].userSelected
Medication.extension.value[x].version
```

### Additional properties missing in KBV Profile 'KBV_PR_ERP_Medication_Ingredient' and 'KBV_PR_ERP_Medication_PZN', not in common missing list:
```
Medication.amount.numerator.extension.extension
Medication.amount.numerator.extension.id
Medication.amount.numerator.extension.url
Medication.amount.numerator.extension.value[x]
```

## Conclusion
The differences outlined above primarily reflect the additional metadata and extension elements present in the KBV profiles that are not found in the ePA profile. These discrepancies indicate potential areas of incompatibility that might need to be addressed in data integration or mapping processes. It is essential to evaluate the clinical relevance and necessity of these elements in specific use cases.

