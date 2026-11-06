from typing import Callable

from .growth_score import score_growth
from .scoring import ScoreResult
from .value_score import score_value

# Order here is the order shown in the dropdown. To add a new perspective
# (quality, momentum, dividends, ...), write a score_xxx(cfg) -> ScoreResult
# and add one line here; the GUI needs no other changes.
LENSES: dict[str, Callable[[object], ScoreResult]] = {
    "Growth": score_growth,
    "Value": score_value,
}