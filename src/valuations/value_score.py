"""
Value lens: is the stock cheap relative to what the business earns, and is it
cheap for a good reason (value trap) or not?

Fields read from InfoConfig (yfinance `Ticker.info` key in brackets):

  pe_ratio [trailingPE]            forward_pe [forwardPE]
  price_to_book [priceToBook]      price_to_sales [priceToSalesTrailing12Months]
  enterprise_to_ebitda [enterpriseToEbitda]
  free_cashflow [freeCashflow]     market_cap [marketCap]
  price [currentPrice]             target_mean_price [targetMeanPrice]
  -- reused from the growth lens --
  return_on_equity, revenue_growth, operating_margins, debt_to_equity, current_ratio
"""
from __future__ import annotations

from typing import Optional

from .growth_score import score_balance_sheet
from .scoring import Dimension, ScoreResult, avg, get, grade, scale, score_with


def _multiple(x: Optional[float], bad: float, good: float) -> Optional[float]:
  """Lower multiples are better. None = no data. <= 0 means losses / negative book: worst."""
  if x is None:
    return None
  if x <= 0:
    return 0.0
  return scale(x, bad, good)


def score_earnings_multiple(cfg) -> Optional[float]:
  trailing = _multiple(get(cfg, "pe_ratio"), bad=35.0, good=10.0)
  forward = _multiple(get(cfg, "forward_pe"), bad=30.0, good=9.0)
  return avg([trailing, forward])


def score_book_and_sales(cfg) -> Optional[float]:
  pb = _multiple(get(cfg, "price_to_book"), bad=6.0, good=1.0)
  ps = _multiple(get(cfg, "price_to_sales"), bad=10.0, good=1.0)
  return avg([pb, ps])


def score_ev_multiple(cfg) -> Optional[float]:
  return _multiple(get(cfg, "enterprise_to_ebitda"), bad=20.0, good=6.0)


def score_cash_yield(cfg) -> Optional[float]:
  """Free cash flow yield: how much cash the business generates per krone of market cap."""
  fcf, cap = get(cfg, "free_cashflow"), get(cfg, "market_cap")
  if fcf is None or cap is None or cap <= 0:
    return None
  return scale(fcf / cap, bad=0.0, good=0.08)


def score_value_trap_check(cfg) -> Optional[float]:
  """Cheap AND shrinking / unprofitable is a trap, so reward a healthy core business."""
  roe = scale(get(cfg, "return_on_equity"), bad=0.0, good=0.15)
  rev = scale(get(cfg, "revenue_growth"), bad=-0.10, good=0.03)
  margin = scale(get(cfg, "operating_margins"), bad=0.0, good=0.15)
  return avg([roe, rev, margin])


def score_analyst_upside(cfg) -> Optional[float]:
  """Weak signal (analysts are optimistic on average), so it carries little weight."""
  price, target = get(cfg, "price"), get(cfg, "target_mean_price")
  if price is None or price <= 0 or target is None:
    return None
  return scale(target / price - 1.0, bad=-0.10, good=0.30)


DIMENSIONS = [
    Dimension("Earnings", 0.25, score_earnings_multiple),
    Dimension("Book/Sales", 0.15, score_book_and_sales),
    Dimension("EV", 0.15, score_ev_multiple),
    Dimension("FCF yield", 0.20, score_cash_yield),
    Dimension("Safety", 0.10, score_balance_sheet),
    Dimension("Quality", 0.10, score_value_trap_check),
    Dimension("Upside", 0.05, score_analyst_upside),
]


# Very low multiples can outvote the quality check in a weighted average, so a
# business that scores badly on quality is capped: cheap + failing is a trap, not value.
TRAP_QUALITY_BELOW = 30.0
TRAP_SCORE_CAP = 45.0


def score_value(cfg) -> ScoreResult:
  result = score_with("Value", cfg, DIMENSIONS)
  quality = result.breakdown.get("Quality")
  if (
      result.score is not None
      and quality is not None
      and quality < TRAP_QUALITY_BELOW
      and result.score > TRAP_SCORE_CAP
  ):
    result.score = TRAP_SCORE_CAP
    result.grade = grade(TRAP_SCORE_CAP)
    result.notes.append("Value trap risk: cheap, but weak or shrinking business - score capped")
  return result