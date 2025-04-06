import React, { useState, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import exercises from './exercises.js'; // Import the exercise objects
import { Routes, Route, Link } from 'react-router-dom';
import './Lessons.css';
import logo from './logo.svg';
import VideoPopup from './components/VideoPopup.js';

function Lessons() {

  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const exerciseParameterIndex = params.get('exercise') ?? 0; // fallback to 0 if null
  const exerciseName = ["Slow Squats", "Hamstring Stretch", "Wrist Flexion"][exerciseParameterIndex];

  // Default header content before transitioning to any exercise
  const defaultTitle = "Let's begin!";
  const defaultDescription = "Here is some information about the exercise that you are doing";
  // const defaultImage = 'logo.svg'; // Fallback or initial image

  const [isButtonHidden, setIsButtonHidden] = useState(true);

  const [isUserInView, setIsUserInView] = useState(false);

  const [feedback, setFeedback] = useState(null);

  // State to track which exercise is currently active.
  // We start with -1 so that the first exercise is at index 0.
  const [exerciseIndex, setExerciseIndex] = useState(-1);

  // State for the current exercise's data. Initially, it uses the default content.
  const [currentExercise, setCurrentExercise] = useState({
    title: defaultTitle,
    shortDescription: defaultDescription,
    longDescription: defaultDescription,
    // image: defaultImage,
  });


  // State to control whether the header is in enlarged mode.
  const [isEnlarged, setIsEnlarged] = useState(false);

  // Function to transition to the next exercise.
  const showNextExercise = () => {
    setIsButtonHidden(true)
    const nextIndex = exerciseIndex + 1;
    if (nextIndex < exercises.length) {
      const nextExercise = exercises[nextIndex];
      setCurrentExercise(nextExercise);
      setExerciseIndex(nextIndex);
      // Enlarge header to show the long description.
      setIsEnlarged(true);
      // After 3 seconds, revert to normal mode (show short description).
      setTimeout(() => {
        setIsEnlarged(false);

        // show button after a few more seconds
        setTimeout(() => {
          setIsButtonHidden(false);
        },1000)
      }, 3000);
    }
  };

  // On component mount, trigger the first exercise and set an interval for subsequent transitions.
  useEffect(() => {

    fetch('http://127.0.0.1:5001/recording_start', { method: 'POST' })
    .then(res => res.json())
    .then(data => console.log("Recording started:", data))
    .catch(err => console.error("Error starting recording:", err));

    // Start with a brief delay before showing the first exercise.
    const initialTimeout = setTimeout(() => {
      showNextExercise();
    }, 100);

    // Automatically cycle through exercises every 10 seconds.
    // const interval = setInterval(() => {
    //   showNextExercise();
    // }, 10000);

    // const interval2 = setInterval(() => {
    //   fetch('http://127.0.0.1:5001/avg_pos')
    //     .then(res => res.json())
    //     .then(data => console.log(data))
    //     .catch(err => console.error(err));
    // }, 1000); // Adjust interval as needed

    // Cleanup timers on component unmount.
    return () => {
      clearTimeout(initialTimeout);
      // clearInterval(interval);
    };
  }, []); // Runs once on mount


  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch('http://127.0.0.1:5001/is_in_frame');
        const data = await res.json();
        if (data["in_frame"] != null) {
          setIsUserInView(data["in_frame"]);
        }
      } catch (err) {
        // Optional: log silently or not at all
        console.error('Fetch failed:', err);
      }
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch(`http://127.0.0.1:5001/pose_feedback?exercise=${encodeURIComponent(exerciseName)}`);
        const data = await res.json();
        if (data != null) {
          setFeedback(data);
        }
      } catch (err) {
        console.error('Fetch failed:', err);
      }
    }, 1000);
    return () => clearInterval(interval);
  }, [exerciseName]);


  // CENTER THE FOOTAGE
  useEffect(() => {
    const interval = setInterval(() => {
      try {
        fetch('http://127.0.0.1:5001/avg_pos')
          .then(res => res.json())
          .then(data => {
            const videoEl = document.getElementById('video');
            if (!videoEl) return;
    
            const [x, y] = data.avg_pos;
            // Clamp x and y from 0 to 1
            const clampedX = Math.max(0, Math.min(1, x));
            const clampedY = Math.max(0, Math.min(1, y));
    
            // Width of the image is 45vw
            const imageWidth = window.innerWidth * 0.45;
            const imageHeight = videoEl.clientHeight;

            const viewWidth = window.innerWidth * 0.38;
            const fullWidth = window.innerHeight * 1.24;

            // full width: 124vh
            // view width: 45vw

            const minOffset = -viewWidth;
            const maxOffset = 0;
    
            var offsetX = 4*((0.5 - clampedX) * imageWidth);
            const offsetY = (0.5 - clampedY) * imageHeight;

            // console.log("viewWidth: " + viewWidth);
            // console.log("fullWidth: " + fullWidth);
            // console.log("minoffset: " + minOffset);
            // console.log("maxoffset: " + maxOffset);

            offsetX = Math.max(minOffset, offsetX)
            offsetX = Math.min(maxOffset, offsetX)
    
            videoEl.style.transform = `translate(${offsetX}px, 0px)`;
          })
          .catch(err => console.error(err));
        } catch (err) {

        }
    }, 500);
  
    return () => clearInterval(interval);
  }, []);


  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch('http://127.0.0.1:5001/angles');
        const data = await res.json();
        console.log("angles: " + data.angles[0]);
      } catch (err) {
        console.error('Fetch failed:', err);
      }
    }, 500);
  
    return () => clearInterval(interval); // Clean up the interval on unmount
  }, []);

  // useEffect(() => {
  //   const interval = setInterval(async () => {
  //     try {
  //       const res = await fetch('http://127.0.0.1:5001/feedback');
  //       const data = await res.json();
  //       console.log("feedback: " + data);
  //     } catch (err) {
  //       console.error('Fetch failed:', err);
  //     }
  //   }, 1000);
  
  //   return () => clearInterval(interval); // Clean up the interval on unmount
  // }, []);

  const handleDone = async () => {
    try {
      const res = await fetch('http://127.0.0.1:5001/recording_end', { method: 'POST' });
      const data = await res.json();
      console.log("Recording ended:", data);
      showNextExercise();
    } catch (error) {
      console.error("Error ending recording:", error);
    }
  };

  return (
    <div className={`lessons ${isEnlarged ? 'enlargedHeader' : ''}`}>
      <div className='header'>
        <div className='headerContent'>
          {/* Header title updates based on the current exercise */}
          <h3>{currentExercise.title}</h3>
          <img src={currentExercise.image} alt={currentExercise.title} />
          {/* Depending on the enlargement state, show the long or short description */}
          <p>{isEnlarged ? currentExercise.longDescription : currentExercise.shortDescription}</p>
        </div>
      </div>
      <div className='mainContent'>
      <div className='visualContent'>
        <div className='video-div'>
          <img id="video" src="http://127.0.0.1:5001/video" alt="Exercise Video" />
          <div className={`notInViewError ${isUserInView ? 'hidden' : ''}`}><p>{`Make sure your entire body is visible!`}</p></div>
        </div>
        <div className='feedbackDiv' style={{backgroundColor: feedback != null ? feedback[2].color : 'gray'}}>
          <h1 style={{color: feedback != null ? feedback[3].textColor : 'black'}}>{feedback != null ? feedback[0].bigText : 'READY?'}</h1>
          <p style={{color: feedback != null ? feedback[3].textColor : 'black'}}>{feedback != null ? feedback[1].smallText : '...'}</p>
        </div>
      </div>
        <Link
          className={`button1 ${isButtonHidden ? 'hidden' : ''}`} id='done-btn'
          onClick={handleDone}
          to="/feedback"
        >
          <div className="message">Done</div>
        </Link>
      </div>
    </div>
  );
}

export default Lessons;