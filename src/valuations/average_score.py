from __future__ import annotations

from typing import Optional
from .growth_score import score_growth
from .value_score import score_value
from .health_score import score_health
from .quality_score import score_quality
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


# Equal weighting across core lenses (adjust weights if you want specific emphasis)
DIMENSIONS = [
    Dimension(key.GROWTH, score_growth_lens),
    Dimension(key.VALUE, score_value_lens),
    Dimension(key.HEALTH, score_health_lens),
    Dimension(key.QUALITY, score_quality_lens),
]


def average_score(cfg) -> ScoreResult:
    return score_with("Composite Average", cfg, DIMENSIONS)