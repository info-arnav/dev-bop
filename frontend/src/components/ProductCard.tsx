import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Plus } from "lucide-react";
import { toast } from "sonner";

interface ProductCardProps {
  id: string;
  name: string;
  aisle?: string;
  department?: string;
  onAddToCart: (product: any) => void;
}

export const ProductCard = ({ 
  id, 
  name, 
  aisle,
  department,
  onAddToCart 
}: ProductCardProps) => {
  const handleAddToCart = () => {
    onAddToCart({ id, name, aisle, department, quantity: 1 });
    toast.success(`${name} added to cart!`);
  };

  return (
    <Card className="group hover:shadow-md transition-all duration-200 hover:border-primary/50">
      <CardContent className="p-4">
        <div className="flex flex-col gap-3">
          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between mb-2">
              {department && (
                <Badge variant="secondary" className="text-xs capitalize">
                  {department}
                </Badge>
              )}
              <p className="font-mono text-xs text-muted-foreground">
                #{id}
              </p>
            </div>
            <h3 className="font-semibold text-base line-clamp-2 mb-1">{name}</h3>
            {aisle && (
              <p className="text-xs text-muted-foreground line-clamp-1">
                {aisle}
              </p>
            )}
          </div>
          <Button 
            onClick={handleAddToCart}
            size="sm"
            variant="outline"
            className="w-full gap-2 group-hover:bg-primary group-hover:text-primary-foreground transition-colors"
          >
            <Plus className="h-4 w-4" />
            Add to Cart
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};
