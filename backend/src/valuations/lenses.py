from typing import Callable
from .growth_score import score_growth
from .value_score import score_value
from .health_score import score_health
from .quality_score import score_quality
from .average_score import average_score
from .garp_score import score_garp
from .scale_disruptor_score import score_scale_disruptor
from .scoring import ScoreResult
from backend.src.helper.lens_keys import LensKeys as key
from typing import Callable, Optional

LENSES: dict[str, Callable[[object, Optional[object]], ScoreResult]] = {
    key.AVERAGE : average_score,
    key.GROWTH : lambda cfg, sp: score_growth(cfg, sp),
    key.VALUE : lambda cfg, sp: score_value(cfg, sp),
    key.HEALTH : lambda cfg, sp: score_health(cfg, sp),
    key.QUALITY : lambda cfg, sp: score_quality(cfg, sp),
    key.GARP : lambda cfg, sp: score_garp(cfg, sp),
    key.SCALE_DISRUPTOR : lambda cfg, sp=None: score_scale_disruptor(cfg, sp),
}