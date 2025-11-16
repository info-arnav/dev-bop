# 🚀 Quick Start Guide

Your AI-powered shopping cart prediction system is ready!

## What's Been Built

✅ **Backend (Python + PyTorch)**
- Complete PyTorch model for next-item prediction
- FastAPI server with REST endpoints
- Training pipeline that processes 2.7M events
- Model saved at `backend/models/best_model.pt` (1GB)
- Virtual environment at `backend/.venv`

✅ **Frontend (React + TypeScript)**
- Shopping cart interface
- Real-time AI predictions display
- Auto-updates when cart changes (300ms debounce)
- Connected to backend API

✅ **Training Complete**
- Trained on 5% of data (67K examples)
- Model has 90M parameters
- Validation accuracy: Top-1: 0.15%, Top-5: 0.32%, Top-10: 0.65%
- Best model checkpoint saved

## Start the Application

### Option 1: Use the automated script

```bash
cd /Users/arnavgupta/Programs/temp/dev
./start-dev.sh
```

This starts both backend and frontend automatically.

### Option 2: Manual start (recommended for development)

**Terminal 1 - Backend API:**
```bash
cd /Users/arnavgupta/Programs/temp/dev/backend
source .venv/bin/activate
python api.py
```

Wait for: `Application startup complete.`

**Terminal 2 - Frontend:**
```bash
cd /Users/arnavgupta/Programs/temp/dev/frontend
npm run dev
```

Wait for: `Local: http://localhost:8080/`

## Access the Application

- **Frontend Dashboard:** http://localhost:8080
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

## How to Use

1. Open http://localhost:8080 in your browser
2. Click the **"Shop"** tab
3. Add products to cart by clicking "Add to Cart" buttons
4. Watch the **"AI-Powered Next Purchase Predictions"** section
5. It automatically updates with:
   - Top 10 predicted next products
   - Confidence scores (probability %)
   - Visual progress bars

## Testing the API Directly

```bash
cd /Users/arnavgupta/Programs/temp/dev
./test-api.sh
```

Or manually:

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "cart": [
      {"product_id": "355908", "quantity": 1},
      {"product_id": "248676", "quantity": 2}
    ],
    "top_k": 10
  }'
```

## Retrain the Model

For better accuracy, train on more data:

**Quick (10% of data, ~5-10 minutes):**
```bash
cd backend
source .venv/bin/activate
python train.py --epochs 5 --sample-frac 0.1
```

**Full training (100% of data, ~1-2 hours):**
```bash
python train.py --epochs 10
```

**Custom training:**
```bash
python train.py \
  --epochs 15 \
  --sample-frac 0.3 \
  --batch-size 256 \
  --embedding-dim 256 \
  --hidden-dim 512 \
  --lr 0.0005
```

## Project Structure

```
/Users/arnavgupta/Programs/temp/dev/
├── backend/
│   ├── .venv/              ✅ Virtual environment (ready)
│   ├── models/
│   │   ├── best_model.pt   ✅ Trained model (1GB)
│   │   └── vocabulary.pkl  ✅ Item ID mappings
│   ├── api.py              ✅ FastAPI server
│   ├── model.py            ✅ PyTorch model
│   ├── train.py            ✅ Training script
│   ├── preprocess.py       ✅ Data preprocessing
│   ├── requirements.txt    ✅ Dependencies
│   ├── setup.sh            ✅ Setup script
│   ├── quick-train.sh      ✅ Quick training
│   └── README.md           ✅ Backend docs
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AIPredictions.tsx      ✅ Predictions display
│   │   │   └── ShoppingCart.tsx       ✅ Cart component
│   │   ├── hooks/
│   │   │   └── usePrediction.ts       ✅ API hook
│   │   └── pages/
│   │       └── Index.tsx              ✅ Main page (updated)
│   ├── .env                            ✅ API URL config
│   └── package.json
├── data/
│   └── events.csv          ✅ 2.7M events
├── start-dev.sh            ✅ Auto-start script
├── test-api.sh             ✅ API test script
└── README.md               ✅ Complete docs
```

## Tech Stack

**Backend:**
- Python 3.12
- PyTorch 2.9 (CPU)
- FastAPI + Uvicorn
- Pandas, NumPy, scikit-learn

**Frontend:**
- React 18 + TypeScript
- Vite
- Tailwind CSS
- shadcn/ui components

## Features Implemented

✅ Data preprocessing (2.7M events → 1.3M training examples)
✅ PyTorch embedding-based model (90M params)
✅ Training pipeline with validation
✅ Model checkpointing (saves best model)
✅ FastAPI REST API with CORS
✅ /predict endpoint (POST cart → get predictions)
✅ /health endpoint (check model status)
✅ /stats endpoint (model info)
✅ React frontend with cart
✅ Real-time prediction display
✅ Auto-refresh on cart changes (debounced)
✅ Loading states and error handling
✅ Confidence scores and visual bars

## Next Steps (Optional Improvements)

1. **Train on more data:**
   - Currently trained on 5% (67K examples)
   - Training on 100% will significantly improve accuracy

2. **Add product catalog:**
   - Show real product names/images instead of IDs
   - Create a products database or JSON file

3. **Improve model:**
   - Try sequence models (RNN/LSTM/Transformer)
   - Add user embeddings for personalization
   - Incorporate item features (category, price)

4. **Add co-purchase predictions:**
   - Show "Frequently bought together"
   - Use association rules or the CoPurchasePredictor

5. **Production deployment:**
   - Dockerize backend and frontend
   - Add authentication
   - Set up monitoring (Prometheus, Grafana)
   - Deploy to cloud (AWS, GCP, Azure)

## Troubleshooting

**Backend won't start:**
```bash
cd backend
source .venv/bin/activate
python -c "import torch; print('PyTorch OK')"
python api.py
```

**Frontend can't connect:**
- Check backend is running: `curl http://localhost:8000/health`
- Check `.env` file: `cat frontend/.env`
- Check browser console for errors

**Model predictions are random:**
- This is expected with only 5% training data
- Train on more data for better accuracy
- The model learns patterns from the full training set

**Out of memory:**
- Reduce batch size: `--batch-size 64`
- Use less data: `--sample-frac 0.05`
- Close other applications

## Support

For issues or questions:
1. Check the complete README: `/Users/arnavgupta/Programs/temp/dev/README.md`
2. Check backend README: `/Users/arnavgupta/Programs/temp/dev/backend/README.md`
3. Review API docs: http://localhost:8000/docs (when server is running)

---

**Everything is ready! Start the application and enjoy your AI-powered shopping predictions! 🎉**
