import os
import openai
import requests
import json
import base64
from dotenv import load_dotenv
from urllib.parse import urlparse
import time

# Load environment variables from .env file
load_dotenv()

# OpenAI API setup
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Get OpenAPI URL from .env
openapi_url = os.getenv("OPENAPI_URL")

# Extract BASE_URL from openapi_url
parsed_url = urlparse(openapi_url)
BASE_URL = f"{parsed_url.scheme}://{parsed_url.netloc}"  # Extracts base domain

print(f"Using OpenAPI URL: {openapi_url}")
print(f"Extracted BASE_URL: {BASE_URL}\n")


# This function determines the authentication type from an OpenAPI schema and returns the appropriate headers. It checks for HTTP Basic Auth, Bearer Token, and API Key authentication methods, and returns the corresponding Authorization header with the required credentials. The function expects the OpenAPI schema to be passed as a dictionary (schema) and uses it to extract the security schemes and requirements.
def get_auth_headers(schema):
    """Determine authentication type from OpenAPI schema and return appropriate headers."""
    print("🔐 Checking authentication requirements...")
    security_schemes = schema.get("components", {}).get("securitySchemes", {})
    security_requirements = schema.get("security", [])

    print(f"Security Schemes: {security_schemes}")
    print(f"Security Requirements: {security_requirements}")

    if not security_requirements:
        if "basic" in security_schemes:
            print("Using HTTP Basic Auth...")
            username = "your-username"
            password = "your-password"
            credentials = f"{username}:{password}"
            encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
            return {"Authorization": f"Basic {encoded_credentials}"}
        elif "bearer" in security_schemes:
            print("Using Bearer Token...")
            return {"Authorization": "Bearer your-access-token"}  # Replace with actual token
        print("No authentication found.")
        return {}

    # Process and select the correct authentication method based on the schema
    auth_headers = {}
    for requirement in security_requirements:
        for scheme_name in requirement:
            scheme = security_schemes.get(scheme_name, {})
            print(f"Processing scheme: {scheme_name} - {scheme}")

            if scheme.get("type") == "http":
                if scheme.get("scheme") == "basic":
                    print("Using HTTP Basic Auth...")
                    username = "your-username"
                    password = "your-password"
                    credentials = f"{username}:{password}"
                    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
                    auth_headers = {"Authorization": f"Basic {encoded_credentials}"}
                elif scheme.get("scheme") == "bearer":
                    print("Using Bearer Token...")
                    auth_headers = {"Authorization": "Bearer your-access-token"}  # Replace with actual token
            elif scheme.get("type") == "apiKey":
                if scheme.get("in") == "header":
                    print(f"Using API Key for {scheme.get('name', 'Authorization')}...")
                    auth_headers = {scheme.get("name", "Authorization"): "your-api-key"}  # Replace with actual API key

    print(f"Auth headers: {auth_headers}\n")
    return auth_headers

# This function uses OpenAI's GPT-4 model to generate a realistic value for a given API parameter based on its name and type. It sends a prompt to OpenAI, which includes the parameter name and type, and returns the generated value. If an error occurs, it returns a default value.
def get_openai_generated_value(param_name, schema_type):
    """Use OpenAI to generate a realistic value based on the parameter name and type."""
    prompt = f"Generate a realistic example value for a parameter named '{param_name}' of type '{schema_type}'."
    
    try:
        print(f"🌟 Generating value for parameter '{param_name}' ({schema_type}) using OpenAI...")
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You generate realistic API parameter values."},
                {"role": "user", "content": prompt},
            ]
        )
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"⚠️ OpenAI error: {e}")
        return "default_value"

# This function resolves a $ref schema reference in an OpenAPI schema by extracting the referenced component from the overall OpenAPI schema. If the reference is valid, it returns the referenced schema; otherwise, it returns the original schema.
def resolve_schema_ref(schema, openapi_schema):
    """Resolve a $ref schema reference by extracting referenced components from the schema."""
    ref_path = schema.get("$ref", "").split("/")
    if len(ref_path) > 2 and ref_path[-2] == "schemas":
        print(f"Resolving $ref: {ref_path[-1]}")
        return openapi_schema.get("components", {}).get("schemas", {}).get(ref_path[-1], {})
    return schema


# Generates a sample value based on the provided OpenAPI schema.

# Purpose

# Creates sample values for testing or mocking API responses.

# Input

# schema: OpenAPI schema object
# openapi_schema: Overall OpenAPI schema object

