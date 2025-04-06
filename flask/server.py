from flask import Flask, Response, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from start import generate_frames as real_generate_frames
import json
import os
import random
import cv2
import threading
import re

recording_conversion_progress = 0  # Global progress variable (0-100%)

latest_avg_pos = None

def generate_frames():
    global latest_avg_pos
    for frame, avg_pos, in_frame, angles, landmarks in real_generate_frames():
        latest_avg_pos = avg_pos
        print("LANNNDDDDDDMARRRRRKSSSSSSSSSSSSSS")
        print(landmarks)
        #print(avg_pos)
        with open('latest_avg_pos.json', 'w') as f:
            json.dump(avg_pos, f)
        with open('in_frame.json', 'w') as g:
            json.dump(in_frame, g)
        with open('angles.json', 'w') as g:
            json.dump(angles, g)
        with open('landmarks.json', 'w') as g:
            json.dump([{
                'x': lm.x,
                'y': lm.y,
                'z': lm.z,
                'visibility': lm.visibility
            } for lm in landmarks], g)
        yield frame

def convert_video(frames):
    global recording_conversion_progress
    import subprocess

    os.makedirs('recordings', exist_ok=True)
    temp_path = 'recordings/temp_frames'
    os.makedirs(temp_path, exist_ok=True)

    # Save frames as JPEG images
    for i, frame in enumerate(frames):
        frame_path = os.path.join(temp_path, f'frame_{i:04d}.jpg')
        cv2.imwrite(frame_path, frame)
        recording_conversion_progress = int(((i + 1) / len(frames)) * 100)

    # Use ffmpeg to encode the video
    output_path = 'recordings/output.mp4'
    cmd = [
        'ffmpeg',
        '-y',  # Overwrite output
        '-framerate', '20',
        '-i', os.path.join(temp_path, 'frame_%04d.jpg'),
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        output_path
    ]
    subprocess.run(cmd)

    # Cleanup temporary frame files
    for file in os.listdir(temp_path):
        os.remove(os.path.join(temp_path, file))
    os.rmdir(temp_path)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    return 'Hello, Flask!'

last_frame = None

# Returns the altered video
@app.route('/video')
def load_video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/is_in_frame')
def is_in_frame():
    # Checks whether all joints are visible in the frame (if parts of their body are obscured or not). Returns true or false.
    if os.path.exists('in_frame.json'):
        with open('in_frame.json') as f:
            in_frame = json.load(f)
        return jsonify({'in_frame': in_frame})
    else:
        return jsonify({'in_frame': None})


@app.route('/set_pose', methods=['POST'])
def set_pose():
    data = request.get_json()
    pose = data.get('pose')
    # Tells the python backend what pose the user is attempting to do, as this is received from frontend
    return jsonify({'status': 'error'}) # Default return

@app.route('/pose_feedback')
def pose_data():
    # Returns a big JSON with lots of data about the user's movements. Has all of the pose data that the backend gets to be processed by frontend
    # This should return the position and angle and other info about every joint, for the frontend to process
    
    feedback = get_feedback_data().get_json()

    print(feedback)

    color = 'green'
    bigText = 'GOOD'
    if (feedback["severity"] > 7):
        color = 'red'
        bigText = 'POOR'
    elif (feedback["severity"] > 4):
        color = 'orange'
        bigText = 'FAIR'

    return jsonify({'bigText': bigText},{'smallText': feedback['small_message']},{'color': color},{'textColor':'white'})

    if(random.random() < 0.3):
        return jsonify({'bigText': 'GREAT'},{'smallText': 'Keep stretching those calves!'},{'color': 'green'},{'textColor':'white'})
    elif (random.random() < 0.3):
        return jsonify({'bigText': 'FAIR'},{'smallText': 'Your posture is slipping.'},{'color': 'orange'},{'textColor':'white'})
    else:
        return jsonify({'bigText': 'STOP'},{'smallText': "You need to re-center yourself!"},{'color': 'red'},{'textColor':'white'})


@app.route('/angles')
def angles():
    if os.path.exists('angles.json'):
        with open('angles.json') as f:
            angles = json.load(f)
        return jsonify({'angles': angles})
    else:
        return jsonify({'angles': None})
    

