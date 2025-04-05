import React, { useState, useEffect } from 'react';
import exercises from './exercises.js'; // Import the exercise objects
import './Lessons.css';
import logo from './logo.svg';

function Lessons() {
  // Default header content before transitioning to any exercise
  const defaultTitle = "Let's begin!";
  const defaultDescription = "Here is some information about the exercise that you are doing";
  const defaultImage = 'logo.svg'; // Fallback or initial image

  const [isButtonHidden, setIsButtonHidden] = useState(true);

  // State to track which exercise is currently active.
  // We start with -1 so that the first exercise is at index 0.
  const [exerciseIndex, setExerciseIndex] = useState(-1);

  // State for the current exercise's data. Initially, it uses the default content.
  const [currentExercise, setCurrentExercise] = useState({
    title: defaultTitle,
    shortDescription: defaultDescription,
    longDescription: defaultDescription,
    image: defaultImage,
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
        },10000)
      }, 3000);
    }
  };

  // On component mount, trigger the first exercise and set an interval for subsequent transitions.
  useEffect(() => {
    // Start with a brief delay before showing the first exercise.
    const initialTimeout = setTimeout(() => {
      showNextExercise();
    }, 100);

    // Automatically cycle through exercises every 10 seconds.
    // const interval = setInterval(() => {
    //   showNextExercise();
    // }, 10000);

    // Cleanup timers on component unmount.
    return () => {
      clearTimeout(initialTimeout);
      // clearInterval(interval);
    };
  }, []); // Runs once on mount

  return (
    <div className={`lessons ${isEnlarged ? 'enlargedHeader' : ''}`}>
      <div className='header'>
        <div className='headerContent'>
          {/* Header title updates based on the current exercise */}
          <h3 className='start'>{currentExercise.title}</h3>
          <img src={currentExercise.image} alt={currentExercise.title} />
          {/* Depending on the enlargement state, show the long or short description */}
          <p>{isEnlarged ? currentExercise.longDescription : currentExercise.shortDescription}</p>
        </div>
      </div>
      <div className='mainContent'>
      <div className='visualContent'>
        <img src="http://localhost:5001/video" alt="Exercise Video" />
      </div>
        <a className={`button ${isButtonHidden ? 'hidden' : ''}`} onClick={showNextExercise} id='done-btn'>I'm done!</a>
      </div>
    </div>
  );
}

export default Lessons;