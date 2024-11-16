// components/SecondPage.js
import React from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "./SecondPage.css";

const SecondPage = () => {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <div className="second-container">
      <div className="sidebar">
        <h2 
          className={`sidebar-title ${location.pathname === '/' ? 'active' : ''}`}
          onClick={() => navigate('/')}
        >
          Home
        </h2>
        <h2 
          className={`sidebar-title ${location.pathname === '/second' ? 'active' : ''}`}
          onClick={() => navigate('/second')}
        >
          Convert Text
        </h2>
        <h2 
          className={`sidebar-title ${location.pathname === '/about' ? 'active' : ''}`}
          onClick={() => navigate('/about')}
        >
          About this App
        </h2>
      </div>

      <div className="main-content">
        <h2>Enter Text in English</h2>
        <textarea className="text-area"></textarea>
        <button className="action-button">Convert to Nepali</button>
        <textarea className="text-area"></textarea>
        <button className="action-button">Get Unicode</button>
        <textarea className="text-area"></textarea>
        <p>Want to know how correct your pronunciation is?</p>
        <button className="record-button">Click here to record your voice</button>
      </div>
    </div>
  );
};

export default SecondPage;