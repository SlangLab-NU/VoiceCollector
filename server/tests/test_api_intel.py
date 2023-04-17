"""
Tests for API handlers

"""
import json
import pytest
import pathlib 
from werkzeug.datastructures import MultiDict

from app import create_app


@pytest.fixture(scope="module", autouse=True)
def client():
    app = create_app()
    return app.test_client()


def test_transcribe(client):
    samples_dir = pathlib.Path(__file__).parent.resolve() / "samples"
    filenames = [
        "0174.wav",
        "0191.wav",
    ]
    data = MultiDict()

    for fname in filenames:
        audio_file = samples_dir / fname
        data.add("audio", open(audio_file, 'rb'))

    response = client.post(
        "/api/v1/intel/transcribe",
        data=data,
    )
    assert response.status_code == 200
    parsed_data = json.loads(response.data)
    assert parsed_data == {"transcriptions": ["you're used to being on the field", 'wy yell or worry over silly items']}


def test_predict_scores(client):
    samples_dir = pathlib.Path(__file__).parent.resolve() / "samples"
    filenames = [
        "0174.wav",
        "0191.wav",
    ]
    reference = [
        "You're used to being on the field.",
        "Why yell or worry over silly items?"
    ]
    data = MultiDict()

    for fname in filenames:
        audio_file = samples_dir / fname
        data.add("audio", open(audio_file, 'rb'))
    
    for ref in reference:
        data.add("ref", ref)

    response = client.post(
        "/api/v1/intel/",
        data=data,
    )
    assert response.status_code == 200
    parsed_data = json.loads(response.data)
    assert str(parsed_data) == "{'cer': [0.9393939393939394, 0.9090909090909091], 'metaphone_match': [1.0, 1.0], 'sequence_matcher': [0.9850746268656716, 0.9705882352941176]}"
