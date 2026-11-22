import threading
import time
from datetime import datetime

from backend.src.calculate_sp.calculate_sp import CalculateSP500

RETRY_AFTER_SECONDS = 600

_lock = threading.Lock()
_state = {"month": None, "value": None, "loading": False, "retry_at": 0.0}


def _load(month: str) -> None:
    try:
        value = CalculateSP500().average_values
        failed = value is None
    except Exception as error:
        print(f"S&P500 benchmark failed: {error}")
        value, failed = None, True

    with _lock:
        _state["value"] = value
        _state["month"] = month if value is not None else None
        _state["retry_at"] = time.time() + RETRY_AFTER_SECONDS if failed else 0.0
        _state["loading"] = False


def get_sp500_benchmark():
    """Returns the benchmark InfoConfig, or None while it's loading or unavailable.
    Never blocks: a missing/outdated benchmark triggers a background load."""
    month = datetime.now().strftime("%Y-%m")

    with _lock:
        if _state["month"] == month and _state["value"] is not None:
            return _state["value"]

        if _state["loading"] or time.time() < _state["retry_at"]:
            return None

        _state["loading"] = True

    threading.Thread(target=_load, args=(month,), daemon=True).start()
    return None