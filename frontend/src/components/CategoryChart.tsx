import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export const CategoryChart = () => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Training Dataset</CardTitle>
        <CardDescription>Instacart grocery data from 204K users</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          <div className="flex justify-between items-center p-3 rounded-lg bg-secondary/30">
            <span className="text-sm font-medium">Total Orders</span>
            <span className="text-lg font-bold">3.4M</span>
          </div>
          <div className="flex justify-between items-center p-3 rounded-lg bg-secondary/30">
            <span className="text-sm font-medium">Training Examples</span>
            <span className="text-lg font-bold">14.2M</span>
          </div>
          <div className="flex justify-between items-center p-3 rounded-lg bg-secondary/30">
            <span className="text-sm font-medium">Model Vocabulary</span>
            <span className="text-lg font-bold">1,094</span>
          </div>
          <div className="flex justify-between items-center p-3 rounded-lg bg-secondary/30">
            <span className="text-sm font-medium">Departments</span>
            <span className="text-lg font-bold">21</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
