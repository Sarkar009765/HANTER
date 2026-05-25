#!/bin/bash
echo "Starting BRO-AI development environment..."

cd "$(dirname "$0")/.."

# Start Python backend
cd core
source venv/bin/activate
python main.py &
BACKEND_PID=$!
cd ..

# Start frontend
cd apps/desktop
npm run tauri-dev &
FRONTEND_PID=$!
cd ../..

echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "Press Ctrl+C to stop both"

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT
wait
