import { useNavigate } from 'react-router-dom';
import { Button } from 'antd';
import 'antd/dist/antd.min.css';
import './animation/globalAnimation.css';
import '../index.css';
import { FormOutlined, AuditOutlined } from '@ant-design/icons';

function WelcomePage() {
  const navigate = useNavigate();
  const handleSignIn = () => {
    navigate('/login_page');
  };

  const handleSignUp = () => {
    navigate('/register_page');
  };

  const text = "Welcome to E-invoice Processing Platform";
  const words = text.split(" ");

  return (
    <div 
      style={{
        backgroundImage: 'linear-gradient(to right, #3ab5b0 0%, #3d99be 31%, #56317a 100%)',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        width: '100vw',
        height: '100vh',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        textAlign: 'center',
        color: 'white',
      }}>
      <h1 style={{ fontSize: '50px', color: 'white', fontFamily: 'Times New Roman, serif', fontStyle: 'italic' }}>
        {words.map((word, index) => (
          <span key={index} className="fadeInWord" style={{ animationDelay: `${index * 0.15}s` }}>
            {word}&nbsp;
          </span>
        ))}
      </h1>
      <div className="button-container" style={{ width: '30%',  display: 'flex',justifyContent: 'center', marginTop: '20px', opacity: 0, animation: 'buttonFadeIn 1s forwards', animationDelay: `${words.length * 0.3}s` }}>
        <Button  className="green-button large-button" icon={<FormOutlined />} shape="round" type="primary" onClick={handleSignIn}>
          Login
        </Button>
        <Button className="large-button" icon={<AuditOutlined />} shape="round" type="primary" onClick={handleSignUp}>
          Register
        </Button>
      </div>
    </div>
  );
}

export default WelcomePage;
