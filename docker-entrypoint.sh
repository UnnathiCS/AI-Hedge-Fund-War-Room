#!/bin/bash

# Start the FastAPI backend
echo "Starting FastAPI backend on port 8501..."
cd /app/debate_engine
python -m uvicorn api:app --host 0.0.0.0 --port 8501 &

# Wait a moment for backend to start
sleep 3

# Start the frontend
echo "Starting React frontend on port 5173..."
cd /app/Frontend_UI
npm run preview -- --host 0.0.0.0 --port 5173 &

# Keep container running
wait
