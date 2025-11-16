import { useState, useEffect, useCallback, useRef } from "react";
import { Input } from "@/components/ui/input";
import { ProductCard } from "./ProductCard";
import { Search, Filter, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Badge } from "@/components/ui/badge";
import { MOCK_PRODUCTS } from "@/data/mockProducts";

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface Product {
  id: number;
  name: string;
  aisle: string;
  department: string;
  aisle_id: number;
  department_id: number;
}

interface ProductCatalogProps {
  onAddToCart: (product: any) => void;
}

export const ProductCatalog = ({ onAddToCart }: ProductCatalogProps) => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedBrand, setSelectedBrand] = useState<string | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [total, setTotal] = useState(0);
  const [isOfflineMode, setIsOfflineMode] = useState(false);
  
  const observerTarget = useRef<HTMLDivElement>(null);

  const loadProducts = useCallback(async (pageNum: number, reset: boolean = false) => {
    if (loading) return;
    
    setLoading(true);
    try {
      const params = new URLSearchParams({
        page: pageNum.toString(),
        page_size: "50",
      });
      
      if (searchQuery) params.append("search", searchQuery);
      if (selectedBrand) params.append("brand", selectedBrand);
      if (selectedCategory) params.append("category", selectedCategory);
      
      const response = await fetch(`${API_BASE_URL}/products?${params}`, {
        signal: AbortSignal.timeout(5000) // 5 second timeout
      });
      
      if (!response.ok) throw new Error('Backend unavailable');
      
      const data = await response.json();
      
      if (reset) {
        setProducts(data.products);
      } else {
        setProducts(prev => [...prev, ...data.products]);
      }
      
      setHasMore(data.has_more);
      setTotal(data.total);
      setIsOfflineMode(false);
    } catch (error) {
      console.warn('Backend unavailable, using mock data:', error);
      setIsOfflineMode(true);
      
      // Use mock products as fallback
      let filteredProducts = MOCK_PRODUCTS;
      
      // Apply search filter
      if (searchQuery) {
        const query = searchQuery.toLowerCase();
        filteredProducts = filteredProducts.filter(p => 
          p.name.toLowerCase().includes(query) ||
          p.aisle.toLowerCase().includes(query) ||
          p.department.toLowerCase().includes(query)
        );
      }
      
      // Apply department filter
      if (selectedBrand) {
        filteredProducts = filteredProducts.filter(p => 
          p.department === selectedBrand
        );
      }
      
      // Apply aisle filter
      if (selectedCategory) {
        filteredProducts = filteredProducts.filter(p => 
          p.aisle === selectedCategory
        );
      }
      
      const mockProducts = filteredProducts.map(p => ({
        id: p.id,
        name: p.name,
        aisle: p.aisle,
        department: p.department,
        aisle_id: 0,
        department_id: 0,
      }));
      
      setProducts(mockProducts);
      setHasMore(false);
      setTotal(mockProducts.length);
    } finally {
      setLoading(false);
    }
  }, [searchQuery, selectedBrand, selectedCategory, loading]);

  // Initial load and reset on filter change
  useEffect(() => {
    setPage(1);
    setProducts([]);
    loadProducts(1, true);
  }, [searchQuery, selectedBrand, selectedCategory]);

  // Infinite scroll observer
  useEffect(() => {
    const observer = new IntersectionObserver(
      entries => {
        if (entries[0].isIntersecting && hasMore && !loading) {
          const nextPage = page + 1;
          setPage(nextPage);
          loadProducts(nextPage);
        }
      },
      { threshold: 0.1 }
    );

    const currentTarget = observerTarget.current;
    if (currentTarget) {
      observer.observe(currentTarget);
    }

    return () => {
      if (currentTarget) {
        observer.unobserve(currentTarget);
      }
    };
  }, [hasMore, loading, page, loadProducts]);

  const getProductName = (product: Product) => {
    return product.name;
  };

  // Extract unique departments and aisles for filters
  const uniqueDepartments = [...new Set(products.map(p => p.department).filter(Boolean))].sort();
  const uniqueAisles = [...new Set(products.map(p => p.aisle).filter(Boolean))].sort();

  return (
    <div className="space-y-4">
      {/* Search and Filters */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
          <Input
            placeholder="Search products, brands, or categories..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10"
          />
        </div>
        
        <div className="flex gap-2">
          {/* Brand Filter */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline" className="gap-2">
                <Filter className="h-4 w-4" />
                Department
                {selectedBrand && <Badge variant="secondary" className="ml-1">1</Badge>}
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-48 max-h-96 overflow-y-auto">
              <DropdownMenuItem onClick={() => setSelectedBrand(null)}>
                All Departments
              </DropdownMenuItem>
              {uniqueDepartments.slice(0, 20).map(dept => (
                <DropdownMenuItem
                  key={dept}
                  onClick={() => setSelectedBrand(dept)}
                  className="capitalize"
                >
                  {dept}
                </DropdownMenuItem>
              ))}
            </DropdownMenuContent>
          </DropdownMenu>

          {/* Category Filter */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline" className="gap-2">
                <Filter className="h-4 w-4" />
                Aisle
                {selectedCategory && <Badge variant="secondary" className="ml-1">1</Badge>}
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-48">
              <DropdownMenuItem onClick={() => setSelectedCategory(null)}>
                All Aisles
              </DropdownMenuItem>
              {uniqueAisles.slice(0, 30).map(aisle => (
                <DropdownMenuItem
                  key={aisle}
                  onClick={() => setSelectedCategory(aisle)}
                  className="capitalize"
                >
                  {aisle}
                </DropdownMenuItem>
              ))}
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>

      {/* Active Filters */}
      {(selectedBrand || selectedCategory) && (
        <div className="flex gap-2 flex-wrap">
          {selectedBrand && (
            <Badge variant="secondary" className="gap-2">
              Brand: <span className="capitalize">{selectedBrand}</span>
              <button onClick={() => setSelectedBrand(null)} className="ml-1 hover:text-destructive">
                ×
              </button>
            </Badge>
          )}
          {selectedCategory && (
            <Badge variant="secondary" className="gap-2">
              Category: <span className="capitalize">{selectedCategory}</span>
              <button onClick={() => setSelectedCategory(null)} className="ml-1 hover:text-destructive">
                ×
              </button>
            </Badge>
          )}
        </div>
      )}

      {/* Results Count */}
      <div className="text-sm text-muted-foreground">
        Showing {products.length} of {total} products
      </div>

      {/* Products Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-4">
        {products.map((product) => (
          <ProductCard
            key={product.id}
            id={product.id.toString()}
            name={product.name}
            aisle={product.aisle}
            department={product.department}
            onAddToCart={onAddToCart}
          />
        ))}
      </div>

      {/* Loading Spinner */}
      {loading && (
        <div className="flex justify-center py-8">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
        </div>
      )}

      {/* Infinite Scroll Trigger */}
      <div ref={observerTarget} className="h-10" />

      {/* End of Results */}
      {!hasMore && products.length > 0 && (
        <div className="text-center py-8 text-muted-foreground">
          No more products to load
        </div>
      )}

      {/* No Results */}
      {!loading && products.length === 0 && (
        <div className="text-center py-16 text-muted-foreground">
          <p className="text-lg">No products found</p>
          <p className="text-sm mt-2">Try adjusting your search or filters</p>
        </div>
      )}
    </div>
  );
};
