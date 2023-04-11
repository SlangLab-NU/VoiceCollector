import React, { useState, useEffect } from "react";
import { Box, Button, Typography, Container, Paper, Stack, Grid } from "@mui/material";
// import { makeStyles } from '@mui/styles';

import SendIcon from '@mui/icons-material/Send';
import FastForwardIcon from '@mui/icons-material/FastForward';
import FastRewindIcon from '@mui/icons-material/FastRewind';
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import StopIcon from "@mui/icons-material/Stop";
import data from '../data.js';
import AudioRecorder from "../components/AudioRecorderCommon.js";


export default function RecordMUI() {
  const [promptNum, setPromptNum] = useState(0);
  const [section, setSection] = useState("");
  const [prompt, setPrompt] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  // Force to initialize a new audio_recorder
  const [key, setKey] = useState(0);
  const [audioUrl, setAudioUrl] = useState(null);
  const [audioBlob, setAudioBlob] = useState(null);

  useEffect(() => {
    setSection(data[promptNum].section);
    setPrompt(data[promptNum].prompt);
  }, [])


  function onSkip() {
    if (promptNum < data.length - 1) {
      setKey(key + 1);
      setPromptNum(promptNum + 1);
      setSection(data[promptNum + 1].section);
      setPrompt(data[promptNum + 1].prompt);
    }
  }

  function onPrev() {
    if (promptNum > 0) {
      setKey(key + 1);
      setPromptNum(promptNum - 1);
      setSection(data[promptNum - 1].section);
      setPrompt(data[promptNum - 1].prompt);
    }
  }

  const handleStopRecording = (audio) => {
    setAudioUrl(audio.url);
    setAudioBlob(audio.blob);
  };

  const handleSubmit = async() => {
    console.log(audioBlob);
    const formData = new FormData();
    formData.append("file", audioBlob, "test.ogg");
    const response =await fetch("http://127.0.0.1:5000/api/v1/format/convert_to_wav", { method: 'POST', body: formData });
    console.log(await response.json())
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
          <Typography sx={{ display: "inline", marginRight: 1 }} variant="h6" align="center" gutterBottom>
            Section
          </Typography>
          <Typography sx={{ display: "inline", backgroundColor: "#E7EBF0" }} variant="h6" align="center" gutterBottom>
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
        <Typography sx={{ marginBottom: 4 }} variant="h5" align="center">
          Read the following sentences
        </Typography>

        <Paper sx={{ height: 200, overflowY: "auto", padding: 1 }} elevation={3}>
          <Typography variant="h6" align="left">
            {prompt}
          </Typography>
        </Paper>
      </Box>


      <Grid container spacing={2}
        direction="row"
        justifyContent="center"
        alignItems="center">
        <Button
          variant="outlined"
          color="secondary"
          startIcon={<FastRewindIcon />}
          sx={{ml: 4, mr: 2}}
          onClick={onPrev}
        >
          Previous
        </Button>

        <AudioRecorder key={key}
        onStopRecording={handleStopRecording}
        />

        <Button
          sx={{ ml: 4, mr: 2 }}
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
          sx={{ ml: 2, mr: 4 }}
          onClick={handleSubmit}
        >
          Submit
        </Button>
      </Grid>

    </Container>
  );
}