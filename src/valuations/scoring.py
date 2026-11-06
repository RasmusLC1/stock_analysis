"""
Shared building blocks for every scoring lens (growth, value, ...).

A lens is just a list of weighted Dimensions. Each dimension returns 0-100,
or None when there is no data. Missing data is dropped (not scored as zero)
and the remaining weights are renormalised; `coverage` says how much of the
total weight was actually backed by data.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional


def get(cfg, name: str) -> Optional[float]:
  """Read a numeric field from InfoConfig; None for missing / NaN / non-numeric."""
  v = getattr(cfg, name, None)
  if v is None:
    return None
  try:
    v = float(v)
  except (TypeError, ValueError):
    return None
  return None if v != v else v  # NaN check


def scale(x: Optional[float], bad: float, good: float) -> Optional[float]:
  """Linear map: x at `bad` -> 0, x at `good` -> 100 (works when good < bad too)."""
  if x is None:
    return None
  t = (x - bad) / (good - bad)
  return max(0.0, min(1.0, t)) * 100.0


def avg(values: list[Optional[float]]) -> Optional[float]:
  vals = [v for v in values if v is not None]
  return sum(vals) / len(vals) if vals else None


def grade(score: Optional[float]) -> str:
  if score is None:
    return "N/A"
  for cutoff, g in [(80, "A"), (65, "B"), (50, "C"), (35, "D")]:
    if score >= cutoff:
      return g
  return "F"


@dataclass
class ScoreResult:
  lens: str  # "Growth", "Value", ...
  ticker: str
  score: Optional[float]  # 0-100, None if no data at all
  grade: str
  coverage: float  # share of total weight that had data (0-1)
  breakdown: dict[str, Optional[float]] = field(default_factory=dict)
  notes: list[str] = field(default_factory=list)  # warnings shown on the card


def score_with(lens: str, cfg, dimensions: list[Dimension]) -> ScoreResult:
    breakdown: dict[str, Optional[float]] = {}
    used_weight = weighted_sum = 0.0
    total_weight = sum(abs(d.weight) for d in dimensions) # Sum of absolute weights

    for d in dimensions:
        s = d.fn(cfg)
        breakdown[d.label] = None if s is None else round(s, 1)
        if s is not None:
            # Multiply by the raw weight (which can be negative)
            weighted_sum += s * d.weight
            # But track used_weight using absolute value to keep the denominator positive
            used_weight += abs(d.weight)

    final = weighted_sum / used_weight if used_weight else None
    
    # Clamp final score strictly between 0 and 100
    if final is not None:
        final = max(0.0, min(100.0, final))

    return ScoreResult(
        lens=lens,
        ticker=getattr(cfg, "ticker_symbol", "?"),
        score=None if final is None else round(final, 1),
        grade=grade(final),
        coverage=round(used_weight / total_weight, 2) if total_weight else 0.0,
        breakdown=breakdown,
    )