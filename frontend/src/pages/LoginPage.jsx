import React from 'react';
import { Button, Form, Input, message, Tooltip } from 'antd';
import { AuditOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import LoginIcon from '@mui/icons-material/Login';
import MuiButton from '@mui/material/Button';
import '../index.css';
import Context from '../Context.js';
import EPPLogo from './img/epp_logo.png';
import { hashProcess } from '../hash.js';

function Login() {
    const { saveToken } = React.useContext(Context);
    const navigate = useNavigate();

    function Register() {
        navigate('/register_page');
        console.log('Register');
    }

    const onFinish = async (values) => {
        await getFetch(values.email, values.password);
    };

    const onFinishFailed = (errorInfo) => {
        console.log('Failed:', errorInfo);
        message.error('Please check the form fields and try again.');
    };

    async function getFetch(email, password) {
        try {
            const hashedPassword = await hashProcess(password);
            console.log('Password:', password);
            const response = await fetch('http://localhost:8000/api/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                },
                body: JSON.stringify({ email: email, password: hashedPassword })
            });

            const data = await response.json();
            console.log('Received data:', data);

            if (data.error) {
                alert(data.error);
            } else {
                console.log('Token:', data.token);
                saveToken(data.token);
                message.success('Login successfully!');
                navigate('/home_page');
            }
        } catch (error) {
            console.error('Fetch error:', error);
            alert('There was a problem with the login request. Please try again later.');
        }
    }

    return (
        <div style={{
            backgroundImage: 'linear-gradient(to right, #3ab5b0 0%, #3d99be 31%, #56317a 100%)',
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            height: '100vh',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            textAlign: 'center',
            color: 'white'
        }}>
            <div style={{
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'flex-start',
                alignItems: 'center',
                backgroundColor: 'white',
                borderRadius: '20px',
                boxShadow: '10px 10px 20px rgba(0, 0, 0, 0.2), 5px 5px 15px rgba(0, 0, 0, 0.1)',
                padding: '30px',
                maxWidth: '400px',
                width: '100%',
                textAlign: 'left',
                border: '1px solid #e0e0e0',
                background: '#fff',
            }}>
                <img src={EPPLogo} alt="EPP Logo" style={{ width: '150px', marginBottom: '30px', marginLeft: '8%' }} />
                <Form
                    name="basic"
                    labelCol={{
                        span: 8,
                    }}
                    wrapperCol={{
                        span: 16,
                    }}
                    style={{
                        width: '100%',
                        margin: 0
                    }}
                    initialValues={{
                        remember: true,
                    }}
                    onFinish={onFinish}
                    onFinishFailed={onFinishFailed}
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
                        <Input />
                    </Form.Item>
                    <Form.Item
                        label="Password"
                        name="password"
                        rules={[
                            {
                                required: true,
                                message: 'Please input your password!',
                            },
                        ]}
                    >
                        <Input.Password />
                    </Form.Item>
                    <Form.Item
                        wrapperCol={{
                            offset: 8,
                            span: 16,
                        }}
                    >
                        <div style={{ display: 'flex', flexDirection: 'row', textAlign: 'center' }}>
                            <MuiButton
                                className='green-button'
                                variant="contained"
                                style={{
                                    marginRight: 50,
                                    flex: 1,
                                }}
                                endIcon={<LoginIcon />}
                                type="submit"
                            >
                                Login
                            </MuiButton>
                            <Tooltip title="To Register">
                                <Button
                                    type="primary"
                                    shape="circle"
                                    icon={<AuditOutlined />}
                                    onClick={Register}
                                    style={{ marginLeft: 'auto' }}
                                />
                            </Tooltip>
                        </div>
                    </Form.Item>
                </Form>
            </div>
        </div>
    );
}

export default Login;
