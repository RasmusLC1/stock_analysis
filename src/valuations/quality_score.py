from __future__ import annotations

from typing import Optional

from .scoring import ScoreResult, avg, get, scale, score_with
from .dimension import Dimension
from src.helper.lens_keys import LensKeys as key

def score_profit_margins(cfg, sp500=None) -> Optional[float]:
    """Gross and Operating margins evaluated against market benchmarks."""
    # If sp500 provides a benchmark, you can use it dynamically, e.g.:
    good_gm = 0.60 if not sp500 else getattr(sp500, 'avg_gross_margin', 0.60)
    
    gm = scale(get(cfg, "gross_margins"), bad=0.15, good=good_gm)
    om = scale(get(cfg, "operating_margins"), bad=0.0, good=0.25)
    return avg([gm, om])

def score_capital_efficiency(cfg, sp500=None) -> Optional[float]:
    """Return on Equity and Return on Assets relative to S&P 500."""
    roe = scale(get(cfg, "return_on_equity"), bad=0.05, good=0.25)
    roa = scale(get(cfg, "return_on_assets"), bad=0.02, good=0.12)
    return avg([roe, roa])

def score_cash_conversion(cfg, sp500=None) -> Optional[float]:
    fcf, rev = get(cfg, "free_cashflow"), get(cfg, "total_revenue")
    if fcf is None or rev is None or rev <= 0:
        return None
    fcf_margin = fcf / rev
    return scale(fcf_margin, bad=0.0, good=0.20)

# Pass sp500 down through dimensions
DIMENSIONS = [
    Dimension("Margins", lambda cfg, sp=None: score_profit_margins(cfg, sp), 0.35),
    Dimension("Returns", lambda cfg, sp=None: score_capital_efficiency(cfg, sp), 0.35),
    Dimension("FCF Gen", lambda cfg, sp=None: score_cash_conversion(cfg, sp), 0.30),
]

def score_quality(cfg, sp500=None) -> ScoreResult:
    return score_with(key.QUALITY, cfg, DIMENSIONS, sp500)