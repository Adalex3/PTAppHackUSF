from flask import Flask, Response, request, jsonify
from start import generate_frames
app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, Flask!'

# Returns the altered video
@app.route('/video')
def load_video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('is_in_frame')
def is_in_frame():
    # Checks whether all joints are visible in the frame (if parts of their body are obscured or not). Returns true or false.
    return jsonify({'in_frame': False}) # Default


@app.route('/set_pose', methods=['POST'])
def set_pose():
    data = request.get_json()
    pose = data.get('pose')
    # Tells the python backend what pose the user is attempting to do, as this is received from frontend
    return jsonify({'status': 'error'}) # Default return

@app.route('pose_feedback')
def pose_data():
    # Returns a big JSON with lots of data about the user's movements. Has all of the pose data that the backend gets to be processed by frontend
    # This should return the position and angle and other info about every joint, for the frontend to process
    return jsonify({'status':'error'}) # Default return

    

if __name__ == '__main__':
    app.run(debug=True, port=5001)