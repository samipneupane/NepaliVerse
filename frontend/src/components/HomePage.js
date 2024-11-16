import React from "react";
import { useNavigate } from "react-router-dom";
import "./HomePage.css";

const HomePage = () => {
  const navigate = useNavigate();

  const handleGetStarted = () => {
    navigate("/second");
  };

  return (
    <div className="home-page">
      <div className="text-section">
        <h1 className="app-title">NEPALIVERSE</h1>
        <h2 className="app-subtitle">
          Translate, convert, and Pronounce Nepali effortlessly with advanced
          speech and text tools.
        </h2>
        <p className="app-description">
          Introducing our cutting-edge language and speech processing app
          designed to bridge the gap between English and Nepali. Whether you're
          looking to translate English to Nepali with precision, convert Preeti
          font text into Unicode, or hear natural Nepali speech, our app has
          you covered. With powerful features like Neural Machine Translation,
          Text-to-Speech conversion, and Speech Similarity Evaluation, we
          provide an immersive experience that enhances language learning,
          accessibility, and communication. Transform your language tasks
          effortlessly and achieve accurate, natural-sounding results every
          time!
        </p>
        <button className="get-started-button" onClick={handleGetStarted}>
          GET STARTED →
        </button>
      </div>
      <div className="image-section">
        <img
          src="images/homepageImg.png" // Replace with your actual image path
          alt="Chatbot Illustration"
          className="home-image"
        />
      </div>
    </div>
  );
};

export default HomePage;
