from dataclasses import dataclass
from typing import Optional


@dataclass
class InfoConfig:
  # Required Identifier
  ticker_symbol: str

  # Basic Info & Profile
  name: Optional[str] = None
  currency: Optional[str] = None
  financial_currency: Optional[str] = None
  sector: Optional[str] = None
  industry: Optional[str] = None
  summary: Optional[str] = None
  website: Optional[str] = None

  # Price & Trading Dynamics
  price: Optional[float | str] = None
  previous_close: Optional[float] = None
  open_price: Optional[float] = None
  day_low: Optional[float] = None
  day_high: Optional[float] = None
  volume: Optional[int] = None
  average_volume: Optional[int] = None

  # Valuation Metrics
  market_cap: Optional[str] = None
  enterprise_value: Optional[str | float] = None
  pe_ratio: Optional[float | str] = None  # Trailing P/E
  forward_pe: Optional[float] = None
  peg_ratio: Optional[float] = None
  price_to_sales: Optional[float] = None
  price_to_book: Optional[float] = None
  enterprise_to_revenue: Optional[float] = None
  enterprise_to_ebitda: Optional[float] = None

  # Profitability & Margins
  profit_margins: Optional[float] = None
  gross_margins: Optional[float] = None
  operating_margins: Optional[float] = None
  ebitda_margins: Optional[float] = None
  return_on_assets: Optional[float] = None
  return_on_equity: Optional[float] = None

  # Income & Cash Flow Statement Highlights
  total_revenue: Optional[float | str] = None
  revenue_growth: Optional[float] = None
  gross_profits: Optional[float | str] = None
  ebitda: Optional[float | str] = None
  net_income: Optional[float | str] = None
  earnings_growth: Optional[float] = None
  eps_trailing: Optional[float] = None
  eps_forward: Optional[float] = None
  free_cashflow: Optional[float | str] = None
  operating_cashflow: Optional[float | str] = None

  # Balance Sheet & Capital Structure
  total_cash: Optional[float | str] = None
  total_debt: Optional[float | str] = None
  debt_to_equity: Optional[float] = None
  current_ratio: Optional[float] = None
  quick_ratio: Optional[float] = None
  book_value: Optional[float] = None

  # Dividends & Capital Return
  dividend_rate: Optional[float] = None
  dividend_yield: Optional[float] = None
  payout_ratio: Optional[float] = None
  ex_dividend_date: Optional[int] = None

  # Technicals & Moving Averages
  beta: Optional[float] = None
  fifty_two_week_low: Optional[float] = None
  fifty_two_week_high: Optional[float] = None
  fifty_day_average: Optional[float] = None
  two_hundred_day_average: Optional[float] = None

  # Share Structure & Short Interest
  shares_outstanding: Optional[int] = None
  float_shares: Optional[int] = None
  short_ratio: Optional[float] = None
  short_percent_of_float: Optional[float] = None
  held_percent_insiders: Optional[float] = None
  held_percent_institutions: Optional[float] = None

  # Analyst Estimates & Consensus
  target_high_price: Optional[float] = None
  target_low_price: Optional[float] = None
  target_mean_price: Optional[float] = None
  target_median_price: Optional[float] = None
  recommendation_key: Optional[str] = None
  number_of_analysts: Optional[int] = None