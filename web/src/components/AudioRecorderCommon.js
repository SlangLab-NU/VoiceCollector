// For the recording logics of the Common Voice project， see the following link:
// Recording page: https://github.com/common-voice/common-voice/blob/5518bc53d42566cf90c6c0d5afefba2956124abf/web/src/components/pages/contribution/speak/speak.tsx
// Implementation of Audio Recorder: https://github.com/common-voice/common-voice/blob/5518bc53d42566cf90c6c0d5afefba2956124abf/web/src/components/pages/contribution/speak/audio-web.ts

import { useState, useRef, useEffect } from "react";
import AudioWeb from "./audio-web";

const AudioRecorder = () => {
  const mimeType = "audio/webm";
  const audioWeb = useRef(null);

  const [permission, setPermission] = useState(false);
  const [recordingStatus, setRecordingStatus] = useState("waiting");
  const [audioInfo, setAudioInfo] = useState(null);
  // const [audio, setAudio] = useState(null);

  const isRecording = () => {
    return recordingStatus === 'recording';
  }

  useEffect(() => {
    audioWeb.current = new AudioWeb(); 

    document.addEventListener('visibilitychange', releaseMicrophone);

    return async () => {
      document.removeEventListener('visibilitychange', releaseMicrophone);

      if (!isRecording()) return;
      await audioWeb.current.stop();
      audioWeb.current = null;
    }
  }, [])

  const releaseMicrophone = () => {
    // If the document is still visible, do not release microphone
    if (!document.hidden) {
      return;
    }

    // Release the microphone
    audioWeb.current.release();
    setRecordingStatus("waiting");
    setPermission(false);
    console.log("Recording stopped");
    console.log("Microphone released");
  };

  const saveRecording = async () => {
    // We noticed that some people hit the Stop button too early, cutting off
    // the recording prematurely. To compensate, we add a short buffer to the
    // end of each recording (issue #1648).

    // const RECORD_STOP_DELAY = 500;
    // setTimeout(async () => {
    //   const info = await this.audio.stop();
    //   this.processRecording(info);
    // }, RECORD_STOP_DELAY);
    // this.recordingStopTime = Date.now();
    // this.setState({
    //   recordingStatus: null,
    // });
    console.log("Recording saved");
  };
  
  const getMicrophonePermission = async () => {
    if (
      !audioWeb.current.isMicrophoneSupported() ||
      !audioWeb.current.isAudioRecordingSupported()
    ) {
      alert("The MediaRecorder API is not supported in your browser.");
    }

    await audioWeb.current.init();
    console.log("Microphone permission granted");
    setPermission(true);
  };

  const startRecording = async () => {
    if (!permission) {
      await getMicrophonePermission();
    }

    await audioWeb.current.start();
    setRecordingStatus("recording");
    console.log("Recording started");
  };

  const stopRecording = async () => {
    const info = await audioWeb.current.stop();
    setAudioInfo(info);
    setRecordingStatus("waiting");
    setPermission(false);
    console.log("Recording stopped");
    saveRecording();
  };


  return (
    <div className="audio-controls">
      {audioInfo ? (
        <div className="audio-container">
          <audio src={audioInfo["url"]} controls></audio>
          <a download href={audioInfo["url"]}>
            Download Recording
          </a>
        </div>
      ) : null}
      {!isRecording() ? (
        <button onClick={startRecording} type="button">
          Start Recording
        </button>
      ) : null}
      {isRecording() ? (
        <button onClick={stopRecording} type="button">
          Stop Recording
        </button>
      ) : null}
    </div>
  );
};


export default AudioRecorder;
