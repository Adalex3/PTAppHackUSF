import React, { useState, useEffect, useRef } from 'react';
import exercises from './exercises.js';
import './Feedback.css';
import logo from './logo.svg';
import anshufreak from './anshufreak.mp4';
import VideoPopup from './components/VideoPopup.js';

function Feedback() {
  const [totalDuration, setTotalDuration] = useState(0);
  const [scrubPos, setScrubPos] = useState(0);
  const [isDragging, setIsDragging] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const videoRef = useRef(null);

  const mapRange = (a, b, c, d, e) => d + ((a - b) * (e - d)) / (c - b);

  const handleScrub = (e) => {
    const viewportWidth = window.innerWidth;
    let newPos = mapRange(e.clientX, viewportWidth * 0.1, viewportWidth * 0.9, 0, 1);
    newPos = Math.min(Math.max(newPos, 0), 1);
    setScrubPos(newPos);
    if (videoRef.current && totalDuration > 0) {
      videoRef.current.currentTime = newPos * totalDuration;
    }
  };

  const handleMouseDown = (e) => {
    if (e.clientX < window.innerWidth * 0.8) {
      setIsPlaying(false);
      setIsDragging(true);
      handleScrub(e);
    }
  };

  const handleMouseUp = () => setIsDragging(false);
  const handleMouseMove = (e) => isDragging && handleScrub(e);

  useEffect(() => {
    window.addEventListener('mouseup', handleMouseUp);
    window.addEventListener('mousemove', handleMouseMove);
    return () => {
      window.removeEventListener('mouseup', handleMouseUp);
      window.removeEventListener('mousemove', handleMouseMove);
    };
  }, [isDragging]);

  const togglePlay = () => {
    if (scrubPos === 1) setScrubPos(0);
    setIsPlaying((prev) => !prev);
  };

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.code === 'Space') {
        e.preventDefault();
        togglePlay();
      } else if (e.code === 'ArrowRight') {
        setIsPlaying(false);
        setScrubPos((pos) => {
          const increment = totalDuration > 0 ? 1 / totalDuration : 0;
          return Math.min(pos + increment, 1);
        });
      } else if (e.code === 'ArrowLeft') {
        setIsPlaying(false);
        setScrubPos((pos) => {
          const decrement = totalDuration > 0 ? 1 / totalDuration : 0;
          return Math.max(pos - decrement, 0);
        });
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [scrubPos, totalDuration]);

  useEffect(() => {
    if (!isDragging && videoRef.current && totalDuration > 0 && !isPlaying) {
      videoRef.current.currentTime = scrubPos * totalDuration;
    }
  }, [scrubPos, totalDuration, isDragging]);

  useEffect(() => {
    const video = videoRef.current;
    if (video) {
      const handleLoadedMetadata = () => {
        console.log("HERE!!!");
        setTotalDuration(video.duration);
      };
      video.addEventListener('loadedmetadata', handleLoadedMetadata);
      return () => {
        video.removeEventListener('loadedmetadata', handleLoadedMetadata);
      };
    }
  }, []);

  useEffect(() => {
    const video = videoRef.current;
    if (video) {
      if (isPlaying) {
        video.play();
      } else {
        video.pause();
      }
    }
  }, [isPlaying]);

  useEffect(() => {
    const video = videoRef.current;
    if (video && totalDuration > 0) {
      const handleTimeUpdate = () => {
        if (!isDragging) {
          setScrubPos(video.currentTime / totalDuration);
        }
      };
      video.addEventListener('timeupdate', handleTimeUpdate);
      return () => video.removeEventListener('timeupdate', handleTimeUpdate);
    }
  }, [totalDuration, isDragging]);

  return (
    <div className="feedback">
      <div className="header">
        <p>Feedback</p>
      </div>
      <div className="mainContent">
        <div className="visualContent">
          <video ref={videoRef} src={anshufreak} />
          <VideoPopup arrowPercent={{ x: 0.5, y: 0.4 }} bubbleText="More information here" />
        </div>
        <div className="scrubHolder">
          <div className="scrub" onMouseDown={handleMouseDown}>
            <div className="baseLine"></div>
            <div className="watchedLine" style={{ width: `calc(80vw * ${scrubPos})` }}></div>
            <button className="playPause" onClick={togglePlay}>
              {isPlaying ? 'Pause' : 'Play'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Feedback;