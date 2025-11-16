import { ProductCard } from "./ProductCard";
import { PRODUCTS, getProductName } from "@/data/products_new";

interface ProductGridProps {
  onAddToCart: (product: any) => void;
}

export const ProductGrid = ({ onAddToCart }: ProductGridProps) => {
  // Use real products from the new dataset
  const products = PRODUCTS.slice(0, 30).map(product => ({
    id: product.id.toString(),
    name: getProductName(product),
    brand: product.brand,
    price: product.price,
    category: product.category,
  }));

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-4">
      {products.map((product) => (
        <ProductCard
          key={product.id}
          {...product}
          onAddToCart={onAddToCart}
        />
      ))}
    </div>
  );
};
