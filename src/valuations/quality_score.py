from __future__ import annotations

from typing import Optional

from .scoring import ScoreResult, avg, get, scale, score_with
from .dimension import Dimension
from src.helper.lens_keys import LensKeys as key

def score_profit_margins(cfg) -> Optional[float]:
    """Gross and Operating margins: pricing power indicator."""
    gm = scale(get(cfg, "gross_margins"), bad=0.15, good=0.60)
    om = scale(get(cfg, "operating_margins"), bad=0.0, good=0.25) # Aligned with growth benchmark
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
    Dimension("Margins", score_profit_margins, 0.35),
    Dimension("Returns", score_capital_efficiency, 0.35),
    Dimension("FCF Gen", score_cash_conversion, 0.30),
]

def score_quality(cfg) -> ScoreResult:
    return score_with(key.QUALITY, cfg, DIMENSIONS)