def get_feedback_data():
    import os, json
    from flask import jsonify
    from mediapipe.python.solutions.pose import PoseLandmark
    # Load the latest measured angles from file
    angles = []
    if os.path.exists('angles.json'):
        with open('angles.json', 'r') as f:
            angles = json.load(f)
    # Load the latest landmarks from file
    landmarks = []
    if os.path.exists('landmarks.json'):
        with open('landmarks.json', 'r') as f:
            landmarks = json.load(f)
        # Initialize or load existing issues

    issues_file = 'posture_issues.json'
    issues_data = {"issues": []}
    if os.path.exists(issues_file):
        with open(issues_file, 'r') as f:
            issues_data = json.load(f)

    # If we don't have valid data, return an empty feedback response
    if not angles or not landmarks:
        return jsonify({
            "position": None,
            "big_message": "",
            "small_message": "",
            "severity": 0
        })
    
    # For this example, we assume the exercise being performed is "Slow Squats"
    # (change this as needed or fetch it from a different source)
    from hard_coded_exercises import get_exercise_by_name, get_joint_angle_from_exercise
    exercise = get_exercise_by_name("Slow Squats")
    
    # According to generate_frames(), the angles list is ordered as:
    # [left_arm_angle, right_arm_angle, left_leg_angle, right_leg_angle]
    # For "Slow Squats", we are interested in the knee angles.
    try:
        measured = {
            PoseLandmark.RIGHT_KNEE: angles[3],
            PoseLandmark.LEFT_KNEE: angles[2]
        }
    except IndexError:
        return jsonify({
            "position": None,
            "big_message": "",
            "small_message": "",
            "severity": 0
        })
    
    # Track current frame (you'll need to implement frame counting in your video processing)
    current_frame = 0  # This should come from your video processing logic
    
    # Iterate over the measured joints and compare to the exercise's error cases
    highest_issue = None
    current_issues = []
    
    for joint, measured_angle in measured.items():
        joint_data = get_joint_angle_from_exercise(exercise, joint)
        for ec in joint_data.error_cases:
            if ec.error_type.compare(measured_angle, ec.threshold):
                if highest_issue is None or ec.severity > highest_issue[0]:
                    highest_issue = (ec.severity, joint, ec)
                
                # Record this issue
                joint_index = joint.value
                if joint_index < len(landmarks):
                    joint_landmark = landmarks[joint_index]
                    position = [joint_landmark.get("x", 0), joint_landmark.get("y", 0)]
                else:
                    position = [0, 0]
                
                current_issues.append({
                    "joint": joint.name,
                    "description": ec.description,
                    "position": position,
                    "frame": current_frame,
                    "severity": ec.severity
                })
    
    # Check if any of the current issues are continuations of existing issues
    for issue in current_issues:
        # Look for matching ongoing issues
        matching_issue = None
        for existing_issue in issues_data["issues"]:
            if (existing_issue["description"] == issue["description"] and 
                current_frame == existing_issue["startFrame"] + existing_issue["frameCount"]):
                matching_issue = existing_issue
                break
        
        if matching_issue:
            # Continue the existing issue
            matching_issue["frameCount"] += 1
            matching_issue["positions"].append(issue["position"])
        else:
            # Start a new issue
            new_issue = {
                "id": len(issues_data["issues"]),
                "description": issue["description"],
                "startFrame": current_frame,
                "frameCount": 1,
                "positions": [issue["position"]]
            }
            issues_data["issues"].append(new_issue)
    
    # Save the updated issues data
    with open(issues_file, 'w') as f:
        json.dump(issues_data, f, indent=2)
    
    # Return feedback for the most severe current issue
    if highest_issue is None:
        return jsonify({
            "position": None,
            "big_message": "",
            "small_message": "",
            "severity": 0
    })

    # Use the error case with the highest severity.
    _, problematic_joint, error_case = highest_issue
    # Retrieve the 2D position (normalized x and y) of the problematic joint from the landmarks.
    joint_index = problematic_joint.value  # PoseLandmark enum value as index
    if joint_index < len(landmarks):
        joint_landmark = landmarks[joint_index]
        position = [joint_landmark.get("x", 0), joint_landmark.get("y", 0)]
    else:
        position = [0, 0]


    # Record Function Goes Here
    
    # Return the position, large message, small message, and severity as a JSON response.
    return jsonify({
        "position": position,
        "big_message": error_case.long_message,
        "small_message": error_case.short_message,
        "severity": error_case.severity
    })

@app.route('/feedback')
def feedback():
    return get_feedback_data()

@app.route('/squat_json')
def squat_json():
    try:
        with open('squat_issues.json', 'r') as f:
            data = f.read()
        return Response(data, mimetype='application/json')
    except FileNotFoundError:
        return jsonify({'error': 'squat_issues.json not found'}), 404
    

@app.route('/avg_pos')
def avg_pos():
    if os.path.exists('latest_avg_pos.json'):
        with open('latest_avg_pos.json') as f:
            pos = json.load(f)
        return jsonify({'avg_pos': pos})
    else:
        return jsonify({'avg_pos': None})
    


@app.route('/recording_start', methods=['POST'])
def recording_start():
    # Import the recording globals from start.py
    import start
    start.recording_active = True
    start.recorded_frames = []  # Clear any previously recorded frames
    return jsonify({'status': 'recording started'})


@app.route('/recording_end', methods=['POST'])
def recording_end():
    print("RECORDING END")
    import start
    start.recording_active = False
    frames = start.recorded_frames

    print("RECORDING END2")

    if not frames:
        print("RECORDING END333")
        return jsonify({'status': 'no frames recorded'}), 400

    print("RECORDING END44")

    global recording_conversion_progress
    recording_conversion_progress = 0  # Reset progress

    # Start the conversion in a background thread
    thread = threading.Thread(target=convert_video, args=(frames,))
    thread.start()

    # Clear the recorded frames list immediately
    start.recorded_frames = []
    
    return jsonify({'status': 'recording processing started'})

@app.route('/recording_progress', methods=['GET'])
def recording_progress():
    global recording_conversion_progress
    return jsonify({'progress': recording_conversion_progress})


@app.route('/recording')
def get_recording():
    path = os.path.join('recordings', 'output.mp4')
    if not os.path.exists(path):
        return jsonify({'error': 'Recording not found'}), 404

    range_header = request.headers.get('Range', None)
    size = os.path.getsize(path)
    byte1, byte2 = 0, None

    if range_header:
        match = re.search(r'bytes=(\d+)-(\d*)', range_header)
        if match:
            byte1 = int(match.group(1))
            if match.group(2):
                byte2 = int(match.group(2))

    byte2 = byte2 if byte2 is not None else size - 1
    length = byte2 - byte1 + 1

    with open(path, 'rb') as f:
        f.seek(byte1)
        data = f.read(length)

    rv = Response(data, status=206, mimetype='video/mp4', direct_passthrough=True)
    rv.headers.add('Content-Range', f'bytes {byte1}-{byte2}/{size}')
    rv.headers.add('Accept-Ranges', 'bytes')
    rv.headers.add('Content-Length', str(length))
    return rv
    

if __name__ == '__main__':
    app.run(debug=True, port=5001)