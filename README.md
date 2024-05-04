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

The frontend for the Structure Comparer Web App is developed using Angular. It provides an interactive user interface to visualize and configure mappings between different FHIR profiles.

#### Setup and Development

Before you start, make sure you have Node.js and the Angular CLI installed. The development environment is prepared to run inside a Dev Container with all necessary dependencies.

1. Navigate to the frontend directory:
    ```bash
    cd /workspaces/structure_comparer/frontend/structure-comparer
    ```

2. Install the required npm packages:
    ```bash
    npm install
    ```

3. Start the development server:
    ```bash
    ng serve
    ```
    The Angular development server will start, and you can access the frontend by navigating to `http://localhost:4200` in your web browser.

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
