import React from 'react';
import { Link } from 'react-router-dom';
import './Lessons.css';

function Lessons() {
  return (
    <div className='lessons enlargedHeader'>
        <div className='header'>
            <h3>Let's begin!</h3>
            <img src='logo.svg'></img>
            <p>Here is some information about the exercise that you are doing</p>
        </div>
        <div className='mainContent'>
            <div className='visualContent'>

            </div>
        </div>
        
    </div>
  );
}

export default Lessons;