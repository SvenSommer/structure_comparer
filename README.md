# KBV and ePA Medication Profile Comparison

## Overview
This document provides a summary of the differences between the KBV E-Rezept profiles and the ePA Medication profile, as identified by the compare.py script. Additionally, a remark field is generated and adjusted to give advice for the mapping process.


## Hosted Results
The results of the comparison can be viewed directly through these hosted links:
- [GEM_ERP_PR_MedicationDispense|1.3.1 -> EPAMedicationDispense|1.0.2-rc1](https://svensommer.github.io/structure_comparer/projects/erp/docs/GEM_ERP_PR_MedicationDispense|1.3.1_to_EPAMedicationDispense|1.0.2-rc1.html)
- [GEM_ERP_PR_MedicationDispense|1.3.1 -> GEM_ERP_PR_MedicationDispense|1.4.0-rc1](https://svensommer.github.io/structure_comparer/projects/erp/docs/GEM_ERP_PR_MedicationDispense|1.3.1_to_GEM_ERP_PR_MedicationDispense|1.4.0-rc1.html)
- [GEM_ERP_PR_MedicationDispense|1.4.0-rc1 -> EPAMedicationDispense|1.0.2-rc1](https://svensommer.github.io/structure_comparer/projects/erp/docs/GEM_ERP_PR_MedicationDispense|1.4.0-rc1_to_EPAMedicationDispense|1.0.2-rc1.html)
- [KBV_PR_ERP_Medication_Compounding|1.1.0, KBV_PR_ERP_Medication_FreeText|1.1.0, KBV_PR_ERP_Medication_Ingredient|1.1.0, KBV_PR_ERP_Medication_PZN|1.1.0 -> EPAMedication|1.0.2-rc1](https://svensommer.github.io/structure_comparer/projects/erp/docs/KBV_PR_ERP_Medication_Compounding|1.1.0_KBV_PR_ERP_Medication_FreeText|1.1.0_KBV_PR_ERP_Medication_Ingredient|1.1.0_KBV_PR_ERP_Medication_PZN|1.1.0_to_EPAMedication|1.0.2-rc1.html)
- [KBV_PR_ERP_Prescription|1.1.0 -> EPAMedicationRequest|1.0.2-rc1](https://svensommer.github.io/structure_comparer/projects/erp/docs/KBV_PR_ERP_Prescription|1.1.0_to_EPAMedicationRequest|1.0.2-rc1.html)
- [KBV_PR_FOR_Organization|1.1.0 -> OrganizationDirectory|0.11.7](https://svensommer.github.io/structure_comparer/projects/erp/docs/KBV_PR_FOR_Organization|1.1.0_to_OrganizationDirectory|0.11.7.html)
- [KBV_PR_FOR_Practitioner|1.1.0 -> PractitionerDirectory|0.11.7](https://svensommer.github.io/structure_comparer/projects/erp/docs/KBV_PR_FOR_Practitioner|1.1.0_to_PractitionerDirectory|0.11.7.html)

## Web-App

This project provides a web app to configure the mapping between different profiles for different projects.

### Backend

The backend can be found at [service/](service/README.md).

#### REST Client Extension

The service can be evaluated through a predefined collection of requests located in `rest/requests.http`. This collection utilizes the [Rest Client](`https://marketplace.visualstudio.com/items?itemName=humao.rest-client`) extension for easy execution.

To execute a request, simply click on the `Send Request` link located above the respective request definition in the requests.http file. This action triggers the request to the configured host, facilitating the testing process directly within your development environment.

### Frontend

Frontend is currently moved to a seperate Repo: https://github.com/SvenSommer/structure_comparer_frontend

#### Features

- **Mappings Visualization**: Visualize mappings between FHIR profiles with detailed views for each mapping, including properties, classifications, and remarks.

- **Edit and Configure Mappings**: Directly edit mappings to adjust classifications, add remarks, and configure mappings as per project requirements.

- **Responsive Design**: The frontend is designed to be responsive, providing a seamless experience across various devices and screen sizes.

#### Building for Production

To build the frontend for production, run the following command:
    ```bash
    ng build --prod
    ```
This will create a `dist/` directory with optimized files ready to be deployed to a production server.

For more information on Angular development, visit [Angular's official documentation](https://angular.io/docs).
