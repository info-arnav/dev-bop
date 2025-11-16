// Product data extracted from the new e-commerce dataset
// This file is auto-generated from backend/models/products.json

export interface Product {
  id: number;
  brand: string;
  price: number;
  category: string;
  popularity: number;
}

// Top 100 most popular products from the dataset
export const PRODUCTS: Product[] = [
  { id: 1005115, brand: "apple", price: 923.71, category: "electronics.smartphone", popularity: 6721 },
  { id: 1004856, brand: "samsung", price: 127.27, category: "electronics.smartphone", popularity: 6413 },
  { id: 1004767, brand: "samsung", price: 245.63, category: "electronics.smartphone", popularity: 5727 },
  { id: 4804056, brand: "apple", price: 162.85, category: "electronics.audio.headphone", popularity: 3943 },
  { id: 1005160, brand: "xiaomi", price: 202.39, category: "electronics.smartphone", popularity: 3239 },
  { id: 1004870, brand: "samsung", price: 282.14, category: "electronics.smartphone", popularity: 3225 },
  { id: 1005105, brand: "apple", price: 1351.59, category: "electronics.smartphone", popularity: 3038 },
  { id: 1004833, brand: "samsung", price: 170.69, category: "electronics.smartphone", popularity: 2992 },
  { id: 1004249, brand: "apple", price: 757.96, category: "electronics.smartphone", popularity: 2796 },
  { id: 1002544, brand: "apple", price: 476.18, category: "electronics.smartphone", popularity: 2730 },
  { id: 1004775, brand: "xiaomi", price: 183.27, category: "electronics.smartphone", popularity: 2564 },
  { id: 1004258, brand: "apple", price: 732.07, category: "electronics.smartphone", popularity: 2557 },
  { id: 1004545, brand: "huawei", price: 132.99, category: "electronics.smartphone", popularity: 2486 },
  { id: 1004237, brand: "apple", price: 705.12, category: "electronics.smartphone", popularity: 2478 },
  { id: 1801995, brand: "xiaomi", price: 26.76, category: "electronics.clocks", popularity: 2435 },
  { id: 1005011, brand: "apple", price: 1079.89, category: "electronics.smartphone", popularity: 2408 },
  { id: 1307067, brand: "apple", price: 1220.32, category: "computers.notebook", popularity: 2385 },
  { id: 1004545, brand: "huawei", price: 132.99, category: "electronics.smartphone", popularity: 2334 },
  { id: 1004833, brand: "samsung", price: 170.69, category: "electronics.smartphone", popularity: 2314 },
  { id: 1004565, brand: "huawei", price: 150.58, category: "electronics.smartphone", popularity: 2279 },
  { id: 4804056, brand: "apple", price: 162.85, category: "electronics.audio.headphone", popularity: 2248 },
  { id: 1004856, brand: "samsung", price: 127.27, category: "electronics.smartphone", popularity: 2231 },
  { id: 4804808, brand: "samsung", price: 22.55, category: "electronics.audio.headphone", popularity: 2197 },
  { id: 1005115, brand: "apple", price: 923.71, category: "electronics.smartphone", popularity: 2190 },
  { id: 3900746, brand: "samsung", price: 237.46, category: "appliances.kitchen.refrigerators", popularity: 2172 },
  { id: 1306421, brand: "hp", price: 514.56, category: "computers.notebook", popularity: 2162 },
  { id: 1004767, brand: "samsung", price: 245.63, category: "electronics.smartphone", popularity: 2115 },
  { id: 1005135, brand: "apple", price: 1187.61, category: "electronics.smartphone", popularity: 2094 },
  { id: 5100948, brand: "xiaomi", price: 19.26, category: "", popularity: 2090 },
  { id: 1801995, brand: "xiaomi", price: 26.76, category: "electronics.clocks", popularity: 2087 }
];

// Helper function to get product name from brand and category
export function getProductName(product: Product): string {
  const categoryName = product.category.split('.').pop()?.replace(/_/g, ' ') || 'Product';
  return `${product.brand.charAt(0).toUpperCase() + product.brand.slice(1)} ${categoryName.charAt(0).toUpperCase() + categoryName.slice(1)}`;
}

// Helper function to format category for display
export function formatCategory(category: string): string {
  if (!category) return '';
  const parts = category.split('.');
  return parts.map(p => p.charAt(0).toUpperCase() + p.slice(1).replace(/_/g, ' ')).join(' > ');
}
