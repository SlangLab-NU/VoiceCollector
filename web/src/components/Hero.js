import * as React from 'react';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import Particle from './Particle';
import Typography from '@mui/material/Typography';



const buttons = [
    <Button key="one">One</Button>,
    <Button key="two">Two</Button>,
    <Button key="three">Three</Button>,
];


function Hero() {
    return (
        <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            height: '100vh'
        }}
        >
            <Stack spacing={2}>
                <Typography variant="h4" component="div">
                    Welcome to VoiceCollector
                </Typography>
                <Typography variant="h5" component="div">
                    We try to understand how people with dysarthria speak
                </Typography>
                <Button variant="contained" href='/record'>Donate Your Voice</Button>
                <Button variant="outlined">Download the Dataset</Button>
                {/* <Button variant="text">Text</Button> */}
            </Stack>
            {/* <Particle /> */}
        </div>


    )

}

export default Hero;

