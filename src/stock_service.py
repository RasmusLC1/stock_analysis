from __future__ import annotations

from pathlib import Path
import pickle
from .yf_api.api_fetch import ApiFetch
from .info.extract_info import ExtractInfo
from .info.info_config import InfoConfig
from .caching.cache import Cache
from yfinance import Ticker

# Central stock handling class
class StockService:
  @staticmethod
  def fetch_stock_summary(ticker_symbol: str, period: str = "1d") -> InfoConfig | None:
    ticker_symbol = StockService._normalize_ticker(ticker_symbol)

    # 1. Construct the expected cache file path
    

    # 2. Check if cache already exists and load it
    cached_data = Cache.check_cache(ticker_symbol, period)
    if cached_data is not None:
      print("CACHE FOUND :\t", ticker_symbol)
      return cached_data

    # 3. Fetch via API if not cached
    ticker: Ticker = ApiFetch.fetch_stock_data(ticker_symbol, period)

    if not ticker:
      raise ValueError(f"Could not retrieve valid data for ticker '{ticker_symbol}'.")

    info = StockService.validate_info(ticker)
    if not info:
      return None

    data: InfoConfig = ExtractInfo.extract_info(info, ticker_symbol)

    if not data:
      raise ValueError(f"Could not extract data '{ticker_symbol}'.")

    # 4. Save successfully fetched data to local cache
    Cache.store_cache(ticker_symbol, period, data)

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