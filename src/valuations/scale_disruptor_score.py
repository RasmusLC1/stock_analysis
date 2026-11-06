from __future__ import annotations

from typing import Optional
from .scoring import ScoreResult, get, scale, grade


def parse_market_cap(val) -> Optional[float]:
    """Parses raw float/int OR formatted string ('1.5B', '$500M', '2.1T') to numeric value."""
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return float(val)
    if isinstance(val, str):
        clean = val.replace("$", "").replace(",", "").strip().upper()
        if not clean or clean == "N/A":
            return None
        try:
            multiplier = 1.0
            if clean.endswith("T"):
                multiplier = 1e12
                clean = clean[:-1]
            elif clean.endswith("B"):
                multiplier = 1e9
                clean = clean[:-1]
            elif clean.endswith("M"):
                multiplier = 1e6
                clean = clean[:-1]
            elif clean.endswith("K"):
                multiplier = 1e3
                clean = clean[:-1]
            return float(clean) * multiplier
        except (ValueError, TypeError):
            return None
    return None


def score_scale_disruptor(cfg) -> ScoreResult:
    """
    Scale Disruptor Score Lens.
    Triggers ONLY for verified small caps (Market Cap < $5B). 
    Returns score=None for large caps or missing market cap data.
    """
    raw_market_cap = getattr(cfg, "market_cap", None) or getattr(cfg, "marketCap", None)
    if raw_market_cap is None:
        raw_market_cap = get(cfg, "market_cap") or get(cfg, "marketCap")

    market_cap = parse_market_cap(raw_market_cap)

    SMALL_CAP_THRESHOLD = 5_000_000_000  # $5 Billion

    # Explicit check: If market cap is missing OR exceeds $5B, do NOT trigger
    if market_cap is None or market_cap > SMALL_CAP_THRESHOLD:
        return ScoreResult(
            lens="ScaleDisruptor",
            ticker=getattr(cfg, "ticker_symbol", "?"),
            score=None,
            grade="N/A",
            coverage=0.0,
            notes=["Exceeds small-cap threshold ($5B) or missing market cap; Scale Disruptor inactive."]
        )

    # Extract metrics tailored for scaling small-caps
    gross_margins = get(cfg, "gross_margins") or get(cfg, "grossMargins")
    current_ratio = get(cfg, "current_ratio") or get(cfg, "currentRatio")
    revenue_growth = get(cfg, "revenue_growth") or get(cfg, "revenueGrowth")

    breakdown = {
        "Gross Margins": gross_margins * 100 if gross_margins is not None else None,
        "Current Ratio": current_ratio,
        "Revenue Growth": revenue_growth * 100 if revenue_growth is not None else None
    }

    gm_score = scale(gross_margins, bad=0.20, good=0.60) if gross_margins is not None else None
    cr_score = scale(current_ratio, bad=1.0, good=3.0) if current_ratio is not None else None
    rg_score = scale(revenue_growth, bad=0.0, good=0.30) if revenue_growth is not None else None

    weights = {
        "gross_margins": 0.40,
        "current_ratio": 0.30,
        "revenue_growth": 0.30
    }

    active_scores = [
        (gm_score, weights["gross_margins"]),
        (cr_score, weights["current_ratio"]),
        (rg_score, weights["revenue_growth"])
    ]

    weighted_sum = sum(s * w for s, w in active_scores if s is not None)
    total_weight = sum(w for s, w in active_scores if s is not None)

    final_score = weighted_sum / total_weight if total_weight > 0 else None
    if final_score is not None:
        final_score = max(0.0, min(100.0, final_score))

    coverage = round(total_weight / sum(weights.values()), 2)

    return ScoreResult(
        lens="ScaleDisruptor",
        ticker=getattr(cfg, "ticker_symbol", "?"),
        score=None if final_score is None else round(final_score, 1),
        grade=grade(final_score),
        coverage=coverage,
        breakdown={k: (round(v, 1) if v is not None else None) for k, v in breakdown.items()}
    )