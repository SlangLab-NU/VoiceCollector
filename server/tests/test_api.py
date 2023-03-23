"""
Tests for API handlers

"""
import json
import jsonschema
import pytest

from app import create_app


@pytest.fixture(scope='module', autouse=True)
def client():
    app = create_app()
    return app.test_client()


def test_not_found(client):
    response = client.get('/noexist')
    assert response.status_code == 404
    parsed_data = json.loads(response.data)
    assert parsed_data.get('error') == 'Not Found'


# def test_hello_world(client):
#     response = client.get('/api/v1/hello/world')
#     parsed_data = json.loads(response.data)
#     assert response.status_code == 200
#     assert parsed_data.get('hello') == 'world'


# def test_hello_foo(client):
#     response = client.get('/api/v1/hello/foo')
#     parsed_data = json.loads(response.data)
#     assert response.status_code == 200
#     assert parsed_data.get('hello') == 'foo'
# TODO: add tests for all routers

def test_get_reference_api(client):
    response = client.get('/api/v1/speak/get_reference')
    print(response.status_code)
    assert response.status_code == 200


# Define the reference schema as a JSON object
REFERENCE_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "image_url": {"type": ["null", "string"]},
            "ref_id": {"type": "number"},
            "section": {"type": "string"},
            "text": {"type": "string"}
        },
        "required": ["ref_id", "section", "text"]
    }
}

def test_validate_json_schema(client):
    # Define the JSON data to be validated
    response = client.get('/api/v1/speak/get_reference')
    parsed_data = json.loads(response.data)
    # Validate the JSON data against the schema
    jsonschema.validate(instance=parsed_data, schema=REFERENCE_SCHEMA)
    # If the JSON data is valid against the schema, the test passes
    assert True


    