import cv2 as cv2
import mediapipe.python.solutions.hands as mp_hands
import mediapipe.python.solutions.drawing_utils as drawing
import mediapipe.python.solutions.drawing_styles as drawing_styles
import mediapipe.python.solutions.holistic as mp_holistic

cap = cv2.VideoCapture(1)

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
            if not ret:
                cap.release()
                break
            else:
                fail, buffer=cv2.imencode('.jpg', img)
                img=buffer.tobytes()
                yield(b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
