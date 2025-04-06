import React, { useEffect, useRef, useState } from 'react';
import './VideoPopup.css';

const VideoPopup = ({ arrowPercent, bubbleText }) => {
  const containerRef = useRef(null);
  const [videoDims, setVideoDims] = useState({ width: 0, height: 0 });

  console.log("init x: " + arrowPercent.x + " y: " + arrowPercent.y);

  const mapRange = (a, b, c, d, e) => {
    return d + ((a - b) * (e - d)) / (c - b);
  };

  // Measure the video container (which is assumed to be the parent overlay)
  useEffect(() => {
    const updateDimensions = () => {
      if (containerRef.current) {
        const rect = containerRef.current.getBoundingClientRect();
        setVideoDims({ width: rect.width, height: rect.height });
      }
    };
    updateDimensions();
    window.addEventListener('resize', updateDimensions);
    return () => window.removeEventListener('resize', updateDimensions);
  }, []);

  const { width, height } = videoDims;
  if (width === 0 || height === 0) {
    // Render empty container until dimensions are measured.
    return <div ref={containerRef} className="video-popup-overlay" />;
  }

  // Compute arrow head's absolute position relative to the video container.
  const VIDEO_HEIGHT_PERCENT = 0.70
  const VIDEO_ASPECT_RATIO = 1.7

  const viewportWidth = window.innerWidth;
  const viewportHeight = window.innerHeight;

  const VIDEO_HEIGHT_CALC = viewportHeight*(VIDEO_HEIGHT_PERCENT);
  const VIDEO_WIDTH_CALC = VIDEO_HEIGHT_CALC*(VIDEO_ASPECT_RATIO);
  const VIDEO_SIDE_CALC = (viewportWidth-VIDEO_WIDTH_CALC)/2;
  const VIDEO_TOP_CALC = 0.085*viewportHeight +  0.0625*viewportHeight;

//   console.log("video top calc: " + VIDEO_TOP_CALC);
//   console.log("arrowPercent.y: " + arrowPercent.y);
//   console.log("VIDEO_HEIGHT_CALC: " + VIDEO_HEIGHT_CALC);

//   console.log("WIDTH:::")
//   console.log("VIDEO_WIDTH_CALC: " + VIDEO_WIDTH_CALC);
//   console.log("VIDEO_SIDE_CALC: " + VIDEO_SIDE_CALC);
//   console.log("arrowPercent.x: " + arrowPercent.x);

  const arrowX = VIDEO_SIDE_CALC+(arrowPercent.x*VIDEO_WIDTH_CALC);
  const arrowY = VIDEO_TOP_CALC+(arrowPercent.y*VIDEO_HEIGHT_CALC);

  // Decide which side: left if arrow is in the left half; right otherwise.
  const side = arrowX < viewportWidth / 2 ? 'left' : 'right';

  // Calculate maximum allowed bubble width: (viewport width - video width) / 2.
//   const viewportWidth = window.innerWidth;
  const maxBubbleWidth = (viewportWidth - width) / 2;
  const defaultBubbleWidth = 200;
  const bubbleWidth = Math.min(defaultBubbleWidth, maxBubbleWidth);
  const bubbleHeight = 100;
  const margin = 10;

  // These are the CENTER x and y coordinates
  var bubbleX = 0;
  const PADDING = 10;
  const y_sign = arrowPercent.y > 0.5 ? 1 : -1;
  const bubbleY = mapRange((y_sign*Math.sqrt((Math.abs(arrowPercent.y*2-1))**1)),-1,1,(viewportHeight*0.2)+PADDING,viewportHeight-bubbleHeight-PADDING);
//   console.log("ARROW PERCENT Y real: " + (arrowPercent.y))
//   console.log("ARROW PERCENT Y: " + (y_sign*Math.sqrt((Math.abs(arrowPercent.y*2-1))**1)))
  const DIVISIONS_FOR_X = 5;
  if(side == 'left') {  
    bubbleX = mapRange(arrowPercent.x,0,0.5,(defaultBubbleWidth/2)+PADDING,viewportWidth/DIVISIONS_FOR_X);
  } else {
    bubbleX = mapRange(arrowPercent.x,0.5,1,(DIVISIONS_FOR_X-1)*(viewportWidth/DIVISIONS_FOR_X),(viewportWidth-defaultBubbleWidth/2)-PADDING);
  }


  // Position the bubble outside the video container, centered vertically on the arrow.
  let bubbleStyle = {};
  let bubbleConnectionX = 0;
  if (side === 'left') {
    bubbleStyle = {
      left: bubbleX-defaultBubbleWidth/2,
      top: bubbleY-bubbleHeight/2,
      width: defaultBubbleWidth,
      height: bubbleHeight,
    };
    bubbleConnectionX = -margin;
  } else {
    bubbleStyle = {
      left: bubbleX-defaultBubbleWidth/2,
      top: bubbleY-bubbleHeight/2,
      width: defaultBubbleWidth,
      height: bubbleHeight,
    };
    bubbleConnectionX = width + margin;
  }

  // Calculate middle X and Y
  var middleX = 0, middleY = 0;
  if(side == 'left'){
    middleX = (arrowX+bubbleX)/1.5;
  } else {
    middleX = (arrowX+bubbleX)/2.25;
  }
  middleY = arrowY;

  return (
    <div ref={containerRef} className="video-popup-overlay">
      <svg className="arrow-svg">
        <defs>
          <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="0" refY="3.5" orient="auto">
            <polygon points="0 0, 10 3.5, 0 7" fill="black" />
          </marker>
        </defs>
        <line
          x1={arrowX}
          y1={arrowY}
          x2={middleX}
          y2={middleY}
          stroke="black"
          strokeWidth="5"
        //   markerEnd="url(#arrowhead)"
        />
        <line
          x1={middleX}
          y1={middleY}
          x2={bubbleX}
          y2={bubbleY}
          stroke="black"
          strokeWidth="5"
          markerEnd="url(#arrowhead)"
        />
      </svg>
      <div className="popup-bubble" style={bubbleStyle}>
        {bubbleText}
      </div>
    </div>
  );
};

export default VideoPopup;