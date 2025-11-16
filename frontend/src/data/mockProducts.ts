/**
 * Mock products for offline/fallback mode
 */

export interface MockProduct {
  id: number;
  name: string;
  aisle: string;
  department: string;
  category: string;
}

export const MOCK_PRODUCTS: MockProduct[] = [
  // Dairy & Cheese
  { id: 1, name: "Organic Whole Milk", aisle: "dairy", department: "dairy eggs", category: "dairy" },
  { id: 2, name: "Mozzarella Cheese", aisle: "dairy", department: "dairy eggs", category: "cheese" },
  { id: 3, name: "Cheddar Cheese", aisle: "dairy", department: "dairy eggs", category: "cheese" },
  { id: 4, name: "Parmesan Cheese", aisle: "dairy", department: "dairy eggs", category: "cheese" },
  { id: 5, name: "Greek Yogurt", aisle: "dairy", department: "dairy eggs", category: "dairy" },
  { id: 6, name: "Butter", aisle: "dairy", department: "dairy eggs", category: "dairy" },
  { id: 7, name: "Cream Cheese", aisle: "dairy", department: "dairy eggs", category: "cheese" },
  
  // Bakery & Pizza
  { id: 8, name: "Pizza Dough", aisle: "bakery", department: "bakery", category: "pizza" },
  { id: 9, name: "Pizza Base", aisle: "bakery", department: "bakery", category: "pizza" },
  { id: 10, name: "Whole Wheat Bread", aisle: "bakery", department: "bakery", category: "bread" },
  { id: 11, name: "Sourdough Bread", aisle: "bakery", department: "bakery", category: "bread" },
  { id: 12, name: "Bagels", aisle: "bakery", department: "bakery", category: "bread" },
  
  // Produce
  { id: 13, name: "Fresh Basil", aisle: "produce", department: "produce", category: "herbs" },
  { id: 14, name: "Tomatoes", aisle: "produce", department: "produce", category: "vegetables" },
  { id: 15, name: "Garlic", aisle: "produce", department: "produce", category: "vegetables" },
  { id: 16, name: "Onions", aisle: "produce", department: "produce", category: "vegetables" },
  { id: 17, name: "Bell Peppers", aisle: "produce", department: "produce", category: "vegetables" },
  { id: 18, name: "Mushrooms", aisle: "produce", department: "produce", category: "vegetables" },
  { id: 19, name: "Avocados", aisle: "produce", department: "produce", category: "vegetables" },
  { id: 20, name: "Bananas", aisle: "produce", department: "produce", category: "fruit" },
  { id: 21, name: "Apples", aisle: "produce", department: "produce", category: "fruit" },
  { id: 22, name: "Strawberries", aisle: "produce", department: "produce", category: "fruit" },
  
  // Pantry
  { id: 23, name: "Olive Oil", aisle: "pantry", department: "pantry", category: "oils" },
  { id: 24, name: "Pasta", aisle: "pantry", department: "pantry", category: "pasta" },
  { id: 25, name: "Tomato Sauce", aisle: "pantry", department: "pantry", category: "sauces" },
  { id: 26, name: "Pizza Sauce", aisle: "pantry", department: "pantry", category: "sauces" },
  { id: 27, name: "Rice", aisle: "pantry", department: "pantry", category: "grains" },
  { id: 28, name: "Flour", aisle: "pantry", department: "pantry", category: "baking" },
  { id: 29, name: "Sugar", aisle: "pantry", department: "pantry", category: "baking" },
  { id: 30, name: "Salt", aisle: "pantry", department: "pantry", category: "spices" },
  { id: 31, name: "Black Pepper", aisle: "pantry", department: "pantry", category: "spices" },
  { id: 32, name: "Italian Seasoning", aisle: "pantry", department: "pantry", category: "spices" },
  
  // Meat & Protein
  { id: 33, name: "Chicken Breast", aisle: "meat", department: "meat seafood", category: "meat" },
  { id: 34, name: "Ground Beef", aisle: "meat", department: "meat seafood", category: "meat" },
  { id: 35, name: "Pepperoni", aisle: "meat", department: "meat seafood", category: "meat" },
  { id: 36, name: "Bacon", aisle: "meat", department: "meat seafood", category: "meat" },
  { id: 37, name: "Salmon", aisle: "meat", department: "meat seafood", category: "seafood" },
  
  // Frozen
  { id: 38, name: "Frozen Pizza", aisle: "frozen", department: "frozen", category: "pizza" },
  { id: 39, name: "Ice Cream", aisle: "frozen", department: "frozen", category: "dessert" },
  { id: 40, name: "Frozen Vegetables", aisle: "frozen", department: "frozen", category: "vegetables" },
  
  // Beverages
  { id: 41, name: "Orange Juice", aisle: "beverages", department: "beverages", category: "juice" },
  { id: 42, name: "Coffee", aisle: "beverages", department: "beverages", category: "coffee" },
  { id: 43, name: "Tea", aisle: "beverages", department: "beverages", category: "tea" },
  { id: 44, name: "Bottled Water", aisle: "beverages", department: "beverages", category: "water" },
  
  // Household
  { id: 45, name: "Paper Towels", aisle: "household", department: "household", category: "paper" },
  { id: 46, name: "Toilet Paper", aisle: "household", department: "household", category: "paper" },
  { id: 47, name: "Dish Soap", aisle: "household", department: "household", category: "cleaning" },
  { id: 48, name: "Laundry Detergent", aisle: "household", department: "household", category: "cleaning" },
  
  // Snacks
  { id: 49, name: "Potato Chips", aisle: "snacks", department: "snacks", category: "chips" },
  { id: 50, name: "Crackers", aisle: "snacks", department: "snacks", category: "crackers" },
  { id: 51, name: "Nuts", aisle: "snacks", department: "snacks", category: "nuts" },
  
  // Personal Care
  { id: 52, name: "Toothpaste", aisle: "personal care", department: "personal care", category: "dental" },
  { id: 53, name: "Shampoo", aisle: "personal care", department: "personal care", category: "hair" },
  { id: 54, name: "Soap", aisle: "personal care", department: "personal care", category: "body" },
  
  // Batteries & Electronics
  { id: 55, name: "AA Batteries", aisle: "household", department: "household", category: "batteries" },
  { id: 56, name: "AAA Batteries", aisle: "household", department: "household", category: "batteries" },
];

