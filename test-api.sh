#!/bin/bash
# Test script to verify the backend API is working

echo "=== Testing Backend API ==="
echo ""

# Check if backend is running
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "❌ Backend is not running"
    echo ""
    echo "Start the backend first:"
    echo "  cd backend"
    echo "  source .venv/bin/activate"
    echo "  python api.py"
    exit 1
fi

echo "✓ Backend is running"
echo ""

# Test health endpoint
echo "1. Testing /health endpoint..."
curl -s http://localhost:8000/health | python3 -m json.tool
echo ""

# Test prediction endpoint with sample cart
echo "2. Testing /predict endpoint with sample cart..."
curl -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "cart": [
      {"product_id": "123", "quantity": 1},
      {"product_id": "456", "quantity": 2}
    ],
    "top_k": 5
  }' | python3 -m json.tool
echo ""

# Test stats endpoint
echo "3. Testing /stats endpoint..."
curl -s http://localhost:8000/stats | python3 -m json.tool
echo ""

echo "=== All Tests Complete ==="
