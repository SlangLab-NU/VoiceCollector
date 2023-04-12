"use strict";
// Taken from https://github.com/common-voice/common-voice/blob/main/web/src/components/pages/contribution/speak/audio-web.ts
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
exports.__esModule = true;
exports.AudioError = void 0;
var getAudioFormat = (function () {
    var preferredFormat = 'audio/webm';
    var audio = document.createElement('audio');
    var format = audio.canPlayType(preferredFormat)
        ? preferredFormat
        : 'audio/webm';
    return function getAudioFormat() {
        return format;
    };
})();
var AudioError;
(function (AudioError) {
    AudioError["NOT_ALLOWED"] = "NOT_ALLOWED";
    AudioError["NO_MIC"] = "NO_MIC";
    AudioError["NO_SUPPORT"] = "NO_SUPPORT";
})(AudioError = exports.AudioError || (exports.AudioError = {}));
var AudioWeb = /** @class */ (function () {
    function AudioWeb() {
        this.recorderListeners = {
            start: null,
            dataavailable: null,
            stop: null
        };
        // this.analyze = this.analyze.bind(this);
    }
    AudioWeb.prototype.isReady = function () {
        return !!this.microphone;
    };
    AudioWeb.prototype.getMicrophone = function () {
        return new Promise(function (res, rej) {
            var _a;
            function deny(error) {
                rej({
                    NotAllowedError: AudioError.NOT_ALLOWED,
                    NotFoundError: AudioError.NO_MIC
                }[error.name] || error);
            }
            function resolve(stream) {
                res(stream);
            }
            if ((_a = navigator.mediaDevices) === null || _a === void 0 ? void 0 : _a.getUserMedia) {
                navigator.mediaDevices
                    .getUserMedia({ audio: true })
                    .then(resolve, deny);
            }
            else {
                // Browser does not support getUserMedia
                rej(AudioError.NO_SUPPORT);
            }
        });
    };
    // Check all the browser prefixes for microhpone support.
    AudioWeb.prototype.isMicrophoneSupported = function () {
        var _a;
        return ((_a = navigator.mediaDevices) === null || _a === void 0 ? void 0 : _a.getUserMedia);
    };
    // Check if audio recording is supported
    AudioWeb.prototype.isAudioRecordingSupported = function () {
        return (
        // typeof window.MediaRecorder !== 'undefined' &&
        // !window.MediaRecorder.notSupported
        typeof window.MediaRecorder !== 'undefined');
    };
    // private analyze() {
    //   this.analyzerNode.getByteFrequencyData(this.frequencyBins);
    //   if (this.volumeCallback) {
    //     this.volumeCallback(Math.max(...this.frequencyBins));
    //   }
    // }
    AudioWeb.prototype.setVolumeCallback = function (cb) {
        this.volumeCallback = cb;
    };
    /**
     * Initialize the recorder, opening the microphone media stream.
     *
     * If microphone access is currently denied, the user is asked to grant
     * access. Since these permission changes take effect only after a reload,
     * the page is reloaded if the user decides to do so.
     *
     */
    AudioWeb.prototype.init = function () {
        return __awaiter(this, void 0, void 0, function () {
            var microphone, audioContext, sourceNode, volumeNode, analyzerNode, outputNode;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (this.isReady()) {
                            return [2 /*return*/];
                        }
                        return [4 /*yield*/, this.getMicrophone()];
                    case 1:
                        microphone = _a.sent();
                        this.microphone = microphone;
                        audioContext = new window.AudioContext();
                        sourceNode = audioContext.createMediaStreamSource(microphone);
                        volumeNode = audioContext.createGain();
                        analyzerNode = audioContext.createAnalyser();
                        outputNode = audioContext.createMediaStreamDestination();
                        // Make sure we're doing mono everywhere.
                        sourceNode.channelCount = 1;
                        volumeNode.channelCount = 1;
                        analyzerNode.channelCount = 1;
                        outputNode.channelCount = 1;
                        // Connect the nodes together
                        sourceNode.connect(volumeNode);
                        volumeNode.connect(analyzerNode);
                        analyzerNode.connect(outputNode);
                        // and set up the recorder.
                        this.recorder = new window.MediaRecorder(outputNode.stream);
                        // Set up the analyzer node, and allocate an array for its data
                        // FFT size 64 gives us 32 bins. But those bins hold frequencies up to
                        // 22kHz or more, and we only care about lower frequencies which is where
                        // most human voice lies, so we use fewer bins.
                        analyzerNode.fftSize = 128;
                        analyzerNode.smoothingTimeConstant = 0.96;
                        this.frequencyBins = new Uint8Array(analyzerNode.frequencyBinCount);
                        // Setup jsNode for audio analysis callbacks.
                        // TODO: `createScriptProcessor` is deprecated, and is a heavy solution for
                        //       what it’s doing (checking recording volume). It should be replaced
                        //       with something lighter, or AudioWorklets once they become more
                        //       widely adopted.
                        this.jsNode = audioContext.createScriptProcessor(256, 1, 1);
                        this.jsNode.connect(audioContext.destination);
                        this.analyzerNode = analyzerNode;
                        this.audioContext = audioContext;
                        return [2 /*return*/];
                }
            });
        });
    };
    AudioWeb.prototype.start = function () {
        var _this = this;
        if (!this.isReady()) {
            console.error('Cannot record audio before microhphone is ready.');
            return Promise.resolve();
        }
        return new Promise(function (res, rej) {
            _this.chunks = [];
            // Remove the old listeners.
            _this.recorder.removeEventListener('start', _this.recorderListeners.start);
            _this.recorder.removeEventListener('dataavailable', _this.recorderListeners.dataavailable);
            // Update the stored listeners.
            _this.recorderListeners.start = function (e) { return res(); };
            _this.recorderListeners.dataavailable = function (e) {
                _this.chunks.push(e.data);
            };
            // Add the new listeners.
            _this.recorder.addEventListener('start', _this.recorderListeners.start);
            _this.recorder.addEventListener('dataavailable', _this.recorderListeners.dataavailable);
            // Finally, start it up.
            // We want to be able to record up to 60s of audio in a single blob.
            // Without this argument to start(), Chrome will call dataavailable
            // very frequently.
            // this.jsNode.onaudioprocess = this.analyze;
            _this.recorder.start(20000);
        });
    };
    AudioWeb.prototype.stop = function () {
        var _this = this;
        if (!this.isReady()) {
            console.error('Cannot stop audio before microphone is ready.');
            return Promise.reject();
        }
        return new Promise(function (res, rej) {
            _this.jsNode.onaudioprocess = undefined;
            _this.recorder.removeEventListener('stop', _this.recorderListeners.stop);
            _this.recorderListeners.stop = function (e) {
                var blob = new Blob(_this.chunks, { type: getAudioFormat() });
                res({
                    url: URL.createObjectURL(blob),
                    blob: blob
                });
            };
            _this.recorder.addEventListener('stop', _this.recorderListeners.stop);
            _this.recorder.stop();
        });
    };
    AudioWeb.prototype.release = function () {
        if (this.microphone) {
            for (var _i = 0, _a = this.microphone.getTracks(); _i < _a.length; _i++) {
                var track = _a[_i];
                track.stop();
            }
        }
        this.microphone = null;
    };
    return AudioWeb;
}());
exports["default"] = AudioWeb;
