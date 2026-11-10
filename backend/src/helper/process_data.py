from backend.src.helper.validate_stock_info import ValidateStockInfo
from backend.src.yf_api.api_fetch import ApiFetch
from backend.src.info.extract_info import ExtractInfo
from backend.src.info.info_config import InfoConfig
from yfinance import Ticker

class ProcessData:

    @staticmethod
    def process_data(ticker_symbol: str, period: str = "1d"):
         # 3. Fetch via API if not cached
          ticker: Ticker = ApiFetch.fetch_stock_data(ticker_symbol, period)
      
          if not ticker:
            raise ValueError(f"Could not retrieve valid data for ticker '{ticker_symbol}'.")
      
          info = ValidateStockInfo.validate_info(ticker)
          if not info:
            return None
      
          data: InfoConfig = ExtractInfo.extract_info(info, ticker_symbol)
      
          if not data:
            raise ValueError(f"Could not extract data '{ticker_symbol}'.")
          return data