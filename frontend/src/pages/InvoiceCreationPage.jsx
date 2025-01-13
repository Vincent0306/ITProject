import React, { useState, useContext } from 'react';
import { Box, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import { Button } from 'antd';
import 'antd/dist/antd.css';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import AuthContext from '../Context'; // Import the AuthContext

const InvoiceCreationPage = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { token } = useContext(AuthContext);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert('Please select a file first!');
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append('json_file', selectedFile);
    formData.append('user_token', token);

    try {
      const response = await fetch('http://localhost:8000/api/ubl/upload/', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const responseData = await response.json();
      console.log(responseData.xml_file_name); 
      navigate('/invoice_detail_page', { 
        state: { 
          xmlData: responseData.details, 
          validationResult: responseData.validation_result,
          fileName: responseData.xml_file_name,
        } 
      });
    } catch (error) {
      alert('Only accept files in PDF or JSON format.')
      console.error('Error uploading file:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      height: '100vh',
      p: 2,
      backgroundColor: '#f5f5f5',
      backgroundImage: 'url(https://www.example.com/background.jpg)',
      backgroundSize: 'cover',
      backgroundPosition: 'center',
    }}>
      <Typography variant="h4" sx={{ mb: 3, color: 'primary.main' }}>
        Please upload a PDF or JSON file
      </Typography>
      <Box sx={{
        border: '2px dashed #ccc',
        borderRadius: '10px',
        width: '70%',
        height: '400px',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        mb: 3,
        position: 'relative',
        backgroundColor: '#fff',
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
        transition: 'transform 0.3s',
        '&:hover': {
          transform: 'scale(1.02)',
        },
      }}>
        <input
          type="file"
          onChange={handleFileChange}
          accept=".json,.pdf"
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
            <InsertDriveFileIcon sx={{ fontSize: 48, mb: 2, color: 'primary.main' }} />
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
      <Button 
        type="primary" 
        loading={loading} 
        style={{ 
          width: '300px', 
          marginTop: '5px', 
          backgroundColor: '#4caf50', 
          borderColor: '#4caf50',
          borderRadius: '8px',
        }} 
        onClick={handleUpload}>
        Upload
      </Button>
    </Box>
  );
};

export default InvoiceCreationPage;
