#!/bin/bash
# Setup script for backend - creates venv and installs dependencies

set -e

echo "=== Setting up Python Backend ==="

# Check Python version
python3 --version

# Create virtual environment
echo -e "\n1. Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment
echo -e "\n2. Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo -e "\n3. Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo -e "\n4. Installing dependencies..."
pip install torch pandas numpy scikit-learn fastapi uvicorn pydantic python-multipart tqdm

echo -e "\n=== Setup Complete ==="
echo "Virtual environment created at: backend/.venv"
echo ""
echo "To activate the virtual environment:"
echo "  cd backend"
echo "  source .venv/bin/activate"
echo ""
echo "To train the model:"
echo "  python train.py --epochs 5 --sample-frac 0.1  # Quick test with 10% of data"
echo "  python train.py --epochs 10  # Full training"
echo ""
echo "To start the API server:"
echo "  python api.py"
echo "  # or use: uvicorn api:app --reload --host 0.0.0.0 --port 8000"
