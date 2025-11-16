import { useState, useEffect } from "react";
import { MetricCard } from "@/components/MetricCard";
import { AccuracyChart } from "@/components/AccuracyChart";
import { CategoryChart } from "@/components/CategoryChart";
import { RecentPredictions } from "@/components/RecentPredictions";
import { ProductCatalog } from "@/components/ProductCatalog";
import { ShoppingCartComponent } from "@/components/ShoppingCart";
import { AIPredictions } from "@/components/AIPredictions";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Target, TrendingUp, Activity, Zap, Store } from "lucide-react";
import { usePrediction } from "@/hooks/usePrediction";

interface CartItem {
  id: string;
  name: string;
  quantity: number;
}

const Index = () => {
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const { predictions, loading, error, getPredictions } = usePrediction();

  // Update predictions when cart changes (with debouncing)
  useEffect(() => {
    const timer = setTimeout(() => {
      if (cartItems.length > 0) {
        const cartForAPI = cartItems.map(item => ({
          product_id: item.id,
          quantity: item.quantity
        }));
        getPredictions(cartForAPI, 10);
      }
    }, 300); // 300ms debounce

    return () => clearTimeout(timer);
  }, [cartItems, getPredictions]);

  const handleAddToCart = (product: any) => {
    setCartItems(prev => {
      const existing = prev.find(item => item.id === product.id);
      if (existing) {
        return prev.map(item =>
          item.id === product.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      }
      return [...prev, { ...product, quantity: 1 }];
    });
  };

  const handleRemoveItem = (id: string) => {
    setCartItems(prev => prev.filter(item => item.id !== id));
  };

  const handleUpdateQuantity = (id: string, quantity: number) => {
    setCartItems(prev =>
      prev.map(item =>
        item.id === id ? { ...item, quantity } : item
      )
    );
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-10">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-lg bg-primary flex items-center justify-center">
                <Target className="h-6 w-6 text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-2xl font-bold">Prediction Analytics</h1>
                <p className="text-sm text-muted-foreground">Shopping behavior prediction dashboard</p>
              </div>
            </div>
            <ShoppingCartComponent 
              items={cartItems}
              onRemoveItem={handleRemoveItem}
              onUpdateQuantity={handleUpdateQuantity}
            />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <Tabs defaultValue="shop" className="w-full">
          <TabsList className="grid w-full max-w-md grid-cols-2 mb-8">
            <TabsTrigger value="shop" className="gap-2">
              <Store className="h-4 w-4" />
              Shop
            </TabsTrigger>
            <TabsTrigger value="analytics" className="gap-2">
              <Target className="h-4 w-4" />
              Analytics
            </TabsTrigger>
          </TabsList>

          <TabsContent value="shop" className="space-y-6">
            <div>
              <h2 className="text-2xl font-bold mb-2">Grocery Product Catalog</h2>
              <p className="text-muted-foreground mb-6">
                Browse 1,094 high-frequency grocery products with real-time AI predictions. Add items to see recommendations!
              </p>
            </div>
            
            {/* AI Predictions Section */}
            {cartItems.length > 0 && (
              <AIPredictions predictions={predictions} loading={loading} error={error} />
            )}
            
            <ProductCatalog onAddToCart={handleAddToCart} />
          </TabsContent>

          <TabsContent value="analytics" className="space-y-6">
            {/* Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <MetricCard
                title="Products"
                value="49.7K"
                change="Grocery items"
                icon={Target}
                trend="up"
              />
              <MetricCard
                title="Orders"
                value="3.4M"
                change="User purchases"
                icon={Activity}
                trend="up"
              />
              <MetricCard
                title="Departments"
                value="21"
                change="Product categories"
                icon={TrendingUp}
                trend="up"
              />
            </div>

            {/* Charts Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <AccuracyChart />
              <CategoryChart />
              <RecentPredictions />
            </div>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
};

export default Index;
