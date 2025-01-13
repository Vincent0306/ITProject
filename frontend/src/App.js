import React, { useContext, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation, useNavigate } from 'react-router-dom';
import WelcomePage from './pages/WelcomePage';
import HomePage from './pages/HomePage';
import Headers from './pages/Headers';
import InvoiceCreationPage from './pages/InvoiceCreationPage';
import Login from './pages/LoginPage';
import Register from './pages/RegisterPage';
import Validation from './pages/ValidationPage';
import Sending from './pages/SendFile';
import Valid from './pages/ValidPage';
import Invalid from './pages/InvalidPage';
import SendInformation from "./pages/SendInformation";
import SendInvoice from "./pages/SendInvoice";
import ReportInformation from "./pages/ReportInformation";
import AuthContext, { AuthProvider } from './Context';
import { message } from 'antd';
import InvoiceDetailPage from './pages/InvoiceDetailPage.jsx';
import InvoiceUBLPage from './pages/InvoiceUBLPage.jsx';

function AppContent() {
  const { saveToken } = useContext(AuthContext);
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    if (storedToken) {
      saveToken(storedToken);
    }

    if (!storedToken && location.pathname !== '/login_page' && location.pathname !== '/register_page' && location.pathname !== '/welcome_page') {
      navigate('/welcome_page');
      message.warning('Please login first');
    }
    else if (storedToken) {
      if (location.pathname === '/login_page' || location.pathname === '/register_page' || location.pathname === '/welcome_page') {
        navigate('/home_page');
      }
    }
  }, [location, saveToken, navigate]);

  const showHeader = location.pathname !== '/login_page' && location.pathname !== '/register_page' && location.pathname !== '/welcome_page';

  return (
    <>
      {showHeader && <Headers />}
      <Routes>
        <Route path="/welcome_page" element={<WelcomePage />}></Route>
        <Route path="/" element={<Navigate to="/welcome_page" />}></Route>
        <Route path="/login_page" element={<Login />}></Route>
        <Route path="/register_page" element={<Register />}></Route>
        <Route path="*" element={<Navigate to="/welcome_page" />}></Route>
        <Route path="/home_page" element={<HomePage />}></Route>
        <Route path='/invoice_creation_upload_page' element={<InvoiceCreationPage/>}></Route>
        <Route path='/invoice_detail_page' element={<InvoiceDetailPage/>}></Route>
        <Route path='/invoice_UBL_page' element={<InvoiceUBLPage/>}></Route>
        <Route path="/validation_page" element={<Validation />}></Route>
        <Route path="/sending_page" element={<Sending />}></Route>
        <Route path="/valid_page" element={<Valid />}></Route>
        <Route path="/invalid_page" element={<Invalid />}></Route>
        <Route path="/send_information" element={<SendInformation />}></Route>
        <Route path="/send_invoice" element={<SendInvoice />}></Route>
        <Route path="/report_information" element={<ReportInformation />}></Route>
      </Routes>
    </>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <AppContent />
      </Router>
    </AuthProvider>
  );
}

export default App;
