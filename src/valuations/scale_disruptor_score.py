from __future__ import annotations

from typing import Optional
from .scoring import ScoreResult, get, scale, grade


def score_scale_disruptor(cfg) -> ScoreResult:
    """
    Scale Disruptor Score Lens.
    Triggers ONLY for small caps (Market Cap < $5B) where trailing net income 
    might be negative due to scaling/R&D, but gross margins and liquidity are strong.
    """
    market_cap = get(cfg, "market_cap") or get(cfg, "marketCap")
    
    # Define small-cap threshold (e.g., $5 Billion)
    SMALL_CAP_THRESHOLD = 5_000_000_000
    
    # If it's a mid or large cap, return None so it drops out of the composite score cleanly
    if market_cap is not None and market_cap > SMALL_CAP_THRESHOLD:
        return ScoreResult(
            lens="ScaleDisruptor",
            ticker=getattr(cfg, "ticker_symbol", "?"),
            score=None,
            grade="N/A",
            coverage=0.0,
            notes=["Exceeds small-cap threshold; Scale Disruptor lens inactive."]
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

    # Score components (0-100 scale)
    # Gross Margins: Higher is better (e.g., 20% = 0, 60%+ = 100)
    gm_score = scale(gross_margins, bad=0.20, good=0.60) if gross_margins is not None else None

    # Current Ratio: Liquidity safety net for small caps (e.g., 1.0 = 0, 3.0+ = 100)
    cr_score = scale(current_ratio, bad=1.0, good=3.0) if current_ratio is not None else None

    # Revenue Growth: Top-line expansion driver (e.g., 0% = 0, 30%+ = 100)
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