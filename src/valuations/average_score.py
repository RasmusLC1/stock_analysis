from __future__ import annotations

from typing import Optional
from .growth_score import score_growth
from .value_score import score_value
from .health_score import score_health
from .quality_score import score_quality
from .garp_score import score_garp  # Imported your new GARP lens
from .scoring import ScoreResult, score_with
from .dimension import Dimension
from src.helper.lens_keys import LensKeys as key


# Individual dimension getters for each core lens score
def score_growth_lens(cfg) -> Optional[float]:
    return score_growth(cfg).score


def score_value_lens(cfg) -> Optional[float]:
    return score_value(cfg).score


def score_health_lens(cfg) -> Optional[float]:
    return score_health(cfg).score


def score_quality_lens(cfg) -> Optional[float]:
    return score_quality(cfg).score


def score_garp_lens(cfg) -> Optional[float]:
    return score_garp(cfg).score


# Updated dimensions including GARP. 
# Note: Negative weights (like Value) are supported safely when score_with uses absolute denominator scaling.
DIMENSIONS = [
    Dimension(key.GROWTH, score_growth_lens, 0.40),
    Dimension(key.GARP, score_garp_lens, 0.25),          # Integrated your new GARP dimension with a balanced weight
    Dimension(key.VALUE, score_value_lens, -0.141),    # Maintained negative correlation weight
    Dimension(key.HEALTH, score_health_lens, 0.197),
    Dimension(key.QUALITY, score_quality_lens, 0.30),
]


def average_score(cfg) -> ScoreResult:
    return score_with("Composite Average", cfg, DIMENSIONS)