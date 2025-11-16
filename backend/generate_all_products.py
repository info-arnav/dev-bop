"""
Generate all products from vocabulary for the frontend catalog.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

import pickle
import json

def main():
    print("=" * 60)
    print("Extracting All Products from Vocabulary")
    print("=" * 60)
    
    # Load vocabulary
    vocab_path = './models/vocabulary.pkl'
    print(f"\nLoading vocabulary from {vocab_path}...")
    
    with open(vocab_path, 'rb') as f:
        vocab_data = pickle.load(f)
    
    product_info = vocab_data.get('product_info', {})
    print(f"Found {len(product_info)} products with metadata")
    
    # Convert all products to list format
    all_products = []
    for product_id, info in product_info.items():
        all_products.append({
            'id': int(product_id),
            'brand': info.get('brand', ''),
            'price': info.get('price', 0.0),
            'category': info.get('category_code', ''),
            'category_id': info.get('category_id', 0)
        })
    
    # Sort by product_id for consistent ordering
    all_products.sort(key=lambda x: x['id'])
    
    # Save all products
    output_path = './models/all_products.json'
    with open(output_path, 'w') as f:
        json.dump(all_products, f)
    
    print(f"\nSaved {len(all_products)} products to {output_path}")
    
    # Print statistics
    print("\n" + "=" * 60)
    print("Product Statistics:")
    print("=" * 60)
    print(f"Total products: {len(all_products)}")
    
    # Count brands and categories
    brands = set(p['brand'] for p in all_products if p['brand'])
    categories = set(p['category'] for p in all_products if p['category'])
    
    print(f"Unique brands: {len(brands)}")
    print(f"Unique categories: {len(categories)}")
    
    # Price statistics
    prices = [p['price'] for p in all_products if p['price'] > 0]
    if prices:
        print(f"Price range: ${min(prices):.2f} - ${max(prices):.2f}")
        print(f"Average price: ${sum(prices)/len(prices):.2f}")
    
    # Products without brand/category
    no_brand = sum(1 for p in all_products if not p['brand'])
    no_category = sum(1 for p in all_products if not p['category'])
    print(f"\nProducts without brand: {no_brand}")
    print(f"Products without category: {no_category}")
    
    print("\nFirst 5 products:")
    for i, product in enumerate(all_products[:5], 1):
        print(f"{i}. ID: {product['id']}, Brand: {product['brand']}, "
              f"Price: ${product['price']:.2f}, Category: {product['category']}")

if __name__ == '__main__':
    main()
