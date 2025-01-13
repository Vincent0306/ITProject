import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import AppRegistrationIcon from '@mui/icons-material/AppRegistration';
import FactCheckIcon from '@mui/icons-material/FactCheck';
import MarkAsUnreadIcon from '@mui/icons-material/MarkAsUnread';

const HomePage = () => {
  const navigate = useNavigate();
  const invoiceCreate = () => {
    navigate('/invoice_creation_upload_page');
  }
  const invoiceValidation = () => {
    navigate('/validation_page');
  }
  const invoiceSending = () => {
    navigate('/sending_page');
  }

  const buttonStyle = {
    width: '13vw',
    height: '20vw',
    fontSize: '2vw',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    textTransform: 'none',
  };

  const iconStyle = {
    fontSize: '10vw',
  };

  return (
    <>
      <Box sx={{
        backgroundImage: 'linear-gradient(to right, #3ab5b0 0%, #3d99be 31%, #56317a 100%)',
        p: 2,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        width: '100vw',
        height: '100vh',
        overflow: 'scroll'
        }}>
        <Typography variant="h2" gutterBottom sx={{ fontSize: '5vw', color: 'white', fontFamily: 'Helvetica', fontWeight: '600' }}>
          FUNCTION SELECTION
        </Typography>
        <Box sx={{ display: 'flex', gap: '20px', marginTop: '20px' }}>
          <Button
            variant="contained"
            color="primary"
            sx={buttonStyle}
            onClick={invoiceCreate}
          >
            Create UBL File
            <AppRegistrationIcon sx={iconStyle} />
          </Button>
          <Button
            variant="contained"
            color="secondary"
            sx={buttonStyle}
            onClick={invoiceValidation}
          >
            Validate UBL File
            <FactCheckIcon sx={iconStyle} />
          </Button>
          <Button
            variant="contained"
            color="success"
            sx={buttonStyle}
            onClick={invoiceSending}
          >
            Send Files
            <MarkAsUnreadIcon sx={iconStyle} />
          </Button>
        </Box>
      </Box>
    </>
  );
};

export default HomePage;
