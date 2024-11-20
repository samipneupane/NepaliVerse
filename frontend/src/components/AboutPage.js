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
        <h2 className="about-title">About This App</h2>
        <p>
          <strong>Welcome to our English-to-Nepali Translation and Pronunciation Analysis App!</strong>
        </p>
        <p>
          This innovative platform bridges the gap between languages by enabling you to 
          convert English text into accurate Nepali translations effortlessly. Whether 
          you're learning Nepali or need quick translations for communication, this app 
          is designed to be your reliable language companion.
        </p>
        <h3>Key Features:</h3>
        <ul>
          <li><strong>Instant Translation:</strong> Type or paste any English text into the app, and get precise Nepali translations within seconds. Alongside the translated text, you'll receive its Unicode representation, ensuring compatibility across all platforms and devices.</li>
          <li><strong>Pronunciation Analysis:</strong> Once your text is translated into Nepali, the app takes it a step further by helping you perfect your pronunciation. Record your voice, and the app will analyze how well you pronounce the Nepali text, providing:
            <ul>
              <li>Similarity Scores to gauge accuracy.</li>
              <li>Feedback on mispronounced words to improve specific areas.</li>
              <li>Insights like word error rates for detailed evaluation.</li>
            </ul>
          </li>
          <li><strong>Audio Playback:</strong> Listen to an audio version of the translated Nepali text to understand the correct pronunciation before you start practicing.</li>
        </ul>
        <h3>Who Is It For?</h3>
        <ul>
          <li><strong>Learners:</strong> Ideal for individuals trying to master Nepali, this app ensures both language understanding and spoken fluency.</li>
          <li><strong>Professionals:</strong> Great for professionals needing quick and accurate translations.</li>
          <li><strong>Educators and Students:</strong> A perfect tool for teaching or learning Nepali language basics.</li>
        </ul>
        <h3>Why Choose Us?</h3>
        <p>
          Our app doesn’t just stop at translation—it empowers you to speak Nepali confidently. 
          The focus on a single direction (English to Nepali) ensures unparalleled accuracy 
          and simplicity, catering to users who want a fast and straightforward solution 
          without distractions.
        </p>
        <p>
          Join us on this journey of breaking language barriers and promoting meaningful 
          communication through technology!
        </p>
      </div>
    </div>
  );
};

export default AboutPage;