def generate_sample_value(schema, openapi_schema):
    """Generate a sample value based on the OpenAPI schema for different data types."""
    if not schema:
        return None

    # Resolve $ref if present
    schema = resolve_schema_ref(schema, openapi_schema)

    # Check for 'example' or 'examples'
    if 'example' in schema:
        print(f"Using 'example' value for type: {schema['example']}")
        return schema['example']
    if 'examples' in schema and isinstance(schema['examples'], dict):
        print(f"Using 'examples' value for type: {next(iter(schema['examples'].values()))['value']}")
        return next(iter(schema['examples'].values())).get('value', {})

    schema_type = schema.get('type', 'string')

    sample_values = {
        "string": "sample_text",
        "integer": 42,
        "number": 12.34,
        "boolean": True,
        "array": [generate_sample_value(schema.get('items', {}), openapi_schema)],
        "object": {key: generate_sample_value(value, openapi_schema) for key, value in schema.get('properties', {}).items()}
    }

    print(f"Generated sample value for type '{schema_type}': {sample_values.get(schema_type, 'sample_value')}")
    return sample_values.get(schema_type, "sample_value")


# This function generates a short description for a test case based on the HTTP method and endpoint. It uses a dictionary to map HTTP methods to descriptive phrases and appends "with a request body" if a request body is present. The generated description is in the format "Tests [action] the [endpoint] endpoint[with request body]."
def generate_test_description(path, method, request_body):
    """Generate a short description for the test case based on HTTP method and endpoint."""
    method_descriptions = {
        "get": "Retrieves data from",
        "post": "Creates a new resource in",
        "put": "Updates a resource in",
        "patch": "Partially updates a resource in",
        "delete": "Deletes a resource from"
    }
    
    request_data_info = " with a request body" if request_body else ""
    return f"Tests {method_descriptions.get(method, 'calls')} the `{path}` endpoint{request_data_info}."

# This code snippet generates pytest test cases for all API endpoints defined in an OpenAPI schema. It fetches the schema, extracts endpoint information, generates sample request parameters and bodies, and creates test functions for each endpoint. The generated test script is then saved to a file named test_api.py in a directory named Test.

def generate_tests_from_openapi():
    """Fetch OpenAPI schema, validate it, and generate pytest test cases for all API endpoints."""
    print("🔄 Fetching OpenAPI schema...")
    response = requests.get(openapi_url)
    if response.status_code != 200:
        print(f"❌ Error fetching OpenAPI schema: {response.status_code}") 
        return
    
    schema = response.json()
    HEADERS = get_auth_headers(schema)
    test_script = f"import requests\n\nBASE_URL = \"{BASE_URL}\"\n\nHEADERS = {json.dumps(HEADERS, indent=4)}\n\n"

    test_index = 0
    total_api_count = 0  # Counter for total APIs
    for path, methods in schema.get('paths', {}).items():
        for method, details in methods.items():
            print(f"\n🔍 Processing endpoint: {method.upper()} {path}")
            parameters = {}

            # Extract example parameters
            for param in details.get('parameters', []):
                if 'name' in param and 'in' in param:
                    sample_value = generate_sample_value(param.get('schema', {}), schema)
                    parameters[param['name']] = sample_value

            # Generate request body for POST & PATCH methods
            request_body = None
            if method.lower() in ['post', 'patch']:
                if 'requestBody' in details and 'content' in details['requestBody']:
                    for content_type, content_data in details['requestBody']['content'].items():
                        if 'schema' in content_data:
                            request_body = generate_sample_value(content_data['schema'], schema)
                        else:
                            request_body = {}
                        break  # Stop at the first valid content type

            # Ensure request_body is a dictionary or None
            if not isinstance(request_body, dict):
                request_body = {}

            expected_status = list(details.get('responses', {}).keys())[0] if details.get('responses', {}) else "200"

            # Convert params to JSON
            params_json = json.dumps(parameters, indent=4)
            request_body_json = json.dumps(request_body, indent=4)

            # Generate description comment
            test_description = generate_test_description(path, method.lower(), request_body)

            # Generate an individual test function
            test_function = f"""
# {test_description}
def test_endpoint_{test_index}():
    url = f"{{BASE_URL}}{path}"
    method = "{method.lower()}"
    params = {params_json}
    request_body = {request_body_json}

    response = requests.request(method, url, json=request_body if request_body else None, params=params, headers=HEADERS)
    assert response.status_code == {expected_status}, f"Failed {method.upper()} {path}: {{response.text}}"
"""
            test_script += test_function
            test_index += 1
            total_api_count += 1  # Increment API count

    # Save pytest script
    if not os.path.exists("Test"):
        os.makedirs("Test")

    test_file_path = "Test/test_api.py"
    with open(test_file_path, "w") as file:
        file.write(test_script)

    print(f"✅ Pytest test cases saved to {test_file_path}")
    print(f"🔢 Total APIs processed: {total_api_count}\n")

if __name__ == "__main__":
    generate_tests_from_openapi()
