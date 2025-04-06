import React, { useState, useEffect, useRef } from 'react';
import exercises from './exercises.js'; // Import the exercise objects
import './Feedback.css';
import logo from './logo.svg';
import VideoPopup from './components/VideoPopup.js';

function Feedback() {

    // TO BE CHANGED LATER
    const totalSeconds = 60;
    const [scrubPos, setScrubPos] = useState(0);
    const [isDragging, setIsDragging] = useState(false);
    const [isPlaying, setIsPlaying] = useState(false);
    const requestRef = useRef();
    const startTimeRef = useRef();
    const lastScrubPos = useRef(0);

    const mapRange = (a, b, c, d, e) => {
        return d + ((a - b) * (e - d)) / (c - b);
    }
  
    const handleScrub = (e) => {
        let viewportWidth = window.innerWidth;
      let newPos = mapRange(e.clientX, viewportWidth*0.1,viewportWidth*0.9,0,1);
      newPos = Math.min(Math.max(newPos, 0), 1); // clamp between 0 and 1

      setScrubPos(newPos);
    };
  
    const handleMouseDown = (e) => {
      if(e.clientX < window.innerWidth*0.8) {
        setIsPlaying(false);
        setIsDragging(true);
        handleScrub(e);
      }
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

    const animate = (timestamp) => {
        if (!startTimeRef.current) startTimeRef.current = timestamp;
        const elapsed = (timestamp - startTimeRef.current) / 1000;
        const progress = Math.min(lastScrubPos.current + elapsed / totalSeconds, 1);
        setScrubPos(progress);
        if (progress < 1) {
          requestRef.current = requestAnimationFrame(animate);
        } else {
          setIsPlaying(false);
        }
      };
    
      useEffect(() => {
        if (isPlaying) {
          startTimeRef.current = null;
          lastScrubPos.current = scrubPos;
          requestRef.current = requestAnimationFrame(animate);
        } else {
          cancelAnimationFrame(requestRef.current);
        }
        return () => cancelAnimationFrame(requestRef.current);
      }, [isPlaying]);
    
      const togglePlay = () => {
        if(scrubPos == 1) {
            setScrubPos(0);
        }
        setIsPlaying((prev) => !prev)
      };

      // SPACEBAR and ARROW
      useEffect(() => {
        const handleKeyDown = (e) => {
          if (e.code === 'Space') {
            e.preventDefault();
            togglePlay();
          } else if (e.code === 'ArrowRight') {
            setIsPlaying(false);
            setScrubPos((pos) => Math.min(pos + 1 / totalSeconds, 1));
          } else if (e.code === 'ArrowLeft') {
            setIsPlaying(false);
            setScrubPos((pos) => Math.max(pos - 1 / totalSeconds, 0));
          }
        };
      
        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
      }, [scrubPos]);

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
            <button className="playPause" onClick={togglePlay}>{isPlaying ? 'Pause' : 'Play'}</button>
        </div>
      </div>
      </div>
    </div>
  );
}

export default Feedback;