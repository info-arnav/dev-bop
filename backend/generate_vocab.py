"""
Generate vocabulary.pkl from the events.csv dataset.
This is needed when training was interrupted and vocabulary wasn't saved.
"""

import pandas as pd
import pickle
import sys

print("Loading events.csv...")
df = pd.read_csv('../data/events.csv')

print(f"Loaded {len(df)} events")
print(f"Found {df['itemid'].nunique()} unique items")

# Build vocabulary
all_items = sorted(df['itemid'].unique().tolist())
item_to_idx = {item: idx + 1 for idx, item in enumerate(all_items)}
idx_to_item = {idx + 1: item for idx, item in enumerate(all_items)}
idx_to_item[0] = 0  # Padding
num_items = len(all_items) + 1

vocabulary = {
    'item_to_idx': item_to_idx,
    'idx_to_item': idx_to_item,
    'num_items': num_items
}

print(f"\nVocabulary size: {num_items} (including padding)")

# Save vocabulary
with open('models/vocabulary.pkl', 'wb') as f:
    pickle.dump(vocabulary, f)

print("✓ Saved vocabulary to models/vocabulary.pkl")

# Also create a product catalog with item IDs for the frontend
product_ids = df['itemid'].value_counts().head(100).index.tolist()
print(f"\nTop 100 most popular product IDs: {product_ids[:10]}...")

# Save product list
products = [{'id': str(item_id), 'count': int(df[df['itemid'] == item_id].shape[0])} 
            for item_id in product_ids]

import json
with open('models/products.json', 'w') as f:
    json.dump(products, f, indent=2)

print("✓ Saved product catalog to models/products.json")
