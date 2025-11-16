"""
FastAPI server for next-item prediction.
Loads trained PyTorch model and serves predictions via REST API.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import torch
import pickle
import os

from model import NextItemPredictor


# Pydantic models for API
class CartItem(BaseModel):
    product_id: str
    quantity: int = 1


class PredictRequest(BaseModel):
    cart: List[CartItem]
    user_id: Optional[str] = None
    top_k: int = Field(default=10, ge=1, le=50)


class PredictionItem(BaseModel):
    product_id: str
    probability: float
    score: float
    name: Optional[str] = None
    aisle: Optional[str] = None
    department: Optional[str] = None


class PredictResponse(BaseModel):
    next_item_predictions: List[PredictionItem]
    co_purchase: List[dict] = []  # Can be extended later


# Global model and vocabulary
model = None
vocabulary = None
device = None


def load_model_and_vocab(model_path: str = "./models/best_model.pt", vocab_path: str = "./models/vocabulary.pkl"):
    """Load trained model and vocabulary at startup."""
    global model, vocabulary, device
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # Load vocabulary
    print(f"Loading vocabulary from {vocab_path}...")
    with open(vocab_path, 'rb') as f:
        vocabulary = pickle.load(f)
    print(f"Loaded vocabulary with {vocabulary['num_items']} items")
    
    # Check if product_info exists in vocabulary
    if 'product_info' in vocabulary:
        print(f"Loaded product metadata for {len(vocabulary['product_info'])} products")
    
    # Load model checkpoint
    print(f"Loading model from {model_path}...")
    checkpoint = torch.load(model_path, map_location=device)
    
    # Create model with saved hyperparameters
    model = NextItemPredictor(
        num_items=checkpoint['num_items'],
        embedding_dim=checkpoint['embedding_dim'],
        hidden_dim=checkpoint['hidden_dim']
    )
    model.load_state_dict(checkpoint['model_state_dict'])
    model = model.to(device)
    model.eval()
    
    print(f"Model loaded successfully!")
    print(f"  Validation loss: {checkpoint.get('val_loss', 'N/A')}")
    if 'val_accuracy' in checkpoint:
        print(f"  Top-k accuracy: {checkpoint['val_accuracy']}")


# Create FastAPI app
app = FastAPI(
    title="Next-Item Prediction API",
    description="Predicts next product purchases based on shopping cart contents",
    version="1.0.0"
)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Load model when server starts."""
    try:
        load_model_and_vocab()
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Server will start but predictions will fail until model is loaded.")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "Next-Item Prediction API",
        "model_loaded": model is not None
    }


@app.get("/health")
async def health():
    """Detailed health check."""
    return {
        "status": "healthy" if model is not None else "unhealthy",
        "model_loaded": model is not None,
        "vocabulary_loaded": vocabulary is not None,
        "device": str(device) if device else None,
        "num_items": vocabulary['num_items'] if vocabulary else None
    }


