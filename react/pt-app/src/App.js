import React, { useRef } from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import './App.css';
import logo from './logo.svg';
import { useEffect } from 'react';
import Lessons from './Lessons';

import Landing from './pages/landing.jsx';

function Home({ buttonRef, handleMouseMove, handleMouseLeave }) {
  return (
    <>

    <Landing></Landing>
      {/* <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <div>
          <h1>FixurPostur</h1>
          <h4>The all-in-one PT aid.</h4>
          <p className="desc">Get real-time feedback on your form using your camera and AI. Follow a custom plan from your doctor or generate one instantly. Track progress, fix mistakes, and move better... smarter!</p>
        </div>
      </header>
      <div className="buttondiv">
        <Link
          className="button"
          to="/lessons"
        >
          Resume Lessons
        </Link>
      </div> */}
    </>
  );
}

function App() {

  useEffect(() => {
    const handleMouseMove = (e) => {
      const button = e.currentTarget;
      const rect = button.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;
      const y = (e.clientY - rect.top) / rect.height - 0.5;
      const angle = x < 0 ? -20 : 20;
      button.style.transform = `rotate3d(${y}, ${-x}, 0, ${angle}deg)`;
      button.style.filter = `drop-shadow(${x * 20}px ${y * 20}px 5px rgba(0,0,0,0.75))`;
      button.style.textShadow = `${x * 10}px ${y * 10}px 5px black`;
    };

    const handleMouseLeave = (e) => {
      const button = e.currentTarget;
      button.style.transform = 'rotate3d(0, 0, 0, 0deg)';
      button.style.filter = 'drop-shadow(0px 0px 5px transparent)';
      button.style.textShadow = '0px 0px 0px transparent';
    };

    const buttons = document.querySelectorAll('.button');
    buttons.forEach(btn => {
      btn.addEventListener('mousemove', handleMouseMove);
      btn.addEventListener('mouseleave', handleMouseLeave);
    });

    // Cleanup
    return () => {
      buttons.forEach(btn => {
        btn.removeEventListener('mousemove', handleMouseMove);
        btn.removeEventListener('mouseleave', handleMouseLeave);
      });
    };
  }, []);

  return (
    <div className="App">
      <Routes>
      <Route path="/" element={<Home />} />
        <Route path="/lessons" element={<Lessons />} />
      </Routes>
    </div>
  );
}

export default App;