from __future__ import annotations

from typing import Optional
from .scoring import ScoreResult, avg, get, scale, score_with
from .dimension import Dimension
from src.helper.lens_keys import LensKeys as key

def score_balance_sheet(cfg) -> Optional[float]:
    """Debt-to-Equity and Current Ratio safety margin for value assessment."""
    de, cr = get(cfg, "debt_to_equity"), get(cfg, "current_ratio")
    return avg([scale(de, bad=200.0, good=30.0), scale(cr, bad=0.8, good=2.0)])

def score_pe(cfg) -> Optional[float]:
    """Trailing P/E ratio: lower is generally cheaper/better for value."""
    pe = get(cfg, "trailing_pe") or get(cfg, "pe_ratio")
    if pe is None or pe <= 0:
        return None
    return scale(pe, bad=40.0, good=10.0)

def score_pb(cfg) -> Optional[float]:
    """Price-to-Book ratio."""
    pb = get(cfg, "price_to_book") or get(cfg, "pb_ratio")
    if pb is None or pb <= 0:
        return None
    return scale(pb, bad=6.0, good=1.0)

def score_ps(cfg) -> Optional[float]:
    """Price-to-Sales ratio."""
    ps = get(cfg, "price_to_sales") or get(cfg, "ps_ratio")
    if ps is None or ps <= 0:
        return None
    return scale(ps, bad=8.0, good=1.0)

def score_dividend_yield(cfg) -> Optional[float]:
    """Dividend yield: higher is better for value/income."""
    div = get(cfg, "dividend_yield")
    if div is None:
        return None
    # yfinance often represents dividend yield as a decimal (e.g. 0.03 = 3%)
    return scale(div, bad=0.0, good=0.06)

DIMENSIONS = [
    Dimension("P/E", score_pe, 0.30),
    Dimension("P/B", score_pb, 0.20),
    Dimension("P/S", score_ps, 0.20),
    Dimension("Balance", score_balance_sheet, 0.15),
    Dimension("Dividend", score_dividend_yield, 0.15),
]

def score_value(cfg) -> ScoreResult:
    return score_with(key.VALUE, cfg, DIMENSIONS)