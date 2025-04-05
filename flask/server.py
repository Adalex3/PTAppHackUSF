from flask import Flask, render_template, Response
from start import generate_frames
app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, Flask!'

@app.route('/video')
def load_video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, port=5001)