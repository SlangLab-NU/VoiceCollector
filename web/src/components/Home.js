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


function Home() {
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
                    {/* <Box sx={{ fontFamily: 'Monospace', fontSize: 'h1.heading' }}> */}
                        Donate Your Voice
                    {/* </Box> */}
                </Typography>
                <Button variant="contained">Contribute Your Voice</Button>
                <Button variant="outlined">Download the Database</Button>
                <Button variant="text">Text</Button>
            </Stack>
            <Particle />
        </div>


    )

}

export default Home;

