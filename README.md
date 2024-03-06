# KBV and ePA Medication Profile Comparison

## Overview
This document provides a summary of the differences between the KBV E-Rezept profiles and the ePA Medication profile, as identified by the compare.py script. Additionally, a remark field is generated and adjusted to give advice for the mapping process.


## Hosted Results
The results of the comparison can be viewed directly through these hosted links:
- [KBV_PR_FOR_Organization in OrganizationDirectory](https://svensommer.github.io/structure_comparer/projects/erp/docs/OrganizationDirectory.html)
- [KBV_PR_FOR_Practitioner in PractitionerDirectory](https://svensommer.github.io/structure_comparer/projects/erp/docs/PractitionerDirectory.html)
- [KBV_PR_ERP_Prescription in EPAMedicationRequest](https://svensommer.github.io/structure_comparer/projects/erp/docs/EPAMedicationRequest.html)
- [KBV_PR_ERP_Medication_Compounding, KBV_PR_ERP_Medication_FreeText, KBV_PR_ERP_Medication_Ingredient, KBV_PR_ERP_Medication_PZN in EPAMedication](https://svensommer.github.io/structure_comparer/projects/erp/docs/EPAMedication.html)

## Web-App

This project provides a web app to configure the mapping between different profiles for different projects.

### Backend

Start the backend service from the repository root

```bash
python server.py --project-dir projects/<name>
```

The started service is available at `localhost:5000`. The OpenAPI specification is available with the route `/spec`.

#### REST Client

The service can be evaluated through a predefined collection of requests located in `rest/requests.http`. This collection utilizes the [Rest Client](`https://marketplace.visualstudio.com/items?itemName=humao.rest-client`) extension for easy execution.

The target `host` for these requests is specified in the devcontainer.json file under the rest-client.environmentVariables setting, as shown below:

```json
"rest-client.environmentVariables": {
    "local": {
        "host": "localhost:5000"
    }
}
```

To execute a request, simply click on the Send Request link located above the respective request definition in the requests.http file. This action triggers the request to the configured host, facilitating the testing process directly within your development environment.

### Frontend

TODO
