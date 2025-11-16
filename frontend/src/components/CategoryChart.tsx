import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export const CategoryChart = () => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Training Dataset</CardTitle>
        <CardDescription>E-commerce events from real user interactions</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          <div className="flex justify-between items-center p-3 rounded-lg bg-secondary/30">
            <span className="text-sm font-medium">Total Orders</span>
            <span className="text-lg font-bold">3.4M</span>
          </div>
          <div className="flex justify-between items-center p-3 rounded-lg bg-secondary/30">
            <span className="text-sm font-medium">Unique Products</span>
            <span className="text-lg font-bold">49,688</span>
          </div>
          <div className="flex justify-between items-center p-3 rounded-lg bg-secondary/30">
            <span className="text-sm font-medium">Departments</span>
            <span className="text-lg font-bold">21</span>
          </div>
          <div className="flex justify-between items-center p-3 rounded-lg bg-secondary/30">
            <span className="text-sm font-medium">Aisles</span>
            <span className="text-lg font-bold">134</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
