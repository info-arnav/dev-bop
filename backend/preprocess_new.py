"""
Data preprocessing utilities for e-commerce event data (new format).
Converts raw events into training examples for next-item prediction.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from collections import defaultdict
import pickle
import json


class DataPreprocessor:
    """Preprocesses e-commerce events for model training."""
    
    def __init__(self):
        self.item_to_idx = {}
        self.idx_to_item = {}
        self.num_items = 0
        self.product_info = {}  # Store product metadata
    
    def build_vocabulary(self, df: pd.DataFrame):
        """Build item ID to index mapping and extract product info."""
        print("Building vocabulary and extracting product metadata...")
        
        # Get unique products with their info
        product_df = df.groupby('product_id').agg({
            'brand': 'first',
            'price': 'mean',  # Average price if it varies
            'category_code': 'first',
            'category_id': 'first'
        }).reset_index()
        
        unique_items = sorted(product_df['product_id'].unique())
        
        # Reserve 0 for padding
        self.item_to_idx = {item: idx + 1 for idx, item in enumerate(unique_items)}
        self.idx_to_item = {idx + 1: item for idx, item in enumerate(unique_items)}
        self.idx_to_item[0] = 0  # Padding
        self.num_items = len(unique_items) + 1  # +1 for padding
        
        # Store product info
        for _, row in product_df.iterrows():
            product_id = row['product_id']
            self.product_info[int(product_id)] = {
                'brand': str(row['brand']) if pd.notna(row['brand']) else '',
                'price': float(row['price']) if pd.notna(row['price']) else 0.0,
                'category_code': str(row['category_code']) if pd.notna(row['category_code']) else '',
                'category_id': int(row['category_id']) if pd.notna(row['category_id']) else 0
            }
        
        print(f"Built vocabulary with {self.num_items} items (including padding)")
        print(f"Stored metadata for {len(self.product_info)} products")
    
    def process_events(
        self,
        csv_path: str,
        min_cart_size: int = 1,
        max_cart_size: int = 20,
        sample_frac: float = 0.01  # Sample 1% by default (67M rows is huge!)
    ) -> Tuple[List[List[int]], List[int], List[int]]:
        """
        Process events CSV into training examples.
        
        Returns:
            carts: list of carts (each cart is a list of item indices)
            next_items: list of next item indices (labels)
            user_ids: list of user IDs for each example
        """
        print(f"Loading events from {csv_path}...")
        print(f"Sampling {sample_frac*100}% of data...")
        
        # Read CSV with sampling
        df = pd.read_csv(csv_path)
        if sample_frac < 1.0:
            df = df.sample(frac=sample_frac, random_state=42)
        
        print(f"Loaded {len(df)} events")
        
        # Build vocabulary from sampled data
        self.build_vocabulary(df)
        
        # Group events by user to create sessions
        print("Creating session-based training examples...")
        carts = []
        next_items = []
        user_ids = []
        
        # Sort by user and timestamp
        df = df.sort_values(['user_id', 'event_time'])
        
        for user_id, group in df.groupby('user_id'):
            # Get sequence of items
            items = group['product_id'].tolist()
            
            # Skip very short sessions
            if len(items) < min_cart_size + 1:
                continue
            
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
                    user_ids.append(user_id)
        
        print(f"Created {len(carts)} training examples")
        return carts, next_items, user_ids
    
    def save_vocabulary(self, path: str):
        """Save vocabulary to pickle file."""
        vocab_data = {
            'item_to_idx': self.item_to_idx,
            'idx_to_item': self.idx_to_item,
            'num_items': self.num_items,
            'product_info': self.product_info
        }
        with open(path, 'wb') as f:
            pickle.dump(vocab_data, f)
        print(f"Saved vocabulary to {path}")
    
    def load_vocabulary(self, path: str):
        """Load vocabulary from pickle file."""
        with open(path, 'rb') as f:
            vocab_data = pickle.load(f)
        self.item_to_idx = vocab_data['item_to_idx']
        self.idx_to_item = vocab_data['idx_to_item']
        self.num_items = vocab_data['num_items']
        self.product_info = vocab_data.get('product_info', {})
        print(f"Loaded vocabulary with {self.num_items} items")
