import React, { useState, useEffect, useRef } from 'react';
import exercises from './exercises.js';
import './Feedback.css';
import logo from './logo.svg';
import VideoPopup from './components/VideoPopup.js';

function Feedback() {
  const [totalDuration, setTotalDuration] = useState(0);
  const [scrubPos, setScrubPos] = useState(0);
  const [isDragging, setIsDragging] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [issues, setIssues] = useState([]);
  const [conversionProgress, setConversionProgress] = useState(0);
  const [videoSrc, setVideoSrc] = useState(null);
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

  useEffect(() => {
    fetch('http://127.0.0.1:5001/squat_json')
      .then(res => res.json())
      .then(data => setIssues(data.issues))
      .catch(err => console.error('Failed to load issues:', err));
  }, []);

  const currentFrame = Math.floor(scrubPos * 192);
  const activeIssues = issues.reduce((acc, issue) => {
    if (currentFrame >= issue.startFrame && currentFrame < issue.startFrame + issue.frameCount) {
      const posIndex = currentFrame - issue.startFrame;
      if (issue.positions && posIndex < issue.positions.length) {
        acc.push({ ...issue, currentPosition: issue.positions[posIndex] });
      }
    }
    return acc;
  }, []);

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch('http://127.0.0.1:5001/recording_progress');
        const data = await res.json();
        // Use data.progress to update your loading indicator
        setConversionProgress(data.progress);
        console.log("PROGRESS: " + data.progress)
      } catch (error) {
        console.error("Error fetching progress:", error);
      }
    }, 10);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (conversionProgress === 100) {
      setVideoSrc('http://127.0.0.1:5001/recording?v=' + Date.now());
    }
  }, [conversionProgress]);

  return (
    <div className="feedback">
      <div className="header">
        <p>Feedback</p>
      </div>
      <div className="mainContent">
        <div className={`visualContent ${conversionProgress == 100 ? '' : 'hidden'}`}>
          <video ref={videoRef} src={videoSrc} />
          {activeIssues.map(issue => (
            <VideoPopup
              key={issue.id}
              arrowPercent={{ x: issue.currentPosition[0], y: issue.currentPosition[1] }}
              bubbleText={issue.description}
            />
          ))}
          {/* <VideoPopup arrowPercent={{x: 0.5, y: 1.0}} bubbleText="HELLO TEHRE!"></VideoPopup> */}
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