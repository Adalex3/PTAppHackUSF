import cv2 as cv2
import mediapipe.python.solutions.drawing_utils as drawing
import mediapipe.python.solutions.drawing_styles as drawing_styles
import mediapipe.python.solutions.holistic as mp_holistic
import numpy as np
import os
from read_video import calc_angle  # Only keep calc_angle since it is used to compute joint angles

# Open the default camera (usually webcam at index 0)
cap = cv2.VideoCapture(0)

# Global variables for recording video frames if needed
recording_active = False
recorded_frames = []

# List of landmarks that must be sufficiently visible and in-frame
NEEDED_LANDMARKS = [
    mp_holistic.PoseLandmark.LEFT_SHOULDER,
    mp_holistic.PoseLandmark.RIGHT_SHOULDER,
    mp_holistic.PoseLandmark.LEFT_ELBOW,
    mp_holistic.PoseLandmark.RIGHT_ELBOW,
    mp_holistic.PoseLandmark.LEFT_WRIST,
    mp_holistic.PoseLandmark.RIGHT_WRIST,
    mp_holistic.PoseLandmark.LEFT_HIP,
    mp_holistic.PoseLandmark.RIGHT_HIP,
    mp_holistic.PoseLandmark.LEFT_KNEE,
    mp_holistic.PoseLandmark.RIGHT_KNEE,
    mp_holistic.PoseLandmark.LEFT_HEEL,
    mp_holistic.PoseLandmark.RIGHT_HEEL
]

