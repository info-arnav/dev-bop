import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export const RecentPredictions = () => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Model Architecture</CardTitle>
        <CardDescription>PyTorch neural network details</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          <div className="p-3 rounded-lg bg-secondary/30">
            <p className="text-sm font-medium mb-1">Embedding Dimension</p>
            <p className="text-xs text-muted-foreground">128-dimensional item embeddings</p>
          </div>
          <div className="p-3 rounded-lg bg-secondary/30">
            <p className="text-sm font-medium mb-1">Hidden Layer</p>
            <p className="text-xs text-muted-foreground">256 neurons with dropout</p>
          </div>
          <div className="p-3 rounded-lg bg-secondary/30">
            <p className="text-sm font-medium mb-1">Aggregation</p>
            <p className="text-xs text-muted-foreground">Mean pooling over cart items</p>
          </div>
          <div className="p-3 rounded-lg bg-secondary/30">
            <p className="text-sm font-medium mb-1">Output</p>
            <p className="text-xs text-muted-foreground">Softmax over all products</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
