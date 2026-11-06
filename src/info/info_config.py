from dataclasses import dataclass
from typing import Tuple, Optional

@dataclass
class InfoConfig:
    name: str
    currency: str
    sector: str
    industry: str
    market_cap: str
    pe_ratio: str
    price: str

