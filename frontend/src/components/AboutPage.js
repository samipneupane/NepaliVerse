// components/AboutPage.js
import React from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "./SecondPage.css";

const AboutPage = () => {
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
        <h2>About this App</h2>
        <p>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor 
          incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis 
          nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
          Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore 
          eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt 
          in culpa qui officia deserunt mollit anim id est laborum.
        </p>
      </div>
    </div>
  );
};

export default AboutPage;