import React, { useState, useEffect } from 'react';
import exercises from './exercises.js'; // Import the exercise objects
import './Feedback.css';
import logo from './logo.svg';
import VideoPopup from './components/VideoPopup.js';

function Feedback() {

    // TO BE CHANGED LATER
    const totalSeconds = 60;

    const mapRange = (a, b, c, d, e) => {
        return d + ((a - b) * (e - d)) / (c - b);
    };

    const [scrubPos, setScrubPos] = useState(0.7621);
    const [isDragging, setIsDragging] = useState(false);
  
    const handleScrub = (e) => {
        let viewportWidth = window.innerWidth;
      let newPos = mapRange(e.clientX, viewportWidth*0.1,viewportWidth*0.9,0,1);
      newPos = Math.min(Math.max(newPos, 0), 1); // clamp between 0 and 1

      setScrubPos(newPos);
    };
  
    const handleMouseDown = (e) => {
      setIsDragging(true);
      handleScrub(e);
    };
  
    const handleMouseUp = () => setIsDragging(false);
  
    const handleMouseMove = (e) => {
      if (isDragging) handleScrub(e);
    };
  
    useEffect(() => {
      window.addEventListener('mouseup', handleMouseUp);
      window.addEventListener('mousemove', handleMouseMove);
      return () => {
        window.removeEventListener('mouseup', handleMouseUp);
        window.removeEventListener('mousemove', handleMouseMove);
      };
    }, [isDragging]);

  return (
    <div className={`feedback`}>
      <div className='header'>
        <p>Feedback</p>
      </div>
      <div className='mainContent'>
      <div className='visualContent'>
        <img src="http://localhost:5001/video" alt="Exercise Video" />
        <VideoPopup arrowPercent={{ x: 0.5, y: 0.4}} bubbleText="More information here" />
      </div>
      <div className='scrubHolder'>
        <div className='scrub' onMouseDown={handleMouseDown}>
            <div className='baseLine'></div>
            <div className='watchedLine' style={{ width: `calc(80vw * ${scrubPos})` }}></div>
        </div>
      </div>
      </div>
    </div>
  );
}

export default Feedback;