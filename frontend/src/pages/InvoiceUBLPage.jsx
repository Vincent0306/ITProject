import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Button, Typography, Box, Grid, Paper } from '@mui/material';
import XMLViewer from 'react-xml-viewer';

const InvoiceUBLPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { ublContent, fileName} = location.state || {};

  const handleDownload = () => {
    const blob = new Blob([ublContent], { type: 'application/xml' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
  };

  const handleValidation = () => {
    navigate('/validation_page', { state: { ublContent, fileName } });
  };

  return (
    <Box sx={{ padding: '20px', backgroundColor: '#f0f4f8', minHeight: '100vh' }}>
      <Box mt={7} textAlign="center">
        <Typography variant="h5" gutterBottom sx={{ color: 'primary.main' }}>
          Generated UBL Content:
        </Typography>
        <Grid container justifyContent="center">
          <Grid item xs={12} sm={10} md={8} lg={8}>
            <Paper elevation={3} sx={{ padding: '20px', borderRadius: '8px' }}>
              <Box
                component="div"
                sx={{
                  width: '100%',
                  fontSize: '14px',
                  fontFamily: 'monospace',
                  textAlign: 'left',
                  padding: '10px',
                  border: '1px solid #ccc',
                  borderRadius: '4px',
                  maxHeight: '550px',
                  overflowY: 'auto',
                  backgroundColor: '#fff',
                }}
              >
                <XMLViewer xml={ublContent} />
              </Box>
            </Paper>
          </Grid>
        </Grid>
        <Box mt={4}>
          <Button
            variant="contained"
            color="primary"
            onClick={handleDownload}
            sx={{ marginRight: '20px', backgroundColor: '#4caf50', '&:hover': { backgroundColor: '#45a049' } }}
          >
            Download UBL File
          </Button>
          <Button
            variant="contained"
            color="primary"
            onClick={handleValidation}
            sx={{ marginRight: '20px', backgroundColor: '#4caf50', '&:hover': { backgroundColor: '#45a049' } }}
          >
            Validate UBL
          </Button>
        </Box>
      </Box>
    </Box>
  );
};

export default InvoiceUBLPage;
