import React, { useState, useEffect, useRef } from 'react';
import exercises from './exercises.js';
import './Feedback.css';
import logo from './logo.svg';
import anshufreak from './anshufreak.mp4'
import VideoPopup from './components/VideoPopup.js';

function Feedback() {
  // Retrieve totalDuration from the video metadata
  const [totalDuration, setTotalDuration] = useState(0);
  const [scrubPos, setScrubPos] = useState(0);
  const [isDragging, setIsDragging] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [frameSrc, setFrameSrc] = useState('');
  const requestRef = useRef();
  const startTimeRef = useRef();
  const lastScrubPos = useRef(0);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  const mapRange = (a, b, c, d, e) => d + ((a - b) * (e - d)) / (c - b);

  const handleScrub = (e) => {
    const viewportWidth = window.innerWidth;
    let newPos = mapRange(e.clientX, viewportWidth * 0.1, viewportWidth * 0.9, 0, 1);
    newPos = Math.min(Math.max(newPos, 0), 1);
    setScrubPos(newPos);
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

  // Animate based on the video's totalDuration
  const animate = (timestamp) => {
    if (!startTimeRef.current) startTimeRef.current = timestamp;
    if (totalDuration > 0) {
      const elapsed = (timestamp - startTimeRef.current) / 1000;
      const progress = Math.min(lastScrubPos.current + elapsed / totalDuration, 1);
      setScrubPos(progress);
      if (progress < 1) {
        requestRef.current = requestAnimationFrame(animate);
      } else {
        setIsPlaying(false);
      }
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
  }, [isPlaying, totalDuration]);

  const togglePlay = () => {
    if (scrubPos === 1) setScrubPos(0);
    setIsPlaying((prev) => !prev);
  };

  // Arrow and Space controls use 1 second relative increments based on totalDuration
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

  // Set the video's current time based on scrubPos and totalDuration
  useEffect(() => {
    if (videoRef.current && totalDuration > 0) {
      videoRef.current.currentTime = scrubPos * totalDuration;
    }
  }, [scrubPos, totalDuration]);

  useEffect(() => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    if (video && canvas && totalDuration > 0) {
      video.currentTime = scrubPos * totalDuration;

      const drawFrame = () => {
        const ctx = canvas.getContext('2d');
        if (ctx) {
          ctx.clearRect(0, 0, canvas.width, canvas.height);
          ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
          setFrameSrc(canvas.toDataURL());
        }
      };

      if (video.readyState >= 2) {
        drawFrame();
      } else {
        const onCanPlay = () => {
          drawFrame();
          video.removeEventListener('canplay', onCanPlay);
        };
        video.addEventListener('canplay', onCanPlay);
      }
    }
  }, [scrubPos, totalDuration]);

  useEffect(() => {
    const video = videoRef.current;
    if (video) {
      // Set totalDuration from video metadata
      const handleLoadedMetadata = () => {
        setTotalDuration(video.duration);
      };
      video.addEventListener('loadedmetadata', handleLoadedMetadata);
      return () => {
        video.removeEventListener('loadedmetadata', handleLoadedMetadata);
      };
    }
  }, []);

  return (
    <div className="feedback">
      <div className="header">
        <p>Feedback</p>
      </div>
      <div className="mainContent">
        <div className="visualContent">
          {frameSrc && <img src={frameSrc} alt="Exercise Video Frame" />}
          <video ref={videoRef} src={anshufreak} style={{ display: 'none' }} />
          <canvas ref={canvasRef} width="640" height="360" style={{ display: 'none' }} />
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