from typing import Callable
from .growth_score import score_growth
from .value_score import score_value
from .health_score import score_health
from .quality_score import score_quality
from .average_score import average_score
from .scoring import ScoreResult
from src.helper.lens_keys import LensKeys as key

LENSES: dict[str, Callable[[object], ScoreResult]] = {
    key.AVERAGE : average_score,
    key.GROWTH : score_growth,
    key.VALUE : score_value,
    key.HEALTH : score_health,
    key.QUALITY : score_quality,
}