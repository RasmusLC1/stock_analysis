from __future__ import annotations

from typing import Optional
from .scoring import ScoreResult, get, scale, grade


def score_garp(cfg, sp500=None) -> ScoreResult:
    """
    GARP (Growth At a Reasonable Price) Score Lens.
    Combines Forward P/E (FPE), Earnings Growth, and PEG Ratio.
    """
    # 1. Extract metrics using your config reader helper
    fpe = get(cfg, "forward_pe") or get(cfg, "fpe")
    growth = get(cfg, "earnings_growth") or get(cfg, "revenue_growth")
    peg = get(cfg, "peg_ratio") or get(cfg, "peg")
    
    breakdown = {
        "Forward P/E": fpe,
        "Growth Rate": growth,
        "PEG Ratio": peg
    }
    
    # Track data coverage for weighting
    valid_metrics = [m for m in [fpe, growth, peg] if m is not None]
    if not valid_metrics:
        return ScoreResult(
            lens="GARP",
            ticker=getattr(cfg, "ticker_symbol", "?"),
            score=None,
            grade="N/A",
            coverage=0.0,
            breakdown=breakdown,
            notes=["Missing all GARP metrics (FPE, Growth, PEG)."]
        )

    # 2. Score individual components (0-100 scale)
    fpe_score = scale(fpe, bad=45.0, good=10.0) if fpe is not None else None
    growth_score = scale(growth, bad=0.0, good=30.0) if growth is not None else None
    peg_score = scale(peg, bad=3.0, good=0.5) if peg is not None else None

    # 3. Handle missing metrics dynamically (renormalize weights)
    weights = {
        "fpe": 0.25,
        "growth": 0.35,
        "peg": 0.40
    }
    
    active_scores = [
        (fpe_score, weights["fpe"]),
        (growth_score, weights["growth"]),
        (peg_score, weights["peg"])
    ]
    
    weighted_sum = sum(s * w for s, w in active_scores if s is not None)
    total_weight = sum(w for s, w in active_scores if s is not None)
    
    final_score = weighted_sum / total_weight if total_weight > 0 else None
    if final_score is not None:
        final_score = max(0.0, min(100.0, final_score))

    coverage = round(total_weight / sum(weights.values()), 2)

    return ScoreResult(
        lens="GARP",
        ticker=getattr(cfg, "ticker_symbol", "?"),
        score=None if final_score is None else round(final_score, 1),
        grade=grade(final_score),
        coverage=coverage,
        breakdown={k: (round(v, 1) if v is not None else None) for k, v in breakdown.items()}
    )