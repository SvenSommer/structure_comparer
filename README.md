# Medication Profile Comparison
## Overview
This document provides a summary of the differences between the KBV Medication profiles and the ePA Medication profile, as identified by the compare.py script. The differences are predominantly in the metadata and extension elements of the FHIR Medication resource.

## Differences (present in KBV-profiles but not in ePA-Profiles)
### Meta Information
* Medication.meta.id: Unique identifier for the resource
* Medication.meta.extension: Extension fields in the metadata
* Medication.meta.versionId: Resource version identifier
* Medication.meta.lastUpdated: Last update timestamp
* Medication.meta.source: Source of the data
* Medication.meta.profile: Profile information
* Medication.meta.security: Security tags for the resource
* Medication.meta.tag: Tag information for the resource
### Extension Elements
* Medication.extension.id: Unique identifier for the extension
* Medication.extension.extension: Nested extension fields
* Medication.extension.url: URL for the extension definition
* Medication.extension.value[x]: Different value types for extensions
* Medication.extension.value[x].coding: Coding details for the extension values
* Medication.extension.value[x].coding.system: System for the coding
* Medication.extension.value[x].coding.version: Version of the coding system
* Medication.extension.value[x].coding.code: Code in the coding system
* Medication.extension.value[x].coding.display: Display text for the code
* Medication.extension.value[x].coding.userSelected: If the coding was user-selected
### Amount Extensions
* Medication.amount.numerator.extension.id: Unique identifier for the numerator extension
* Medication.amount.numerator.extension.extension: Nested extension fields for the numerator
* Medication.amount.numerator.extension.url: URL for the numerator extension definition
* Medication.amount.numerator.extension.value[x]: Different value types for numerator extensions

## Conclusion
The differences outlined above primarily reflect the additional metadata and extension elements present in the KBV profiles that are not found in the ePA profile. These discrepancies indicate potential areas of incompatibility that might need to be addressed in data integration or mapping processes. It is essential to evaluate the clinical relevance and necessity of these elements in specific use cases.

