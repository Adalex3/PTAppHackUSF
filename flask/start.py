import cv2 as cv2
import mediapipe.python.solutions.hands as mp_hands
import mediapipe.python.solutions.drawing_utils as drawing
import mediapipe.python.solutions.drawing_styles as drawing_styles
import mediapipe.python.solutions.holistic as mp_holistic

cap = cv2.VideoCapture(1)

def generate_frames():
    #reading the camera frame
    while True:
        success, frame=cap.read()
        if not success:
            break
        else:
            ret, buffer=cv2.imencode('.jpg', frame)
            frame=buffer.tobytes()
            yield(b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

'''
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

        cv2.imshow("Full Body Sample", img)

        if cv2.waitKey(27) == ord('\x1b'):
            break
'''
# cap.release()
# cv2.destroyAllWindows()
