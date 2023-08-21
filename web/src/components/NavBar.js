import Breadcrumbs from '@mui/material/Breadcrumbs';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid'; // Grid version 1

function NavBar() {
    return (
        <Grid display="flex" justifyContent="center" alignItems="center"
        // style={{backgroundColor: '#c1cbd7'}}
        >
            <Breadcrumbs aria-label="breadcrumb">
                <Link underline="hover" color="inherit" href="/">
                    Donate & Download
                </Link>
                <Link
                    underline="hover"
                    color="inherit"
                    href="/ContactUs"
                >
                    About Us
                </Link>
                <Link
                    underline="hover"
                    color="inherit"
                    href="/ContactUs"
                >
                    Contact Us
                </Link>
            </Breadcrumbs>
        </Grid>
    );
}

export default NavBar;