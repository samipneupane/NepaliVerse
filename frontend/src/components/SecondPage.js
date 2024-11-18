import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import axios from "axios";
import "./SecondPage.css";

const SecondPage = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const [inputText, setInputText] = useState("");
  const [nepaliTranslation, setNepaliTranslation] = useState("");
  const [unicodeNepali, setUnicodeNepali] = useState("");
  const [audioFile, setAudioFile] = useState("");
  const [error, setError] = useState("");


  const [loading, setLoading] = useState(false);

  console.log("input text: ", inputText);

  const handleConvertToNepali = async () => {
    setLoading(true); // Start loading
    try {
      const response = await axios.post("http://127.0.0.1:8000/core/translation/", 
        { input_text: inputText },
        {
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          }
        }
      );
      setNepaliTranslation(response.data.nepali_translation);
      setUnicodeNepali(response.data.unicode_nepali);
      setAudioFile(response.data.audio_file);
      setError("");
    } catch (err) {
      const errorMessage = err.response?.data?.error || 
                           err.response?.data?.detail || 
                           err.response?.data?.input_text?.[0] ||
                           err.message;
      setError(`Error: ${errorMessage}`);
    } finally {
      setLoading(false); // Stop loading
    }
  };

  
  return (
    <div className="second-container">
      {/* Sidebar */}
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

      {/* Main Content */}
      <div className="main-content">
        <h2>Enter Text in English</h2>
        <textarea
          className="text-area"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Type here..."
        ></textarea>

<button className="action-button" onClick={handleConvertToNepali} disabled={loading}>
  {loading ? (
    <>
      Converting... <span className="spinner"></span>
    </>
  ) : (
    "Convert to Nepali"
  )}
</button>

        {error && <p className="error-text">{error}</p>}

        {/* Nepali Translation */}
        {nepaliTranslation && (
          <>
            <h3>Nepali Translation:</h3>
            <textarea
              className="text-area"
              value={nepaliTranslation}
              readOnly
            ></textarea>
          </>
        )}

        {/* Unicode Nepali */}
        {unicodeNepali && (
          <>
            <h3>Unicode Nepali:</h3>
            <textarea
              className="text-area"
              value={unicodeNepali}
              readOnly
            ></textarea>
          </>
        )}

        {/* Audio File */}
        {audioFile && (
          <>
            <h3>Audio File:</h3>
            <a href={audioFile} target="_blank" rel="noreferrer">
              Listen to Pronunciation
            </a>
          </>
        )}

        <p>Want to know how correct your pronunciation is?</p>
        <button className="record-button">Click here to record your voice</button>
      </div>
    </div>
  );
};

export default SecondPage;
