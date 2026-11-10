from dataclasses import dataclass, field
from typing import Callable, Optional


@dataclass(frozen=True)
class Dimension:
  label: str
  fn: Callable[[object], Optional[float]]
  weight: float = 1.0  # Default value comes last