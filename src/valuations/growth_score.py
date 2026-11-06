from __future__ import annotations

from typing import Optional

from .scoring import ScoreResult, avg, get, scale, score_with
from .dimension import Dimension
from src.helper.lens_keys import LensKeys as key

def score_growth_rate(cfg) -> Optional[float]:
    rev = scale(get(cfg, "revenue_growth"), bad=0.0, good=0.25)
    earn = scale(get(cfg, "earnings_growth"), bad=0.0, good=0.30)
    return avg([rev, earn])


def score_growth_consistency(cfg) -> Optional[float]:
    """Growth in both revenue AND earnings beats one-sided growth."""
    rev, earn = get(cfg, "revenue_growth"), get(cfg, "earnings_growth")
    if rev is None or earn is None:
        return None
    if rev <= 0 and earn <= 0:
        return 0.0
    if rev <= 0 or earn <= 0:
        return 25.0
    return scale(earn / rev, bad=0.25, good=1.0)


def score_profitability(cfg) -> Optional[float]:
    gm = scale(get(cfg, "gross_margins"), bad=0.15, good=0.60)
    om = scale(get(cfg, "operating_margins"), bad=0.0, good=0.25) # Standardized to match quality
    return avg([gm, om])


def score_returns(cfg) -> Optional[float]:
    roe = scale(get(cfg, "return_on_equity"), bad=0.05, good=0.25)
    roa = scale(get(cfg, "return_on_assets"), bad=0.02, good=0.12)
    return avg([roe, roa])


def score_cash_quality(cfg) -> Optional[float]:
    fcf, rev = get(cfg, "free_cashflow"), get(cfg, "total_revenue")
    ocf, ni = get(cfg, "operating_cashflow"), get(cfg, "net_income_to_common")
    fcf_margin = scale(fcf / rev, bad=0.0, good=0.20) if fcf is not None and rev else None
    conv = scale(ocf / ni, bad=0.5, good=1.2) if ocf is not None and ni and ni > 0 else None
    return avg([fcf_margin, conv])


DIMENSIONS = [
    Dimension("Growth", score_growth_rate, 0.30),
    Dimension("Consistency", score_growth_consistency, 0.15),
    Dimension("Profit", score_profitability, 0.20),
    Dimension("Returns", score_returns, 0.20),
    Dimension("Cash", score_cash_quality, 0.15),
]


def score_growth(cfg) -> ScoreResult:
    return score_with(key.GROWTH, cfg, DIMENSIONS)


score_company = score_growth