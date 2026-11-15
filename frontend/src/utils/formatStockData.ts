import type { StockData } from "../services/stockApi";

export const STOCK_SECTIONS: Record<string, string[]> = {
  "COMPANY INFORMATION": [
    "name",
    "ticker_symbol",
    "sector",
    "industry",
    "currency",
    "financial_currency",
    "summary",
    "website",
  ],
  "VALUATION & PRICING": [
    "price",
    "previous_close",
    "open_price",
    "day_low",
    "day_high",
    "market_cap",
    "enterprise_value",
    "pe_ratio",
    "forward_pe",
    "peg_ratio",
    "price_to_sales",
    "price_to_book",
    "enterprise_to_revenue",
    "enterprise_to_ebitda",
  ],
  "PROFITABILITY & GROWTH": [
    "profit_margins",
    "gross_margins",
    "operating_margins",
    "ebitda_margins",
    "return_on_assets",
    "return_on_equity",
    "total_revenue",
    "revenue_growth",
    "gross_profits",
    "ebitda",
    "net_income",
    "earnings_growth",
    "eps_trailing",
    "eps_forward",
  ],
  "FINANCIAL HEALTH": [
    "free_cashflow",
    "operating_cashflow",
    "total_cash",
    "total_debt",
    "debt_to_equity",
    "current_ratio",
    "quick_ratio",
    "book_value",
  ],
  "DIVIDENDS & MARKET SENTIMENT": [
    "dividend_rate",
    "dividend_yield",
    "payout_ratio",
    "beta",
    "recommendation_key",
    "number_of_analysts",
    "target_mean_price",
  ],
  "TECHNICALS & SHARE STRUCTURE": [
    "fifty_two_week_low",
    "fifty_two_week_high",
    "fifty_day_average",
    "two_hundred_day_average",
    "volume",
    "average_volume",
    "shares_outstanding",
    "float_shares",
    "short_ratio",
    "short_percent_of_float",
    "held_percent_insiders",
    "held_percent_institutions",
  ],
};

function toLabel(field: string): string {
  return field.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

export function formatStockData(data: StockData): string {
  const record = data as unknown as Record<string, unknown>;

  return Object.entries(STOCK_SECTIONS)
    .map(([section, fields]) => {
      const lines = fields
        .filter((field) => record[field] !== null && record[field] !== undefined)
        .map((field) => `${toLabel(field)}: ${record[field]}`);

      return lines.length > 0 ? `${section}\n${lines.join("\n")}` : "";
    })
    .filter(Boolean)
    .join("\n\n");
}
