from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from start import generate_frames as real_generate_frames
import json
import os
import random
import cv2

latest_avg_pos = None

def generate_frames():
    global latest_avg_pos
    for frame, avg_pos, in_frame in real_generate_frames():
        latest_avg_pos = avg_pos
        #print(avg_pos)
        with open('latest_avg_pos.json', 'w') as f:
            json.dump(avg_pos, f)
        with open('in_frame.json', 'w') as g:
            json.dump(in_frame, g)
        yield frame

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

    # Ensure the recordings directory exists.
    os.makedirs('recordings', exist_ok=True)

    print("RECORDING END555")
    
    # Determine frame dimensions from the first recorded frame.
    height, width, _ = frames[0].shape
    # Define codec and create VideoWriter (using 20 FPS here)
    out = cv2.VideoWriter('recordings/output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 20, (width, height))

    print("RECORDING END666")
    
    for frame in frames:
        print("RECORDING END7777")
        out.write(frame)
    out.release()
    print("RECORDING END888")

    # Clear the recorded frames list.
    start.recorded_frames = []
    
    return jsonify({'status': 'recording saved', 'file': 'recordings/output.mp4'})
    

if __name__ == '__main__':
    app.run(debug=True, port=5001)