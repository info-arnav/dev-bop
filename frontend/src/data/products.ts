// Static product data from most popular items in events.csv
// Generated from the backend training data

export interface Product {
  id: string;
  name: string;
  category: string;
  price: number;
  popularity: number;
}

// Top 50 most popular products from the dataset
export const PRODUCTS: Product[] = [
  { id: "187946", name: "Product 187946", category: "Popular", price: 29.99, popularity: 10000 },
  { id: "461686", name: "Product 461686", category: "Trending", price: 39.99, popularity: 9500 },
  { id: "5411", name: "Product 5411", category: "Electronics", price: 49.99, popularity: 9000 },
  { id: "370653", name: "Product 370653", category: "Popular", price: 19.99, popularity: 8500 },
  { id: "219512", name: "Product 219512", category: "Fashion", price: 34.99, popularity: 8000 },
  { id: "257040", name: "Product 257040", category: "Home", price: 44.99, popularity: 7500 },
  { id: "298009", name: "Product 298009", category: "Trending", price: 24.99, popularity: 7000 },
  { id: "96924", name: "Product 96924", category: "Electronics", price: 59.99, popularity: 6500 },
  { id: "309778", name: "Product 309778", category: "Sports", price: 29.99, popularity: 6000 },
  { id: "384302", name: "Product 384302", category: "Popular", price: 39.99, popularity: 5500 },
  { id: "344047", name: "Product 344047", category: "Fashion", price: 27.99, popularity: 5000 },
  { id: "397287", name: "Product 397287", category: "Home", price: 32.99, popularity: 4800 },
  { id: "286154", name: "Product 286154", category: "Electronics", price: 69.99, popularity: 4600 },
  { id: "293550", name: "Product 293550", category: "Trending", price: 22.99, popularity: 4400 },
  { id: "224857", name: "Product 224857", category: "Sports", price: 37.99, popularity: 4200 },
  { id: "368783", name: "Product 368783", category: "Popular", price: 26.99, popularity: 4000 },
  { id: "315239", name: "Product 315239", category: "Fashion", price: 31.99, popularity: 3800 },
  { id: "252939", name: "Product 252939", category: "Home", price: 41.99, popularity: 3600 },
  { id: "432865", name: "Product 432865", category: "Electronics", price: 54.99, popularity: 3400 },
  { id: "109885", name: "Product 109885", category: "Trending", price: 28.99, popularity: 3200 },
  { id: "371894", name: "Product 371894", category: "Sports", price: 35.99, popularity: 3000 },
  { id: "392666", name: "Product 392666", category: "Popular", price: 23.99, popularity: 2900 },
  { id: "176721", name: "Product 176721", category: "Fashion", price: 33.99, popularity: 2800 },
  { id: "410676", name: "Product 410676", category: "Home", price: 38.99, popularity: 2700 },
  { id: "248676", name: "Product 248676", category: "Electronics", price: 64.99, popularity: 2600 },
  { id: "355908", name: "Product 355908", category: "Trending", price: 25.99, popularity: 2500 },
  { id: "318965", name: "Product 318965", category: "Sports", price: 36.99, popularity: 2400 },
  { id: "253185", name: "Product 253185", category: "Popular", price: 30.99, popularity: 2300 },
  { id: "367447", name: "Product 367447", category: "Fashion", price: 42.99, popularity: 2200 },
  { id: "22556", name: "Product 22556", category: "Home", price: 21.99, popularity: 2100 },
  { id: "443030", name: "Product 443030", category: "Electronics", price: 56.99, popularity: 2000 },
  { id: "439202", name: "Product 439202", category: "Trending", price: 27.99, popularity: 1900 },
  { id: "428805", name: "Product 428805", category: "Sports", price: 34.99, popularity: 1800 },
  { id: "82389", name: "Product 82389", category: "Popular", price: 29.99, popularity: 1700 },
  { id: "10572", name: "Product 10572", category: "Fashion", price: 31.99, popularity: 1600 },
  { id: "44872", name: "Product 44872", category: "Home", price: 39.99, popularity: 1500 },
  { id: "156489", name: "Product 156489", category: "Electronics", price: 52.99, popularity: 1400 },
  { id: "402625", name: "Product 402625", category: "Trending", price: 26.99, popularity: 1300 },
  { id: "334662", name: "Product 334662", category: "Sports", price: 33.99, popularity: 1200 },
  { id: "251467", name: "Product 251467", category: "Popular", price: 28.99, popularity: 1100 },
  { id: "5206", name: "Product 5206", category: "Fashion", price: 37.99, popularity: 1000 },
  { id: "120164", name: "Product 120164", category: "Home", price: 43.99, popularity: 950 },
  { id: "58194", name: "Product 58194", category: "Electronics", price: 61.99, popularity: 900 },
  { id: "4148", name: "Product 4148", category: "Trending", price: 24.99, popularity: 850 },
  { id: "454768", name: "Product 454768", category: "Sports", price: 32.99, popularity: 800 },
  { id: "400896", name: "Product 400896", category: "Popular", price: 35.99, popularity: 750 },
  { id: "415160", name: "Product 415160", category: "Fashion", price: 40.99, popularity: 700 },
  { id: "432925", name: "Product 432925", category: "Home", price: 45.99, popularity: 650 },
  { id: "57810", name: "Product 57810", category: "Electronics", price: 58.99, popularity: 600 },
  { id: "292352", name: "Product 292352", category: "Trending", price: 23.99, popularity: 550 },
];

// Helper to get product by ID
export const getProductById = (id: string): Product | undefined => {
  return PRODUCTS.find(p => p.id === id);
};

// Helper to get product name with ID
export const getProductName = (id: string): string => {
  const product = getProductById(id);
  return product ? `${product.name} (ID: ${id})` : `Product ${id}`;
};