@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    """
    Predict next items based on current cart.
    
    Args:
        request: PredictRequest with cart items and optional user_id
    
    Returns:
        PredictResponse with top-k predicted items and probabilities
    """
    if model is None or vocabulary is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Handle empty cart
    if not request.cart:
        # Return top popular items (first N items by index as fallback)
        top_items = list(range(1, min(request.top_k + 1, vocabulary['num_items'])))
        predictions = [
            PredictionItem(
                product_id=str(vocabulary['idx_to_item'].get(idx, idx)),
                probability=0.1,
                score=0.1
            )
            for idx in top_items
        ]
        return PredictResponse(next_item_predictions=predictions)
    
    # Convert cart product IDs to indices
    cart_indices = []
    for item in request.cart:
        try:
            # Try to convert product_id to int (since our data uses integer IDs)
            item_id = int(item.product_id)
            idx = vocabulary['item_to_idx'].get(item_id, 0)
            if idx > 0:  # Only add if item is in vocabulary
                cart_indices.append(idx)
        except (ValueError, KeyError):
            # Skip items not in vocabulary
            continue
    
    # If no valid items in cart after filtering, return popular items
    if not cart_indices:
        top_items = list(range(1, min(request.top_k + 1, vocabulary['num_items'])))
        predictions = [
            PredictionItem(
                product_id=str(vocabulary['idx_to_item'].get(idx, idx)),
                probability=0.1,
                score=0.1
            )
            for idx in top_items
        ]
        return PredictResponse(next_item_predictions=predictions)
    
    # Pad cart to model's expected length (max 20 items)
    max_cart_size = 20
    padded_cart = [0] * max_cart_size
    start_idx = max(0, len(cart_indices) - max_cart_size)
    for i, idx in enumerate(cart_indices[start_idx:]):
        padded_cart[i] = idx
    
    # Convert to tensor
    cart_tensor = torch.tensor([padded_cart], dtype=torch.long).to(device)
    
    # Get predictions
    with torch.no_grad():
        top_items, top_probs = model.predict_top_k(cart_tensor, k=request.top_k)
    
    # Convert to response format
    predictions = []
    product_info = vocabulary.get('product_info', {})
    
    for item_idx, prob in zip(top_items[0].cpu().numpy(), top_probs[0].cpu().numpy()):
        item_id = vocabulary['idx_to_item'].get(int(item_idx), int(item_idx))
        
        # Get product metadata if available
        metadata = product_info.get(item_id, {})
        
        predictions.append(
            PredictionItem(
                product_id=str(item_id),
                probability=float(prob),
                score=float(prob),
                name=metadata.get('name'),
                aisle=metadata.get('aisle'),
                department=metadata.get('department')
            )
        )
    
    return PredictResponse(next_item_predictions=predictions)


@app.get("/stats")
async def get_stats():
    """Get model statistics."""
    if model is None or vocabulary is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "num_items": vocabulary['num_items'],
        "vocabulary_size": len(vocabulary['item_to_idx']),
        "model_parameters": sum(p.numel() for p in model.parameters()),
    }


@app.get("/products")
async def get_products(
    search: Optional[str] = None,
    page: int = 1,
    page_size: int = 50,
    department: Optional[str] = None,
    aisle: Optional[str] = None,
    min_frequency: int = 500  # Only return products with 500+ occurrences
):
    """
    Get paginated product list with search and filters.
    Returns frequent grocery products (500+ occurrences) from the Instacart dataset.
    """
    # Load all products from JSON file
    products_file = "./models/all_products.json"
    if not os.path.exists(products_file):
        raise HTTPException(status_code=404, detail="Products file not found. Run generate_vocab_instacart.py first.")
    
    import json
    with open(products_file, 'r') as f:
        all_products = json.load(f)
    
    # Filter to only frequent products (those in the trained model)
    if vocabulary and 'item_to_idx' in vocabulary:
        # Only show products that are in the model's vocabulary
        valid_product_ids = set(vocabulary['item_to_idx'].keys())
        all_products = [p for p in all_products if int(p.get('id', 0)) in valid_product_ids]
    
    # Filter by search query
    if search:
        search_lower = search.lower()
        all_products = [
            p for p in all_products
            if search_lower in p.get('name', '').lower()
            or search_lower in p.get('aisle', '').lower()
            or search_lower in p.get('department', '').lower()
            or search_lower in str(p.get('id', ''))
        ]
    
    # Filter by department
    if department:
        all_products = [p for p in all_products if p.get('department', '').lower() == department.lower()]
    
    # Filter by aisle
    if aisle:
        all_products = [p for p in all_products if p.get('aisle', '').lower() == aisle.lower()]
    
    # Pagination
    total = len(all_products)
    start = (page - 1) * page_size
    end = start + page_size
    products = all_products[start:end]
    
    return {
        "products": products,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
        "has_more": end < total
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
