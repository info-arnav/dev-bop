# Backend - Next-Item Prediction Model

PyTorch-based model for predicting the next product a user will purchase based on their shopping cart.

## Quick Start

### 1. Set up virtual environment and install dependencies

```bash
cd backend
bash setup.sh
```

Or manually:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Train the model

Quick test with 10% of data:
```bash
source .venv/bin/activate
python train.py --epochs 5 --sample-frac 0.1
```

Full training (will take longer):
```bash
python train.py --epochs 10
```

Training options:
- `--data`: Path to events CSV (default: `../data/events.csv`)
- `--output-dir`: Where to save models (default: `./models`)
- `--embedding-dim`: Embedding size (default: 128)
- `--hidden-dim`: Hidden layer size (default: 256)
- `--batch-size`: Batch size (default: 256)
- `--epochs`: Number of epochs (default: 10)
- `--lr`: Learning rate (default: 0.001)
- `--max-cart-size`: Maximum cart size (default: 20)
- `--sample-frac`: Fraction of data to use (default: 1.0)

### 3. Start the API server

```bash
source .venv/bin/activate
python api.py
```

Or with uvicorn for auto-reload during development:
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

## Project Structure

```
backend/
├── .venv/              # Virtual environment (created by setup)
├── models/             # Saved model checkpoints (created by training)
│   ├── best_model.pt   # Best model checkpoint
│   ├── final_model.pt  # Final model checkpoint
│   └── vocabulary.pkl  # Item ID mappings
├── api.py              # FastAPI server
├── model.py            # PyTorch model definitions
├── preprocess.py       # Data preprocessing utilities
├── train.py            # Training script
├── requirements.txt    # Python dependencies
├── setup.sh            # Setup script
└── README.md           # This file
```

## API Endpoints

### POST /predict
Predict next items based on cart contents.

Request body:
```json
{
  "cart": [
    {"product_id": "12345", "quantity": 1},
    {"product_id": "67890", "quantity": 2}
  ],
  "user_id": "optional_user_id",
  "top_k": 10
}
```

Response:
```json
{
  "next_item_predictions": [
    {
      "product_id": "11111",
      "probability": 0.25,
      "score": 0.25
    },
    ...
  ],
  "co_purchase": []
}
```

### GET /health
Health check endpoint with model status.

### GET /stats
Model statistics (vocabulary size, parameters, etc.).

## Model Architecture

**NextItemPredictor**:
- Item embeddings (128-dim by default)
- Cart aggregation via mean pooling
- 2-layer MLP with dropout
- Softmax output over all items

**Training**:
- Loss: Cross-entropy
- Optimizer: Adam with learning rate scheduling
- Metrics: Top-1, Top-5, Top-10 accuracy

## Development

Activate environment:
```bash
source .venv/bin/activate
```

Run with auto-reload:
```bash
uvicorn api:app --reload
```

Test the API:
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"cart": [{"product_id": "12345", "quantity": 1}], "top_k": 5}'
```

## Notes

- The dataset has 2.7M events across ~1.3M unique visitors
- Training on full data may take 1-2 hours depending on hardware
- Use `--sample-frac` for quick testing
- Model checkpoints are saved in `models/` directory
- GPU acceleration is automatic if CUDA is available
