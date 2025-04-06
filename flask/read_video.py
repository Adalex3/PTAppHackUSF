import cv2
import mediapipe as mp
import pickle
import os

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        results = self.pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
