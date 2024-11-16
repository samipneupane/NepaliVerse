// import React, { useEffect, useState } from 'react';
// import NepaliversePage from './components/NepaliVersePage';
// function App() {
//     const [message, setMessage] = useState('');

//     useEffect(() => {
//         fetch('http://127.0.0.1:8000/api/home/')
//             .then(response => response.json())
//             .then(data => setMessage(data.message))
//             .catch(error => console.error('Error:', error));
//     }, []);

//     return (
//         // <div>
//         //     <h1>Welcome to My React App</h1>
//         //     <p>Message from Backend: {message}</p>
//         // </div>
//         <NepaliversePage/>
//     );
// }

// export default App;




import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./components/HomePage";
import SecondPage from "./components/SecondPage";
import AboutPage from "./components/AboutPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/second" element={<SecondPage />} />
        <Route path="/about" element={<AboutPage />} />
      </Routes>
    </Router>
  );
}

export default App;
