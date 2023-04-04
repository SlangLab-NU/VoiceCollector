import json
import pathlib
import pytest

from app import create_app


@pytest.fixture(scope='module', autouse=True)
def client():
    app = create_app()
    return app.test_client()

def test_format_check_pass(client):
    samples_dir = pathlib.Path(__file__).parent.resolve() / "samples"
    filenames = [
        "silence_valid_format.wav",
        "silence_stereo.wav",
        "silence_22khz.wav",
        "silence.m4a",
    ]
    results = [
        "{'result': True}",
        "{'channels': {'actual': 2, 'expected': 1}, 'result': False}",
        "{'channels': {'actual': 2, 'expected': 1}, 'result': False, 'sample_rate': {'actual': 22050, 'expected': 48000}}",
        "{'filename_format': {'actual': 'm4a', 'expected': 'wav'}, 'result': False}",
    ]

    for fname, result in zip(filenames, results):
        audio_file = samples_dir / fname
        with open(audio_file, 'rb') as f:
            data = {"file": f}
            response = client.post(
                "/api/v1/validate/format",
                data=data,
            )
        assert response.status_code == 200
        parsed_data = json.loads(response.data)
        assert str(parsed_data) == result


def test_silence_check_pass(client):
    samples_dir = pathlib.Path(__file__).parent.resolve() / "samples"
    filenames = [
        "voice_gawei.wav",
        "low_voice_silence.wav",
        "low_voice_long_pause.wav",
        "low_voice_very_long_silence.wav",
    ]
    results = [
        "{'result': True, 'silence_ratio': 0.3928571428571429, 'volume': -29.117730341169}",
        "{'result': True, 'silence_ratio': 0.7074235807860262, 'volume': -41.00134167022599}",
        "{'result': True, 'silence_ratio': 0.8668639053254438, 'volume': -42.668657847696984}",
        "{'result': True, 'silence_ratio': 0.7418224299065421, 'volume': -41.61762061851039}"
    ]

    for fname, result in zip(filenames, results):
        audio_file = samples_dir / fname
        with open(audio_file, 'rb') as f:
            data = {"file": f}
            response = client.post(
                "/api/v1/validate/volume_pause",
                data=data,
            )
        assert response.status_code == 200
        parsed_data = json.loads(response.data)
        assert str(parsed_data) == result