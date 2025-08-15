
# Physical Trainer Movement Helper App — Project Requirements

This project is a smart movement and rehabilitation assistant designed to guide users through physical exercises with live camera feedback. Users can either upload a treatment plan from their doctor or have GPT-4o generate a custom plan for them. The app leverages computer vision to identify form issues and provides detailed, real-time corrections through a sleek, easy-to-use interface.

---

## Core Workflow

### Step 1: Add Your Treatment Plan
- Upload your prescribed exercise plan from a healthcare provider **or**
- Use GPT-4o to generate a personalized plan based on your needs

### Step 2: Perform the Exercises with Camera Feedback
- The app uses Mediapipe and OpenCV for pose estimation
- You’ll be guided through hardcoded exercises that we’ve trained the app to understand
- Real-time feedback will tell you **what’s wrong** and **how to fix it**, with actionable and specific suggestions

### Step 3: Get a Visual Summary
- After you’re done, you’ll see a clean, visual breakdown of your performance
- Charts, highlights, and annotations will show what you did well and what needs improvement

---

## Optional Features

### Mistake Highlight Reel
- The app can clip short video segments where your form broke down
- Playback lets you review mistakes with visual overlays and suggestions

### Doctor Review Portal
- Option to send your feedback and performance to your doctor
- Uses Firebase to store and sync data
- Doctors can log in through a separate interface to check in on your progress

---

## Phase 2: Raspberry Pi Integration (Optional)
In the future, we’ll allow you to run the pose estimation on a Raspberry Pi with a camera module. It’ll send pose data over WiFi to your computer, offloading the heavy lifting and letting the app run more smoothly on lightweight systems.

---

## Tech Stack

- **Frontend**: React, Tailwind CSS, Recharts or Chart.js
- **Pose Estimation**: Mediapipe, OpenCV (Python)
- **Backend**: Firebase (for auth and storage), Flask or FastAPI (for GPT integration)
- **Video Handling**: FFmpeg or MediaRecorder API
- **Optional Hardware**: Raspberry Pi 4, Camera Module v2

---

## Milestones

1. Treatment Plan UI + GPT generation
2. Pose Detection + Feedback for Core Movements
3. Real-Time Guidance with Specific Corrections
4. Visual Summary Dashboard
5. Mistake Replay System (optional)
6. Doctor Sharing Portal (optional)
7. Raspberry Pi Streaming Support (optional)
