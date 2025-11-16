"""
Data preprocessing utilities for e-commerce event data.
Converts raw events into training examples for next-item prediction.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from collections import defaultdict
import pickle


class DataPreprocessor:
    """Preprocesses e-commerce events for model training."""
    
    def __init__(self):
        self.item_to_idx = {}
        self.idx_to_item = {}
        self.num_items = 0
    
    def build_vocabulary(self, items: List[int]):
        """Build item ID to index mapping."""
        unique_items = sorted(set(items))
        # Reserve 0 for padding
        self.item_to_idx = {item: idx + 1 for idx, item in enumerate(unique_items)}
        self.idx_to_item = {idx + 1: item for idx, item in enumerate(unique_items)}
        self.idx_to_item[0] = 0  # Padding
        self.num_items = len(unique_items) + 1  # +1 for padding
        
        print(f"Built vocabulary with {self.num_items} items (including padding)")
    
    def process_events(
        self,
        csv_path: str,
        min_cart_size: int = 1,
        max_cart_size: int = 20
    ) -> Tuple[List[List[int]], List[int], List[int]]:
        """
        Process events CSV into training examples.
        
        Returns:
            carts: list of carts (each cart is a list of item indices)
            next_items: list of next item indices (labels)
            visitor_ids: list of visitor IDs for each example
        """
        print(f"Loading events from {csv_path}...")
        df = pd.read_csv(csv_path)
        print(f"Loaded {len(df)} events")
        
        # Build vocabulary from all items
        all_items = df['itemid'].unique().tolist()
        self.build_vocabulary(all_items)
        
        # Group events by visitor to create sessions
        print("Creating session-based training examples...")
        carts = []
        next_items = []
        visitor_ids = []
        
        for visitor_id, group in df.groupby('visitorid'):
            # Sort by timestamp
            group = group.sort_values('timestamp')
            
            # Get sequence of items (only addtocart and view events)
            items = group['itemid'].tolist()
            
            # Create training examples: for each position, use previous items as cart
            for i in range(min_cart_size, len(items)):
                cart = items[max(0, i - max_cart_size):i]
                next_item = items[i]
                
                # Convert to indices
                cart_indices = [self.item_to_idx.get(item, 0) for item in cart]
                next_item_idx = self.item_to_idx.get(next_item, 0)
                
                if next_item_idx > 0:  # Skip if next item not in vocabulary
                    carts.append(cart_indices)
                    next_items.append(next_item_idx)
                    visitor_ids.append(visitor_id)
        
        print(f"Created {len(carts)} training examples")
        return carts, next_items, visitor_ids
    
    def pad_carts(
        self,
        carts: List[List[int]],
        max_length: int = 20
    ) -> np.ndarray:
        """Pad carts to same length."""
        padded = np.zeros((len(carts), max_length), dtype=np.int64)
        
        for i, cart in enumerate(carts):
            length = min(len(cart), max_length)
            padded[i, :length] = cart[-length:]  # Take last max_length items
        
        return padded
    
    def save_vocabulary(self, path: str):
        """Save vocabulary mappings."""
        vocab = {
            'item_to_idx': self.item_to_idx,
            'idx_to_item': self.idx_to_item,
            'num_items': self.num_items
        }
        with open(path, 'wb') as f:
            pickle.dump(vocab, f)
        print(f"Saved vocabulary to {path}")
    
    def load_vocabulary(self, path: str):
        """Load vocabulary mappings."""
        with open(path, 'rb') as f:
            vocab = pickle.load(f)
        self.item_to_idx = vocab['item_to_idx']
        self.idx_to_item = vocab['idx_to_item']
        self.num_items = vocab['num_items']
        print(f"Loaded vocabulary with {self.num_items} items")


def compute_item_popularity(carts: List[List[int]], num_items: int) -> Dict[int, float]:
    """Compute popularity scores for items (for baseline)."""
    item_counts = defaultdict(int)
    total = 0
    
    for cart in carts:
        for item in cart:
            if item > 0:  # Skip padding
                item_counts[item] += 1
                total += 1
    
    # Normalize to probabilities
    popularity = {item: count / total for item, count in item_counts.items()}
    return popularity
