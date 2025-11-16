"""
Generate vocabulary from Instacart dataset.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from preprocess_instacart import InstacartPreprocessor
import json

def main():
    print("=" * 60)
    print("Generating Vocabulary from Instacart Dataset")
    print("=" * 60)
    
    # Initialize preprocessor
    preprocessor = InstacartPreprocessor()
    
    # Load and process data with product frequency filtering
    data_df, products_df = preprocessor.load_data('../data')
    
    # Filter products by frequency - keep only top products with 5000+ occurrences
    print("\nFiltering products by frequency...")
    product_counts = data_df['product_id'].value_counts()
    popular_products = product_counts[product_counts >= 5000].index.tolist()
    print(f"Keeping {len(popular_products)} products with >= 5000 occurrences (from {len(product_counts)} total)")
    
    # Filter dataset to only popular products
    data_df = data_df[data_df['product_id'].isin(popular_products)]
    print(f"Filtered to {len(data_df)} order-product pairs")
    
    # Build vocabulary from filtered products
    preprocessor.build_vocabulary(data_df)
    
    # Save vocabulary
    os.makedirs('./models', exist_ok=True)
    preprocessor.save_vocabulary('./models/vocabulary.pkl')
    
    # Export only the frequent products for frontend
    print("\nExporting frequent products...")
    all_products = []
    for product_id, info in preprocessor.product_info.items():
        # Only export products that are in the vocabulary (frequent products)
        if product_id in preprocessor.item_to_idx:
            all_products.append({
                'id': product_id,
                'name': info['name'],
                'aisle': info['aisle'],
                'department': info['department'],
                'aisle_id': info['aisle_id'],
                'department_id': info['department_id']
            })
    
    # Sort by product_id
    all_products.sort(key=lambda x: x['id'])
    
    # Save all products
    with open('./models/all_products.json', 'w') as f:
        json.dump(all_products, f)
    
    print(f"Saved {len(all_products)} products to ./models/all_products.json")
    
    # Print statistics
    print("\n" + "=" * 60)
    print("Dataset Statistics:")
    print("=" * 60)
    print(f"Total products: {len(all_products)}")
    print(f"Vocabulary size: {preprocessor.num_items}")
    
    # Count aisles and departments
    aisles = set(p['aisle'] for p in all_products if p['aisle'])
    departments = set(p['department'] for p in all_products if p['department'])
    
    print(f"Unique aisles: {len(aisles)}")
    print(f"Unique departments: {len(departments)}")
    
    print("\nTop 10 products by ID:")
    for i, product in enumerate(all_products[:10], 1):
        print(f"{i}. {product['name']} ({product['department']} > {product['aisle']})")
    
    print("\nVocabulary generated successfully!")

if __name__ == '__main__':
    main()
