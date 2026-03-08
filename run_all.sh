#!/bin/bash

# 1. Start backend server
echo "Starting FastAPI backend..."
PYTHONPATH=. uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

# 2. Start scheduler in background
echo "Starting scheduler..."
PYTHONPATH=. python3 backend/scheduler.py &

# 3. Start frontend
echo "Starting React frontend..."
cd frontend && npm start &

wait
