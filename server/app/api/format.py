from werkzeug.datastructures import FileStorage
from io import IOBase
from flask import Blueprint, jsonify, request, send_file
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

def convert_to_wav(file, actual_format):
    # Python file object from open(...)
    if isinstance(file, IOBase):
        fname = file.name
    # Flask FileStorage object from request.files
    elif isinstance(file, FileStorage):
        fname = file.filename
    
    dst_path = tmp_dir / (fname.split(".")[0] + ".wav")
    if actual_format == "weba" or actual_format == "webm":
        sound = AudioSegment.from_file(file, "webm")
    elif actual_format == "wav":
        sound = AudioSegment.from_wav(file)
    
    sound = sound.set_channels(config["channels"])
    sound = sound.set_frame_rate(config["sample_rate"])
    sound = sound.set_sample_width(config["sample_width"])
    sound.export(dst_path, format="wav")
    return dst_path

@blueprint.route('/convert_to_wav', methods=["POST"])
def convert_to_wav_handler():
    if 'audio' not in request.files:
            response = jsonify(msg="Error: No audio files in request")
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 400
    if request.files['audio'].filename == '':
            response = jsonify(msg="Not selected file exists")
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, 400
    else: 
        # dest_song = os.path.splitext(file.filename)[0]+'.wav'
        file = request.files['audio']
        actual_format = file.filename.split(".")[-1]
        # dest_audio = file.filename.split(".")[0]
        # print("format:", actual_format)

        if actual_format in ["weba", "webm", "wav"]:
            output_path = convert_to_wav(file, actual_format)
            # Return the converted file
            # response = jsonify({"msg": "converted"})
            response = send_file(output_path)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        
        response = jsonify(format={"expected": "weba/webm", "actual": actual_format}, result=False)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 400

        


