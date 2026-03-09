#!/bin/bash

# Ensure we are in the project root
cd "$(dirname "$0")"

# 1. Start backend server
echo "Starting FastAPI backend..."
PYTHONPATH=. uvicorn backend.main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 < /dev/null &
BACKEND_PID=$!

# 2. Start scheduler in background
echo "Starting scheduler..."
PYTHONPATH=. python3 backend/scheduler.py > scheduler.log 2>&1 < /dev/null &
SCHEDULER_PID=$!

# 3. Start frontend
echo "Starting React frontend..."
cd frontend
BROWSER=none npm start > ../frontend.log 2>&1 < /dev/null &
FRONTEND_PID=$!
cd ..

# Handle shutdown
trap "kill $BACKEND_PID $SCHEDULER_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM EXIT

echo ""
echo "=========================================================="
echo "Servers are running in the background."
echo "You can now enter commands in this terminal (e.g., to create an admin account)."
echo "To stop the servers and exit, type 'exit' or press Ctrl+D."
echo "=========================================================="
echo ""

# Start an interactive bash session
bash
