from __future__ import annotations

from typing import Optional

from .scoring import Dimension, ScoreResult, avg, get, scale, score_with


def score_profit_margins(cfg) -> Optional[float]:
  """Gross and Operating margins: pricing power indicator."""
  gm = scale(get(cfg, "gross_margins"), bad=0.15, good=0.60)
  om = scale(get(cfg, "operating_margins"), bad=0.0, good=0.20)
  return avg([gm, om])


def score_capital_efficiency(cfg) -> Optional[float]:
  """Return on Equity and Return on Assets."""
  roe = scale(get(cfg, "return_on_equity"), bad=0.05, good=0.25)
  roa = scale(get(cfg, "return_on_assets"), bad=0.02, good=0.12)
  return avg([roe, roa])


def score_cash_conversion(cfg) -> Optional[float]:
  """Free cash flow margin relative to revenue."""
  fcf, rev = get(cfg, "free_cashflow"), get(cfg, "total_revenue")
  if fcf is None or rev is None or rev <= 0:
    return None
  fcf_margin = fcf / rev
  return scale(fcf_margin, bad=0.0, good=0.20)


DIMENSIONS = [
    Dimension("Margins", 0.35, score_profit_margins),
    Dimension("Returns", 0.35, score_capital_efficiency),
    Dimension("FCF Gen", 0.30, score_cash_conversion),
]


def score_quality(cfg) -> ScoreResult:
  return score_with("Quality", cfg, DIMENSIONS)