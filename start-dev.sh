#!/bin/bash
# Start both backend API and frontend dev server

set -e

echo "=== Starting Dev Dashboard AI ==="

# Check if model exists
if [ ! -f "backend/models/best_model.pt" ]; then
    echo "⚠️  Warning: Model not found at backend/models/best_model.pt"
    echo "Please train the model first:"
    echo "  cd backend"
    echo "  source .venv/bin/activate"
    echo "  python train.py --epochs 5 --sample-frac 0.1"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Start backend in background
echo "Starting backend API server..."
cd backend
source .venv/bin/activate
python api.py > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

echo "Backend API started (PID: $BACKEND_PID)"
echo "Logs: backend.log"

# Wait for backend to be ready
echo "Waiting for backend to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✓ Backend is ready!"
        break
    fi
    sleep 1
    echo -n "."
done
echo ""

# Start frontend
echo "Starting frontend dev server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "=== Services Started ==="
echo "Backend API: http://localhost:8000"
echo "  Docs: http://localhost:8000/docs"
echo "  Health: http://localhost:8000/health"
echo ""
echo "Frontend: http://localhost:8080"
echo ""
echo "To stop all services:"
echo "  kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "Press Ctrl+C to stop all services"

# Handle Ctrl+C
trap "echo ''; echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT

# Wait for both processes
wait
