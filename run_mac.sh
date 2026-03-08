#!/bin/bash

# Ensure we are in the project root
cd "$(dirname "$0")"

# 1. Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# 2. Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# 3. Install dependencies
echo "Installing backend dependencies..."
pip install --upgrade pip
pip install -r backend/requirements.txt

# 4. Start backend server
echo "Starting FastAPI backend..."
PYTHONPATH=. uvicorn backend.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# 5. Start scheduler in background
echo "Starting scheduler..."
PYTHONPATH=. python3 backend/scheduler.py &
SCHEDULER_PID=$!

# 6. Start frontend
echo "Starting React frontend..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi
npm start &
FRONTEND_PID=$!

# Handle shutdown
trap "kill $BACKEND_PID $SCHEDULER_PID $FRONTEND_PID; exit" INT TERM
echo "Running... Press Ctrl+C to stop."
wait