/**
 * Smart prediction rules based on common shopping patterns
 */
export const PREDICTION_RULES: Record<string, number[]> = {
  // Pizza ingredients lead to more pizza ingredients
  "pizza": [2, 13, 26, 35, 17, 18, 23, 32], // Mozzarella, Basil, Pizza Sauce, Pepperoni, Peppers, Mushrooms, Olive Oil, Seasoning
  "cheese": [8, 9, 13, 24, 26, 35, 23], // Pizza dough/base, Basil, Pasta, Sauce, Pepperoni, Oil
  "basil": [2, 14, 23, 15, 24, 25], // Mozzarella, Tomatoes, Olive Oil, Garlic, Pasta, Tomato Sauce
  
  // Breakfast items
  "milk": [5, 20, 42, 10, 12, 39], // Yogurt, Bananas, Coffee, Bread, Bagels, Ice Cream
  "bread": [6, 1, 36, 3, 7], // Butter, Milk, Bacon, Cheddar, Cream Cheese
  "eggs": [36, 10, 6, 1, 3], // Bacon, Bread, Butter, Milk, Cheese
  
  // Cooking basics
  "tomato": [13, 15, 16, 23, 24, 25], // Basil, Garlic, Onions, Olive Oil, Pasta, Sauce
  "garlic": [23, 16, 13, 14, 24, 25], // Olive Oil, Onions, Basil, Tomatoes, Pasta, Sauce
  "onion": [15, 14, 17, 33, 34, 27], // Garlic, Tomatoes, Peppers, Chicken, Beef, Rice
  
  // Pasta meal
  "pasta": [25, 2, 4, 23, 13, 15], // Tomato Sauce, Mozzarella, Parmesan, Olive Oil, Basil, Garlic
  "sauce": [24, 2, 13, 15, 23, 4], // Pasta, Mozzarella, Basil, Garlic, Olive Oil, Parmesan
  
  // Meat & protein
  "chicken": [27, 16, 15, 17, 23, 31], // Rice, Onions, Garlic, Peppers, Olive Oil, Pepper
  "beef": [16, 15, 14, 17, 27, 31], // Onions, Garlic, Tomatoes, Peppers, Rice, Pepper
  
  // Fresh produce
  "avocado": [14, 16, 21, 22, 1, 5], // Tomatoes, Onions, Apples, Strawberries, Milk, Yogurt
  "banana": [1, 5, 21, 22, 42, 39], // Milk, Yogurt, Apples, Strawberries, Coffee, Ice Cream
  
  // Household
  "batteries": [45, 46, 47, 44, 52, 53], // Paper products, cleaning, personal care
  "paper": [47, 48, 44, 55, 56], // Cleaning supplies, batteries
  
  // Beverages
  "coffee": [1, 28, 29, 10, 12, 5], // Milk, Flour, Sugar, Bread, Bagels, Yogurt
  "juice": [1, 20, 21, 22, 5, 12], // Milk, Bananas, Apples, Strawberries, Yogurt, Bagels
};

