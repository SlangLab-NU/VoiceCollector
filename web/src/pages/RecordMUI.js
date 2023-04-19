import React, { useState, useEffect } from "react";
import { Box, Button, Typography, Container, Paper, Stack, Grid } from "@mui/material";
// import { makeStyles } from '@mui/styles';

import SendIcon from '@mui/icons-material/Send';
import FastForwardIcon from '@mui/icons-material/FastForward';
import FastRewindIcon from '@mui/icons-material/FastRewind';
import AudioRecorder from "../components/AudioRecorderCommon.js";
import DoneIcon from '@mui/icons-material/Done';
import ErrorIcon from '@mui/icons-material/Error';
import Alert from '@mui/material/Alert';

import axios from 'axios';

export default function RecordMUI() {
  const [promptNum, setPromptNum] = useState(0);
  const [section, setSection] = useState("");
  const [prompt, setPrompt] = useState("");
  // Force to initialize a new audio_recorder
  const [key, setKey] = useState(0);
  const [alertOpen, setAlertOpen] = useState(false);
  const [audioUrl, setAudioUrl] = useState(null);
  const [audioBlob, setAudioBlob] = useState(null);
  const [submitStatus, setSubmitStatus] = useState(null)
  const [data, setData] = useState([]);
  const [allowSubmit, setAllowSubmit] = useState(false);

  const fetchData = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/v1/speak/get_reference');
      const data = response.data;
      setData(data);
      setSection(data[promptNum].section);
      setPrompt(data[promptNum].prompt);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };


  useEffect(() => {
    fetchData();
  }, []);

  function clearAudio() {
    setAudioUrl(null);
    setAudioBlob(null);
  }

  function onSkip() {
    if (promptNum < data.length - 1) {
      setKey(key + 1);
      setPromptNum(promptNum + 1);
      setSection(data[promptNum + 1].section);
      setPrompt(data[promptNum + 1].prompt);
      setSubmitStatus(null);
      setAllowSubmit(false);
      clearAudio();
    }
  }

  function onPrev() {
    if (promptNum > 0) {
      setKey(key + 1);
      setPromptNum(promptNum - 1);
      setSection(data[promptNum - 1].section);
      setPrompt(data[promptNum - 1].prompt);
      setSubmitStatus(null);
      setAllowSubmit(false);
      clearAudio();
    }
  }

  const handleStopRecording = (audio) => {
    if(audio != null){
      setAllowSubmit(true);
    }
    setAudioUrl(audio.url);
    setAudioBlob(audio.blob);
  };

  const handleSubmit = async() => {
    if(audioBlob == null){
      // TODO: show warning alert here
      console.log("No valid audio file to submit")
      return;
    }
    const formData = new FormData();
    // Get current date with format YYYY-MM-DD HH:MM:SS
    const currentDate = new Date().toISOString().slice(0, 19).replace('T', ' ');
    // Get a random number for session id
    const rand = (Math.random() * 100);
    const filename = "test" + rand + ".webm"

    formData.append("session_id", rand);
    formData.append("date", currentDate);
    formData.append("ref_id", data[promptNum].ref_id);
    formData.append("audio", audioBlob, filename);

    const response = await fetch("http://127.0.0.1:5000/api/v1/speak/submit/" + filename, { method: 'POST', body: formData });
    
    if(response.status === 200){
      setSubmitStatus(true);
    } else {
      // When submission failed, set status to back to empty and show alert
      setSubmitStatus(null);
      setAlertOpen(true);
    }
    else{
      const formData = new FormData();
      const currentDate = new Date()
      // Get a random number for session id
      const rand = (Math.random() * 100);
      const filename = "test" + rand + ".webm"
  
      formData.append("session_id", rand);
      formData.append("date", currentDate);
      formData.append("ref_id", data[promptNum].ref_id);
      formData.append("audio", audioBlob, filename);
  
      const response = await fetch("http://127.0.0.1:5000/api/v1/speak/submit/" + filename, { method: 'POST', body: formData });
      if (await response == JSON.parse("true")) {
        setSubmitStatus(true);
      } else {
        setSubmitStatus(null);
        setAlertOpen(true);
      }
    }
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
          width: "80%",
          height: 500,
        }}
      >
        {section !== 'Image' ? (
          <Box>
            <Typography sx={{ marginBottom: 4 }} variant="h5" align="center">
              Read the following sentences
            </Typography>
            <Paper sx={{ height: 400, overflowY: "auto", padding: 1 }} elevation={3}>
              <Typography variant="h6" align="left">
                {prompt}
              </Typography>
            </Paper>
          </Box>
        ) : (
          <Box>
            <Typography sx={{ marginBottom: 4 }} variant="h5" align="center">
              {prompt}
            </Typography>
            <img src={`/assets/${data[promptNum].image_url}`} alt='' className='image' style={{
              maxWidth: '100%',
              maxHeight: 'calc(100% - 48px)', // Subtract the height occupied by the Typography component and marginBottom
              objectFit: 'contain',
            }} />
          </Box>
        )}

      </Box>


      <Grid container spacing={2}
        display="flex"
        direction="row"
        justifyContent="center"
        alignItems="center">
        <Button
          variant="outlined"
          color="secondary"
          startIcon={<FastRewindIcon />}
          sx={{ ml: 4, mr: 2 }}
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
          {submitStatus ? "next" : "skip"}
        </Button>
        <Button
          disabled = {!allowSubmit}
          variant="contained"
          endIcon={submitStatus == null ? <SendIcon />
            : (submitStatus ? <DoneIcon /> : <ErrorIcon />)}
          sx={{ ml: 2, mr: 4 }}
          onClick={handleSubmit}
        >
          Submit
        </Button>
        {alertOpen && (
          <Alert severity="error" onClose={() => setAlertOpen(false)}
            sx={{
              fontSize: '14px',
              marginTop: '15px',
              width: '500px'
            }}>
            Submission failed. Please try again.
          </Alert>)}
      </Grid>

    </Container>
  );
}