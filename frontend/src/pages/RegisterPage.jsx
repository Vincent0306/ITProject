import React, { useState } from 'react';
import { Button, Form, Input, message, Tooltip } from 'antd';
import { AuditOutlined } from '@ant-design/icons';
import EPPLogo from './img/epp_logo.png';
import MuiButton from '@mui/material/Button';
import { useNavigate } from 'react-router-dom';
import LoginIcon from '@mui/icons-material/Login';
import { hashProcess } from '../hash.js';

const PostRegister = () => {
    const [Email, setEmail] = useState('');
    const [Password, setPassword] = useState('');
    const navigate = useNavigate();

    const onFinish = async (values) => {
        await FetchRegister(values.email, values.password);
    };

    const onFinishFailed = (errorInfo) => {
        console.log('Failed:', errorInfo);
        message.error('Please check the form fields and try again.');
    };

    async function FetchRegister(email, password) {
        try {
            const hashedPassword = await hashProcess(password);
            const response = await fetch('http://localhost:8000/api/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                },
                body: JSON.stringify({ email: email, password: hashedPassword })
            });
            const data = await response.json();
            if (data.error) {
                message.error(data.error);
            } else {
                message.success('Register successfully!');
                navigate('/login_page');
            }
        } catch (error) {
            console.error('Fetch error:', error);
            message.error('There was a problem with the registration request. Please try again later.');
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
                        span: 10,
                    }}
                    wrapperCol={{
                        span: 14,
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
                        <Input value={Email} onChange={(e) => setEmail(e.target.value)} />
                    </Form.Item>

                    <Form.Item
                        name="password"
                        label="Password"
                        rules={[
                            {
                                required: true,
                                message: 'Please input your password!',
                            },
                        ]}
                        hasFeedback
                    >
                        <Input.Password value={Password} onChange={(e) => setPassword(e.target.value)} />
                    </Form.Item>
                    <Form.Item
                        name="confirm"
                        label="Confirm Password"
                        dependencies={['password']}
                        hasFeedback
                        rules={[
                            {
                                required: true,
                                message: 'Please confirm your password!',
                            },
                            ({ getFieldValue }) => ({
                                validator(_, value) {
                                    if (!value || getFieldValue('password') === value) {
                                        return Promise.resolve();
                                    }
                                    return Promise.reject(new Error('Passwords not match!'));
                                },
                            }),
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
                                className='blue-button'
                                variant="contained"
                                style={{
                                    marginRight: 50,
                                    flex: 1,
                                    color: 'white'
                                }}
                                endIcon={<AuditOutlined />}
                                type="submit"
                            >
                                Register
                            </MuiButton>
                            <Tooltip title="To Login">
                                <Button
                                    className='green-button'
                                    type="primary"
                                    shape="circle"
                                    icon={<LoginIcon />}
                                    onClick={() => navigate('/login_page')}
                                    style={{ marginLeft: 'auto' }}
                                />
                            </Tooltip>
                        </div>
                    </Form.Item>
                </Form>
            </div>
        </div>
    )
}

export default PostRegister;
