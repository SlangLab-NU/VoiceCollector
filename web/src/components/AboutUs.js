
import * as React from 'react';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Unstable_Grid2';

import Typography from '@mui/material/Typography';
import impairedSpeech from '../assets/2.jpg'

function AboutUs() {
  return (
    <Grid container spacing={3} columns={16}>
      <Grid xs={16}>
        <Box
          component="img"
          sx={{
            height: 500,
            width: 500,
          }}
          alt="The house from the offer."
          src={impairedSpeech}
        />
      </Grid>

      <Grid xs={8}>
        <h1>
          Our datasets is Special because...
        </h1>
      </Grid>
      <Grid xs={8}>
        <Typography color="text.primary">
          We build a data collection platform which is the first one
          focusing on impaired speakers.
        </Typography>
        <br />
        <Typography color="text.primary">
          We publish a dataset which contains high-quality audio
          for dysarthria speakers including severities. To our best
          knowledge, it is the biggest public dataset in the domain.
        </Typography>
        <br />
        <Typography color="text.primary">
          We integrate wav2vec 2.0, a state-of-the-art pre-trained
          speech recognition model, into our validation process to
          verify data quality and generate intelligibility scores as
          additional features.
        </Typography>
      </Grid>
    </Grid>

  )

}

export default AboutUs;