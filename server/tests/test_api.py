"""
Tests for API handlers

"""
import json

import pytest

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
