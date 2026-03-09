#!/bin/bash
cd frontend
FORCE_COLOR=1 npm start | cat &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"
sleep 10
kill $FRONTEND_PID
echo "Killed"
