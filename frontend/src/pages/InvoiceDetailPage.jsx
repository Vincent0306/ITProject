import React, { useState, useEffect, useContext  } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Card, CardContent, Grid, TextField, Button, Typography, IconButton, Dialog, DialogActions, DialogContent, DialogTitle, Box } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import AuthContext from '../Context';

const InvoiceDetailPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { xmlData, validationResult: initialValidationResult, fileName } = location.state || {};
  const [data, setData] = useState({});
  const [validationResult, setValidationResult] = useState({});
  const [open, setOpen] = useState(false);
  const [currentField, setCurrentField] = useState("");
  const [currentValue, setCurrentValue] = useState("");
  const { token } = useContext(AuthContext);

  useEffect(() => {
    if (xmlData) {
      console.log("Received XML Data:", xmlData);
      setData(xmlData);
      setValidationResult(initialValidationResult);
    }
  }, [xmlData, initialValidationResult]);

  const handleEditClick = (field) => {
    setCurrentField(field);
    setCurrentValue(data[field]);
    setOpen(true);
  };

  const handleSave = () => {
    setData({
      ...data,
      [currentField]: currentValue,
    });
    setValidationResult({
      ...validationResult,
      [currentField]: 1,
    });
    setOpen(false);
  };

  const handleConfirm = async () => {
    const payload = { updates: data, xml_file_name: fileName, user_token: token };
    console.log('Payload:', payload);
    try {
      const response = await fetch('http://localhost:8000/api/ubl/update-xml-and-convert/', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });
  
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const blob = await response.blob();
      const ublText = await blob.text();
      navigate('/invoice_UBL_page', { state: { ublContent: ublText, fileName} });
      
    } catch (error) {
      console.error('Error generating UBL file:', error);
    }
  };

  return (
    <Box sx={{
      padding: '20px',
      backgroundColor: '#f0f4f8',
      minHeight: '100vh'
    }}>
      <Typography variant="h5" align="center" sx={{ marginBottom: '20px', marginTop: '60px', color: 'primary.main' }}>
        Here are some information detected for your file. Please check and complete the form below.
      </Typography>
      <Grid container spacing={3} justifyContent="center">
        {Object.keys(data).map((key, index) => (
          data[key] && (
            key.startsWith('InvoiceLine_') ? (
              Object.keys(data[key]).map((subKey, subIndex) => (
                <Grid item xs={12} sm={10} md={8} lg={5} key={`${index}-${subIndex}`}>
                  <Card sx={{ boxShadow: 3, borderRadius: 2, position: 'relative' }}>
                    <CardContent>
                      <Typography variant="h6" sx={{ color: validationResult[key]?.[subKey] === 0 ? 'red' : 'inherit' }}>
                        {subKey.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}
                      </Typography>
                      <TextField
                        fullWidth
                        value={typeof data[key][subKey] === 'string' ? data[key][subKey] : JSON.stringify(data[key][subKey])}
                        margin="normal"
                        InputProps={{
                          readOnly: true,
                          style: {
                            color: validationResult[key]?.[subKey] === 0 ? 'red' : 'inherit',
                            backgroundColor: '#fff',
                            borderRadius: 1,
                            padding: '10px',
                            boxShadow: 'inset 0 1px 3px rgba(0,0,0,0.12)'
                          }
                        }}
                      />
                      <IconButton onClick={() => handleEditClick(`${key}.${subKey}`, data[key][subKey])} sx={{ position: 'absolute', top: '10px', right: '10px' }}>
                        <EditIcon />
                      </IconButton>
                    </CardContent>
                  </Card>
                </Grid>
              ))
            ) : (
              <Grid item xs={12} sm={10} md={8} lg={5} key={index}>
                <Card sx={{ boxShadow: 3, borderRadius: 2, position: 'relative' }}>
                  <CardContent>
                    <Typography variant="h6" sx={{ color: validationResult[key] === 0 ? 'red' : 'inherit' }}>
                      {key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}
                    </Typography>
                    <TextField
                      fullWidth
                      value={typeof data[key] === 'string' ? data[key] : JSON.stringify(data[key])}
                      margin="normal"
                      InputProps={{
                        readOnly: true,
                        style: {
                          color: validationResult[key] === 0 ? 'red' : 'inherit',
                          backgroundColor: '#fff',
                          borderRadius: 1,
                          padding: '10px',
                          boxShadow: 'inset 0 1px 3px rgba(0,0,0,0.12)'
                        }
                      }}
                    />
                    <IconButton onClick={() => handleEditClick(key, data[key])} sx={{ position: 'absolute', top: '10px', right: '10px' }}>
                      <EditIcon />
                    </IconButton>
                  </CardContent>
                </Card>
              </Grid>
            )
          )
        ))}
      </Grid>
      <Dialog open={open} onClose={() => setOpen(false)}>
        <DialogTitle>Edit {currentField.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            value={currentValue}
            onChange={(e) => setCurrentValue(e.target.value)}
            margin="normal"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button onClick={handleSave} color="primary">Save</Button>
        </DialogActions>
      </Dialog>
      <Button
        variant="contained"
        color="primary"
        sx={{
          marginTop: '20px',
          display: 'block',
          marginLeft: 'auto',
          marginRight: 'auto',
          backgroundColor: '#4caf50',
          '&:hover': {
            backgroundColor: '#45a049'
          }
        }}
        onClick={handleConfirm}
      >
        Confirm
      </Button>
    </Box>
  );
};

export default InvoiceDetailPage;
