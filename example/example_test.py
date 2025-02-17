import requests

BASE_URL = "http://localhost:3000"

HEADERS = {
    "Authorization": "Basic MTU3ZWZjZWMtYWNhNC00ZTFjLWEw=="
}
# Tests Retrieves data from the `/` endpoint.
def test_endpoint_0():
    url = f"{BASE_URL}/"
    method = "get"
    params = {}
    request_body = {}

    response = requests.request(method, url, json=request_body if request_body else None, params=params)
    assert response.status_code == 200, f"Failed GET /: {response.text}"

# Tests Creates a new resource in the `/users` endpoint with a request body.
def test_endpoint_1():
    url = f"{BASE_URL}/users"
    method = "post"
    params = {}
    request_body = {
    "name": "John Doe",
    "email": "johndoe@example.com",
    "age": 25
}

    response = requests.request(method, url, json=request_body if request_body else None, params=params)
    assert response.status_code == 201, f"Failed POST /users: {response.text}"

# Tests Retrieves data from the `/users` endpoint.
def test_endpoint_2():
    url = f"{BASE_URL}/users"
    method = "get"
    params = {}
    request_body = {}

    response = requests.request(method, url, json=request_body if request_body else None, params=params)
    assert response.status_code == 200, f"Failed GET /users: {response.text}"

# Tests Retrieves data from the `/users/{id}` endpoint.
def test_endpoint_3():
    url = f"{BASE_URL}/users/{id}"
    method = "get"
    params = {
    "id": 1
}
    request_body = {}

    response = requests.request(method, url, json=request_body if request_body else None, params=params)
    assert response.status_code == 200, f"Failed GET /users/{id}: {response.text}"

# Tests Partially updates a resource in the `/users/{id}` endpoint with a request body.
def test_endpoint_4():
    url = f"{BASE_URL}/users/{id}"
    method = "patch"
    params = {
    "id": 1
}
    request_body = {
    "name": "John Doe",
    "email": "johndoe@example.com",
    "age": 25
}

    response = requests.request(method, url, json=request_body if request_body else None, params=params)
    assert response.status_code == 200, f"Failed PATCH /users/{id}: {response.text}"

# Tests Deletes a resource from the `/users/{id}` endpoint.
def test_endpoint_5():
    url = f"{BASE_URL}/users/{id}"
    method = "delete"
    params = {
    "id": 1
}
    request_body = {}

    response = requests.request(method, url, json=request_body if request_body else None, params=params)
    assert response.status_code == 200, f"Failed DELETE /users/{id}: {response.text}"
