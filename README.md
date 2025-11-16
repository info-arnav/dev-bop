# Dev Dashboard AI - Complete Setup Guide

AI-driven dashboard that predicts the next product a user will purchase based on their shopping cart.

## Project Structure

```
dev/
├── backend/          # Python PyTorch model training & FastAPI server
│   ├── .venv/       # Python virtual environment
│   ├── models/      # Saved model checkpoints
│   ├── api.py       # FastAPI server
│   ├── model.py     # PyTorch model definitions
│   ├── train.py     # Training script
│   └── preprocess.py
├── frontend/         # React + Vite dashboard (formerly dev-dashboard-ai)
│   └── src/
├── data/            # Training data
│   └── events.csv   # E-commerce events (2.7M rows)
└── start-dev.sh     # Start both backend and frontend
```

## Quick Start

### 1. Backend Setup (Python + PyTorch)

```bash
cd backend
bash setup.sh
```

This creates a virtual environment at `backend/.venv` and installs all dependencies.

### 2. Train the Model

Quick test (5% of data, ~2-5 minutes):
```bash
cd backend
source .venv/bin/activate
python train.py --epochs 3 --sample-frac 0.05 --batch-size 512
```

Full training (100% of data, ~1-2 hours):
```bash
python train.py --epochs 10
```

The trained model will be saved to `backend/models/best_model.pt`.

### 3. Start Everything

From the project root:

```bash
chmod +x start-dev.sh
./start-dev.sh
```

This will:
- Start the FastAPI backend on `http://localhost:8000`
- Start the Vite frontend on `http://localhost:8080`
- Wait for you to press Ctrl+C to stop both

Or manually:

**Terminal 1 - Backend:**
```bash
cd backend
source .venv/bin/activate
python api.py
# or: uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install  # first time only
npm run dev
```

### 4. Use the Dashboard

1. Open `http://localhost:8080` in your browser
2. Click the "Shop" tab
3. Add products to your cart using the "Add to Cart" buttons
4. Watch the **AI-Powered Next Purchase Predictions** section update automatically
5. The model shows the top 10 products the user is most likely to purchase next, with confidence scores

## API Endpoints

### POST /predict
Get next-item predictions based on cart.

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "cart": [
      {"product_id": "123", "quantity": 1},
      {"product_id": "456", "quantity": 2}
    ],
    "top_k": 10
  }'
```

Response:
```json
{
  "next_item_predictions": [
    {
      "product_id": "789",
      "probability": 0.234,
      "score": 0.234
    },
    ...
  ]
}
```

### GET /health
Check API and model status.

```bash
curl http://localhost:8000/health
```

### GET /docs
Interactive API documentation (Swagger UI):
```
http://localhost:8000/docs
```

## Development

### Backend

**Activate virtual environment:**
```bash
cd backend
source .venv/bin/activate
```

**Run with auto-reload:**
```bash
uvicorn api:app --reload
```

**Retrain with different hyperparameters:**
```bash
python train.py \
  --epochs 10 \
  --embedding-dim 256 \
  --hidden-dim 512 \
  --batch-size 256 \
  --lr 0.001
```

### Frontend

**Install dependencies:**
```bash
cd frontend
npm install
```

**Run dev server:**
```bash
npm run dev
```

**Build for production:**
```bash
npm run build
npm run preview
```

**Change API URL:**
Edit `frontend/.env`:
```
VITE_API_URL=http://localhost:8000
```

## Model Details

**Architecture:**
- Embedding-based next-item predictor
- 128-dim item embeddings by default
- Mean-pooling over cart items
- 2-layer MLP with dropout
- ~90M parameters (for 235K vocabulary)

**Training Data:**
- 2.7M e-commerce events (views, addtocart)
- ~1.3M sessions from unique visitors
- Creates 1.3M training examples (cart → next_item pairs)

**Metrics:**
- Top-1, Top-5, Top-10 accuracy
- Model tracks validation loss across epochs
- Best model saved based on validation loss

**Performance:**
- Training: ~5-10 minutes for 5% sample, ~1-2 hours full data (CPU)
- Inference: <50ms per prediction
- GPU acceleration automatic if available

## Files Generated

After training:
```
backend/
└── models/
    ├── best_model.pt      # Best model checkpoint (saved during training)
    ├── final_model.pt     # Final model after all epochs
    └── vocabulary.pkl     # Item ID → index mappings
```

## Troubleshooting

**"Model not loaded" error:**
- Make sure you've trained the model first: `python train.py`
- Check that `backend/models/best_model.pt` exists

**CORS errors in browser:**
- The backend allows all origins in dev mode
- For production, update CORS settings in `backend/api.py`

**Frontend can't connect to backend:**
- Check backend is running: `curl http://localhost:8000/health`
- Verify `.env` file has correct `VITE_API_URL`
- Check browser console for errors

**Training takes too long:**
- Use `--sample-frac 0.1` for 10% of data
- Reduce `--epochs` to 3-5
- Increase `--batch-size` to 512 or 1024

**Out of memory during training:**
- Reduce `--batch-size` to 128 or 64
- Use `--sample-frac` to train on less data
- Close other applications

## Next Steps

1. **Improve model:**
   - Try different architectures (RNN, Transformer)
   - Add user embeddings for personalization
   - Incorporate item features (category, price)

2. **Add co-purchase predictions:**
   - Implement association rules
   - Train CoPurchasePredictor model
   - Show in frontend UI

3. **Production deployment:**
   - Containerize with Docker
   - Add model versioning
   - Set up monitoring and logging
   - Add authentication

4. **Frontend enhancements:**
   - Show product names/images from catalog
   - Add recommendation explanations
   - Real-time A/B testing UI
   - Performance analytics dashboard

## Tech Stack

**Backend:**
- Python 3.12+
- PyTorch 2.9+
- FastAPI
- Pandas, NumPy, scikit-learn

**Frontend:**
- React 18
- TypeScript
- Vite
- Tailwind CSS
- shadcn/ui components

**Data:**
- CSV format (timestamp, visitorid, event, itemid, transactionid)
- 2.7M events, 235K unique products

## License

This is a demo project for educational purposes.