def generate_frames():
    """
    Continuously captures frames from the webcam, processes them using MediaPipe Holistic to extract landmarks,
    computes joint angles for the arms and legs, overlays the angles onto the image, and yields the processed frame.
    """
    # Initialize MediaPipe Holistic model with detection and tracking confidence thresholds
    with mp_holistic.Holistic(min_detection_confidence=0.5, 
                              min_tracking_confidence=0.5, 
                              model_complexity=0) as holistic:
        while cap.isOpened():
            ret, frame = cap.read()
            
            # If frame is not captured, release the capture and exit the loop
            if not ret:
                cap.release()
                break

            # Convert the BGR image to RGB for processing by MediaPipe
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = holistic.process(img_rgb)

            # Convert the image back to BGR for OpenCV display
            img = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

            # Draw face landmarks
            drawing.draw_landmarks(
                img,
                results.face_landmarks,
                mp_holistic.FACEMESH_CONTOURS,
                drawing.DrawingSpec(color=(80, 110, 10), thickness=1, circle_radius=1),
                drawing.DrawingSpec(color=(80, 256, 121), thickness=1, circle_radius=1)
            )

            # Draw right hand landmarks
            drawing.draw_landmarks(
                img,
                results.right_hand_landmarks,
                mp_holistic.HAND_CONNECTIONS,
                drawing.DrawingSpec(color=(80, 22, 10), thickness=2, circle_radius=4),
                drawing.DrawingSpec(color=(80, 44, 121), thickness=2, circle_radius=2)
            )

            # Draw left hand landmarks
            drawing.draw_landmarks(
                img,
                results.left_hand_landmarks,
                mp_holistic.HAND_CONNECTIONS,
                drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                drawing.DrawingSpec(color=(121, 44, 250), thickness=2, circle_radius=2)
            )

            # Draw pose landmarks (skeleton)
            drawing.draw_landmarks(
                img,
                results.pose_landmarks,
                mp_holistic.POSE_CONNECTIONS,
                drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
                drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
            )

            # Check if the detected pose landmarks are valid for processing
            in_frame = check_if_frame(results.pose_landmarks)

            try:
                # Extract the list of detected pose landmarks
                landmarks = results.pose_landmarks.landmark

                # Get coordinates for left arm joints
                left_shoulder = [landmarks[mp_holistic.PoseLandmark.LEFT_SHOULDER.value].x, 
                                 landmarks[mp_holistic.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_holistic.PoseLandmark.LEFT_ELBOW.value].x, 
                              landmarks[mp_holistic.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[mp_holistic.PoseLandmark.LEFT_WRIST.value].x,
                              landmarks[mp_holistic.PoseLandmark.LEFT_WRIST.value].y]

                # Get coordinates for right arm joints
                right_shoulder = [landmarks[mp_holistic.PoseLandmark.RIGHT_SHOULDER.value].x, 
                                  landmarks[mp_holistic.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_holistic.PoseLandmark.RIGHT_ELBOW.value].x, 
                               landmarks[mp_holistic.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[mp_holistic.PoseLandmark.RIGHT_WRIST.value].x,
                               landmarks[mp_holistic.PoseLandmark.RIGHT_WRIST.value].y]
                
                shoulder_center = [(left_shoulder[0] + right_shoulder[0])/2,
                           (left_shoulder[1] + right_shoulder[1])/2]
                
                # Get coordinates for left leg joints
                left_hip = [landmarks[mp_holistic.PoseLandmark.LEFT_HIP.value].x, 
                            landmarks[mp_holistic.PoseLandmark.LEFT_HIP.value].y]
                left_knee = [landmarks[mp_holistic.PoseLandmark.LEFT_KNEE.value].x, 
                             landmarks[mp_holistic.PoseLandmark.LEFT_KNEE.value].y]
                left_heel = [landmarks[mp_holistic.PoseLandmark.LEFT_HEEL.value].x, 
                             landmarks[mp_holistic.PoseLandmark.LEFT_HEEL.value].y]

                # Get coordinates for right leg joints
                right_hip = [landmarks[mp_holistic.PoseLandmark.RIGHT_HIP.value].x, 
                             landmarks[mp_holistic.PoseLandmark.RIGHT_HIP.value].y]
                right_knee = [landmarks[mp_holistic.PoseLandmark.RIGHT_KNEE.value].x, 
                              landmarks[mp_holistic.PoseLandmark.RIGHT_KNEE.value].y]
                right_heel = [landmarks[mp_holistic.PoseLandmark.RIGHT_HEEL.value].x, 
                              landmarks[mp_holistic.PoseLandmark.RIGHT_HEEL.value].y]

                # Calculate the joint angles using the calc_angle function
                left_arm_angle = calc_angle(left_shoulder, left_elbow, left_wrist)
                right_arm_angle = calc_angle(right_shoulder, right_elbow, right_wrist)
                left_leg_angle = calc_angle(left_hip, left_knee, left_heel)
                right_leg_angle = calc_angle(right_hip, right_knee, right_heel)

                # Get dimensions of the frame to correctly place the text
                height, width = frame.shape[:2]

                # Overlay the computed angles on the image near the respective joints
                cv2.putText(img, str(left_arm_angle),
                            tuple(np.multiply(left_elbow, [width, height]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(img, str(right_arm_angle),
                            tuple(np.multiply(right_elbow, [width, height]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(img, str(left_leg_angle),
                            tuple(np.multiply(left_knee, [width, height]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(img, str(right_leg_angle),
                            tuple(np.multiply(right_knee, [width, height]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                # Calculate the average position of all detected landmarks.
                # This can be useful for additional processing or to center overlays.
                total_x = sum([lm.x for lm in landmarks])
                total_y = sum([lm.y for lm in landmarks])
                avg_position = (total_x / len(landmarks), total_y / len(landmarks))

            except Exception as e:
                # If any error occurs during processing, simply pass and continue to the next frame.
                avg_position = (0, 0)
                pass

            # If recording is active, save a copy of the current processed frame
            if recording_active:
                recorded_frames.append(img.copy())

            # Encode the processed frame as JPEG
            success, buffer = cv2.imencode('.jpg', img)
            if not success:
                continue

            # Yield the JPEG image as bytes along with the average landmark position and the frame validity flag
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n', avg_position, in_frame, [left_arm_angle, right_arm_angle, left_leg_angle, right_leg_angle])

def check_if_frame(landmarks):
    """
    Checks if all the required landmarks are visible and within the image frame boundaries.
    Returns True if all required landmarks meet the criteria, False otherwise.
    """
    if not landmarks:
        return False

    for landmark in NEEDED_LANDMARKS:
        landmark_point = landmarks.landmark[landmark]
        # Check if landmark visibility is high enough and its coordinates are within [0, 1]
        if landmark_point.visibility < 0.5:
            return False
        if not (0 <= landmark_point.x <= 1 and 0 <= landmark_point.y <= 1):
            return False
    return True