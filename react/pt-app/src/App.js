import React, { useRef } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {

  const buttonRef = useRef(null);

  const handleMouseMove = (e) => {
    const button = buttonRef.current;
    const rect = button.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width - 0.5;
    const y = (e.clientY - rect.top) / rect.height - 0.5;
    if(x < 0) {
      button.style.transform = `rotate3d(${y}, ${-x}, 0, -20deg)`;
    } else {
      button.style.transform = `rotate3d(${y}, ${-x}, 0, 20deg)`;
    }
    button.style.filter = `drop-shadow(${x*20}px ${y*20}px 5px rgba(0,0,0,0.75))`;
    button.style.textShadow = `${x*10}px ${y*10}px 5px black`;
    
  };

  const handleMouseLeave = () => {
    const button = buttonRef.current;
    button.style.transform = 'rotate3d(0, 0, 0, 0deg)';
    button.style.filter = `drop-shadow(0px 0px 5px transparent)`;
    button.style.textShadow = `0px 0px 0px transparent`;
  };


  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo"></img>
        <div>
          <h1>FixurPostur</h1>
          <h4>The all-in-one PT aid.</h4>
          <p className="desc">Get real-time feedback on your form using your camera and AI. Follow a custom plan from your doctor or generate one instantly. Track progress, fix mistakes, and move better... smarter!</p>
        </div>
      </header>

      <div className="buttondiv">
      <a
          className="button"
          ref={buttonRef}
          onMouseMove={handleMouseMove}
          onMouseLeave={handleMouseLeave}
          href='#'
        >
          Resume Lessons
        </a>
      </div>


    </div>
    // <div className="App">
    //   <header className="App-header">
    //     <img src={logo} className="App-logo" alt="logo" />
    //     <p>
    //       Edit <code>src/App.js</code> and save to reload.
    //     </p>
    //     <a
    //       className="App-link"
    //       href="https://reactjs.org"
    //       target="_blank"
    //       rel="noopener noreferrer"
    //     >
    //       Learn React
    //     </a>
    //   </header>
    // </div>
  );
}

export default App;
