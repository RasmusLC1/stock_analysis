from __future__ import annotations

from .info.info_config import InfoConfig
from .caching.cache import Cache
from .helper.process_data import ProcessData

# Central stock handling class
class StockService:
  @staticmethod
  def fetch_stock_summary(ticker_symbol: str, period: str = "1d") -> InfoConfig | None:
    ticker_symbol = StockService._normalize_ticker(ticker_symbol)

    # 2. Check if cache already exists and load it
    cached_data = Cache.check_cache(ticker_symbol, period)
    if cached_data is not None:
      print("CACHE FOUND:\t", ticker_symbol)
      return cached_data

    data = ProcessData.process_data(ticker_symbol, period)
    if not data:
       print("Failed to create data: ", ticker_symbol)
       return None

    # 4. Save successfully fetched data to local cache
    Cache.store_cache(ticker_symbol, period, data)

    return data
  

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