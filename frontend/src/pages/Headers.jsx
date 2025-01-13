import React, { useContext, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import LogoutIcon from '@mui/icons-material/Logout';
import EPPLogo from './img/epp_logo.png';
import { Tooltip } from 'antd';
import Context from '../Context.js';
import './css/Headers.css';

const Headers = () => {
  const [expanded, setExpanded] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const { removeToken } = useContext(Context);

  const navigateHomePage = () => {
    navigate('/home_page');
  };

  const Logout = () => {
    removeToken();
    navigate('/welcome_page');
  };

  const InvoiceCreation = () => {
    navigate('/invoice_creation_upload_page');
  };

  const toggleExpand = () => {
    setExpanded(!expanded);
  };

  const getButtonClassName = (paths) => {
    return paths.includes(location.pathname) ? 'custom-button hover' : 'custom-button';
  };

  const InvoiceValidation=()=>{
    navigate('/validation_page');
  }

  const SendingFiles=()=>{
    navigate('/sending_page');
  }

  return (
    <div className={`app-bar ${expanded ? 'expanded' : 'collapsed'}`}>
      <Toolbar style={{ boxShadow: '0', paddingLeft: '0' }}>
        <button onClick={toggleExpand} style={{ padding: 0, backgroundColor: 'transparent', border: 0 }}>
          <img src={EPPLogo} alt="EPP Logo" className="logo" />
        </button>
        {expanded && (
          <>
            <div className="center-buttons">
              <button className={getButtonClassName('/home_page')} onClick={navigateHomePage}>HOME PAGE</button>
              <div className="divider"></div>
              <button className={getButtonClassName(['/invoice_creation_upload_page', '/invoice_detail_page', '/invoice_UBL_page'])} onClick={InvoiceCreation}>INVOICE CREATION</button>
              <div className="divider"></div>
              <button className={getButtonClassName(['/validation_page', '/valid_page', '/invalid_page'])} onClick={InvoiceValidation}>INVOICE VALIDATION</button>
              <div className="divider"></div>
              <button className={getButtonClassName(['/sending_page', '/send_information','/report_information','/send_invoice'])} onClick={SendingFiles}>SENDING FILE</button>
            </div>
            <Tooltip title="Log out">
              <IconButton color="inherit" onClick={Logout} style={{ marginLeft: 'auto' }}>
                <LogoutIcon />
              </IconButton>
            </Tooltip>
          </>
        )}
      </Toolbar>
    </div>
    );
};

export default Headers;
