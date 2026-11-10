
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

export async function fetchStock(ticker: string): Promise<StockData> {
  const response = await fetch(
    `/api/stocks/${encodeURIComponent(ticker)}`
  );

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to retrieve stock");
  }

  return response.json();
}
