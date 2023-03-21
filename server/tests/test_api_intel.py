"""
Tests for API handlers

"""
import json

import pytest

from app import create_app


@pytest.fixture(scope="module", autouse=True)
def client():
    app = create_app()
    return app.test_client()


def test_get_scores(client):
    response = client.get(
        "/api/v1/intel/",
        json={
            "y_pred": "when he speaks he voices egisabe crant and quimus nus tramfl",
            "y_true": "When he speaks, his voice is just a bit cracked and quivers a trifle.",
        },
    )
    # response = client.get("/api/v1/intel")
    assert response.status_code == 200
    parsed_data = response.json
    assert str(parsed_data) == "{'cer': 0.5333333333333333, 'metaphone_match': 0.6428571428571428, 'sequence_matcher': 0.6875}"
