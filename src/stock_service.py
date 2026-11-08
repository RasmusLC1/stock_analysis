from __future__ import annotations

from datetime import date
from .yf_api.api_fetch import ApiFetch
from .info.extract_info import ExtractInfo
from .info.info_config import InfoConfig
from .caching.cache import Cache

# Central stock handling class
class StockService:
  @staticmethod
  def fetch_stock_summary(ticker_symbol: str, start: str | None = None) -> InfoConfig | None:
    ticker_symbol = StockService._normalize_ticker(ticker_symbol)

    # Picking today (the default) means "latest"; ISO date strings compare correctly as text
    if not start or start >= date.today().isoformat():
      start = None
    key = start or "latest"

    cached_data = Cache.check_cache(ticker_symbol, key)
    if cached_data is not None:
      print("CACHED DATA")
      return cached_data

    result = ApiFetch.fetch_stock_data(ticker_symbol, start)
    if not result:
      raise ValueError(f"Could not retrieve valid data for ticker '{ticker_symbol}'.")
    ticker, hist = result

    info = StockService.validate_info(ticker)
    if not info:
      return None

    data: InfoConfig = ExtractInfo.extract_info(info, ticker_symbol)
    if not data:
      raise ValueError(f"Could not extract data '{ticker_symbol}'.")

    if start:  # change from the first trading day on/after the picked date to the latest close
      data.price_change_pct = (hist["Close"].iloc[-1] / hist["Close"].iloc[0] - 1) * 100

    Cache.store_cache(ticker_symbol, key, data)
    return data


  @staticmethod
  def validate_info(ticker):
    info = ticker.info
    
    # Validate ticker existence
    if (
        not info
        or (
            "regularMarketPrice" not in info
            and "currentPrice" not in info
            and "longName" not in info
        )
    ):
      return None

    return info

  @staticmethod
  def _normalize_ticker(ticker_symbol: str) -> str:
      ticker_symbol = ticker_symbol.strip().upper()
      
      # Example mapping for known European favorites or general heuristic
      european_defaults = {
          "RHM": "RHM.DE",
          "ASML": "ASML.AS",
          "RUA": "RUA.PA",
      }
      
      if ticker_symbol in european_defaults:
          return european_defaults[ticker_symbol]
      
      return ticker_symbol