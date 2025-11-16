# Welcome to your this project

## Project info

# Dev Dashboard AI

An AI-driven dashboard that predicts the next product a user will purchase based on their current cart and estimates probabilities of buying groups of products together.

This repository contains a React + Vite dashboard and the scaffolding to train and evaluate a model that predicts next-item recommendations and co-purchase probabilities.

## Quick overview

- Input: a user's current shopping cart (list of product IDs, quantities, and optionally features like categories or prices).
- Output: a ranked list of candidate next-items with purchase probability, and probability distributions for common item sets (items likely to be bought together).
- UX: the dashboard shows predictions in real time; when the cart is updated, the probabilities refresh and the UI updates.

## Project contract (simple)

- Model input: { cart: [{ product_id: string, quantity: number }], user_id?: string, context?: { time_of_day?: string, device?: string } }
- Model output: {
  next_item_predictions: [{ product_id: string, probability: number, score?: number }],
  co_purchase: [{ items: [product_id], probability: number }]
  }
- Error modes: empty cart -> return top-popular defaults; missing product ids -> validation error; model unavailable -> fallback to popularity baseline.

## Key features

- Real-time UI that recalculates and shows next-item probabilities as cart changes.
- Batch training pipeline for building next-item and co-purchase models.
- Simple REST/HTTP or local prediction endpoint used by the dashboard.

## Repo structure (high level)

- `src/` — front-end React app (dashboard, components, hooks).
- `model/` — (suggested) training scripts, notebooks, dataset schema (create if missing).
- `data/` — (suggested) raw and processed datasets (not committed to git if large).
- `scripts/` — helper scripts (preprocessing, evaluation, packaging).
- `README.md` — this file.

Adjust paths above if you keep training code elsewhere.

## Data format / schema

Recommended CSV format (one row per event or cart snapshot):

- Columns:
  - user_id
  - timestamp (ISO 8601)
  - cart_items (JSON string or pipe-separated list of product_id:qty)
  - next_item (product_id) — label for supervised training
  - features (optional JSON with device, category, price buckets)

Example row (CSV):

"u123", "2025-11-01T12:34:56Z", "[{\"product_id\":\"p1\",\"quantity\":1},{\"product_id\":\"p2\",\"quantity\":2}]", "p7", "{\"device\":\"mobile\"}"

Preprocessing steps:

1. Expand cart JSON into item IDs and encode as sequences (or bags) depending on model.
2. Generate training examples by sliding over sessions to create (cart -> next_item) pairs.
3. Generate co-purchase labels by counting itemsets that appear together within sessions/orders.

## Model ideas

- Simple baselines:
  - Popularity baseline (top-k most-purchased items overall or per-category).
  - Frequent itemset / association rules (Apriori) to find co-purchase probabilities.
- ML models:
  - Gradient-boosted trees on aggregated cart features (LightGBM/XGBoost).
  - Sequence models (RNN, Transformer) treating cart as a sequence.
  - Embedding + dot-product retrieval (learn product embeddings with negative sampling).

## Training quick-start (recommended minimal setup)

1. Create a Python virtual environment and install packages (example):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # create this file with dependencies like pandas, scikit-learn, torch, lightgbm
```

2. Prepare your dataset in `data/` and run preprocessing:

```bash
python scripts/preprocess.py --input data/raw/events.csv --output data/processed/train.parquet
```

3. Train a quick baseline model:

```bash
python model/train_baseline.py --train data/processed/train.parquet --output model/baseline.pkl
```

4. Evaluate:

```bash
python model/evaluate.py --model model/baseline.pkl --test data/processed/test.parquet
```

Notes: Add or adapt the scripts above under `scripts/` and `model/` depending on your framework (scikit-learn, LightGBM, PyTorch, etc.).

## Serving & API

Create a small prediction API (Flask, FastAPI) that loads the trained model and exposes an endpoint like:

- POST /predict
  - Body: { cart: [{ product_id, quantity }], user_id?: string }
  - Response: model output described in the contract above.

Example using FastAPI:

```python
from fastapi import FastAPI
@app.post("/predict")
def predict(payload: dict):
		# load model once at startup
		return predict_from_cart(payload["cart"], payload.get("user_id"))
```

Have the front-end call this endpoint to fetch live predictions when the cart changes.

## Dashboard behavior

- The UI shows:

  - Current cart items
  - Top-N predicted next items with probabilities
  - Common co-purchase itemsets and their probabilities
  - Controls to add/remove items from cart — every update triggers a prediction refresh

- UX details:
  - Debounce cart edits (200-400ms) before calling the API to avoid flooding.
  - Show a small spinner or skeleton while predictions are fetched.
  - Fall back to popularity-based predictions if API fails.

## Development

- Install dependencies and run the app:

```bash
npm install
npm run dev
```

- Build for production:

```bash
npm run build
npm run preview
```

## Evaluation metrics

- For next-item prediction:
  - Top-k accuracy (e.g., whether true next item is in top-1/top-5/top-10)
  - Mean reciprocal rank (MRR)
  - Precision@k / Recall@k
- For co-purchase probabilities:
  - Calibration (reliability diagrams), AUC where appropriate, and precision/recall for high-probability sets.

## Edge cases and notes

- Empty carts: return personalized defaults (if user history exists) or global-popular items.
- Cold start users/products: use category-level or popularity fallbacks.
- Large carts: subsample or aggregate items into feature vectors to keep model input size reasonable.

## Next steps / roadmap

1. Add `model/` and `scripts/` folders with starter examples (preprocessing + a simple LightGBM baseline).
2. Add a `requirements.txt` and example notebooks for exploratory data analysis.
3. Add CI tests for model training scripts and front-end integration tests.
4. Add Dockerfiles for reproducible training and serving.

## How to contribute

- Open issues for feature requests or bugs.
- Create branches and PRs against `main`. Keep changes small and include tests where feasible.
