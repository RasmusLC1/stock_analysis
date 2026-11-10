
import type { ScoreResult } from "../types/stock";

// Stock information returned by Python
export interface StockData {
  ticker_symbol: string;
  name?: string | null;
  currency?: string | null;
  sector?: string | null;
  industry?: string | null;
  price?: number | string | null;
  market_cap?: string | null;
  pe_ratio?: number | string | null;
  forward_pe?: number | null;
  revenue_growth?: number | null;
  earnings_growth?: number | null;
  return_on_equity?: number | null;
  profit_margins?: number | null;
  debt_to_equity?: number | null;
  current_ratio?: number | null;
  dividend_yield?: number | null;
  [key: string]: string | number | null | undefined;
}

// Retrieve stock information
export async function fetchStock(
  ticker: string
): Promise<StockData> {
  const response = await fetch(
    `/api/stocks/${encodeURIComponent(ticker)}`
  );

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to retrieve stock");
  }

  return response.json();
}

// Retrieve calculated stock score
export async function fetchStockScore(
  ticker: string,
  lens: string = "average"
): Promise<ScoreResult> {
  const response = await fetch(
    `/api/stocks/${encodeURIComponent(ticker)}/score?lens=${encodeURIComponent(lens)}`
  );

  if (!response.ok) {
    const error = await response.json();
    throw new Error(
      error.detail || "Failed to calculate stock score"
    );
  }

  return response.json();
}
