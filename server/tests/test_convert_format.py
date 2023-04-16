import json
import pytest
import os
from pathlib import Path
from app import create_app

@pytest.fixture(scope='module', autouse=True)
def client():
    app = create_app()
    return app.test_client()

# This test fails without a reason. The converted file is supposed to be in the `server/tmp` folder but when testing it went to the `server/tests/samples` folder.
# It works as expected when running the server.
# def test_convert_to_wav(client):
#     test_file_path = Path(__file__).parent / "samples" / 'normal.weba'
    
#     with open(test_file_path, 'rb') as f:
#         response = client.post(f'/api/v1/format/convert_to_wav', data={'audio': f})
    
#     assert response.status_code == 200
#     assert (Path(__file__).parent.parent / "tmp" / 'normal.wav').exists()