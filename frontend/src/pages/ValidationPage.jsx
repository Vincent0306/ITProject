import React, { useState, useContext } from 'react';
import { Box, Button, Typography, Checkbox, FormControlLabel, FormGroup, CircularProgress } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import AuthContext from '../Context';
import CloudUploadIcon from "@mui/icons-material/CloudUpload"; // Import the AuthContext

const ValidationPage = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [selectedRules, setSelectedRules] = useState([]);
  const [loading, setLoading] = React.useState(false);
  const navigate = useNavigate();
  const { token } = useContext(AuthContext); // Retrieve the token from the context

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
  };

  const handleRuleChange = (event) => {
    const value = event.target.value;
    setSelectedRules((prev) =>
      event.target.checked ? [...prev, value] : prev.filter((rule) => rule !== value)
    );
  };

  const handleValidate = async () => {
    if (!selectedFile || selectedRules.length === 0) {
      alert('Please select a file and validation rules.');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('rules', JSON.stringify(selectedRules));
    formData.append('user_token', token); // Include the token in the body
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/validate/', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const validationResult = await response.json();

      if (validationResult.successful === false) {
        navigate('/invalid_page', { state: { validationResult } });
      } else {
        navigate('/valid_page', { state: { validationResult } });
      }
    } catch (error) {
      console.error('Validation failed:', error);
    }finally {
      setLoading(false)
    }
  };

  return (
    <Box sx={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      height: '100vh',
      p: 2
    }}>
      <Typography variant="h4" sx={{ mb: 3, color: 'primary.main' }}>
        Please upload an XML file and select validation rules
      </Typography>
      <FormGroup sx={{ mb: 3 }}>
        <FormControlLabel
          control={<Checkbox value="AUNZ_PEPPOL_1_0_10" onChange={handleRuleChange} />}
          label="AUNZ_PEPPOL_1_0_10"
        />
        <FormControlLabel
          control={<Checkbox value="AUNZ_PEPPOL_SB_1_0_10" onChange={handleRuleChange} />}
          label="AUNZ_PEPPOL_SB_1_0_10"
        />
        <FormControlLabel
          control={<Checkbox value="AUNZ_UBL_1_0_10" onChange={handleRuleChange} />}
          label="AUNZ_UBL_1_0_10"
        />
      </FormGroup>
      <Box sx={{
        border: '2px dashed #ccc',
        width: '70%',
        height: '400px',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        mb: 3,
        position: 'relative'
      }}>
        <input
          type="file"
          onChange={handleFileChange}
          accept=".xml"
          style={{
            position: 'absolute',
            width: '100%',
            height: '100%',
            opacity: 0,
            cursor: 'pointer',
          }}
        />
        {selectedFile ? (
          <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <InsertDriveFileIcon sx={{ fontSize: 48, mb: 2 }} />
            <Typography variant="h6">{selectedFile.name}</Typography>
          </Box>
        ) : (
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
              <CloudUploadIcon sx={{ fontSize: 64, mb: 2, color: '#ccc' }} />
              <Typography variant="h6">
                Drag file here to upload
              </Typography>
            </Box>
        )}
      </Box>
      <Button variant="contained" sx={{ width: '300px', marginTop: '5px',backgroundColor:'#4caf50' }} onClick={handleValidate}>
        {loading ? <CircularProgress size={24} sx={{ color: 'white' }} /> : 'Validate'}
      </Button>
    </Box>
  );
};

export default ValidationPage;
