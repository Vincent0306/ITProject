import React, { useContext } from 'react';
import { Button } from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import AuthContext from '../Context'; // Import the AuthContext

const InvalidPage = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const { validationResult } = location.state || {};

    // Extract validation_id from validationResult
    const validationId = validationResult && validationResult.validation_id;
    const report_name = validationResult && validationResult.original_file_name; 

    const { token } = useContext(AuthContext); // Retrieve the token from the context

    const handleDownload = async (format) => {
        if (!validationId) {
            console.error('No validation ID available.');
            return;
        }

        try {
            const response = await fetch('http://localhost:8000/api/download_report/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    report_format: format,
                    validation_id: validationId,
                    user_token: token, // Include the token in the body
                    original_file_name: report_name,
                }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(new Blob([blob]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `${report_name}_report.${format}`);
            document.body.appendChild(link);
            link.click();
            link.parentNode.removeChild(link);
        } catch (error) {
            console.error('Download failed:', error);
        }
    };

    const handleSendReport = (format) => {
        navigate('/sending_page', { state: { validationResult, format } });
    };

    const ExitButton = () => {
        navigate('/home_page');
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', textAlign: 'center', alignItems: 'center', justifyContent: 'center' }}>
            <p style={{ fontSize: '50px', fontWeight: 'bold', paddingTop: '15%' }}>Unfortunately! Your invoice is invalid!</p>
            <p style={{ fontSize: '20px', fontWeight: 'bold' }}>Check report in the following format</p>
            <div style={{ display: 'flex', flexDirection: 'row', textAlign: 'center', alignItems: 'center', justifyContent: 'center' }}>
                <Button variant="contained" sx={{ width: '200px', margin: '10px' }} onClick={() => handleDownload('json')}>
                    JSON
                </Button>
                <Button variant="contained" sx={{ width: '200px', margin: '10px' }} onClick={() => handleDownload('html')}>
                    HTML
                </Button>
                <Button variant="contained" sx={{ width: '200px', margin: '10px' }} onClick={() => handleDownload('pdf')}>
                    PDF
                </Button>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', textAlign: 'center', alignItems: 'center', justifyContent: 'center', marginTop: '30px' }}>
                <p style={{ fontSize: '20px', fontWeight: 'bold' }}>After you download the report, you can choose:</p>
                <Button variant="contained" sx={{ width: '300px', margin: '10px', backgroundColor:'#4caf50' }} onClick={() => handleSendReport('json')}>
                    Send report
                </Button>
            </div>
            <Button variant="contained" sx={{ width: '300px', marginTop: '5px', backgroundColor:'orangered' }} onClick={ExitButton}>
                Exit
            </Button>
        </div>
    );
};

export default InvalidPage;