/**
 * Generate mock predictions based on cart contents
 */
export function generateMockPredictions(cartProductIds: number[], topK: number = 10): { id: number; name: string; score: number; aisle: string; department: string }[] {
  const scores = new Map<number, number>();
  
  // Initialize all products with base score
  MOCK_PRODUCTS.forEach(product => {
    scores.set(product.id, 0.001);
  });
  
  // Calculate scores based on cart items
  cartProductIds.forEach(cartId => {
    const cartProduct = MOCK_PRODUCTS.find(p => p.id === cartId);
    if (!cartProduct) return;
    
    // Check for category-based rules
    const category = cartProduct.category.toLowerCase();
    const name = cartProduct.name.toLowerCase();
    
    // Find matching rules
    Object.entries(PREDICTION_RULES).forEach(([keyword, relatedIds]) => {
      if (category.includes(keyword) || name.includes(keyword)) {
        relatedIds.forEach((relatedId, index) => {
          if (!cartProductIds.includes(relatedId)) {
            const currentScore = scores.get(relatedId) || 0;
            // Higher score for items earlier in the list
            const boost = 0.1 - (index * 0.01);
            scores.set(relatedId, currentScore + boost);
          }
        });
      }
    });
    
    // Add general category affinity
    MOCK_PRODUCTS.forEach(product => {
      if (product.id !== cartId && !cartProductIds.includes(product.id)) {
        if (product.department === cartProduct.department) {
          const currentScore = scores.get(product.id) || 0;
          scores.set(product.id, currentScore + 0.02);
        }
        if (product.category === cartProduct.category) {
          const currentScore = scores.get(product.id) || 0;
          scores.set(product.id, currentScore + 0.03);
        }
      }
    });
  });
  
  // Sort by score and return top K
  const predictions = Array.from(scores.entries())
    .filter(([id]) => !cartProductIds.includes(id))
    .sort((a, b) => b[1] - a[1])
    .slice(0, topK)
    .map(([id, score]) => {
      const product = MOCK_PRODUCTS.find(p => p.id === id)!;
      return {
        id: product.id,
        name: product.name,
        score: score,
        aisle: product.aisle,
        department: product.department,
      };
    });
  
  return predictions;
}
