"""
Preprocess Instacart dataset for next-item prediction.
Dataset: orders.csv, products.csv, order_products__train.csv, order_products__prior.csv
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import pickle
import json
import os


class InstacartPreprocessor:
    """Preprocesses Instacart orders for model training."""
    
    def __init__(self):
        self.item_to_idx = {}
        self.idx_to_item = {}
        self.num_items = 0
        self.product_info = {}
    
    def load_data(self, data_dir='../data'):
        """Load all Instacart CSV files."""
        print("Loading Instacart dataset...")
        
        # Load products
        products_df = pd.read_csv(f'{data_dir}/products.csv')
        print(f"Loaded {len(products_df)} products")
        
        # Load aisles and departments
        aisles_df = pd.read_csv(f'{data_dir}/aisles.csv')
        departments_df = pd.read_csv(f'{data_dir}/departments.csv')
        
        # Merge product info
        products_df = products_df.merge(aisles_df, on='aisle_id', how='left')
        products_df = products_df.merge(departments_df, on='department_id', how='left')
        
        # Store product info
        for _, row in products_df.iterrows():
            self.product_info[int(row['product_id'])] = {
                'name': str(row['product_name']),
                'aisle': str(row['aisle']) if pd.notna(row.get('aisle')) else '',
                'department': str(row['department']) if pd.notna(row.get('department')) else '',
                'aisle_id': int(row['aisle_id']),
                'department_id': int(row['department_id'])
            }
        
        # Load orders
        orders_df = pd.read_csv(f'{data_dir}/orders.csv')
        print(f"Loaded {len(orders_df)} orders")
        
        # Load order products (use prior set for training as it's larger)
        order_products_df = pd.read_csv(f'{data_dir}/order_products__prior.csv')
        print(f"Loaded {len(order_products_df)} order-product pairs")
        
        # Merge orders with products
        data_df = order_products_df.merge(orders_df[['order_id', 'user_id', 'order_number']], on='order_id')
        
        return data_df, products_df
    
    def build_vocabulary(self, data_df):
        """Build product ID to index mapping."""
        print("Building vocabulary...")
        
        unique_products = sorted(data_df['product_id'].unique())
        
        # Reserve 0 for padding
        self.item_to_idx = {item: idx + 1 for idx, item in enumerate(unique_products)}
        self.idx_to_item = {idx + 1: item for idx, item in enumerate(unique_products)}
        self.idx_to_item[0] = 0  # Padding
        self.num_items = len(unique_products) + 1
        
        print(f"Built vocabulary with {self.num_items} items (including padding)")
    
    def process_events(
        self,
        data_dir='../data',
        min_cart_size: int = 1,
        max_cart_size: int = 20,
        sample_frac: float = 0.20,
        min_product_count: int = 500  # Only keep products that appear at least 100 times
    ) -> Tuple[List[List[int]], List[int], List[int]]:
        """
        Process Instacart dataset into training examples.
        
        Returns:
            carts: list of carts (each cart is a list of item indices)
            next_items: list of next item indices (labels)
            user_ids: list of user IDs for each example
        """
        # Load data
        data_df, products_df = self.load_data(data_dir)
        
        # Filter products by frequency - keep only popular products
        print("Filtering products by frequency...")
        product_counts = data_df['product_id'].value_counts()
        popular_products = product_counts[product_counts >= min_product_count].index.tolist()
        print(f"Keeping {len(popular_products)} products with >= {min_product_count} occurrences (from {len(product_counts)} total)")
        
        # Filter dataset to only popular products
        data_df = data_df[data_df['product_id'].isin(popular_products)]
        print(f"Filtered to {len(data_df)} order-product pairs")
        
        # Sample if needed
        if sample_frac < 1.0:
            print(f"Sampling {sample_frac*100}% of users...")
            unique_users = data_df['user_id'].unique()
            sampled_users = np.random.choice(unique_users, size=int(len(unique_users) * sample_frac), replace=False)
            data_df = data_df[data_df['user_id'].isin(sampled_users)]
            print(f"Sampled {len(data_df)} order-product pairs")
        
        # Build vocabulary
        self.build_vocabulary(data_df)
        
        # Create training examples from user order sequences
        print("Creating training examples...")
        carts = []
        next_items = []
        user_ids = []
        
        # Sort by user and order number
        data_df = data_df.sort_values(['user_id', 'order_number', 'add_to_cart_order'])
        
        for user_id, user_orders in data_df.groupby('user_id'):
            # Get sequence of all products ordered by this user
            product_sequence = user_orders['product_id'].tolist()
            
            # Skip very short sequences
            if len(product_sequence) < min_cart_size + 1:
                continue
            
            # Create training examples: use sliding window
            for i in range(min_cart_size, len(product_sequence)):
                cart = product_sequence[max(0, i - max_cart_size):i]
                next_item = product_sequence[i]
                
                # Convert to indices
                cart_indices = [self.item_to_idx.get(item, 0) for item in cart]
                next_item_idx = self.item_to_idx.get(next_item, 0)
                
                if next_item_idx > 0:  # Skip if next item not in vocabulary
                    carts.append(cart_indices)
                    next_items.append(next_item_idx)
                    user_ids.append(user_id)
        
        print(f"Created {len(carts)} training examples from {data_df['user_id'].nunique()} users")
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
