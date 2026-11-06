"""
Growth quality scoring for a yfinance-backed InfoConfig.

Idea: score several independent dimensions 0-100, then combine with weights.
Missing data never counts as "bad" - a dimension with no data is dropped and
the remaining weights are renormalised. A coverage value tells you how much of
the score was actually backed by data.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional


# --------------------------------------------------------------------------
# 1. The fields this needs on InfoConfig (names match yfinance `Ticker.info`)
# --------------------------------------------------------------------------
# class InfoConfig:
#     ticker_symbol: str
#     # Growth
#     revenue_growth: Optional[float] = None            # info["revenueGrowth"]  (YoY, quarterly)
#     earnings_growth: Optional[float] = None           # info["earningsGrowth"]
#     earnings_quarterly_growth: Optional[float] = None # info["earningsQuarterlyGrowth"]
#     # Profitability / efficiency
#     gross_margins: Optional[float] = None             # info["grossMargins"]
#     operating_margins: Optional[float] = None         # info["operatingMargins"]
#     profit_margins: Optional[float] = None            # info["profitMargins"]
#     return_on_equity: Optional[float] = None          # info["returnOnEquity"]
#     return_on_assets: Optional[float] = None          # info["returnOnAssets"]
#     # Cash & balance sheet
#     free_cashflow: Optional[float] = None             # info["freeCashflow"]
#     operating_cashflow: Optional[float] = None        # info["operatingCashflow"]
#     total_revenue: Optional[float] = None             # info["totalRevenue"]
#     net_income_to_common: Optional[float] = None      # info["netIncomeToCommon"]
#     debt_to_equity: Optional[float] = None            # info["debtToEquity"]  (yfinance gives %, e.g. 85.0)
#     current_ratio: Optional[float] = None             # info["currentRatio"]
#     # Valuation vs growth
#     peg_ratio: Optional[float] = None                 # info["trailingPegRatio"] / info["pegRatio"]
#     forward_pe: Optional[float] = None                # info["forwardPE"]
#     trailing_pe: Optional[float] = None               # info["trailingPE"]


# --------------------------------------------------------------------------
# 2. Helpers
# --------------------------------------------------------------------------
def _get(cfg, name: str) -> Optional[float]:
    v = getattr(cfg, name, None)
    if v is None:
        return None
    try:
        v = float(v)
    except (TypeError, ValueError):
        return None
    if v != v:  # NaN
        return None
    return v


def scale(x: Optional[float], bad: float, good: float) -> Optional[float]:
    """Linear map: x<=bad -> 0, x>=good -> 100. Works if good < bad too."""
    if x is None:
        return None
    t = (x - bad) / (good - bad)
    return max(0.0, min(1.0, t)) * 100.0


def avg(values: list[Optional[float]]) -> Optional[float]:
    vals = [v for v in values if v is not None]
    return sum(vals) / len(vals) if vals else None


# --------------------------------------------------------------------------
# 3. Dimension scorers (each returns 0-100 or None if no data)
# --------------------------------------------------------------------------
def score_growth_rate(cfg) -> Optional[float]:
    """How fast are revenue and earnings growing?"""
    rev = scale(_get(cfg, "revenue_growth"), bad=0.0, good=0.25)       # 25%+ YoY = max
    earn = scale(_get(cfg, "earnings_growth"), bad=0.0, good=0.30)
    return avg([rev, earn])


def score_growth_consistency(cfg) -> Optional[float]:
    """
    Growth that shows up in both revenue AND earnings is higher quality than
    one-sided growth. Penalise big divergence (e.g. earnings up via cost cuts
    while revenue shrinks, or revenue up while earnings collapse).
    """
    rev = _get(cfg, "revenue_growth")
    earn = _get(cfg, "earnings_growth")
    if rev is None or earn is None:
        return None
    if rev <= 0 and earn <= 0:
        return 0.0
    if rev <= 0 or earn <= 0:
        return 25.0
    # Both positive: reward earnings growing at least as fast as revenue
    # (operating leverage), mildly penalise earnings lagging far behind.
    ratio = earn / rev
    return scale(ratio, bad=0.25, good=1.0)


def score_profitability(cfg) -> Optional[float]:
    """Can the business turn growth into profit?"""
    gm = scale(_get(cfg, "gross_margins"), bad=0.15, good=0.60)
    om = scale(_get(cfg, "operating_margins"), bad=0.0, good=0.25)
    return avg([gm, om])


def score_returns(cfg) -> Optional[float]:
    """Does it earn good returns on the capital it reinvests?"""
    roe = scale(_get(cfg, "return_on_equity"), bad=0.05, good=0.25)
    roa = scale(_get(cfg, "return_on_assets"), bad=0.02, good=0.12)
    return avg([roe, roa])


def score_cash_quality(cfg) -> Optional[float]:
    """Growth backed by cash, not just accounting profit."""
    fcf = _get(cfg, "free_cashflow")
    rev = _get(cfg, "total_revenue")
    ocf = _get(cfg, "operating_cashflow")
    ni = _get(cfg, "net_income_to_common")

    fcf_margin = scale(fcf / rev, bad=0.0, good=0.20) if fcf is not None and rev else None
    # Cash conversion: operating cash flow vs net income (>=1 is healthy)
    conv = None
    if ocf is not None and ni is not None and ni > 0:
        conv = scale(ocf / ni, bad=0.5, good=1.2)
    return avg([fcf_margin, conv])


def score_balance_sheet(cfg) -> Optional[float]:
    """Is the growth financed sustainably?"""
    de = _get(cfg, "debt_to_equity")  # yfinance returns percent (85 = 0.85x)
    cr = _get(cfg, "current_ratio")
    de_score = scale(de, bad=200.0, good=30.0) if de is not None else None
    cr_score = scale(cr, bad=0.8, good=2.0)
    return avg([de_score, cr_score])


def score_growth_valuation(cfg) -> Optional[float]:
    """Are you paying a sane price for the growth? PEG ~1 or below is good."""
    peg = _get(cfg, "peg_ratio")
    if peg is None or peg <= 0:
        return None
    return scale(peg, bad=3.0, good=1.0)


# --------------------------------------------------------------------------
# 4. Combine
# --------------------------------------------------------------------------
@dataclass
class Dimension:
    name: str
    weight: float
    fn: Callable


DIMENSIONS = [
    Dimension("growth_rate",        0.25, score_growth_rate),
    Dimension("growth_consistency", 0.10, score_growth_consistency),
    Dimension("profitability",      0.20, score_profitability),
    Dimension("returns",            0.15, score_returns),
    Dimension("cash_quality",       0.15, score_cash_quality),
    Dimension("balance_sheet",      0.10, score_balance_sheet),
    Dimension("valuation",          0.05, score_growth_valuation),
]


@dataclass
class GrowthResult:
    ticker: str
    score: Optional[float]                 # 0-100, None if no data at all
    grade: str
    coverage: float                        # share of total weight that had data (0-1)
    breakdown: dict = field(default_factory=dict)


def grade(score: Optional[float]) -> str:
    if score is None:
        return "N/A"
    for cutoff, g in [(80, "A"), (65, "B"), (50, "C"), (35, "D")]:
        if score >= cutoff:
            return g
    return "F"


def score_company(cfg) -> GrowthResult:
    breakdown, used_weight, weighted_sum = {}, 0.0, 0.0
    total_weight = sum(d.weight for d in DIMENSIONS)

    for d in DIMENSIONS:
        s = d.fn(cfg)
        breakdown[d.name] = None if s is None else round(s, 1)
        if s is not None:
            weighted_sum += s * d.weight
            used_weight += d.weight

    coverage = used_weight / total_weight
    final = weighted_sum / used_weight if used_weight else None
    return GrowthResult(
        ticker=cfg.ticker_symbol,
        score=None if final is None else round(final, 1),
        grade=grade(final),
        coverage=round(coverage, 2),
        breakdown=breakdown,
    )