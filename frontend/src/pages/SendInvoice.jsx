import React, { useContext } from 'react';
import { useLocation, useNavigate } from "react-router-dom";
import { Form, Input, message, Button } from "antd";
import { Box, Typography } from "@mui/material";
import AuthContext from '../Context'; // Import AuthContext to get the token

const SendInvoice = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const { validationResult } = location.state || {};
    const { token } = useContext(AuthContext); // Retrieve the token from the context
    const [email, setEmail] = React.useState('');
    const [loading, setLoading] = React.useState(false);

    const validationId = validationResult && validationResult.validation_id;

    const Exit_button = () => {
        navigate('/home_page');
    };

    const handleSubmit = async () => {
        if ( !email) {
            alert('Please enter an email address.');
            return;
        }
        setLoading(true);
        try {
            const response = await fetch('http://localhost:8000/api/handle_xml_file_path_email/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: email,
                    validation_id: validationId,
                    user_token: token,
                })
            });

            const result = await response.json();

            if (response.ok) {
                message.success(result.message);
                navigate('/send_information');
            } else {
                message.error(result.error || 'An error occurred');
            }
        } catch (error) {
            console.error('Error:', error);
            message.error('An error occurred while sending the file');
        }finally {
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
            <Typography variant="h4" sx={{mb: 3, color: 'primary.main'}}>
                Please input the email
            </Typography>
            <Form
                name="basic"
                labelCol={{span: 10}}
                wrapperCol={{span: 14}}
                style={{width: '400px', marginBottom: '20px'}}
                initialValues={{remember: true}}
                onFinish={handleSubmit}
                onFinishFailed={(errorInfo) => console.log('Failed:', errorInfo)}
                autoComplete="off"
            >
                <Form.Item
                    label="Email"
                    name="email"
                    rules={[
                        {
                            type: 'email',
                            message: 'E-mail format is not valid!',
                        },
                        {
                            required: true,
                            message: 'Please input your Email!',
                        },
                    ]}
                >
                    <Input value={email} onChange={(e) => setEmail(e.target.value)}
                           placeholder="Please input the email"/>
                </Form.Item>
            </Form>
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
                onClick={handleSubmit}
            >
                Send
            </Button>
            <Button
                type="primary"
                style={{
                    width: '300px',
                    marginTop: '5px',
                    backgroundColor: 'orangered',
                    borderColor: '#orangered',
                    borderRadius: '8px',
                }}
                onClick={Exit_button}
            >
                Exit
            </Button>

        </Box>
    );
};

export default SendInvoice;
