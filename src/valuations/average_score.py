from __future__ import annotations

from typing import Optional
from .growth_score import score_growth
from .value_score import score_value
from .health_score import score_health
from .quality_score import score_quality
from .garp_score import score_garp
from .scale_disruptor_score import score_scale_disruptor  # Imported new scale disruptor lens
from .scoring import ScoreResult, score_with
from .dimension import Dimension
from src.helper.lens_keys import LensKeys as key


# Individual dimension getters accepting sp500 context
def score_growth_lens(cfg, sp500=None) -> Optional[float]:
    return score_growth(cfg, sp500).score


def score_value_lens(cfg, sp500=None) -> Optional[float]:
    return score_value(cfg, sp500).score


def score_health_lens(cfg, sp500=None) -> Optional[float]:
    return score_health(cfg, sp500).score


def score_quality_lens(cfg, sp500=None) -> Optional[float]:
    return score_quality(cfg, sp500).score


def score_garp_lens(cfg, sp500=None) -> Optional[float]:
    return score_garp(cfg, sp500).score


def score_scale_disruptor_lens(cfg, sp500=None) -> Optional[float]:
    """Returns the scale disruptor score if small cap, otherwise None (dropping it)."""
    return score_scale_disruptor(cfg, sp500).score


# Updated dimensions including Scale Disruptor
DIMENSIONS = [
    Dimension(key.GROWTH, score_growth_lens, 0.40),
    Dimension(key.QUALITY, score_quality_lens, 0.30),
    Dimension(key.HEALTH, score_health_lens, 0.15),
    Dimension("GARP", score_garp_lens, 0.10),
    Dimension(key.VALUE, score_value_lens, -0.05),
    Dimension("ScaleDisruptor", score_scale_disruptor_lens, 0.15),
]


def average_score(cfg, sp500=None) -> ScoreResult:
    return score_with("Composite Average", cfg, DIMENSIONS, context=sp500)