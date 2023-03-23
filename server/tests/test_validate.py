import json
import pathlib
import pytest

from app import create_app


@pytest.fixture(scope='module', autouse=True)
def client():
    app = create_app()
    return app.test_client()


def test_silence_check_pass(client):
    # current_dir = pathlib.Path(__file__).parent.resolve()
    # audio_file = current_dir/"test.wav"
    # data = {"file": (audio_file, "test.wav")}
        
    # client.post(
    #     data=data,
    #     buffered=True,
    #     content_type="multipart/form-data",
    # )
    
    # response = client.post('/volume_pause')
    # assert response.status_code == 200
    # parsed_data = json.loads(response.data)
    response = client.post('/volume_pause', data={})
    assert response.status_code == 200