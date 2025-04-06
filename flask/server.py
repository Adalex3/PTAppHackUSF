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
    for frame, avg_pos, in_frame in real_generate_frames():
        latest_avg_pos = avg_pos
        print(avg_pos)
        with open('latest_avg_pos.json', 'w') as f:
            json.dump(avg_pos, f)
        with open('in_frame.json', 'w') as g:
            json.dump(in_frame, g)
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
CORS(app)  # Enable CORS for all routes

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
    if(random.random() < 0.3):
        return jsonify({'bigText': 'GREAT'},{'smallText': 'Keep stretching those calves!'},{'color': 'green'},{'textColor':'white'})
    elif (random.random() < 0.3):
        return jsonify({'bigText': 'FAIR'},{'smallText': 'Your posture is slipping.'},{'color': 'orange'},{'textColor':'white'})
    else:
        return jsonify({'bigText': 'STOP'},{'smallText': "You need to re-center yourself!"},{'color': 'red'},{'textColor':'white'})

    



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