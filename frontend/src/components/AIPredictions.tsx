import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { TrendingUp, AlertCircle } from "lucide-react";
import { Alert, AlertDescription } from "@/components/ui/alert";

interface PredictionItem {
  product_id: string;
  probability: number;
  score: number;
  name?: string;
  aisle?: string;
  department?: string;
}

interface AIPredictionsProps {
  predictions: PredictionItem[];
  loading: boolean;
  error: string | null;
}

export const AIPredictions = ({ predictions, loading, error }: AIPredictionsProps) => {
  const getProductName = (pred: PredictionItem) => {
    if (pred.name) {
      return pred.name;
    }
    return `Product #${pred.product_id}`;
  };

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center gap-2">
          <TrendingUp className="h-5 w-5 text-primary" />
          <CardTitle>AI-Powered Next Purchase Predictions</CardTitle>
        </div>
        <CardDescription>
          Top products the user is likely to purchase next based on current cart
        </CardDescription>
      </CardHeader>
      <CardContent>
        {error && (
          <Alert variant="destructive" className="mb-4">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {loading && (
          <div className="space-y-3">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="flex items-center justify-between">
                <Skeleton className="h-4 w-24" />
                <Skeleton className="h-6 w-16" />
              </div>
            ))}
          </div>
        )}

        {!loading && !error && predictions.length === 0 && (
          <div className="text-center py-8 text-muted-foreground">
            <p>Add items to cart to see predictions</p>
          </div>
        )}

        {!loading && predictions.length > 0 && (
          <div className="space-y-3">
            {predictions.map((pred, index) => (
              <div
                key={pred.product_id}
                className="flex items-center justify-between p-3 rounded-lg border bg-card hover:bg-accent/50 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <Badge variant="outline" className="w-8 h-8 flex items-center justify-center">
                    {index + 1}
                  </Badge>
                  <div>
                    <p className="font-medium">{getProductName(pred)}</p>
                    <div className="flex items-center gap-2 text-xs text-muted-foreground">
                      {pred.department && (
                        <span className="font-semibold text-primary">{pred.department}</span>
                      )}
                      {pred.aisle && (
                        <span>{pred.aisle}</span>
                      )}
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <div className="text-right">
                    <div className="font-semibold text-primary">
                      {(pred.probability * 100).toFixed(1)}%
                    </div>
                  </div>
                  <div className="w-24 bg-secondary rounded-full h-2">
                    <div
                      className="bg-primary h-2 rounded-full transition-all"
                      style={{ width: `${pred.probability * 100}%` }}
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
};
