
export interface Metric {
  name: string;
  value: string | number;
  category: string;
  description?: string;
}


export interface ScoreResult {
  score: number | null;
  grade: string;
  breakdown: Record<string, number | null>;
  coverage: number;
  notes: string[];
}


export interface StockSummary {
  ticker: string;
  companyName: string;
  metrics: Metric[];
}

export interface Lens {
  key: string;
  name: string;
}
