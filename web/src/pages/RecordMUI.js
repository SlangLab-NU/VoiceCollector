import React, { useState, useEffect } from "react";
import { Box, Button, Typography, Container, Paper, Stack, Grid } from "@mui/material";
// import { makeStyles } from '@mui/styles';

import SendIcon from '@mui/icons-material/Send';
import FastForwardIcon from '@mui/icons-material/FastForward';
import FastRewindIcon from '@mui/icons-material/FastRewind';
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import StopIcon from "@mui/icons-material/Stop";
import AudioRecorder from "../components/AudioRecorderCommon.js";
import DoneIcon from '@mui/icons-material/Done';
import ErrorIcon from '@mui/icons-material/Error';

import axios from 'axios';

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
  const [submitStatus, setSubmitStatus] = useState(null)
  const [data, setData] = useState([]);

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

  function onSkip() {
    if (promptNum < data.length - 1) {
      setKey(key + 1);
      setPromptNum(promptNum + 1);
      setSection(data[promptNum + 1].section);
      setPrompt(data[promptNum + 1].prompt);
      setSubmitStatus(null);
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
    if(audioBlob == null){
      console.log("No valid audio file to submit")
    }
    const formData = new FormData();
    formData.append("file", audioBlob, "test.ogg");
    // const response =await fetch("http://127.0.0.1:5000/api/v1/validate/format", { method: 'POST', body: formData });
    const response = JSON.parse('true')
    if(await response  ==  JSON.parse("true")){
      // TODO: change skip button to 'next'
      setSubmitStatus(true);
    }else{
      // when submission failed, set status to false
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
            Tell me what is happening in this picture
          </Typography>
          <img src={`/assets/${prompt}`} alt='' className='image' style={{
            maxWidth: '100%',
            maxHeight: 'calc(100% - 48px)', // Subtract the height occupied by the Typography component and marginBottom
            objectFit: 'contain',
          }}/>
      </Box>
      )}
        
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
          {submitStatus ? "next" : "skip"}
        </Button>
        <Button
          variant="contained"
          endIcon={ submitStatus == null? <SendIcon /> 
          : (submitStatus ? <DoneIcon /> :<ErrorIcon />)}
          sx={{ ml: 2, mr: 4 }}
          onClick={handleSubmit}
        >
          Submit
        </Button>
      </Grid>

    </Container>
  );
}