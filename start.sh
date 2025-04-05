#!/bin/bash

# Navigate to Flask folder and run Flask server
cd flask
echo "Starting Flask server..."
python server.py &
FLASK_PID=$!
cd ..

# Navigate to React app and start it
cd react/pt-app
echo "Starting React app..."
npm start &
REACT_PID=$!
cd ../..

# Trap Ctrl+C and kill background processes
trap "kill $FLASK_PID $REACT_PID" EXIT

# Wait for both processes to complete
wait