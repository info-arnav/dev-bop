# Quick Start Guide - Instacart Prediction System

## Check Training Status

Training is currently running in the background. To monitor progress:

```bash
# Check if training is still running
ps aux | grep train_instacart | grep -v grep

# View training output in real-time
tail -f backend/training.log

# View last 50 lines
tail -50 backend/training.log
```

## After Training Completes

### 1. Verify Model Created
```bash
ls -lh backend/models/best_model.pt
```

### 2. Start Backend API
```bash
cd backend
.venv/bin/python api.py
```

The API will start on `http://localhost:8000`

### 3. Start Frontend (in new terminal)
```bash
cd frontend
npm run dev
```

The frontend will start on `http://localhost:5173`

## Test the System

1. **Open the app**: Navigate to `http://localhost:5173`

2. **Browse Products**:
   - Use the "Shop" tab
   - Search for products (e.g., "cookies", "milk", "banana")
   - Filter by Department (e.g., "snacks", "dairy eggs")
   - Filter by Aisle (e.g., "cookies cakes", "yogurt")

3. **Add Items to Cart**:
   - Click "Add to Cart" on several products
   - Watch the AI predictions appear automatically

4. **View Predictions**:
   - See top 10 predicted next purchases
   - Each prediction shows:
     - Product name
     - Department (highlighted)
     - Aisle
     - Probability score

5. **Check Analytics**:
   - Switch to "Analytics" tab
   - View dataset statistics
   - See model information

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Get Products
```bash
# All products (paginated)
curl "http://localhost:8000/products?page=1&page_size=20"

# Search products
curl "http://localhost:8000/products?search=chocolate"

# Filter by department
curl "http://localhost:8000/products?department=snacks"

# Filter by aisle
curl "http://localhost:8000/products?aisle=cookies%20cakes"
```

### Get Predictions
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "cart": [
      {"product_id": "24852", "quantity": 1},
      {"product_id": "13176", "quantity": 2}
    ],
    "top_k": 10
  }'
```

## Expected Results

### Training (when complete)
- **Training Time**: ~20-30 minutes for 5 epochs
- **Top-1 Accuracy**: 20-30%
- **Top-10 Accuracy**: 50-70%
- **Model Size**: ~35.6M parameters

### Predictions
- Real product names (e.g., "Chocolate Sandwich Cookies")
- Meaningful departments (e.g., "snacks", "dairy eggs", "produce")
- Specific aisles (e.g., "cookies cakes", "yogurt", "fresh vegetables")
- Strong sequential patterns (grocery shopping has repeat purchases)

## Troubleshooting

### Training Taking Too Long?
Training 5 epochs on 5.1M examples can take 20-30 minutes on CPU. Check progress:
```bash
tail -f backend/training.log
```

### API Won't Start?
Make sure training has completed and model file exists:
```bash
ls -lh backend/models/best_model.pt
```

### Frontend Build Issues?
Rebuild if needed:
```bash
cd frontend
npm run build
```

### No Predictions Showing?
1. Check API is running on port 8000
2. Check browser console for errors
3. Verify cart has items added
4. Check API health: `curl http://localhost:8000/health`

## Dataset Info

- **49,688** grocery products
- **21** departments (dairy, produce, snacks, etc.)
- **134** aisles (yogurt, cookies, fresh vegetables, etc.)
- **3.4M** orders
- **32M** order-product pairs

## File Structure

```
backend/
├── models/
│   ├── best_model.pt         # Trained model (created after training)
│   ├── vocabulary.pkl         # 49,678 items ✅
│   └── all_products.json      # 49,688 products ✅
├── api.py                     # FastAPI server ✅
├── train_instacart.py         # Training script (running)
└── training.log               # Training output

frontend/
├── src/
│   ├── components/            # All updated for Instacart ✅
│   └── pages/                 # Dashboard updated ✅
└── dist/                      # Built frontend ✅
```

## Performance Tips

### For Faster Training (Optional)
If you have a GPU and want faster training:
```bash
# Install CUDA-enabled PyTorch
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

### For Production
1. Build frontend for production: `npm run build`
2. Serve with nginx or similar
3. Configure CORS properly in `api.py`
4. Use gunicorn/uvicorn workers for API
5. Add caching for products endpoint

## What's Different from E-commerce Dataset

| Aspect | E-commerce | Instacart |
|--------|-----------|-----------|
| Products | 78,066 | 49,688 |
| Product Info | brand, price, category | name, aisle, department |
| Dataset Size | 67.5M events | 32M order-product pairs |
| Categories | 127 | 21 departments, 134 aisles |
| Expected Accuracy | 1% (random browsing) | 20-30% (repeat purchases) |
| Use Case | Electronics browsing | Grocery shopping |

## Next Steps

Once training completes and you've tested the system:

1. **Analyze Results**:
   - Check which products are commonly predicted together
   - Analyze prediction accuracy by department
   - Look at common shopping patterns

2. **Improve Model**:
   - Train on 100% of data (currently 20%)
   - Experiment with larger hidden dimensions
   - Try adding department/aisle embeddings
   - Add user features if available

3. **Enhance Frontend**:
   - Add product images
   - Show "frequently bought together"
   - Add shopping list functionality
   - Display prediction confidence visually

4. **Productionize**:
   - Add user authentication
   - Store cart in database
   - Track prediction accuracy in production
   - A/B test different models
