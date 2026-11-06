from typing import Callable
from .growth_score import score_growth
from .value_score import score_value
from .health_score import score_health
from .quality_score import score_quality
from .scoring import ScoreResult

LENSES: dict[str, Callable[[object], ScoreResult]] = {
    "Growth": score_growth,
    "Value": score_value,
    "Health": score_health,
    "Quality": score_quality,
}