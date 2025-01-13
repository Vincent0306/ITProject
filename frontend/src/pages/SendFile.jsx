import React from 'react';
import { Form, Input, Button, message } from 'antd';
// import { InboxOutlined } from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import {Box, Typography} from "@mui/material";
import InsertDriveFileIcon from "@mui/icons-material/InsertDriveFile";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";

const App = () => {
    const [email, setEmail] = React.useState('');
    const [fileList, setFileList] = React.useState([]);
    const [loading, setLoading] = React.useState(false);
    const navigate = useNavigate();
    // const onFinishFailed = (errorInfo) => {
    //     console.log('Failed:', errorInfo);
    // };

    const onFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            const allowedExtensions = ['.json', '.pdf', '.html', '.xml'];
            const fileExtension = file.name.slice(file.name.lastIndexOf('.')).toLowerCase();
            if (!allowedExtensions.includes(fileExtension)) {
                message.error('Unsupported file type. Only .json, .pdf, .html files are allowed!');
                return;
            }

            if (fileExtension === '.xml') {
                message.warning('Please go to the validation page to validate the invoice!');
                return
                // navigate('/validation_page');
            }
            setFileList([file]);
        }
    };

    const BacktoHome = () => {
        navigate('/home_page');
    };

    const handleSubmit = async () => {
        if (fileList.length === 0 || !email) {
            alert('Please select a file and enter an email address.');
            return;
        }

        const formData = new FormData();
        formData.append('file', fileList[0]);
        formData.append('email', email);
        setLoading(true);
        try {
            const response = await fetch('http://localhost:8000/api/send-file-email/', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (response.ok) {
                message.success(result.message);
                navigate('/report_information')
            } else {
                message.error(result.error || 'An error occurred');
            }
        } catch (error) {
            console.error('Error:', error);
            message.error('An error occurred while sending the file');
        } finally {
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
            p: 2,
            pt: 10,
            backgroundColor: '#f5f5f5',
            backgroundImage: 'url(https://www.example.com/background.jpg)',
            backgroundSize: 'cover',
            backgroundPosition: 'center',
        }}>
            <Typography variant="h4" sx={{mb: 3, color: 'primary.main'}}>
                Please input the email and upload the file
            </Typography>
            <Form
                name="basic"
                labelCol={{span: 10}}
                wrapperCol={{span: 14}}
                style={{ width: '90%', maxWidth: '400px', marginBottom: '20px' }}
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
                    onChange={onFileChange}
                    accept=".json,.pdf,.html,.xml"
                    style={{
                        position: 'absolute',
                        width: '100%',
                        height: '100%',
                        opacity: 0,
                        cursor: 'pointer',
                    }}
                />
                {fileList.length > 0 ? (
                    <Box sx={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
                        <InsertDriveFileIcon sx={{fontSize: 48, mb: 2, color: 'primary.main'}}/>
                        <Typography variant="h6">{fileList[0].name}</Typography>
                    </Box>
                ) : (
                    <Box sx={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
                        <CloudUploadIcon sx={{fontSize: 64, mb: 2, color: '#ccc'}}/>
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
                    borderColor: 'orangered',
                    borderRadius: '8px',
                }}
                onClick={BacktoHome}
            >
                Exit
            </Button>
        </Box>
    );
};

export default App;
