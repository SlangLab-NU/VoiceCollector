// src/componetns/Footer.tsx

import React from "react";
import { Box, Container, Grid, Typography } from "@mui/material";
function Footer (){
  return (
    <Box
      sx={{
        width: "100%",
        height: "auto",
        backgroundColor: "white",
        paddingTop: "1rem",
        paddingBottom: "1rem",
      }}
    >
      <Container maxWidth="lg">
        <Grid container direction="column" alignItems="center">
          <Grid item xs={12}>
            <Typography color="black" variant="h5">
              Voice Collector
            </Typography>
          </Grid>
          <Grid item xs={12}>
            <Typography color="textSecondary" variant="subtitle1">
              {`${new Date().getFullYear()} | React | Material UI | React Router`}
            </Typography>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

export default Footer;