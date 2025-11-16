"""
Generate vocabulary and product metadata from the new dataset.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from preprocess_new import DataPreprocessor
import pandas as pd
import json

def main():
    print("=" * 60)
    print("Generating Vocabulary from New Dataset")
    print("=" * 60)
    
    # Initialize preprocessor
    preprocessor = DataPreprocessor()
    
    # Load a sample of data to build vocabulary
    csv_path = '../data/dataset.csv'
    print(f"\nLoading dataset from {csv_path}...")
    print("Reading 1% sample to build vocabulary...")
    
    # Read sample
    df = pd.read_csv(csv_path)
    df_sample = df.sample(frac=0.01, random_state=42)
    print(f"Sampled {len(df_sample)} events from {len(df)} total")
    
    # Build vocabulary
    preprocessor.build_vocabulary(df_sample)
    
    # Save vocabulary
    os.makedirs('./models', exist_ok=True)
    preprocessor.save_vocabulary('./models/vocabulary.pkl')
    
    # Extract top products for frontend
    print("\nExtracting top 500 most popular products...")
    product_counts = df_sample['product_id'].value_counts().head(500)
    
    top_products = []
    for product_id, count in product_counts.items():
        if product_id in preprocessor.product_info:
            info = preprocessor.product_info[product_id]
            top_products.append({
                'id': int(product_id),
                'brand': info['brand'],
                'price': info['price'],
                'category': info['category_code'],
                'popularity': int(count)
            })
    
    # Save products
    with open('./models/products.json', 'w') as f:
        json.dump(top_products, f, indent=2)
    
    print(f"Saved top {len(top_products)} products to ./models/products.json")
    
    # Print statistics
    print("\n" + "=" * 60)
    print("Vocabulary Statistics:")
    print("=" * 60)
    print(f"Total unique products: {preprocessor.num_items - 1}")
    print(f"Products with metadata: {len(preprocessor.product_info)}")
    
    # Count brands and categories
    brands = set(info['brand'] for info in preprocessor.product_info.values() if info['brand'])
    categories = set(info['category_code'] for info in preprocessor.product_info.values() if info['category_code'])
    
    print(f"Unique brands: {len(brands)}")
    print(f"Unique categories: {len(categories)}")
    
    # Price statistics
    prices = [info['price'] for info in preprocessor.product_info.values() if info['price'] > 0]
    if prices:
        print(f"Price range: ${min(prices):.2f} - ${max(prices):.2f}")
        print(f"Average price: ${sum(prices)/len(prices):.2f}")
    
    print("\nTop 10 products:")
    for i, product in enumerate(top_products[:10], 1):
        print(f"{i}. ID: {product['id']}, Brand: {product['brand']}, "
              f"Price: ${product['price']:.2f}, Category: {product['category']}")

if __name__ == '__main__':
    main()
