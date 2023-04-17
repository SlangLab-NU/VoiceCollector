"""
Tests for API handlers

"""
import json
import jsonschema
import pytest
import io
import os
from app import create_app

@pytest.fixture(scope='module', autouse=True)
def client():
    app = create_app()
    return app.test_client()


def test_default(client):
    response = client.get('/api/v1/')
    assert response.status_code == 200
    parsed_data = json.loads(response.data)
    assert parsed_data.get('msg') == 'Welcome to VoiceCollector backend API.'


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
            "prompt": {"type": "string"},
            "promptNum": {"type": "number"}
        },
        "required": ["ref_id","section", "prompt", "promptNum"]
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

def test__write_record_route(client):
    # Test data
    data = {
        "session_id": "session_id234",
        "s3_url": "audio123.wav",
        "date": "2023-03-23 12:34:56",
        "validated": True,
        "ref_id": 3,
        "sequence_matcher": 0.9,
        "cer": 0.8,
        "metaphone_match": 0.7
    }
    # Send a POST request with the test data
    response = client.post(
        "/api/v1/speak/write_record",
        data=json.dumps(data),
        content_type="application/json"
    )
    # Check if the response has a success status code (200)
    assert response.status_code == 200
    # Check if the response JSON has the expected result
    response_data = json.loads(response.data)
    assert response_data["result"] == "success"

def test__write_record_route_invalid_data(client):
    # Test data
    data = {
        "s3_url": "audio123.wav",
        "date": "2023-03-23 12:34:56",
        "validated": True,
        "ref_id": 3,
        "sequence_matcher": 0.9,
        "cer": 0.8,
        "metaphone_match": 0.7
    }
    # Send a POST request with the test data
    response = client.post(
        "/api/v1/speak/write_record",
        data=json.dumps(data),
        content_type="application/json"
    )
    # Check if the response has a failed status code (400)
    assert response.status_code == 400 
    # Check if the response JSON has the expected result
    assert response.get_json()['message'].startswith("'session_id' is a required property")

    data2 = {
        "session_id": 1,
        "s3_url": "audio123.wav",
        "date": "2023-03-23 12:34:56",
        "validated": True,
        "ref_id": 3,
        "sequence_matcher": 0.9,
        "cer": 0.8,
        "metaphone_match": 0.7
    }
    # Send a POST request with the test data
    response = client.post(
        "/api/v1/speak/write_record",
        data=json.dumps(data2),
        content_type="application/json"
    )
    # Check if the response has a failed status code (400)
    assert response.status_code == 400 
    # Check if the response JSON has the expected result
    assert response.get_json()['message'].startswith("1 is not of type 'string'")
    

def test_write_file_route(client):
    # Test with no file
    response = client.post('/api/v1/speak/write_file/test_file.wav')
    assert response.get_json()['msg'] == "Error: No audio files in request"

    # Test with valid file
    test_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'samples', '0174.wav')
    for i in range(10):
            with open(test_file_path, 'rb') as f:
                response = client.post(f'/api/v1/speak/write_file/test_file_{i}.wav', data={'audio': f})
            assert response.status_code == 200


def test_submit(client):
    # Test with valid file
    test_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "samples", 'normal.weba')
    with open(test_file_path, 'rb') as f:
        data = {
            "session_id": "session_ggg",
            "date": "2023-01-01 11:11:11",
            "ref_id": 3,
            "audio": f,
        }
        response = client.post(f'/api/v1/speak/submit/test_ggg.wav', data=data)

    assert response.status_code == 200
