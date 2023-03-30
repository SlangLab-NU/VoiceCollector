import React, { useState, useEffect } from "react";
import { Box, Button, Typography, Container, Paper, Stack } from "@mui/material";
// import { makeStyles } from '@mui/styles';
import MicIcon from "@mui/icons-material/Mic";
import SendIcon from '@mui/icons-material/Send';
import FastForwardIcon from '@mui/icons-material/FastForward';
import FastRewindIcon from '@mui/icons-material/FastRewind';
import MicOffIcon from "@mui/icons-material/MicOff";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import StopIcon from "@mui/icons-material/Stop";
import data from '../data.js';


export default function RecordMUI() {
  const [promptNum, setPromptNum] = useState(0);
  const [section, setSection] = useState("");
  const [prompt, setPrompt] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [audioUrl, setAudioUrl] = useState(null);

  useEffect(() => {
    setSection(data[promptNum].section);
    setPrompt(data[promptNum].prompt);
  }, [])
  

  function onSkip() {
    if (promptNum < data.length - 1) {
      setPromptNum(promptNum + 1);
      setSection(data[promptNum + 1].section);
      setPrompt(data[promptNum + 1].prompt);
    }
  }

  function onPrev() {
    if (promptNum > 0) {
      setPromptNum(promptNum - 1);
      setSection(data[promptNum - 1].section);
      setPrompt(data[promptNum - 1].prompt);
    }
  }

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
          Prompt {promptNum + 1}/{data.length}
        </Typography>
        <Box>
          <Typography sx={{display: "inline", marginRight: 1}} variant="h6" align="center" gutterBottom>
            Section 
          </Typography>
          <Typography sx={{display: "inline", backgroundColor: "#E7EBF0"}} variant="h6" align="center" gutterBottom>
            {section}
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
          <Typography variant="h6" align="left">
            {prompt}
          </Typography>
        </Paper>
      </Box>

      <Box sx={{flexDirection: "row"}}>
        <Button
          variant="outlined"
          color="secondary"
          startIcon={<FastRewindIcon />}
          sx={{ml: 4, mr: 2}}
          onClick={onPrev}
        >
          Previous
        </Button>

        <Button
          variant="contained"
          sx={{ml: 4, mr: 4}}
          color="primary"
          startIcon={isRecording ? <MicOffIcon /> : <MicIcon />}
          onClick={() =>
            isRecording ? handleStopRecording() : handleStartRecording()
          }
        >
          {isRecording ? "Stop Recording" : "Start Recording"}
        </Button>
        {/* {audioUrl && (
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
        )} */}
        {audioUrl && <audio src={audioUrl} controls />}
        <Button
          sx={{ml: 4, mr: 2}}
          variant="outlined"
          color="secondary"
          endIcon={<FastForwardIcon />}
          onClick={onSkip}
        >
          Skip
        </Button>
        <Button
          variant="contained" 
          endIcon={<SendIcon />}
          sx={{ml: 2, mr: 4}}
        >
          Submit
        </Button>

      </Box>
    </Container>
  );
}
