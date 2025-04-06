import cv2 as cv2
import mediapipe.python.solutions.drawing_utils as drawing
import mediapipe.python.solutions.drawing_styles as drawing_styles
import mediapipe.python.solutions.holistic as mp_holistic
import numpy as np
from read_video import process_video_file, calculate_frame_angles, calc_angle
cap = cv2.VideoCapture(1)

ref_landmarks, ref_angles = process_video_file("squat.mp4")
current_ref_frame = 0

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
                fail, buffer=cv2.imencode('.jpg', img)
                img=buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n', avg_position, in_frame)

def check_if_frame(landmarks):
    if not landmarks:
        return False
    for landmark in NEEDED_LANDMARKS:
        landmark_point = landmarks.landmark[landmark]
        if landmark_point.visibility < 0.5:
            return False
        if not (0 <= landmark_point.x <= 1 and 0 <= landmark_point.y <= 1):
            return False
    return True
