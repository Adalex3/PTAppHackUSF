import React from 'react';
import '../styles/Landing.css';
import '../styles/Grid.css';
import NavBar from '../components/navbar.jsx';
import Grid from '../components/grid.jsx';
import group1 from '../components/Group1.svg';
import group2 from '../components/Group2.svg';

// import '../components/Group.svg';

const Landing = () => {
  return (
    <>
    <NavBar></NavBar>
    <div className="container">
        <div className='menu'>
            
                <Grid></Grid>
 
                
        </div>
        <div className='img-container'>
            <img id='weight' src={group1}></img>
            <img id="bench" src={group2}></img>
        </div>
    </div> 
    </>       

    );
};

export default Landing;



{/* <body>
  <div class="container">
    <div class="rectangle left-rectangle"></div>
    <div class="content">
      <h1>Main Content Area</h1>
      <p>This is where your main content would go. The rectangles float on either side of this content.</p>
    </div>
    <div class="rectangle right-rectangle"></div>
  </div>
</body> */}