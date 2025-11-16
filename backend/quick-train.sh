#!/bin/bash
# Quick training script for backend model

cd "$(dirname "$0")"

source .venv/bin/activate

echo "=== Quick Model Training ==="
echo ""
echo "This will train a model on 5% of the data for 3 epochs (~2-5 minutes)"
echo ""

python train.py --epochs 3 --sample-frac 0.05 --batch-size 512

echo ""
echo "=== Training Complete ==="
echo ""
echo "Model saved to: models/best_model.pt"
echo "Vocabulary saved to: models/vocabulary.pkl"
echo ""
echo "To start the API server:"
echo "  python api.py"
echo ""
echo "To train on more data:"
echo "  python train.py --epochs 10 --sample-frac 0.2  # 20% of data"
echo "  python train.py --epochs 10                    # Full data (1-2 hours)"
