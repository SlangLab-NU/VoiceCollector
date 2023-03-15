
import React, { useState } from "react";
import Box from '@mui/material/Box';
import Grid from '@mui/material/Unstable_Grid2';
import impairedSpeaker from '../assets/3.jpg'
import TextField from '@mui/material/TextField';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import SendIcon from '@mui/icons-material/Send';



function ContactUs() {
    const [submitted, setSubmitted] = useState(false);
    const handleSubmit = () => {
        setTimeout(() => {
            setSubmitted(true);
        }, 100);
    };

    if (submitted) {
        return (
            <>
                <div className="text-2xl">Thank you!</div>
                <div className="text-md">We'll be in touch soon.</div>
            </>
        );
    }

    return (
        <Grid container spacing={3} columns={16} marginTop={10}>
            <Grid xs={8}>
                <Box
                    component="img"
                    sx={{
                        height: 500,
                        width: 600,
                    }}
                    alt="The house from the offer."
                    src={impairedSpeaker}
                />
            </Grid>
            <Grid xs={8}>
                <Stack spacing={3}>
                    <h1>
                        Make a Contact With Us
                    </h1>
                    <TextField id="input-firstname" label="First Name" variant="outlined"
                        style={{ width: 200 }} />
                    <TextField id="input-lastname" label="Last Name" variant="outlined"
                        style={{ width: 200 }} />
                    <TextField id="input-email" label="Email" variant="outlined"
                        style={{ width: 200 }} />
                    <TextField
                        id="input-why-contact"
                        label="Why contact?"
                        multiline
                        rows={4}
                        style={{ width: 400 }}
                    />
                    <Button
                        variant="outlined"
                        endIcon={<SendIcon />}
                        style={{ width: 200 }}>Send</Button>
                </Stack>
            </Grid>
        </Grid>
    );
}

export default ContactUs;
