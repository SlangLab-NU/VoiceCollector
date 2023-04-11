from flask import Blueprint, jsonify, request, flash
from ..scripts import silence_check, volume_check, length_check
import wave
import contextlib
import json
import pathlib
import soundfile as sf
from pydub import AudioSegment
import sys
sys.path.append('/usr/bin/ffmpeg')

blueprint = Blueprint('format', __name__, url_prefix="/format")

current_dir = pathlib.Path(__file__).parent.resolve()
config_path = current_dir / ".." / "config.json"

@blueprint.route('/convert_to_wav', methods=["POST","GET"])
def convert_to_wav():
    if request.method == 'GET' :
        response = jsonify("GET")
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    if 'file' not in request.files:
            # response = jsonify(filename_format={"expected": expected_format, "actual": actual_format}, result=False)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
    else: 
        # dest_song = os.path.splitext(file.filename)[0]+'.wav'
        file = request.files['file']
        actual_format = file.filename.split(".")[-1]
        # dest_audio = file.filename.split(".")[0]
        print("format:",actual_format)
        if actual_format == "ogg":
            print("OGG FILE FOUND!")
            original_audio = AudioSegment.from_ogg(file)
            original_audio.export("./test.wav", format="wav")
            response = jsonify("converted")
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        
            

