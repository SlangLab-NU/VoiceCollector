import React, { useState } from "react";
import { Box, Button, Typography, Container, Paper, Stack } from "@mui/material";
// import { makeStyles } from '@mui/styles';
import MicIcon from "@mui/icons-material/Mic";
import MicOffIcon from "@mui/icons-material/MicOff";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import StopIcon from "@mui/icons-material/Stop";
import data from '../data.js';


export default function RecordMUI() {
  const [promptNum, setPromptNum] = useState("");
  const [section, setSection] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [audioUrl, setAudioUrl] = useState(null);

  const handleStartRecording = () => {
    setIsRecording(true);
    setIsPlaying(false);
    setAudioUrl(null);
  };

  const handleStopRecording = (blob) => {
    setIsRecording(false);
    setAudioUrl(URL.createObjectURL(blob));
  };

  const handleStartPlaying = () => {
    setIsPlaying(true);
  };

  const handleStopPlaying = () => {
    setIsPlaying(false);
  };

  return (
    <Container>
      <Box
        sx={{
          marginTop: 4,
          marginBottom: 4,
        }}
      >
        <Typography variant="h6" align="center" gutterBottom>
          Prompt 1/7
        </Typography>
        <Box>
          <Typography sx={{display: "inline", marginRight: 1}} variant="h6" align="center" gutterBottom>
            Section 
          </Typography>
          <Typography sx={{display: "inline", backgroundColor: "#E7EBF0"}} variant="h6" align="center" gutterBottom>
            Sentences 
          </Typography>
        </Box>
      </Box>
      <Box
        sx={{
          // border: `2px solid`,
          borderRadius: 2,
          // Paddings
          pt: 4,
          pb: 4,
          pl: 10,
          pr: 10,
          mb: 4,
          backgroundColor: "#E7EBF0",
        }}
      >
        <Typography sx={{marginBottom: 4}} variant="h5" align="center">
            Read the following sentences
        </Typography>

        <Paper sx={{height: 200, overflowY: "auto", padding: 1}} elevation={3}>
          <Typography variant="subtitle1" align="left">
            You wished to know all about my grandfather. Well, he is nearly
            ninety-three years old. He dresses himself in an ancient black frock
            coat, usually minus several buttons; yet he still thinks as swiftly
            as ever. A long, flowing beard clings to his chin, giving those who
            observe him a pronounced feeling of the utmost respect. When he
            speaks his voice is just a bit cracked and quivers a trifle. Twice
            each day he plays skillfully and with zest upon our small organ.
            Except in the winter when the ooze or snow or ice prevents, he
            slowly takes a short walk in the open air each day. We have often
            urged him to walk more and smoke less, but he always answers,
            “Banana Oil!” Grandfather likes to be modern in his language.
          </Typography>
        </Paper>
      </Box>

      <Box>
      <Button
        variant="contained"
        sx={{marginRight: 4}}
        color="primary"
        startIcon={isRecording ? <MicOffIcon /> : <MicIcon />}
        onClick={() =>
          isRecording ? handleStopRecording() : handleStartRecording()
        }
      >
        {isRecording ? "Stop Recording" : "Start Recording"}
      </Button>
      <Button
        variant="contained"
        color="secondary"
      >
        Skip
      </Button>
      {audioUrl && (
        <Button
          variant="contained"
          color="secondary"
          startIcon={isPlaying ? <StopIcon /> : <PlayArrowIcon />}
          onClick={() =>
            isPlaying ? handleStopPlaying() : handleStartPlaying()
          }
        >
          {isPlaying ? "Stop Playback" : "Start Playback"}
        </Button>
      )}
      {audioUrl && <audio src={audioUrl} controls />}
      </Box>
    </Container>
  );
}
