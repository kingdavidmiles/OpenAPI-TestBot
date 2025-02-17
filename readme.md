# API Test Generator

## Overview

This project provides an automated solution to generate API test cases using Python and `pytest`. The main goal of the project is to streamline the process of writing API tests by automatically generating test cases based on the specifications defined in an OpenAPI schema (also known as Swagger). 

### Key Features:
- **Automated Test Generation**: The project reads an OpenAPI schema (typically in JSON or YAML format) which describes the structure and endpoints of the API. Based on this schema, the tool automatically generates test cases for each endpoint.
  
- **Support for Different HTTP Methods**: The generated tests cover various HTTP methods like `GET`, `POST`, `PATCH`, and `DELETE`, ensuring that different types of requests are tested.

- **Realistic Test Data Generation**: It integrates with the OpenAI API to generate realistic and dynamic sample data for the test requests. This helps simulate actual API interactions with real-world input, making the tests more robust and representative of real usage.

- **BASE_URL Extraction**: The tool automatically extracts the `BASE_URL` from the OpenAPI URL provided. This URL is crucial for constructing valid API request URLs. It simplifies the configuration, as you don’t need to manually define the base API URL for every test case.

- **Security Header Handling:** The tool can automatically check if security is defined in the API schema and will generate the necessary authentication headers based on the security type (e.g., Basic Auth or Bearer Token). If Basic Auth is used, it will encode the username and password in Base64. For Bearer Token, it will use the provided token to generate the correct authorization header.

- **Comprehensive Coverage**: The test cases generated ensure all specified endpoints and their operations are tested for functionality. This includes validating parameters, request bodies, and responses (status codes, response body, etc.).

This tool saves time and effort in writing repetitive test cases manually, ensuring that all aspects of the API are covered, from basic request functionality to handling edge cases. It can be used to test REST APIs, ensuring that they function correctly and reliably across different endpoints.


## Prerequisites
Ensure you have the following installed on your system:
- Python 3.7+
- `pip`
- `pytest`
- `requests`
- `python-dotenv`
- `prance`
- `responses`

## Installation
```sh
# Clone this repository
git clone https://github.com/kingdavidmiles/test_pilotAI
cd api-test-generator

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

## Configuration
```sh
# Create a .env file and specify the OpenAPI schema URL and OpenAI API key
OPENAI_API_KEY= XXXXXXXXXXXXXXXXXXXXXXXXXX  - #replace with your OpenAPI key
OPENAPI_URL=http://localhost:1337/api-json  #replace with your  openapi key (swagger json)
```
Ensure your API server is running and accessible at the specified URL.

## Authentication with Basic Auth
If the API requires Basic Authentication, you will need to encode the username and password into Base64 and include it in the request header. Follow these steps to convert Basic Auth to Base64:

- Format the credentials: Combine your username and password with a colon (:) separator, like this:
`username:password`

- Base64 encode the credentials: You can convert the formatted credentials into Base64 using a terminal command:

**echo -n "username:password" | base64**

This will output a Base64-encoded string, for example:

`dXNlcm5hbWU6cGFzc3dvcmQ=`

Include in the request header: Add the encoded credentials to the Authorization header like this:

headers = {
    "Authorization": "Basic dXNlcm5hbWU6cGFzc3dvcmQ="
}

Replace `dXNlcm5hbWU6cGFzc3dvcmQ=` with your own encoded credentials.

## Usage
```sh
# Run the script to generate test cases
python ai_testing_tool/generate_tests.py 

# The generated test cases will be stored in the Test/ directory as test_api.py

# Execute all tests using pytest
pytest Test/test_api.py

# Run an individual test case
pytest Test/test_api.py::test_endpoint_1
```

## Features
- Automatically fetches OpenAPI schema (requires OpenAPI 3.1.0).
- Generates `pytest` test cases with sample data.
- Supports `GET`, `POST`, `PATCH`, and `DELETE` methods.
- Resolves `$ref` references in OpenAPI specifications.
- Uses OpenAI to generate realistic sample data.

## Dependencies
These libraries are used for:
- `openai`: Communicating with the OpenAI API for generating test cases and analyzing responses.
- `requests`: To make HTTP requests to APIs.
- `pytest`: For running your tests.
- `prance`: To read and parse OpenAPI (Swagger) specifications.
- `responses`: To mock API responses for testing.

## Troubleshooting
**Issue:** Empty request body for `POST` and `PATCH` requests.
- **Solution:** Ensure your OpenAPI schema provides `example` values or adjust the AI-based sample data generation.

**Issue:** OpenAPI schema not found.
- **Solution:** Check the `OPENAPI_URL` in your `.env` file and ensure your API is accessible.

## Contributing
Feel free to fork the repository, create feature branches, and submit pull requests!

## License
This project is licensed under the MIT License.

