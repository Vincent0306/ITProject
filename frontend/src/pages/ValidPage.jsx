import React from 'react';
import { Button } from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';

const ValidPage = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const { validationResult } = location.state || {}; // Get the state passed from ValidationPage

    const Exit_button = () => {
        navigate('/home_page');
    };

    const SendUBL = () => {
        navigate('/send_invoice', { state: { validationResult } }); // Pass the validationResult state to SendInvoice
    };

    return (
        <div style={{display:'flex', flexDirection:'column', textAlign:'center', alignItems:'center', justifyContent:'center'}}>
            <p style={{fontSize:'50px', fontWeight:'bold',paddingTop:'15%'}}>Congratulations! Your invoice is valid!</p>
            <Button variant="contained" sx={{ width: '300px', marginTop: '10px', backgroundColor:'#4caf50' }} onClick={SendUBL}>
                Send UBL
            </Button>
            <Button variant="contained" sx={{ width: '300px', marginTop: '10px',backgroundColor:'orangered' }} onClick={Exit_button}>
                Exit
            </Button>
        </div>
    );
};

export default ValidPage;
