from __future__ import annotations

from typing import Optional

from .scoring import ScoreResult, avg, get, scale, score_with
from .dimension import Dimension
from src.helper.lens_keys import LensKeys as key

def score_leverage(cfg) -> Optional[float]:
    """Debt-to-Equity: lower leverage is healthier."""
    de = get(cfg, "debt_to_equity")
    if de is None:
        return None
    return scale(de, bad=200.0, good=30.0)


def score_liquidity(cfg) -> Optional[float]:
    """Current ratio and quick ratio: ability to cover short-term obligations."""
    cr = scale(get(cfg, "current_ratio"), bad=0.8, good=2.0)
    qr = scale(get(cfg, "quick_ratio"), bad=0.5, good=1.5)
    return avg([cr, qr])


def score_debt_coverage(cfg) -> Optional[float]:
    """Cash relative to total debt buffer, recalibrated for efficient capital structures."""
    cash, debt = get(cfg, "total_cash"), get(cfg, "total_debt")
    if cash is None or debt is None or debt <= 0:
        return None
    ratio = cash / debt
    # Adjusted thresholds: 5% cash-to-debt is baseline, 30%+ is strong for asset-heavy compounders
    return scale(ratio, bad=0.05, good=0.30)


DIMENSIONS = [
    Dimension("Leverage", score_leverage, 0.40),
    Dimension("Liquidity", score_liquidity, 0.40),
    Dimension("Cash Buffer", score_debt_coverage, 0.20),
]


def score_health(cfg) -> ScoreResult:
    return score_with(key.HEALTH, cfg, DIMENSIONS)