import { useRef, useState } from "react";

import { fetchStock, fetchStockScore } from "../services/stockApi";
import type { StockData } from "../services/stockApi";
import type { ScoreResult } from "../types/stock";

export function useStockAnalysis() {
  const [ticker, setTicker] = useState("AAPL");
  const [stock, setStock] = useState<StockData | null>(null);
  const [score, setScore] = useState<ScoreResult | null>(null);
  const [activeLens, setActiveLens] = useState("Average");

  const [loading, setLoading] = useState(false);
  const [scoreLoading, setScoreLoading] = useState(false);
  const [error, setError] = useState("");

  // Incremented on every request; responses from older requests are ignored.
  const requestId = useRef(0);

  async function analyze() {
    const searchTicker = ticker.trim();

    if (!searchTicker) {
      setError("Please enter a stock ticker.");
      return;
    }

    const id = ++requestId.current;

    setLoading(true);
    setScoreLoading(false);
    setError("");
    setStock(null);
    setScore(null);

    try {
      const [stockResult, scoreResult] = await Promise.all([
        fetchStock(searchTicker),
        fetchStockScore(searchTicker, activeLens),
      ]);

      if (id !== requestId.current) return;

      setStock(stockResult);
      setScore(scoreResult);
    } catch (err) {
      if (id !== requestId.current) return;
      setError(err instanceof Error ? err.message : "An unexpected error occurred.");
    } finally {
      if (id === requestId.current) setLoading(false);
    }
  }

  async function changeLens(lens: string) {
    setActiveLens(lens);

    if (!stock) return;

    const id = ++requestId.current;

    setScoreLoading(true);
    setError("");

    try {
      const result = await fetchStockScore(stock.ticker_symbol, lens);

      if (id !== requestId.current) return;

      setScore(result);
    } catch (err) {
      if (id !== requestId.current) return;
      setError(err instanceof Error ? err.message : "Failed to calculate stock score.");
    } finally {
      if (id === requestId.current) setScoreLoading(false);
    }
  }

  return {
    ticker,
    setTicker,
    stock,
    score,
    activeLens,
    loading,
    scoreLoading,
    error,
    analyze,
    changeLens,
  };
}
