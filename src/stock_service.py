import yfinance as yf
from .yf_api.api_fetch import ApiFetch
from .info.extract_info import ExtractInfo
from .info.info_config import InfoConfig
from yfinance import Ticker

# Central stock handling class
class StockService:
  @staticmethod
  def fetch_stock_summary(ticker_symbol: str) -> dict:
    ticker: Ticker = ApiFetch.fetch_stock_data(ticker_symbol)

    if not ticker:
      raise ValueError( f"Could not retrieve valid data for ticker '{ticker_symbol}'.")

    info = StockService.validate_info(ticker)

    data: InfoConfig = ExtractInfo.extract_info(info, ticker_symbol)

    if not data:
      raise ValueError( f"Could not extract data '{ticker_symbol}'.")

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

      