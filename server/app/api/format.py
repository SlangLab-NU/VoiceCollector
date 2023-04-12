from werkzeug.datastructures import FileStorage
from io import IOBase
from flask import Blueprint, jsonify, request, redirect
import json
import pathlib
from pydub import AudioSegment

blueprint = Blueprint('format', __name__, url_prefix="/format")

current_dir = pathlib.Path(__file__).parent.resolve()
config_path = current_dir / ".." / "config.json"
config = json.loads(config_path.read_text())
tmp_dir = current_dir.parent.parent / "tmp"

if not tmp_dir.exists():
    tmp_dir.mkdir()

def convert_to_wav(file):
    # Python file object from open(...)
    if isinstance(file, IOBase):
        fname = file.name
    # Flask FileStorage object from request.files
    elif isinstance(file, FileStorage):
        fname = file.filename
    
    dst_path = tmp_dir / (fname.split(".")[0] + ".wav")
    audio = AudioSegment.from_file(file, "webm")
    audio.set_channels(config["channels"])
    audio.set_frame_rate(config["sample_rate"])
    audio.set_sample_width(config["sample_width"])
    audio.export(dst_path, format="wav")

@blueprint.route('/convert_to_wav', methods=["POST"])
def convert_to_wav_handler():
    if 'file' not in request.files:
            response = dict(msg="Error: No audio files in request")
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 400
    else: 
        # dest_song = os.path.splitext(file.filename)[0]+'.wav'
        file = request.files['file']
        actual_format = file.filename.split(".")[-1]
        # dest_audio = file.filename.split(".")[0]
        # print("format:", actual_format)
        if actual_format == "weba":
            convert_to_wav(file)
            response = jsonify("converted")
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        
        response = jsonify(format={"expected": "weba", "actual": actual_format}, result=False)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 400

        


