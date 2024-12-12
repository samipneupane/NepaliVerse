import React, { useState, useRef } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import axios from "axios";
import "./SecondPage.css";

const SecondPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const mediaRecorder = useRef(null);
  const audioChunks = useRef([]);

  const [inputText, setInputText] = useState("");
  const [nepaliTranslation, setNepaliTranslation] = useState("");
  const [unicodeNepali, setUnicodeNepali] = useState("");
  const [audioFile, setAudioFile] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [similarityResult, setSimilarityResult] = useState(null);


  const handleConvertToNepali = async () => {
    // Clear previous results
    setNepaliTranslation("");
    setUnicodeNepali("");
    setAudioFile(""); // clear previous audio file
    setSimilarityResult(null);
    setError("");
    
    setLoading(true);
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
      
      // Convert base64 audio to a Blob
      const audioBlob = base64ToBlob(response.data.audio_file, 'audio/wav');
      const audioUrl = URL.createObjectURL(audioBlob);  // create a URL for the audio Blob
      setAudioFile(audioUrl); // set the audio URL in the state
      setError("");
    } catch (err) {
      const errorMessage = err.response?.data?.error || 
                          err.response?.data?.detail || 
                          err.response?.data?.input_text?.[0] ||
                          err.message;
      setError(`Error: ${errorMessage}`);
    } finally {
      setLoading(false);
    }
  };
  

  const base64ToBlob = (base64, type) => {
    const byteCharacters = atob(base64);  // Decode base64 string to bytes
    const byteArrays = [];
  
    for (let offset = 0; offset < byteCharacters.length; offset += 1024) {
      const slice = byteCharacters.slice(offset, offset + 1024);
      const byteNumbers = new Array(slice.length);
  
      for (let i = 0; i < slice.length; i++) {
        byteNumbers[i] = slice.charCodeAt(i);
      }
  
      const byteArray = new Uint8Array(byteNumbers);
      byteArrays.push(byteArray);
    }
  
    return new Blob(byteArrays, { type });
  };
  

  const convertToMonoWav = async (stereoBlob) => {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const arrayBuffer = await stereoBlob.arrayBuffer();
    const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
    
    // Create mono buffer
    const monoBuffer = audioContext.createBuffer(1, audioBuffer.length, audioBuffer.sampleRate);
    const monoChannel = monoBuffer.getChannelData(0);
    
    // If stereo, convert to mono by averaging channels
    if (audioBuffer.numberOfChannels === 2) {
      const leftChannel = audioBuffer.getChannelData(0);
      const rightChannel = audioBuffer.getChannelData(1);
      for (let i = 0; i < audioBuffer.length; i++) {
        monoChannel[i] = (leftChannel[i] + rightChannel[i]) / 2;
      }
    } else {
      // If already mono, just copy the data
      const channel = audioBuffer.getChannelData(0);
      monoChannel.set(channel);
    }

    // Convert to WAV
    const wavBuffer = new ArrayBuffer(44 + monoBuffer.length * 2);
    const view = new DataView(wavBuffer);

    // WAV Header
    const writeString = (view, offset, string) => {
      for (let i = 0; i < string.length; i++) {
        view.setUint8(offset + i, string.charCodeAt(i));
      }
    };

    writeString(view, 0, 'RIFF');
    view.setUint32(4, 36 + monoBuffer.length * 2, true);
    writeString(view, 8, 'WAVE');
    writeString(view, 12, 'fmt ');
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true); // PCM format
    view.setUint16(22, 1, true); // Mono
    view.setUint32(24, monoBuffer.sampleRate, true);
    view.setUint32(28, monoBuffer.sampleRate * 2, true);
    view.setUint16(32, 2, true);
    view.setUint16(34, 16, true);
    writeString(view, 36, 'data');
    view.setUint32(40, monoBuffer.length * 2, true);

    // Convert float32 to int16
    const floatTo16BitPCM = (output, offset, input) => {
      for (let i = 0; i < input.length; i++, offset += 2) {
        const s = Math.max(-1, Math.min(1, input[i]));
        output.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
      }
    };

    floatTo16BitPCM(view, 44, monoChannel);

    return new Blob([wavBuffer], { type: 'audio/wav' });
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          channelCount: 1, // Request mono audio if possible
          sampleRate: 44100 // Standard sample rate
        } 
      });
      mediaRecorder.current = new MediaRecorder(stream);
      audioChunks.current = [];

      mediaRecorder.current.ondataavailable = (event) => {
        audioChunks.current.push(event.data);
      };

      mediaRecorder.current.onstop = async () => {
        const audioBlob = new Blob(audioChunks.current, { type: 'audio/webm' });
        const monoWavBlob = await convertToMonoWav(audioBlob);
        await submitRecording(monoWavBlob);
      };

      mediaRecorder.current.start();
      setIsRecording(true);
      setError("");
    } catch (err) {
      setError("Error accessing microphone: " + err.message);
    }
  };

  const stopRecording = () => {
    if (mediaRecorder.current && mediaRecorder.current.state !== 'inactive') {
      mediaRecorder.current.stop();
      mediaRecorder.current.stream.getTracks().forEach(track => track.stop());
      setIsRecording(false);
    }
  };

  const submitRecording = async (audioBlob) => {
    if (!nepaliTranslation) {
      setError("Please convert text to Nepali first");
      return;
    }

    const formData = new FormData();
    formData.append('input_text', nepaliTranslation);
    formData.append('audio', audioBlob, 'recording.wav');

    try {
      setLoading(true);
      const response = await axios.post(
        "http://127.0.0.1:8000/core/similarity/",
        formData,
        {
          headers: {
            'Accept': 'application/json',
          }
        }
      );
      setSimilarityResult(response.data);
      setError("");
    } catch (err) {
      setError("Error submitting recording: " + err.message);
    } finally {
      setLoading(false);
    }
  };

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
        <textarea
          className="text-area"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Type here..."
        ></textarea>

        <button 
          className="action-button" 
          onClick={handleConvertToNepali} 
          disabled={loading}
        >
          {loading ? (
            <>
              Converting... <span className="spinner"></span>
            </>
          ) : (
            "Convert to Nepali"
          )}
        </button>

        {error && <p className="error-text">{error}</p>}

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

 
{audioFile && (
  <>
    <h3>Audio File:</h3>
    <audio controls>
      <source src={audioFile} type="audio/wav" />
      Your browser does not support the audio element.
    </audio>
  </>
)}


{unicodeNepali && (<>
  <p>Want to know how correct your pronunciation is?</p>
        <button 
          className={`record-button ${isRecording ? 'recording' : ''}`}
          onClick={isRecording ? stopRecording : startRecording}
          disabled={loading}
        >
          {isRecording ? "Stop Recording" : "Click here to record your voice"}
        </button>
</>)}

        {similarityResult && (
          <div className="similarity-results">
            <h3>Pronunciation Analysis:</h3>
            <p>Similarity Score: {similarityResult.similarity_score}%</p>
            <p>Category: {similarityResult.similarity_category}</p>
            {similarityResult.mispronounced_words.length > 0 && (
              <>
                <p>Mispronounced Words:</p>
                <ul>
                  {similarityResult.mispronounced_words.map((word, index) => (
                    <li key={index}>{word}</li>
                  ))}
                </ul>
              </>
            )}
            {similarityResult.word_error_rate !== null && (
              <p>Word Error Rate: {similarityResult.word_error_rate.toFixed(2)}</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default SecondPage;