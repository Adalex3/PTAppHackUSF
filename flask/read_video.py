import cv2
import mediapipe as mp
import numpy as np
from mediapipe.python.solutions import holistic as mp_holistic

def process_video_file(video_path):
    """
    Process an exercise video file and extract pose data
    Returns:
    - landmarks_list: List of frames with landmark positions
    - angles_list: List of frames with joint angles
    """
    landmarks_list = []
    angles_list = []
    
    cap = cv2.VideoCapture(video_path)
    
    with mp_holistic.Holistic(
        min_detection_confidence=0.5, 
        min_tracking_confidence=0.5,
        model_complexity=0
    ) as holistic:
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            # Convert to RGB and process
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = holistic.process(image)
            
            # Get landmarks for this frame
            frame_landmarks = {}
            if results.pose_landmarks:
                for landmark in mp_holistic.PoseLandmark:
                    lm = results.pose_landmarks.landmark[landmark.value]
                    frame_landmarks[landmark.name] = (lm.x, lm.y, lm.z, lm.visibility)
            landmarks_list.append(frame_landmarks)
            
            # Get angles for this frame
            frame_angles = calculate_frame_angles(results)
            angles_list.append(frame_angles)
                
    cap.release()
    return landmarks_list, angles_list

def calculate_frame_angles(results):
    angles = {}
    if not results.pose_landmarks:
        return angles
        
    landmarks = results.pose_landmarks.landmark
    
    try:
        # Left arm
        left_shoulder = [landmarks[mp_holistic.PoseLandmark.LEFT_SHOULDER.value].x, 
                        landmarks[mp_holistic.PoseLandmark.LEFT_SHOULDER.value].y]
        left_elbow = [landmarks[mp_holistic.PoseLandmark.LEFT_ELBOW.value].x, 
                      landmarks[mp_holistic.PoseLandmark.LEFT_ELBOW.value].y]
        left_wrist = [landmarks[mp_holistic.PoseLandmark.LEFT_WRIST.value].x,
                      landmarks[mp_holistic.PoseLandmark.LEFT_WRIST.value].y]
        angles['left_arm'] = calc_angle(left_shoulder, left_elbow, left_wrist)
        
        # Right arm
        right_shoulder = [landmarks[mp_holistic.PoseLandmark.RIGHT_SHOULDER.value].x, 
                         landmarks[mp_holistic.PoseLandmark.RIGHT_SHOULDER.value].y]
        right_elbow = [landmarks[mp_holistic.PoseLandmark.RIGHT_ELBOW.value].x, 
                       landmarks[mp_holistic.PoseLandmark.RIGHT_ELBOW.value].y]
        right_wrist = [landmarks[mp_holistic.PoseLandmark.RIGHT_WRIST.value].x,
                       landmarks[mp_holistic.PoseLandmark.RIGHT_WRIST.value].y]
        angles['right_arm'] = calc_angle(right_shoulder, right_elbow, right_wrist)
        
        # Left leg
        left_hip = [landmarks[mp_holistic.PoseLandmark.LEFT_HIP.value].x,
                    landmarks[mp_holistic.PoseLandmark.LEFT_HIP.value].y]
        left_knee = [landmarks[mp_holistic.PoseLandmark.LEFT_KNEE.value].x,
                     landmarks[mp_holistic.PoseLandmark.LEFT_KNEE.value].y]
        left_heel = [landmarks[mp_holistic.PoseLandmark.LEFT_HEEL.value].x,
                     landmarks[mp_holistic.PoseLandmark.LEFT_HEEL.value].y]
        angles['left_leg'] = calc_angle(left_hip, left_knee, left_heel)
        
        # Right leg
        right_hip = [landmarks[mp_holistic.PoseLandmark.RIGHT_HIP.value].x,
                     landmarks[mp_holistic.PoseLandmark.RIGHT_HIP.value].y]
        right_knee = [landmarks[mp_holistic.PoseLandmark.RIGHT_KNEE.value].x,
                      landmarks[mp_holistic.PoseLandmark.RIGHT_KNEE.value].y]
        right_heel = [landmarks[mp_holistic.PoseLandmark.RIGHT_HEEL.value].x,
                      landmarks[mp_holistic.PoseLandmark.RIGHT_HEEL.value].y]
        angles['right_leg'] = calc_angle(right_hip, right_knee, right_heel)
        
    except Exception as e:
        print(f"Angle calculation error: {e}")
    
    return angles

def calc_angle(a, b, c):
    """Calculate angle between three points"""
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[0] - b[0], c[1] - b[1]) - np.arctan2(a[0] - b[0], a[1] - b[1])
    angle = np.abs(radians * 180/np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
    
    return angle