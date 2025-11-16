# 🛒 Next-Item Prediction System

AI-powered recommendation system that predicts the next product a customer will add to their cart based on their current shopping behavior. Built with PyTorch and deployed with FastAPI + React.

## 🎯 Features

- **Deep Learning Model**: 4.3M parameter neural network trained on 14M+ real grocery shopping sequences
- **High Accuracy**: 34% top-10 accuracy, 23% top-5 accuracy on Instacart dataset
- **Real-time Predictions**: Fast inference via FastAPI endpoint
- **Interactive Dashboard**: React-based UI for visualizing predictions
- **Production Ready**: Organized codebase with proper structure and documentation

## 📊 Model Performance

Trained on 1,094 high-frequency grocery products from Instacart dataset:
- **Top-1 Accuracy**: 6.12%
- **Top-5 Accuracy**: 23.00%
- **Top-10 Accuracy**: 34.21%
- **Model Size**: 16MB
- **Training Data**: 14.2M shopping sequences from 204K users

## 🏗️ Project Structure

```
dev/
├── backend/
│   ├── api.py                    # FastAPI server with /predict endpoint
│   ├── model.py                  # PyTorch model architecture
│   ├── train_instacart.py        # Main training script
│   ├── scripts/                  # Utility scripts
│   │   ├── generate_vocab_instacart.py
│   │   ├── generate_all_products.py
│   │   └── train.py (legacy)
│   ├── data_processing/          # Data preprocessing
│   │   ├── preprocess_instacart.py
│   │   └── preprocess.py (legacy)
│   └── models/                   # Saved model checkpoints
│       ├── best_model.pt         # Trained model (16MB)
│       ├── vocabulary.pkl        # Item vocabulary
│       └── all_products.json     # Product metadata
├── frontend/                     # React dashboard
│   └── src/
│       ├── components/
│       └── pages/
├── data/                         # Instacart dataset (not in repo)
└── LICENSE                       # MIT License
```

## 🚀 Quick Start

### 1. Backend Setup

```bash
cd backend
bash setup.sh  # Creates .venv and installs dependencies
```

### 2. Run the API Server

```bash
cd backend
source .venv/bin/activate
python api.py
```

API will be available at `http://localhost:8000`

### 3. Frontend Setup & Run

```bash
cd frontend
npm install  # First time only
npm run dev
```

Frontend will be available at `http://localhost:5173`

## 📡 API Endpoints

### POST `/predict`
Get next-item predictions based on current cart.

**Request:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "product_ids": [24852, 13176, 21137],
    "top_k": 10
  }'
```

**Response:**
```json
{
  "predictions": [
    {
      "product_id": 21903,
      "name": "Organic Hass Avocado",
      "aisle": "fresh fruits",
      "department": "produce",
      "score": 0.0234
    },
    ...
  ]
}
```

### GET `/products`
Get all available products in the model vocabulary.

```bash
curl http://localhost:8000/products
```

### GET `/health`
Check API and model status.

```bash
curl http://localhost:8000/health
```

### GET `/docs`
Interactive API documentation (Swagger UI):
```
http://localhost:8000/docs
```

## 🔧 Training Your Own Model

### Prerequisites
Download the Instacart dataset from [Kaggle](https://www.kaggle.com/c/instacart-market-basket-analysis/data) and place CSV files in `data/instacart/` directory.

### Generate Vocabulary
```bash
cd backend
source .venv/bin/activate
python scripts/generate_vocab_instacart.py
python scripts/generate_all_products.py
```

### Train Model
```bash
python train_instacart.py
```

Training hyperparameters (in `train_instacart.py`):
- **Embedding Dimension**: 512
- **Hidden Dimension**: 1024
- **Batch Size**: 4096
- **Epochs**: 8
- **Learning Rate**: 0.001
- **Product Threshold**: 5000+ occurrences

Training takes ~25 minutes per epoch on M-series Mac with MPS acceleration.

## 🏛️ Architecture

### Model
- **Type**: Deep MLP with residual connections
- **Input**: Variable-length cart (padded to 20 items)
- **Embedding**: 512-dimensional product embeddings
- **Hidden Layers**: 3 layers with [1024, 512, 512] dimensions
- **Output**: Softmax over 1,094 products
- **Regularization**: BatchNorm + 0.4 Dropout
- **Parameters**: 4.3M

### Data Processing
1. Filter products by frequency (5000+ occurrences)
2. Create sliding windows from order sequences
3. Convert product IDs to vocabulary indices
4. Pad carts to fixed length (20 items)
5. 80/20 train/validation split

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

## 📧 Contact

Arnav Gupta - [@info-arnav](https://github.com/info-arnav)

Project Link: [https://github.com/info-arnav/dev-bop](https://github.com/info-arnav/dev-bop)

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
