/**
 * Hook for making predictions using the backend API
 */

import { useState, useCallback } from 'react';

export interface CartItem {
  product_id: string;
  quantity: number;
}

export interface PredictionItem {
  product_id: string;
  probability: number;
  score: number;
  name?: string;
  aisle?: string;
  department?: string;
}

export interface PredictResponse {
  next_item_predictions: PredictionItem[];
  co_purchase: any[];
}

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export function usePrediction() {
  const [predictions, setPredictions] = useState<PredictionItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const getPredictions = useCallback(async (cart: CartItem[], topK: number = 10) => {
    if (cart.length === 0) {
      setPredictions([]);
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          cart,
          top_k: topK,
        }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`);
      }

      const data: PredictResponse = await response.json();
      setPredictions(data.next_item_predictions);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to get predictions';
      setError(errorMessage);
      console.error('Prediction error:', err);
      // Fallback to empty predictions on error
      setPredictions([]);
    } finally {
      setLoading(false);
    }
  }, []);

  const checkHealth = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      const data = await response.json();
      return data;
    } catch (err) {
      console.error('Health check failed:', err);
      return { status: 'unhealthy', model_loaded: false };
    }
  }, []);

  return {
    predictions,
    loading,
    error,
    getPredictions,
    checkHealth,
  };
}
