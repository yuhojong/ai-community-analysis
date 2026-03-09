#!/bin/bash

# Ensure we are in the project root
cd "$(dirname "$0")"

echo "Cleaning up any existing processes on ports 8000 and 3000..."
for port in 8000 3000; do
    pids=$(lsof -t -i:$port 2>/dev/null)
    if [ ! -z "$pids" ]; then
        echo "Killing existing process on port $port..."
        kill -9 $pids 2>/dev/null || true
    fi
done

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

# Ensure .env exists before starting services
if [ ! -f ".env" ]; then
    echo "Generating .env file..."
    python3 -c "import backend.database"
fi

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
cd ..

# Handle shutdown
cleanup() {
    echo "Shutting down servers..."
    kill $BACKEND_PID $SCHEDULER_PID $FRONTEND_PID 2>/dev/null || true

    # Kill any lingering processes on ports 8000 and 3000
    for port in 8000 3000; do
        pids=$(lsof -t -i:$port 2>/dev/null)
        if [ ! -z "$pids" ]; then
            kill -9 $pids 2>/dev/null || true
        fi
    done
    exit
}

trap cleanup INT TERM EXIT

echo ""
echo "=========================================================="
echo "Servers are running in the background."
echo "You can now enter commands in this terminal (e.g., to create an admin account)."
echo "To stop the servers and exit, type 'exit' or press Ctrl+D."
echo "=========================================================="
echo ""

# Start an interactive bash session
bash
