import React from 'react';
import { Button } from '@mui/material';
import {useNavigate} from "react-router-dom";

const SendInformation = () => {
    const navigate = useNavigate();
    const Exit_button = () => {
        navigate('/home_page');
    }

    const SendAnotherInvoice = () => {
        navigate('/sending_page');
    }

    return (
        <div style={{
            display: 'flex',
            flexDirection: 'column',
            textAlign: 'center',
            alignItems: 'center',
            justifyContent: 'center'
        }}>
            <p style={{fontSize: '50px', fontWeight: 'bold', paddingTop: '15%'}}>Invoice Send Successfully!</p>
            <Button variant="contained" sx={{width: '300px', marginTop: '20px'}} onClick={Exit_button}>
                Exit
            </Button>
        </div>
    );
};

export default SendInformation;
