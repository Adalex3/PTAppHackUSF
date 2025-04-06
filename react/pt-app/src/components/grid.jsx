import React, { useState } from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import '../App.css';

import { useEffect } from 'react';
import Lessons from '../Lessons';




const Grid = () => {
    const [selectedTop, setSelectedTop] = useState(null);  // Track top row selection
    const [selectedBottom, setSelectedBottom] = useState(null);  // Track bottom row selection
  
    const handleTopButtonClick = (index) => {
      setSelectedTop(index);
    };
  
    const handleBottomButtonClick = (index) => {
      setSelectedBottom(index);
    };

    return (
      <>
    <div className='grid-wrapper'>
      <div className='grid-title'>EXERCISE</div>

      <div className='grid-container'>
        <button 
          className={` grid-button ${selectedTop === 0 ? 'selected' : ''}`} 
          onClick={() => handleTopButtonClick(0)}>
          SLOW SQUATS 
        </button>
        <button 
          className={` grid-button ${selectedTop === 1 ? 'selected' : ''}`} 
          onClick={() => handleTopButtonClick(1)}>
            HAMSTRING STRETCH
        </button>
        <button 
          className={` grid-button ${selectedTop === 2 ? 'selected' : ''}`} 
          onClick={() => handleTopButtonClick(2)}>
          WRIST FLEXION
        </button>
      

      {/* Middle Row with Reps */}
      <div className="grid-label">REPS</div>

      {/* Bottom Row */}
        <button 
          className={` grid-button ${selectedBottom === 0 ? 'selected' : ''}`} 
          onClick={() => handleBottomButtonClick(0)}>
          5
        </button>
        <button 
          className={`= grid-button ${selectedBottom === 1 ? 'selected' : ''}`} 
          onClick={() => handleBottomButtonClick(1)}>
          8
        </button>
        <button 
          className={`= grid-button ${selectedBottom === 2 ? 'selected' : ''}`} 
          onClick={() => handleBottomButtonClick(2)}>
          12
        </button>
      </div>

      <div className="buttondiv">
      <Link
        className="button1"
        to={`/lessons?exercise=${selectedTop}&reps=${selectedBottom}`}
      >
        <div className="label1"> Resume Lessons</div>
      </Link>
    </div>
    </div>  
      </>       
  
      );
  };
  

//   function App() {

//     useEffect(() => {
//       const handleMouseMove = (e) => {
//         const button = e.currentTarget;
//         const rect = button.getBoundingClientRect();
//         const x = (e.clientX - rect.left) / rect.width - 0.5;
//         const y = (e.clientY - rect.top) / rect.height - 0.5;
//         const angle = x < 0 ? -20 : 20;
//         button.style.transform = `rotate3d(${y}, ${-x}, 0, ${angle}deg)`;
//         button.style.filter = `drop-shadow(${x * 20}px ${y * 20}px 5px rgba(0,0,0,0.75))`;
//         button.style.textShadow = `${x * 10}px ${y * 10}px 5px black`;
//       };
  
//       const handleMouseLeave = (e) => {
//         const button = e.currentTarget;
//         button.style.transform = 'rotate3d(0, 0, 0, 0deg)';
//         button.style.filter = 'drop-shadow(0px 0px 5px transparent)';
//         button.style.textShadow = '0px 0px 0px transparent';
//       };
  
//       const buttons = document.querySelectorAll('.button');
//       buttons.forEach(btn => {
//         btn.addEventListener('mousemove', handleMouseMove);
//         btn.addEventListener('mouseleave', handleMouseLeave);
//       });
  
//       // Cleanup
//       return () => {
//         buttons.forEach(btn => {
//           btn.removeEventListener('mousemove', handleMouseMove);
//           btn.removeEventListener('mouseleave', handleMouseLeave);
//         });
//       };
//     }, []);
//   }

  export default Grid;