import cv2 as cv2
import mediapipe.python.solutions.drawing_utils as drawing
import mediapipe.python.solutions.drawing_styles as drawing_styles
import mediapipe.python.solutions.holistic as mp_holistic
import numpy as np
import os
from read_video import process_video_file, calc_angle



cap = cv2.VideoCapture(0)


video_path = os.path.join("assets", "squat.mp4")
if not os.path.exists(video_path):
    raise FileNotFoundError(f"Video file not found at: {video_path}")
ref_landmarks, ref_angles = process_video_file(video_path)
current_ref_frame = 0

# Global variables for recording
recording_active = False
recorded_frames = []

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
    #reading the camera frame
    global current_ref_frame
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5, model_complexity=0) as holistic:
        while cap.isOpened():
            ret, frame = cap.read()

            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = holistic.process(img)

            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            drawing.draw_landmarks(
                img,
                results.face_landmarks,
                mp_holistic.FACEMESH_CONTOURS,
                drawing.DrawingSpec(color=(80, 110, 10), thickness=1, circle_radius=1),
                drawing.DrawingSpec(color=(80, 256, 121), thickness=1, circle_radius=1)
            )

            drawing.draw_landmarks(
                img,
                results.right_hand_landmarks,
                mp_holistic.HAND_CONNECTIONS,
                drawing.DrawingSpec(color=(80, 22, 10), thickness=2, circle_radius=4),
                drawing.DrawingSpec(color=(80, 44, 121), thickness=2, circle_radius=2)
            )

            drawing.draw_landmarks(
                img,
                results.left_hand_landmarks,
                mp_holistic.HAND_CONNECTIONS,
                drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                drawing.DrawingSpec(color=(121, 44, 250), thickness=2, circle_radius=2)
            )

            drawing.draw_landmarks(
                img,
                results.pose_landmarks,
                mp_holistic.POSE_CONNECTIONS,
                drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
                drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
            )

            avg_position = (0, 0)
            in_frame = check_if_frame(results.pose_landmarks)
            try:
                landmarks = results.pose_landmarks.landmark

                left_shoulder = [landmarks[mp_holistic.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_holistic.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_holistic.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_holistic.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[mp_holistic.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_holistic.PoseLandmark.LEFT_WRIST.value].y]

                right_shoulder = [landmarks[mp_holistic.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_holistic.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_holistic.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_holistic.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[mp_holistic.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_holistic.PoseLandmark.RIGHT_WRIST.value].y]

                left_heel = [landmarks[mp_holistic.PoseLandmark.LEFT_HEEL.value].x, landmarks[mp_holistic.PoseLandmark.LEFT_HEEL.value].y]
                left_knee = [landmarks[mp_holistic.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_holistic.PoseLandmark.LEFT_KNEE.value].y]
                left_hip = [landmarks[mp_holistic.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_holistic.PoseLandmark.LEFT_HIP.value].y]

                right_heel = [landmarks[mp_holistic.PoseLandmark.RIGHT_HEEL.value].x, landmarks[mp_holistic.PoseLandmark.RIGHT_HEEL.value].y]
                right_knee = [landmarks[mp_holistic.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_holistic.PoseLandmark.RIGHT_KNEE.value].y]
                right_hip = [landmarks[mp_holistic.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_holistic.PoseLandmark.RIGHT_HIP.value].y]

                left_arm_angle = calc_angle(left_shoulder, left_elbow, left_wrist)
                right_arm_angle = calc_angle(right_shoulder, right_elbow, right_wrist)
                
                left_leg_angle = calc_angle(left_hip, left_knee, left_heel)
                right_leg_angle = calc_angle(right_hip, right_knee, right_heel)

                height, width = frame.shape[:2]

                cv2.putText(img, str(left_arm_angle), tuple(np.multiply(left_elbow, [width, height]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(img, str(right_arm_angle), tuple(np.multiply(right_elbow, [width, height]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(img, str(left_leg_angle), tuple(np.multiply(left_knee, [width, height]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(img, str(right_leg_angle), tuple(np.multiply(right_knee, [width, height]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                live_angles = {
                'left_arm': left_arm_angle,
                'right_arm': right_arm_angle,
                'left_leg': left_leg_angle,
                'right_leg': right_leg_angle
                } 

                JOINT_TOLERANCES = {
                'left_arm': 15, 
                'right_arm': 15,
                'left_leg': 10,
                'right_leg': 10,
                }

                JOINT_MAPPING = {
                'left_arm': 'LEFT_ELBOW',   
                'right_arm': 'RIGHT_ELBOW',
                'left_leg': 'LEFT_KNEE',
                'right_leg': 'RIGHT_KNEE',
                # Add more mappings as needed
                }

                joint_positions = {}  # Dictionary to store screen coordinates

                ref_frame_angles = ref_angles[current_ref_frame % len(ref_angles)]
                current_ref_frame += 1

                # Initialize comparison variables
                angle_diffs = {}
                total_score = 0  # Reset for each frame
                valid_angles = 0

                # Compare each joint
                for joint in ref_frame_angles:
                    if joint in live_angles:
                        actual_diff = abs(ref_frame_angles[joint] - live_angles[joint])
                        tolerance = JOINT_TOLERANCES.get(joint, 15)
                        joint_score = max(0, 1 - (actual_diff / tolerance))

                        if actual_diff < tolerance * 2:
                            angle_diffs[joint] = joint_score
                            total_score += joint_score
                            valid_angles += 1
                        else:
                            angle_diffs[joint] = 0

                # Calculate overall similarity
                similarity = (total_score / valid_angles) * 100 if valid_angles > 0 else 0

                # Get joint positions for visualization
                joint_positions = {}
                if results.pose_landmarks:
                    for landmark in mp_holistic.PoseLandmark:
                        lm = results.pose_landmarks.landmark[landmark.value]
                        x, y = int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])
                        joint_positions[landmark.name] = (x, y)

                # Apply visual feedback to the display image (img, not frame)
                for joint_name, score in angle_diffs.items():
                    landmark_name = JOINT_MAPPING.get(joint_name)
                    if landmark_name and landmark_name in joint_positions:
                        position = joint_positions[landmark_name]
                        
                        # Determine circle properties based on score
                        if score == 0:  # Not tracked
                            color = (128, 128, 128)  # Gray
                            radius = 3
                        elif score > 0.7:  # Good
                            color = (0, 255, 0)  # Green
                            radius = 8  
                        elif score > 0.4:  # Okay
                            color = (0, 255, 255)  # Yellow
                            radius = 6
                        else:  # Needs work
                            color = (0, 0, 255)  # Red
                            radius = 8
                        
                        # Draw on the image (must use img, not frame)
                        cv2.circle(img, position, radius, color, -1)
                        
                        # Optional: Add joint name
                        cv2.putText(img, joint_name, (position[0]+10, position[1]),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
                        
                print(f"Joint positions: {joint_positions}")
                print(f"Angle diffs: {angle_diffs}")

                # Calculate average position
                total_x = 0
                total_y = 0
                for landmark in landmarks:
                    total_x += landmark.x
                    total_y += landmark.y
                total_x /= len(landmarks)
                total_y /= len(landmarks)

                avg_position = (total_x,total_y)

            except:
                pass

            if not ret:
                cap.release()
                break
            else:
                if recording_active:
                    recorded_frames.append(img.copy())
                fail, buffer=cv2.imencode('.jpg', img)
                img=buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n', avg_position, in_frame)

def check_if_frame(landmarks):
    if not landmarks:
        return False
    total_visibility = 0
    for landmark in NEEDED_LANDMARKS:
        landmark_point = landmarks.landmark[landmark]
        if landmark_point.visibility < 0.5:
            return False
        if not (0 <= landmark_point.x <= 1 and 0 <= landmark_point.y <= 1):
            return False
    return True
